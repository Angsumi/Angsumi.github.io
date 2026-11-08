(() => {
 const form=document.querySelector('#hosted-login'),status=document.querySelector('#owner-login-status');
 const base=window.ANGSUMI_LEADS_API;
 const configured=typeof base==='string'&&/^https:\/\/[a-z0-9.-]+\/functions\/v1\/lead-api$/.test(base);
 window.angsumiOwnerLogout=()=>{window.ANGSUMI_OWNER_TOKEN=null;location.reload();};
 if(!configured){status.textContent='The hosted owner workspace is not configured. Records remain unavailable here.';form.querySelector('button').disabled=true;return;}
 async function activate(token){
  const response=await fetch(base+'/api/admin/session',{headers:{Authorization:'Bearer '+token,apikey:window.ANGSUMI_SUPABASE_PUBLIC_KEY}});
  if(!response.ok)throw Error('This sign-in link is expired or does not belong to the authorized owner.');
  window.ANGSUMI_OWNER_TOKEN=token;window.ANGSUMI_CRM_BASE=base;
  document.querySelector('#owner-login').hidden=true;document.querySelector('#owner-workspace').hidden=false;
  const script=document.createElement('script');script.src='/assets/crm.js';document.body.append(script);
 }
 const callback=new URLSearchParams(location.hash.slice(1)),callbackToken=callback.get('access_token');
 if(location.hash)history.replaceState(null,'',location.pathname);
 if(callbackToken)activate(callbackToken).catch(error=>{status.textContent=error.message;});
 form.addEventListener('submit',async event=>{event.preventDefault();const button=form.querySelector('button');button.disabled=true;status.textContent='Requesting a sign-in link…';try{
  const response=await fetch(base+'/api/login',{method:'POST',headers:{'Content-Type':'application/json',apikey:window.ANGSUMI_SUPABASE_PUBLIC_KEY,Authorization:'Bearer '+window.ANGSUMI_SUPABASE_PUBLIC_KEY},body:JSON.stringify({email:document.querySelector('#owner-email').value,mode:'otp'}),signal:AbortSignal.timeout(20000)});
  const result=await response.json();if(!response.ok||!result.link_requested)throw Error('The link could not be requested. Please retry later.');
  status.textContent='If this is the approved owner email, a sign-in link has been sent. Open it in your email to continue.';
 }catch(error){status.textContent=error.message;}finally{button.disabled=false;}});
 document.querySelector('#hosted-export').addEventListener('click',async event=>{event.preventDefault();try{
  const response=await fetch(base+'/api/admin/export',{headers:{Authorization:'Bearer '+window.ANGSUMI_OWNER_TOKEN,apikey:window.ANGSUMI_SUPABASE_PUBLIC_KEY}});if(!response.ok)throw Error('Export unavailable');
  const url=URL.createObjectURL(await response.blob()),link=document.createElement('a');link.href=url;link.download='angsumi-leads.csv';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }catch(error){document.querySelector('#crm-status').textContent=error.message;}});
})();
