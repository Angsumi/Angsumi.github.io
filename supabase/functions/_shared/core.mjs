export const statuses=['NEW','NEEDS_INFORMATION','CONTACTED','QUALIFIED','DISCOVERY','PROPOSAL_SENT','NEGOTIATION','WON','LOST'];
export const categories=['research','digital','training'];
const fields=['institution','field','project_type','dataset_type','samples','stage','deliverables','deadline','business_type','business_name','platform','workflow','functionality','level','interest','format','availability'];
export function text(value='',limit=1000){if(typeof value!=='string'||value.length>limit||value.includes('\0'))throw Error('Invalid field');return value.trim();}
export function validate(p){
 if(!p||typeof p!=='object'||Array.isArray(p))throw Error('Expected inquiry');
 if(p.website)throw Error('Unable to accept');
 const data={};for(const [key,limit] of [['name',120],['email',254],['phone',40],['description',3000],['category',30],['budget',40],['landing_page',200]])data[key]=text(p[key],limit);
 data.email=data.email.toLowerCase();
 if(!data.name||!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(data.email)||!categories.includes(data.category)||data.description.length<10||p.contact_consent!==true)throw Error('Required fields missing');
 if(!['','not_sure','under_5000','5000_15000','15000_50000','50000_plus'].includes(data.budget))throw Error('Invalid budget');
 data.source=['direct','google','instagram','github','youtube','referral','other'].includes(p.source)?p.source:'other';
 data.campaign=['none','research-checklist','digital-readiness','bioinformatics-labs','workshop'].includes(p.campaign)?p.campaign:'none';
 if(!/^\/(?:[a-z0-9_-]+\/)*$/.test(data.landing_page))data.landing_page='/inquiry/';
 if(p.details!==undefined&&(!p.details||typeof p.details!=='object'||Array.isArray(p.details)))throw Error('Invalid context');
 data.details={};for(const key of fields)if(key in (p.details||{}))data.details[key]=text(p.details[key],500);
 data.contact_consent=true;data.marketing_consent=p.marketing_consent===true;data.consent_version='2026-11-08';return data;
}
export function score(data,config={category_relevance:20,clear_requirements:20,known_budget:10,ready_to_start:20,defined_timeline:15,organization_context:15,high_threshold:70,medium_threshold:40}){
 const d=data.details;const conditions={category_relevance:categories.includes(data.category),clear_requirements:data.description.length>=80,known_budget:!['','not_sure'].includes(data.budget),ready_to_start:['data_ready','requirements_ready','ready'].includes(d.stage),defined_timeline:Boolean(d.deadline||d.availability),organization_context:Boolean(d.institution||d.business_name)};
 const reasons={};for(const [key,yes] of Object.entries(conditions))if(yes)reasons[key]=config[key];const total=Object.values(reasons).reduce((a,b)=>a+b,0);return {total,priority:total>=config.high_threshold?'high':total>=config.medium_threshold?'medium':'low',reasons};
}
export function update(p){
 if(!p||typeof p!=='object'||Array.isArray(p))throw Error('Invalid update');const changes={};
 for(const key of ['status','assigned_to','outcome','next_follow_up','last_contact'])if(key in p){changes[key]=text(p[key],200);if(key==='status'&&!statuses.includes(changes[key]))throw Error('Invalid status');if(['last_contact','next_follow_up'].includes(key)&&changes[key]&&(!/(Z|[+-]\d\d:\d\d)$/.test(changes[key])||Number.isNaN(Date.parse(changes[key]))))throw Error('Timezone required');}
 for(const key of ['replied','opted_out','inactive'])if(key in p){if(typeof p[key]!=='boolean')throw Error('Invalid preference');changes[key]=p[key];}
 if('revenue' in p){if(p.revenue!==null&&(typeof p.revenue!=='number'||!Number.isFinite(p.revenue)||p.revenue<0||p.revenue>1e12))throw Error('Invalid revenue');changes.revenue=p.revenue;}
 return {changes,note:text(p.note,3000)};
}
export function publicLead(row){const {request_key,fingerprint,unsubscribe_token,...safe}=row;return safe;}
export function csvCell(value){const s=String(value??'');return '"'+(/^[\s]*[=+@-]/.test(s)?"'":'')+s.replaceAll('"','""')+'"';}
export async function hash(value){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value)))].map(b=>b.toString(16).padStart(2,'0')).join('');}
