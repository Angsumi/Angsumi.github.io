import {createClient} from 'npm:@supabase/supabase-js@2';
import {hash} from '../_shared/core.mjs';
const env=key=>Deno.env.get(key);
const db=createClient(env('SUPABASE_URL'),env('SUPABASE_SERVICE_ROLE_KEY'),{auth:{persistSession:false,autoRefreshToken:false}});
const checked=async query=>{const {data,error}=await query;if(error)throw Error('Database request failed');return data;};
Deno.serve(async request=>{
 const reply=(status,body)=>Response.json(body,{status,headers:{'Cache-Control':'no-store'}});
 try{
  const secret=env('NOTIFICATION_WORKER_SECRET');
  if(request.method!=='POST'||!secret||secret.length<32||await hash('Bearer '+(request.headers.get('X-ANGSUMI-Worker-Token')||''))!==await hash('Bearer '+secret))return reply(401,{error:'Worker authentication required'});
  if(env('ENABLE_LIVE_EMAIL')!=='true')return reply(503,{error:'Live email disabled'});
  const key=env('RESEND_API_KEY'),domainId=env('RESEND_DOMAIN_ID'),from=env('MAIL_FROM'),owner=env('OWNER_EMAIL'),replyTo=env('REPLY_TO');
  if(!key||!domainId||!from||!owner||!replyTo||!env('PUBLIC_SITE_URL')||!env('PUBLIC_LEAD_API'))return reply(503,{error:'Email configuration incomplete'});
  // Deployment gate is set only after provider verification. The restricted sending key and Resend enforce the sender domain on every send.
  if(env('RESEND_DOMAIN_VERIFIED')!=='true'||from.split('@')[1]!=='mail.angsumi.online')return reply(503,{error:'Verified sending domain required'});
  if(!/^https:\/\/[^/]+$/.test(env('PUBLIC_SITE_URL'))||!/^https:\/\//.test(env('PUBLIC_LEAD_API')))return reply(503,{error:'HTTPS links required'});
  if(env('MARKETING_ENABLED')==='true'){
   // Recipient opt-in and NEW status are checked again immediately before delivery.
   const leads=await checked(db.from('angsumi_leads').select('*').eq('status','NEW').eq('replied',false).eq('opted_out',false).eq('inactive',false).contains('data',{marketing_consent:true}).limit(500));
   for(const lead of leads)for(const day of [1,3,7])await checked(db.from('angsumi_outbox').upsert({lead_id:lead.id,kind:'follow_up_'+day,due_at:new Date(Date.parse(lead.created_at)+day*86400000).toISOString()},{onConflict:'lead_id,kind',ignoreDuplicates:true}));
  }
  const jobs=await checked(db.rpc('angsumi_claim_jobs'));const counts={sent:0,failed:0,cancelled:0,review:0};
  for(const job of jobs){
   try{
    const lead=await checked(db.from('angsumi_leads').select('*').eq('id',job.lead_id).single()),data=lead.data,marketing=job.kind.startsWith('follow_up_');
    if(marketing&&(env('MARKETING_ENABLED')!=='true'||!data.marketing_consent||lead.status!=='NEW'||lead.replied||lead.opted_out||lead.inactive)){
     await checked(db.from('angsumi_outbox').update({state:'cancelled'}).eq('id',job.id));counts.cancelled++;continue;
    }
    // Provider dedupe expires. Never automatically replay an ambiguous old delivery.
    if(Date.now()-Date.parse(job.first_attempt_at)>23*3600000){await checked(db.from('angsumi_outbox').update({state:'review',last_error:'Past provider idempotency window; owner review required'}).eq('id',job.id));counts.review++;continue;}
    const unsubscribe=env('PUBLIC_SITE_URL')+'/unsubscribe/#'+lead.unsubscribe_token;
    const resources={research:env('PUBLIC_SITE_URL')+'/resources/downloads/rna-seq-checklist.md',digital:env('PUBLIC_SITE_URL')+'/resources/downloads/digital-readiness.md',training:env('PUBLIC_SITE_URL')+'/resources/labs/'};
    let body=`Hello ${data.name},\n\nWe received your ${data.category} inquiry. Reference: ${lead.id}. We will review the scope and contact you about next steps. Please do not send confidential datasets by email.`;
    if(job.kind==='owner_notification')body=`A ${data.category} inquiry was safely saved. Reference: ${lead.id}. Priority: ${lead.priority}. Sign in to the protected owner workspace to review.`;
    if(marketing){const message={follow_up_1:'Would a short requirements conversation help? Reply with the question you want to resolve first.',follow_up_3:'Here is a resource for planning your next step: '+resources[data.category],follow_up_7:'Is your project still active? Reply if you would like to continue, or tell us if your plans have changed.'}[job.kind];body=`Hello ${data.name},\n\n${message}\n\nReference: ${lead.id}. You opted in to relevant resources and follow-ups.\nStop promotional follow-ups: ${unsubscribe}`;}
    const payload={from,to:[job.kind==='owner_notification'?owner:data.email],reply_to:replyTo,subject:'ANGSUMI inquiry '+lead.id,text:body+'\n\nANGSUMI — Research | Data | Impact'};
    const templateId=job.kind==='acknowledgement'?env('ACK_TEMPLATE_ID'):job.kind==='owner_notification'?env('OWNER_TEMPLATE_ID'):null;
    if(templateId){payload.template={id:templateId,variables:job.kind==='acknowledgement'?{LEAD_ID:lead.id,CONTACT_NAME:data.name,CATEGORY:data.category}:{LEAD_ID:lead.id,CATEGORY:data.category,PRIORITY:lead.priority}};delete payload.text;}
    if(marketing)payload.headers={'List-Unsubscribe':'<'+env('PUBLIC_LEAD_API')+'/api/unsubscribe/'+lead.unsubscribe_token+'>','List-Unsubscribe-Post':'List-Unsubscribe=One-Click'};
    const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json','Idempotency-Key':lead.id+'/'+job.kind},body:JSON.stringify(payload)});
    if(!response.ok)throw Error('Provider rejected delivery');const receipt=await response.json();if(!receipt.id)throw Error('Provider did not confirm');
    await checked(db.from('angsumi_outbox').update({state:'sent',sent_at:new Date().toISOString(),provider_id:receipt.id,last_error:null}).eq('id',job.id));
    await checked(db.from('angsumi_activities').insert({lead_id:lead.id,kind:'notification_sent',detail:job.kind}));counts.sent++;
   }catch(_){await checked(db.from('angsumi_outbox').update({state:'pending',due_at:new Date(Date.now()+Math.min(3600000,300000*2**job.attempts)).toISOString(),last_error:'Delivery not confirmed; retry within provider idempotency window'}).eq('id',job.id));counts.failed++;}
  }
  return reply(200,counts);
 }catch(_){return reply(503,{error:'Notification worker failed; saved leads remain intact'});}
});
