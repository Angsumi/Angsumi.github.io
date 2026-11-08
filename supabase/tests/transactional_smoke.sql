-- Synthetic-only production smoke check; rollback leaves no inquiries or notification jobs.
begin;
set local role service_role;
do $$
declare first_result jsonb; second_result jsonb; smoke_lead_id text; job_count integer; is_limited boolean;
begin
 first_result=public.angsumi_capture('{"name":"Synthetic database smoke test","email":"synthetic@example.invalid","category":"research","description":"Synthetic schema verification, not a customer inquiry","budget":"not_sure","details":{},"contact_consent":true,"marketing_consent":false}'::jsonb,'schema-smoke-test-request-20261108','schema-smoke-test-fingerprint-20261108',20,'low','{"category_relevance":20}'::jsonb);
 smoke_lead_id=first_result->>'id';
 if first_result->>'saved'<>'true' or first_result->>'duplicate'<>'false' then raise exception 'Initial persistence assertion failed'; end if;
 second_result=public.angsumi_capture('{"name":"Synthetic database smoke test"}'::jsonb,'schema-smoke-test-request-20261108','schema-smoke-test-fingerprint-20261108',20,'low','{}'::jsonb);
 if second_result->>'id'<>smoke_lead_id or second_result->>'duplicate'<>'true' then raise exception 'Idempotency assertion failed'; end if;
 if (select count(*) from public.angsumi_outbox where smoke_lead_id=first_result->>'id')<>2 then raise exception 'Atomic outbox assertion failed'; end if;
 perform public.angsumi_update(smoke_lead_id,'{"status":"QUALIFIED","replied":true}'::jsonb,'Synthetic review note');
 if not exists(select 1 from public.angsumi_leads l where l.id=smoke_lead_id and l.status='QUALIFIED' and l.replied) then raise exception 'Pipeline update assertion failed'; end if;
 if (select count(*) from public.angsumi_activities a where a.lead_id=first_result->>'id')<>3 then raise exception 'Activity history assertion failed'; end if;
 select count(*) into job_count from public.angsumi_claim_jobs() j where j.lead_id=first_result->>'id';
 if job_count<>2 then raise exception 'Job claim assertion failed'; end if;
 is_limited=public.angsumi_limit('synthetic-smoke-rate',1,3600);
 if is_limited then raise exception 'First rate request incorrectly blocked'; end if;
 is_limited=public.angsumi_limit('synthetic-smoke-rate',1,3600);
 if not is_limited then raise exception 'Rate-limit assertion failed'; end if;
end $$;
rollback;
