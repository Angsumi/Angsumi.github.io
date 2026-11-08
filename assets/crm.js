(async () => {
  'use strict';
  let csrf, leads=[], selected=null, reporting={};
  const $=id=>document.getElementById(id),status=$('crm-status');
  const hosted=Boolean(window.ANGSUMI_OWNER_TOKEN),base=window.ANGSUMI_CRM_BASE||'';
  const node=(tag,text)=>{const el=document.createElement(tag);el.textContent=text;return el;};
  async function api(path,options={}) {
    const response=await fetch(base+path,{...options,headers:{'Content-Type':'application/json',...(!hosted?{'X-CSRF-Token':csrf||''}:{Authorization:'Bearer '+window.ANGSUMI_OWNER_TOKEN,apikey:window.ANGSUMI_SUPABASE_PUBLIC_KEY}),...options.headers}});
    if(response.status===401){if(hosted)window.angsumiOwnerLogout();else location.assign('/login/');throw Error('Session expired');}
    if(!response.ok)throw Error('Request failed. Your previous data remain saved.');
    return response.json();
  }
  function render(){
    const total=leads.length,won=leads.filter(l=>l.status==='WON').length;
    const qualified=leads.filter(l=>['QUALIFIED','DISCOVERY','PROPOSAL_SENT','NEGOTIATION','WON'].includes(l.status)).length;
    const proposed=leads.filter(l=>['PROPOSAL_SENT','NEGOTIATION','WON'].includes(l.status)).length;
    const overdue=leads.filter(l=>!['WON','LOST'].includes(l.status)&&!l.inactive&&l.next_follow_up&&Date.parse(l.next_follow_up)<=Date.now()).length;
    $('metrics').replaceChildren();
    for(const [label,value] of [['Inquiries',total],['Qualified pipeline',qualified],['Won',won],['Won / inquiries',total?(won/total*100).toFixed(1)+'%':'—'],['Revenue recorded (INR)',leads.filter(l=>l.status==='WON').reduce((s,l)=>s+(l.revenue||0),0).toLocaleString('en-IN')],['Follow-ups due',overdue]]){
      const box=node('div','');box.className='metric';box.append(node('strong',value),node('span',label));$('metrics').append(box);
    }
    const query=$('search').value.toLowerCase(),category=$('category-filter').value,pipeline=$('status-filter').value,priority=$('priority-filter').value;
    let shown=leads.filter(l=>(!category||l.data.category===category)&&(!pipeline||l.status===pipeline)&&(!priority||l.priority===priority)&&JSON.stringify([l.id,l.data.name,l.data.email,l.data.description]).toLowerCase().includes(query));
    if($('sort').value==='score')shown.sort((a,b)=>b.score-a.score);
    if($('sort').value==='follow_up')shown.sort((a,b)=>(a.next_follow_up||'z').localeCompare(b.next_follow_up||'z'));
    $('leads').replaceChildren();
    for(const l of shown){const tr=node('tr','');for(const value of [l.id+' · '+l.data.name,l.data.category,l.priority+' / '+l.score,l.status,l.next_follow_up||'Not set'])tr.append(node('td',value));const td=node('td',''),button=node('button','Review');button.type='button';button.addEventListener('click',()=>open(l.id));td.append(button);tr.append(td);$('leads').append(tr);}
    if(!shown.length){const tr=node('tr',''),td=node('td','No inquiries match these filters.');td.colSpan=6;tr.append(td);$('leads').append(tr);}
    status.textContent=`${shown.length} of ${total} inquiries`;
    $('reports').replaceChildren();
    for(const [title,key] of [['Pathways','category'],['Sources','source'],['Landing pages','landing_page'],['Resource campaigns','campaign']]){
      const counts=new Map();for(const lead of leads){const label=lead.data[key]||'Unspecified';counts.set(label,(counts.get(label)||0)+1);}
      const box=node('article','');box.className='card';box.append(node('h3',title));for(const [label,count] of counts)box.append(node('p',`${label}: ${count}`));if(!counts.size)box.append(node('p','No measured inquiries yet.'));$('reports').append(box);
    }
    const proposalBox=node('article','');proposalBox.className='card';proposalBox.append(node('h3','Pipeline facts'),node('p',`Ever qualified: ${reporting.ever_qualified??0}. Ever proposed: ${reporting.ever_proposed??0}. Proposal-to-won: ${reporting.proposal_to_won_percent===null?'—':reporting.proposal_to_won_percent+'%'}.`),node('p','Status history includes lost opportunities. Entering WON or NEGOTIATION implies the earlier qualification/proposal stages; it does not prove a proposal document was sent.'));$('reports').append(proposalBox);
  }
  const localDate=value=>{if(!value)return '';const d=new Date(value);return new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,16);};
  async function open(id){
    try{selected=await api('/api/admin/leads/'+id);$('detail').hidden=false;$('detail-title').textContent=selected.id;
      $('brief').textContent=JSON.stringify({contact:selected.data.name,email:selected.data.email,phone:selected.data.phone,project:selected.data.description,context:selected.data.details,budget:selected.data.budget,source:selected.data.source,campaign:selected.data.campaign,score_reasons:selected.score_reasons,marketing_consent:selected.data.marketing_consent},null,2);
      const form=$('update');for(const key of ['status','assigned_to','outcome','revenue'])form.elements[key].value=selected[key]??'';
      for(const key of ['next_follow_up','last_contact'])form.elements[key].value=localDate(selected[key]);
      for(const key of ['replied','opted_out','inactive'])form.elements[key].checked=Boolean(selected[key]);form.elements.note.value='';
      $('history').textContent=JSON.stringify({activities:selected.activities,notifications:selected.notifications},null,2);$('detail').focus();
    }catch(error){status.textContent=error.message;}
  }
  async function refresh(){const [list,facts]=await Promise.all([api('/api/admin/leads'),api('/api/admin/reporting')]);leads=list.leads.filter(lead=>lead.data.internal_test!==true);reporting=facts;render();}
  try{const session=await api('/api/admin/session');csrf=session.csrf;for(const s of session.statuses){$('status-filter').append(new Option(s,s));$('edit-status').append(new Option(s,s));}await refresh();}catch(error){status.textContent=error.message;}
  for(const id of ['search','category-filter','status-filter','priority-filter','sort'])$(id).addEventListener('input',render);
  $('update').addEventListener('submit',async event=>{event.preventDefault();if(!selected)return;const form=event.target,button=form.querySelector('button');button.disabled=true;const changes={};for(const key of ['status','assigned_to','outcome','note'])changes[key]=form.elements[key].value;changes.revenue=form.elements.revenue.value===''?null:Number(form.elements.revenue.value);for(const key of ['replied','opted_out','inactive'])changes[key]=form.elements[key].checked;for(const key of ['last_contact','next_follow_up'])changes[key]=form.elements[key].value?new Date(form.elements[key].value).toISOString():'';try{await api('/api/admin/leads/'+selected.id,{method:'PATCH',body:JSON.stringify(changes)});await refresh();await open(selected.id);status.textContent='Changes saved.';}catch(error){status.textContent=error.message;}finally{button.disabled=false;}});
  $('logout').addEventListener('click',async()=>{try{await api('/api/admin/logout',{method:'POST',body:'{}'});if(hosted)window.angsumiOwnerLogout();else location.assign('/login/');}catch(error){status.textContent=error.message;}});
})();
