(() => {
  'use strict';
  const form=document.getElementById('requirementsForm'),base=window.ANGSUMI_LEADS_API,key=window.ANGSUMI_SUPABASE_PUBLIC_KEY;
  if(!form||!base||!key)return;
  const field=id=>document.getElementById(id),button=form.querySelector('button[type="submit"]');
  const status=document.createElement('p');status.setAttribute('role','status');status.setAttribute('aria-live','polite');form.after(status);
  field('form_details').minLength=10;
  let busy=false,saved=false,started=false;const requestKey=crypto.randomUUID();
  const category=()=>/Bioinformatics|Scientific Data Analysis/.test(field('form_service').value)?'research':'digital';
  form.addEventListener('input',()=>{if(!started){started=true;window.angsumiTrackBusiness?.('form_start',{category:category()});}});
  form.addEventListener('submit',async event=>{
    event.preventDefault();if(busy||saved||!form.reportValidity())return;
    busy=true;button.disabled=true;status.textContent='Saving your inquiry…';
    const budget={'Under ₹5,000':'under_5000','₹5,000 – ₹15,000':'5000_15000','₹15,000 – ₹30,000':'15000_50000','₹30,000+':'not_sure','Flexible / Discuss First':'not_sure'}[field('form_budget').value]||'not_sure';
    const payload={name:field('form_name').value,email:field('form_email').value,phone:field('form_phone').value,category:category(),description:field('form_details').value,budget,details:{business_type:field('form_represent').value,project_type:field('form_service').value},source:document.referrer?'other':'direct',campaign:'none',landing_page:'/',website:form.elements._gotcha.value,contact_consent:field('legacy-consent').checked,marketing_consent:false};
    try{
      const response=await fetch(base+'/api/leads',{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':requestKey,apikey:key,Authorization:'Bearer '+key},body:JSON.stringify(payload),signal:AbortSignal.timeout(20000)});
      const result=await response.json();if(!response.ok||!result.saved||!/^ANG-[A-F0-9]{16}$/.test(result.id))throw Error();
      saved=true;form.hidden=true;status.textContent='Your inquiry is saved. Reference: '+result.id+'. We will review your goals and contact you about next steps.';status.tabIndex=-1;status.focus();
      if(!result.duplicate)window.angsumiTrackBusiness?.('generate_lead',{category:payload.category});
    }catch(_){status.textContent='We could not confirm your inquiry was saved. Retry with the same details or contact us on WhatsApp. Please do not include confidential records.';}
    finally{busy=false;button.disabled=saved;}
  });
})();
