import {statuses,validate,score,update,publicLead,csvCell,hash} from '../_shared/core.mjs';
async function readJSON(request){const reader=request.body?.getReader();if(!reader)throw Error('Missing body');let size=0;const chunks=[];while(true){const {value,done}=await reader.read();if(done)break;size+=value.length;if(size>16384){await reader.cancel();throw Error('Body too large');}chunks.push(value);}const bytes=new Uint8Array(size);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.length;}return JSON.parse(new TextDecoder().decode(bytes));}
export function createHandler({db,auth,env}){
 const allowed=new Set((env('ALLOWED_ORIGINS')||'').split(',').map(s=>s.trim()).filter(Boolean));
 const get=async query=>{const {data,error}=await query;if(error)throw Error('Database request failed');return data;};
 const all=async(table,columns='*')=>{const rows=[];for(let offset=0;;offset+=500){const page=await get(db.from(table).select(columns).order('id').range(offset,offset+499));rows.push(...page);if(page.length<500)return rows;}};
 return async function(request){
  const origin=request.headers.get('origin')||'',url=new URL(request.url),method=request.method;
  let path=url.pathname.replace(/^(?:\/functions\/v1)?\/lead-api(?=\/|$)/,'');
  const headers={'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Vary':'Origin'};
  if(allowed.has(origin))headers['Access-Control-Allow-Origin']=origin;
  const respond=(status,body,type)=>new Response(type?body:JSON.stringify(body),{status,headers:{...headers,...(type?{'Content-Type':type}:{})}});
  try{
   if(method==='OPTIONS')return allowed.has(origin)?new Response(null,{status:204,headers:{...headers,'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS','Access-Control-Allow-Headers':'Content-Type,Idempotency-Key,Authorization,apikey'}}):respond(403,{error:'Origin not allowed'});
   if(['POST','PATCH'].includes(method)&&!allowed.has(origin)&&!/^\/api\/unsubscribe\/[a-f0-9]{64}$/.test(path))return respond(403,{error:'Origin not allowed'});
   if(path==='/api/health'&&method==='GET')return respond(200,{ready:Boolean(env('ADMIN_USER_ID')&&env('RATE_LIMIT_SALT')),provider:'supabase'});
   if(['/api/leads','/api/login'].includes(path)&&method==='POST'){
    const salt=env('RATE_LIMIT_SALT');if(!salt)return respond(503,{error:'Intake not configured'});
    // Global durable guard is authoritative; proxy-derived client buckets are an additional signal.
    const global=await get(db.rpc('angsumi_limit',{p_key:'global'+path,p_max:path.endsWith('login')?100:500,p_seconds:3600}));
    const ip=request.headers.get('x-forwarded-for')?.split(',')[0]?.trim()||'unknown';
    const limited=await get(db.rpc('angsumi_limit',{p_key:await hash(salt+path+ip),p_max:path.endsWith('login')?5:10,p_seconds:path.endsWith('login')?900:3600}));
    if(global||limited)return respond(429,{error:'Please wait or use the direct contact route'});
   }
   if(path==='/api/leads'&&method==='POST'){
    const data=validate(await readJSON(request)),key=request.headers.get('Idempotency-Key')||'';
    if(!/^[A-Za-z0-9_-]{16,100}$/.test(key))throw Error('Invalid key');
    const config=env('LEAD_SCORING_JSON')?JSON.parse(env('LEAD_SCORING_JSON')):undefined;
    const points=score(data,config);const fingerprint=await hash(JSON.stringify(data));
    const result=await get(db.rpc('angsumi_capture',{p_data:data,p_key:key,p_fingerprint:fingerprint,p_score:points.total,p_priority:points.priority,p_reasons:points.reasons}));
    return respond(result.duplicate?200:201,result);
   }
   if(path==='/api/login'&&method==='POST'){
    const p=await readJSON(request);if(typeof p.email!=='string'||p.email.length>254)throw Error('Invalid login');
    if(p.mode==='otp'){
     // Return the same response for unknown addresses; only the configured owner receives a link.
     if(p.email.trim().toLowerCase()===env('ADMIN_EMAIL')){
      const {data:ownerRecord,error:lookupError}=await db.auth.admin.getUserById(env('ADMIN_USER_ID'));
      if(lookupError||!ownerRecord?.user)return respond(503,{error:'Owner account could not be verified.'});
      // Pre-provisioned owners must verify their invitation before ordinary passwordless sign-in.
      // Public signup stays disabled; no account is auto-confirmed here.
      const {error}=ownerRecord.user.email_confirmed_at
       ? await auth.auth.signInWithOtp({email:p.email.trim().toLowerCase(),options:{shouldCreateUser:false,emailRedirectTo:'https://angsumi.online/owner/'}})
       : await db.auth.admin.inviteUserByEmail(p.email.trim().toLowerCase(),{redirectTo:'https://angsumi.online/owner/'});
      if(error)return respond(503,{error:'Unable to send a sign-in link. Please retry later.'});
     }
     return respond(200,{link_requested:true});
    }
    if(typeof p.password!=='string'||p.password.length>512)throw Error('Invalid login');
    if(!env('ADMIN_USER_ID'))return respond(503,{error:'Owner access is not configured'});
    const {data,error}=await auth.auth.signInWithPassword({email:p.email,password:p.password});
    if(error||data.user?.id!==env('ADMIN_USER_ID'))return respond(401,{error:'Invalid owner sign-in'});
    return respond(200,{access_token:data.session.access_token,expires_in:data.session.expires_in});
   }
   if((path==='/api/unsubscribe'||/^\/api\/unsubscribe\/[a-f0-9]{64}$/.test(path))&&method==='POST'){
    const p=path==='/api/unsubscribe'?await readJSON(request):{token:path.split('/').pop()};if(!/^[A-Za-z0-9]{64}$/.test(p.token||''))throw Error('Invalid link');
    const row=await get(db.from('angsumi_leads').select('id').eq('unsubscribe_token',p.token).maybeSingle());
    if(row)await get(db.rpc('angsumi_update',{p_id:row.id,p_changes:{opted_out:true},p_note:'Promotional follow-up stopped by recipient'}));
    return respond(200,{unsubscribed:true});
   }
   if(!path.startsWith('/api/admin/'))return respond(404,{error:'Not found'});
   const token=request.headers.get('authorization')?.match(/^Bearer (.+)$/)?.[1];
   if(!token||!env('ADMIN_USER_ID'))return respond(401,{error:'Owner sign-in required'});
   const {data:userData,error:authError}=await auth.auth.getUser(token);
   if(authError||userData.user?.id!==env('ADMIN_USER_ID'))return respond(401,{error:'Owner sign-in required'});
   if(path==='/api/admin/session'&&method==='GET')return respond(200,{csrf:'bearer-auth-no-cookie',statuses});
   if(path==='/api/admin/logout'&&method==='POST')return respond(200,{signed_out:true}); // Browser clears in-memory token; Auth token expires normally.
   if(path==='/api/admin/leads'&&method==='GET')return respond(200,{leads:(await all('angsumi_leads')).map(publicLead).sort((a,b)=>b.created_at.localeCompare(a.created_at))});
   if(path==='/api/admin/reporting'&&method==='GET'){
    const leads=(await all('angsumi_leads')).filter(lead=>lead.data.internal_test!==true),leadIds=new Set(leads.map(lead=>lead.id)),activities=(await all('angsumi_activities','id,lead_id,kind,detail')).filter(activity=>leadIds.has(activity.lead_id));const qualified=new Set(),proposed=new Set();
    for(const a of activities.filter(a=>a.kind==='updated')){const s=JSON.parse(a.detail).status;if(['QUALIFIED','DISCOVERY','PROPOSAL_SENT','NEGOTIATION','WON'].includes(s))qualified.add(a.lead_id);if(['PROPOSAL_SENT','NEGOTIATION','WON'].includes(s))proposed.add(a.lead_id);}
    const won=leads.filter(l=>l.status==='WON');return respond(200,{total_inquiries:leads.length,ever_qualified:qualified.size,ever_proposed:proposed.size,currently_won:won.length,proposal_to_won_percent:proposed.size?Math.round(won.filter(l=>proposed.has(l.id)).length/proposed.size*1000)/10:null,revenue_recorded:won.reduce((n,l)=>n+Number(l.revenue||0),0),currency:'INR'});
   }
   if(path==='/api/admin/export'&&method==='GET'){
    const rows=(await all('angsumi_leads')).map(l=>[l.id,l.created_at,l.data.category,l.data.name,l.data.email,l.data.source,l.status,l.priority,l.data.budget,l.revenue]);
    return respond(200,[['id','received','category','name','email','source','status','priority','budget','revenue_inr'],...rows].map(r=>r.map(csvCell).join(',')).join('\r\n'),'text/csv; charset=utf-8');
   }
   const match=path.match(/^\/api\/admin\/leads\/(ANG-[A-F0-9]{16})$/);
   if(match&&['GET','PATCH'].includes(method)){
    if(method==='PATCH'){const {changes,note}=update(await readJSON(request));await get(db.rpc('angsumi_update',{p_id:match[1],p_changes:changes,p_note:note}));}
    const row=await get(db.from('angsumi_leads').select('*').eq('id',match[1]).maybeSingle());if(!row)return respond(404,{error:'Not found'});
    const activities=await get(db.from('angsumi_activities').select('*').eq('lead_id',row.id).order('id'));
    const notifications=await get(db.from('angsumi_outbox').select('kind,state,attempts,due_at,sent_at,last_error').eq('lead_id',row.id));
    return respond(200,{...publicLead(row),activities,notifications});
   }
   return respond(404,{error:'Not found'});
  }catch(_){return respond(400,{error:'Unable to complete request. Check your details or retry; no delivery success is assumed.'});}
 };
}
