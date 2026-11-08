(() => {
  'use strict';
  const form = document.querySelector('#intake');
  if (!form) return;
  const local = ['127.0.0.1', 'localhost'].includes(location.hostname);
  const configured = window.ANGSUMI_LEADS_API;
  const base = local ? '' : typeof configured === 'string' && /^https:\/\/[a-z0-9.-]+(?:\/functions\/v1\/lead-api)?$/.test(configured) ? configured : null;
  const status = document.querySelector('#intake-status');
  const steps = [...form.querySelectorAll('[data-step]')];
  let step = 0, busy = false, started = false, saved = false;
  let submissionKey = crypto.randomUUID();
  // Fixed public labels only; never read user-entered content for analytics.
  const category = form.elements.category;
  const validCategories = ['research', 'training'];
  const params = new URLSearchParams(location.search);
  if (validCategories.includes(params.get('category'))) category.value = params.get('category');
  const knownServices = ['rna-seq-analysis','metagenomics-analysis','bioinformatics-consulting','scientific-data-analysis','scientific-figure-preparation','python-research-automation'];
  if (knownServices.includes(params.get('service'))) form.elements.project_type.value = params.get('service');
  const campaign = ['research-checklist','bioinformatics-labs','workshop'].includes(params.get('campaign')) ? params.get('campaign') : 'none';
  const source = ['google','instagram','github','youtube','referral'].includes(params.get('utm_source')) ? params.get('utm_source') : document.referrer ? 'other' : 'direct';
  const knownLandingPaths = ['/', '/resources/', '/resources/labs/', '/portfolio/', '/training/', '/services/rna-seq-analysis/', '/services/metagenomics-analysis/', '/services/bioinformatics-consulting/', '/services/scientific-data-analysis/', '/services/scientific-figure-preparation/', '/services/python-research-automation/'];
  let landingPage = '/inquiry/';
  try { const ref = new URL(document.referrer); if (ref.origin===location.origin && knownLandingPaths.includes(ref.pathname)) landingPage=ref.pathname; } catch (_) { /* Direct visit. */ }
  const track = (name) => window.angsumiTrackBusiness?.(name, {category:category.value, campaign});
  function message(text, error=false) { status.textContent=text; status.dataset.error=String(error); }
  function conditions() {
    form.querySelectorAll('[data-category]').forEach(el => {
      const active = el.dataset.category === category.value;
      el.hidden = !active;
      el.querySelectorAll('input,select,textarea').forEach(input => input.disabled = !active);
    });
  }
  function show(index) {
    step=index;
    steps.forEach((el,i) => el.hidden = i!==index);
    document.querySelectorAll('[data-step-label]').forEach((el,i) => {
      if (i===index) el.setAttribute('aria-current','step'); else el.removeAttribute('aria-current');
    });
    document.querySelector('#progress-bar').style.width = `${(index+1)/3*100}%`;
    document.querySelector('#back').hidden=index===0;
    document.querySelector('#next').hidden=index===2;
    document.querySelector('#send').hidden=index!==2;
    const heading=steps[index].querySelector('legend'); heading.tabIndex=-1; heading.focus();
  }
  const valid = () => [...steps[step].querySelectorAll('input,select,textarea')].filter(el=>!el.disabled).every(el=>el.reportValidity());
  category.addEventListener('change',conditions); conditions();
  document.querySelector('#next').addEventListener('click',()=>{if(valid()){message('');show(step+1);}});
  document.querySelector('#back').addEventListener('click',()=>show(step-1));
  form.addEventListener('input',()=>{if(!started){started=true;track('form_start');}});
  window.addEventListener('pagehide',()=>{if(started&&!saved)track('form_abandonment');});
  if (base===null) {
    message('Structured inquiry delivery is being configured. Use the email or WhatsApp contact links below; this form will not claim to save an inquiry.',true);
    document.querySelector('#send').disabled=true;
  }
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(step<2){if(valid())show(step+1);return;}
    if(busy||saved||base===null||!valid())return;
    busy=true;document.querySelector('#send').disabled=true;message('Saving your inquiry…');
    const data = new FormData(form), details={};
    form.querySelectorAll('[data-detail]:not(:disabled)').forEach(el=>details[el.name]=el.value);
    const payload={name:data.get('name'),email:data.get('email'),phone:data.get('phone')||'',category:category.value,
      description:data.get('description'),budget:data.get('budget')||'',details,source,campaign,landing_page:landingPage,
      website:data.get('website'),contact_consent:data.get('contact_consent')==='on',marketing_consent:data.get('marketing_consent')==='on'};
    try {
      const response=await fetch(base+'/api/leads',{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':submissionKey,...(window.ANGSUMI_SUPABASE_PUBLIC_KEY?{apikey:window.ANGSUMI_SUPABASE_PUBLIC_KEY,Authorization:'Bearer '+window.ANGSUMI_SUPABASE_PUBLIC_KEY}:{})},body:JSON.stringify(payload),signal:AbortSignal.timeout(20000)});
      const result=await response.json();
      if(!response.ok||result.saved!==true||!/^ANG-[A-F0-9]{16}$/.test(result.id))throw Error('not saved');
      saved=true;form.hidden=true;
      const success=document.querySelector('#success');success.hidden=false;
      document.querySelector('#lead-reference').textContent=result.id;success.focus();
      if(!result.duplicate)track('generate_lead');
      message('');
    } catch (_) {
      message('We could not confirm your inquiry was saved. Retry with the same details, or contact us directly. A retry will not create a second identical inquiry.',true);
    } finally {busy=false;document.querySelector('#send').disabled=saved;}
  });
})();
