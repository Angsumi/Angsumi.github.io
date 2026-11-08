begin;
-- Additive schema only. Do not run against an existing business schema without review.
create table public.angsumi_leads (
 id text primary key,
 request_key text unique not null,
 fingerprint text not null,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 data jsonb not null,
 status text not null default 'NEW' check (status in ('NEW','NEEDS_INFORMATION','CONTACTED','QUALIFIED','DISCOVERY','PROPOSAL_SENT','NEGOTIATION','WON','LOST')),
 score integer not null,
 priority text not null check(priority in ('high','medium','low')),
 score_reasons jsonb not null,
 assigned_to text not null default '',
 last_contact timestamptz,
 next_follow_up timestamptz default now()+interval '1 day',
 outcome text not null default '',
 revenue numeric check(revenue>=0 and revenue<=1000000000000),
 replied boolean not null default false,
 opted_out boolean not null default false,
 inactive boolean not null default false,
 unsubscribe_token text unique not null
);
create index angsumi_lead_fingerprint on public.angsumi_leads(fingerprint,created_at);
create table public.angsumi_activities (
 id bigint generated always as identity primary key,
 lead_id text not null references public.angsumi_leads(id),
 created_at timestamptz not null default now(),
 kind text not null,
 detail text not null
);
create table public.angsumi_outbox (
 id bigint generated always as identity primary key,
 lead_id text not null references public.angsumi_leads(id),
 kind text not null,
 due_at timestamptz not null default now(),
 state text not null default 'pending' check(state in ('pending','sending','sent','cancelled','review')),
 attempts integer not null default 0,
 first_attempt_at timestamptz,
 last_error text,
 sent_at timestamptz,
 provider_id text,
 unique(lead_id,kind)
);
create table public.angsumi_rate_limits (
 key text not null,
 window_start timestamptz not null,
 count integer not null default 1,
 primary key(key,window_start)
);
alter table public.angsumi_leads enable row level security;
alter table public.angsumi_activities enable row level security;
alter table public.angsumi_outbox enable row level security;
alter table public.angsumi_rate_limits enable row level security;
revoke all on public.angsumi_leads,public.angsumi_activities,public.angsumi_outbox,public.angsumi_rate_limits from anon,authenticated;
-- Only authenticated, owner-checked Edge Functions use the server-only service credential.

create function public.angsumi_capture(p_data jsonb,p_key text,p_fingerprint text,p_score integer,p_priority text,p_reasons jsonb)
returns jsonb language plpgsql security definer set search_path=public as $$
declare previous public.angsumi_leads; new_id text;
begin
 perform pg_advisory_xact_lock(hashtextextended(p_fingerprint,0));
 select * into previous from angsumi_leads where request_key=p_key;
 if found then
  if previous.fingerprint<>p_fingerprint then raise exception 'Idempotency key conflict'; end if;
  return jsonb_build_object('id',previous.id,'saved',true,'duplicate',true);
 end if;
 select * into previous from angsumi_leads where fingerprint=p_fingerprint and created_at>now()-interval '24 hours' limit 1;
 if found then return jsonb_build_object('id',previous.id,'saved',true,'duplicate',true); end if;
 new_id='ANG-'||upper(substr(replace(gen_random_uuid()::text,'-',''),1,16));
 insert into angsumi_leads(id,request_key,fingerprint,data,score,priority,score_reasons,unsubscribe_token)
 values(new_id,p_key,p_fingerprint,p_data,p_score,p_priority,p_reasons,replace(gen_random_uuid()::text,'-','')||replace(gen_random_uuid()::text,'-',''));
 insert into angsumi_activities(lead_id,kind,detail) values(new_id,'received','Inquiry saved; scoring is advisory');
 insert into angsumi_outbox(lead_id,kind) values(new_id,'acknowledgement'),(new_id,'owner_notification');
 return jsonb_build_object('id',new_id,'saved',true,'duplicate',false);
end $$;

create function public.angsumi_update(p_id text,p_changes jsonb,p_note text default '')
returns void language plpgsql security definer set search_path=public as $$
begin
 perform 1 from angsumi_leads where id=p_id for update;
 if not found then raise exception 'Unknown inquiry'; end if;
 update angsumi_leads set
  status=case when p_changes ? 'status' then p_changes->>'status' else status end,
  assigned_to=case when p_changes ? 'assigned_to' then p_changes->>'assigned_to' else assigned_to end,
  outcome=case when p_changes ? 'outcome' then p_changes->>'outcome' else outcome end,
  revenue=case when p_changes ? 'revenue' then (p_changes->>'revenue')::numeric else revenue end,
  next_follow_up=case when p_changes ? 'next_follow_up' then nullif(p_changes->>'next_follow_up','')::timestamptz else next_follow_up end,
  last_contact=case when p_changes ? 'last_contact' then nullif(p_changes->>'last_contact','')::timestamptz else last_contact end,
  replied=case when p_changes ? 'replied' then (p_changes->>'replied')::boolean else replied end,
  opted_out=case when p_changes ? 'opted_out' then (p_changes->>'opted_out')::boolean else opted_out end,
  inactive=case when p_changes ? 'inactive' then (p_changes->>'inactive')::boolean else inactive end,
  updated_at=now() where id=p_id;
 insert into angsumi_activities(lead_id,kind,detail) values(p_id,'updated',p_changes::text);
 if length(p_note)>0 then insert into angsumi_activities(lead_id,kind,detail) values(p_id,'note',p_note); end if;
end $$;

create function public.angsumi_limit(p_key text,p_max integer,p_seconds integer)
returns boolean language plpgsql security definer set search_path=public as $$
declare current_count integer; bucket timestamptz;
begin
 bucket=to_timestamp(floor(extract(epoch from now())/p_seconds)*p_seconds);
 insert into angsumi_rate_limits(key,window_start) values(p_key,bucket)
 on conflict(key,window_start) do update set count=angsumi_rate_limits.count+1 returning count into current_count;
 delete from angsumi_rate_limits where window_start<now()-interval '2 days';
 return current_count>p_max;
end $$;

create function public.angsumi_claim_jobs()
returns setof public.angsumi_outbox language sql security definer set search_path=public as $$
 update angsumi_outbox set state='sending',attempts=attempts+1,first_attempt_at=coalesce(first_attempt_at,now())
 where id in (select id from angsumi_outbox where state='pending' and due_at<=now() and attempts<5 order by id for update skip locked limit 30)
 returning *;
$$;

revoke all on function public.angsumi_capture(jsonb,text,text,integer,text,jsonb),public.angsumi_update(text,jsonb,text),public.angsumi_limit(text,integer,integer),public.angsumi_claim_jobs() from public,anon,authenticated;
grant execute on function public.angsumi_capture(jsonb,text,text,integer,text,jsonb),public.angsumi_update(text,jsonb,text),public.angsumi_limit(text,integer,integer),public.angsumi_claim_jobs() to service_role;
grant all on public.angsumi_leads,public.angsumi_activities,public.angsumi_outbox,public.angsumi_rate_limits to service_role;
grant usage,select on sequence public.angsumi_activities_id_seq,public.angsumi_outbox_id_seq to service_role;

commit;
