"""Apply small, repeatable changes to retained static pages after legacy generators."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'index.html';s=p.read_text()
s=s.replace('Get a Free Project Review <span class="arrow-icon">→</span>','Discuss a Research Project <span class="arrow-icon">→</span>')
s=s.replace('<a class="btn-primary-pill" href="#cta">','<a class="btn-primary-pill" href="/inquiry/?category=research" data-growth-event="cta_click" data-category="research">',1)
s=s.replace('<a class="btn-secondary-pill" href="#proof">\n                <span class="play-icon">▶</span> See Real Work','<a class="btn-secondary-pill" href="/inquiry/?category=digital" data-growth-event="cta_click" data-category="digital">\n                Build My Digital Solution')
s=s.replace('Bioinformatics, scientific data analysis, websites and custom digital systems for researchers and growing organizations.','You do the research. We help your data speak. Bioinformatics and reproducible analysis for researchers; websites and digital workflows for institutions and growing businesses.')
s=s.replace('<div class="metric-val">3–5 days</div>','<div class="metric-val">Scoped first</div>').replace('<div class="metric-desc">Typical delivery</div>','<div class="metric-desc">Agreed milestones</div>')
s=s.replace('aria-label="Key Metrics &amp; Guarantees"','aria-label="Project planning and starting scope"')
s=s.replace('Every website we engineer achieves <strong>sub-second load speeds</strong> and a 100% Core Web Vitals score on mobile. We hand-code clean semantic HTML, CSS, and modern JavaScript, completely eliminating the database bloat and security vulnerabilities of 30+ slow WordPress plugins.','We test representative pages on mobile and desktop and review loading, layout and interaction. Performance depends on the page, hosting, device and connection. We agree measurable targets and report test conditions rather than guaranteeing a perfect score.')
s=s.replace('Standard starter websites and focused bioinformatics data sprints are delivered within 3 to 5 business days. Advanced portals, custom apps, and complex multi-omics pipelines typically take 7 to 14 days.','Timeline depends on input readiness, analysis or software complexity, review rounds and integrations. We agree milestones and acceptance checks after scoping your project.')
s=s.replace('<strong>No.</strong> Unlike SaaS platforms like Wix, Squarespace, or Shopify that charge ₹2,000–₹4,000 every single month for basic features and transaction fees, Angsumi gives you <strong>100% source code ownership</strong> with one-time transparent pricing and zero monthly platform hostage fees.','Hosting, domains, messaging, payment providers and ongoing support can have recurring costs. We itemize these during scoping and agree source-code ownership and third-party license terms in writing.')
s=s.replace('Our starter websites start at <strong>₹2,000 fixed price</strong> with zero agency bloat. Specialized bioinformatics and data analysis consulting starts from <strong>₹3,000</strong> depending on dataset complexity and project scope. Multi-page business web portals start from ₹5,000, and full custom web platforms/apps range from ₹8,500 to ₹18,000.','Displayed starting prices are indicative entry scopes, not a quote for a complete research workflow or custom platform. Research analysis is quoted after reviewing study design, data scale, deliverables and compute. Hosting, provider charges, revisions and support are itemized in the proposal.')
s=s.replace('<div class="metric-val">&#8377;3,000+</div>','<div class="metric-val">By scope</div>')
# Research card must not promise a full analytical project at an inconsistent entry price.
s=s.replace('<h3>Bioinformatics &amp; Data</h3>\n              <div class="amount-wrap">\n                <div class="amount-main">$24</div>\n                <div class="amount-sub">₹2,000</div>','<h3>Bioinformatics &amp; Data</h3>\n              <div class="amount-wrap">\n                <div class="amount-main">Scoped quote</div>\n                <div class="amount-sub">After project review</div>')
s=s.replace('Every website we engineer achieves sub-second load speeds and a 100% Core Web Vitals score on mobile.','Performance is measured for the agreed pages, hosting and test conditions.')
s=s.replace('href="https://angsumi.online/ADRE/"','href="/training/"')
s=s.replace('href="/ADRE"','href="/training/"').replace('src="/ADRE"','src="/training/"')
# Keep the old endpoint while the new API is being configured.
s=s.replace('id="form_phone" required','id="form_phone"')
if 'id="legacy-consent"' not in s:
 s=s.replace('<form action="https://formspree.io/f/xwlegzkn" method="POST" id="requirementsForm">','<form action="https://formspree.io/f/xwlegzkn" method="POST" id="requirementsForm">\n<p><a href="/inquiry/">Use the guided research, digital or training inquiry →</a></p><input type="text" name="_gotcha" tabindex="-1" aria-hidden="true" style="position:absolute;left:-10000px" autocomplete="off">')
 s=s.replace('<!-- Trust Badge -->','<label style="display:flex;gap:12px;align-items:flex-start;margin:16px 0"><input id="legacy-consent" type="checkbox" required name="contact_consent"><span>You may contact me about this inquiry. <a href="/privacy-policy/">Privacy notice</a>. Do not include confidential records.</span></label>\n<!-- Trust Badge -->')
s=s.replace('Your inquiry is sent securely to Angsumi. We usually respond within a few hours via WhatsApp or email.','This existing contact route uses Formspree to deliver your inquiry. Please do not include confidential records. A response time is agreed when we contact you.')
section='''<!-- growth-pathways:start --><section style="padding:60px 24px;background:#faf7ef;color:#292b29"><div style="max-width:1120px;margin:auto"><p style="letter-spacing:.15em;color:#642e3c;font-size:12px;font-weight:700">RESEARCH · BUILD · LEARN</p><h2 style="font:42px/1.15 Georgia,serif">Three goals. Three clear starting points.</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:24px"><article style="padding:26px;border:1px solid #dddcd1"><h3>Research &amp; bioinformatics</h3><p>Have RNA-seq data, a microbiome question or figures that need a clearer story?</p><p><a href="/services/rna-seq-analysis/">RNA-seq</a> · <a href="/services/metagenomics-analysis/">Metagenomics</a> · <a href="/services/scientific-figure-preparation/">Scientific figures</a></p><a href="/inquiry/?category=research">Discuss a Research Project →</a></article><article style="padding:26px;border:1px solid #dddcd1"><h3>Digital systems &amp; software</h3><p>Still coordinating bookings, school workflows or business inquiries through scattered messages?</p><p><a href="/services/doctor-clinic-website-design/">Clinic websites</a> · <a href="/services/school-management-system/">School systems</a> · <a href="/services/online-exam-portal-development/">Exam platforms</a></p><a href="/inquiry/?category=digital">Build My Digital Solution →</a></article><article style="padding:26px;border:1px solid #dddcd1"><h3>Education &amp; training</h3><p>Learn bioinformatics, Python and reproducible research one practical workflow at a time.</p><p><a href="/resources/labs/">Find an interactive lab</a> · <a href="/resources/">Download free checklists</a></p><a href="/training/">Explore learning &amp; workshops →</a></article></div><p style="margin-top:24px"><a href="/portfolio/">Explore source-backed work and methods →</a></p></div></section><!-- growth-pathways:end -->'''
if '<!-- growth-pathways:start -->' in s:s=re.sub(r'<!-- growth-pathways:start -->.*?<!-- growth-pathways:end -->',section,s,flags=re.S)
else:s=s.replace('<section class="hero" id="hook">', '<section class="hero" id="hook">',1).replace('    <section class="cta-section" id="cta">',section+'\n    <section class="cta-section" id="cta">',1)
s=s.replace('<div class="metric-val">100%</div>','<div class="metric-val">Agreed terms</div>').replace('Code &amp; data ownership','Source &amp; license ownership')
s=s.replace('<strong>Yes, 100%.</strong> You retain complete legal ownership of your domain name, website source code, data analysis scripts, research results, and database. You are never locked into our services and can host or migrate your files anywhere you want.','Ownership, handover, hosting accounts and third-party license conditions are agreed in the proposal. Research data rights and authorship follow the applicable agreements and permissions.')
s=s.replace('Standard starter websites and focused bioinformatics data sprints are delivered within <strong>3 to 5 business days</strong>. Advanced portals, custom apps, and complex multi-omics pipelines typically take 7 to 14 days.','Timeline depends on input readiness, complexity, review rounds and integrations. We agree milestones after scoping your project.')
s=s.replace('nipam.web.app','nipam-fb25f.web.app')
s=s.replace('angsumi.online/ADRE','angsumi.online/bioinformatics/').replace('https://angsumi.online/bioinformatics//','https://angsumi.online/bioinformatics/')
s=s.replace('AxomRank Prep Engine','Bioinformatics Learning Labs').replace('Focused practice and mock test portal built for Assam\'s ADRE / SLRC examination candidates, providing fast mobile test-taking capabilities.','Ten interactive learning laboratories covering alignment, transcriptomics, microbial analysis and structural biology.')
s=s.replace('> ADRE / SLRC</li>','> Bioinformatics</li>').replace('> Mock Tests</li>','> Interactive Labs</li>').replace('> Instant Scoring</li>','> Workflow Concepts</li>').replace('> Assam Exam Prep</li>','> Research Learning</li>').replace('Explore AxomRank','Explore Learning Labs').replace('Exam Preparation','Research Education')
s=s.replace('href="/training/" target="_blank"','href="/resources/labs/" target="_blank"')
s=s.replace('href="#proof" class="btn-discuss-green"','href="/inquiry/?category=research" class="btn-discuss-green"').replace('href="#cta" class="btn-discuss-peach"','href="/inquiry/?category=digital" class="btn-discuss-peach"')
p.write_text(s)
# Add meaningful paths to the retained services directory and selected existing service pages.
for relative in ['services/index.html','services/doctor-clinic-website-design/index.html','services/school-management-system/index.html','services/online-exam-portal-development/index.html']:
 p=ROOT/relative;s=p.read_text()
 addon='''<!-- growth-service:start --><section style="padding:36px 24px;background:#faf7ef;color:#292b29"><div style="max-width:1000px;margin:auto"><h2>Start with the right scope.</h2><p>Agree requirements, access roles, data protection, acceptance checks, hosting and support before development. Provider fees and ongoing maintenance are itemized in the proposal.</p><p><a href="/inquiry/?category=digital">Discuss a digital project →</a> · <a href="/resources/?category=digital">Free requirements templates</a></p><h3>Research and training</h3><p><a href="/services/rna-seq-analysis/">RNA-seq analysis</a> · <a href="/services/metagenomics-analysis/">Metagenomics analysis</a> · <a href="/services/bioinformatics-consulting/">Bioinformatics consulting</a> · <a href="/services/scientific-data-analysis/">Scientific data analysis</a> · <a href="/services/scientific-figure-preparation/">Scientific figures</a> · <a href="/services/python-research-automation/">Python research automation</a> · <a href="/training/">Training</a></p></div></section><!-- growth-service:end -->'''
 if '<!-- growth-service:start -->' in s:s=re.sub(r'<!-- growth-service:start -->.*?<!-- growth-service:end -->',addon,s,flags=re.S)
 else:s=s.replace('</main>',addon+'</main>',1) if '</main>' in s else s.replace('</body>',addon+'</body>')
 p.write_text(s)
# Disclose the new data flow without making a legal-compliance claim.
p=ROOT/'privacy-policy/index.html';s=p.read_text()
privacy='''<!-- growth-privacy:start --><section style="padding:32px;max-width:900px;margin:auto"><h2>Structured project inquiries</h2><p>The structured inquiry system stores the contact details and project scope you choose to provide, your selected pathway, a coarse source/campaign label, consent version, and operational activity such as status, owner notes and follow-up dates. We use it to review and respond to your request. Marketing resources and follow-ups require a separate optional choice, and can be stopped using the unsubscribe route or by contacting us.</p><p>No files are accepted. Do not submit participant data, medical records, credentials or confidential raw research data. An appropriate transfer route is agreed separately. The existing inquiry and workshop forms use Formspree. New structured inquiries are stored in a separately protected lead database when the API is configured; email delivery uses the configured transactional provider.</p><p>Access is restricted to the business owner. Ask ANGSUMI through the published contact route about access, correction or removal of your inquiry. Inactive inquiry retention will be reviewed with the owner before production launch; no indefinite retention is promised. Optional analytics uses fixed non-personal labels and omits form content and URL query details. An inquiry reference confirms storage, not payment, acceptance of work or guaranteed notification delivery.</p></section><!-- growth-privacy:end -->'''
if '<!-- growth-privacy:start -->' in s:s=re.sub(r'<!-- growth-privacy:start -->.*?<!-- growth-privacy:end -->',privacy,s,flags=re.S)
else:s=s.replace('</body>',privacy+'</body>')
p.write_text(s)
# Retain old sitemap entries, then add real pages only.
p=ROOT/'sitemap.xml';s=p.read_text()
paths=['inquiry','resources','resources/labs','portfolio','training']+[f'services/{n}' for n in ['rna-seq-analysis','metagenomics-analysis','bioinformatics-consulting','scientific-data-analysis','scientific-figure-preparation','python-research-automation']]
for path in paths:
 url='https://angsumi.online/'+path+'/'
 if '<loc>'+url+'</loc>' not in s:s=s.replace('</urlset>','<url><loc>'+url+'</loc></url>\n</urlset>')
p.write_text(s)
print('Updated homepage, preserved service pages, privacy notice and sitemap')
# Turn the existing exact-price calculator into an explicit planning estimate.
p=ROOT/'tools/cost-calculator/index.html';s=p.read_text()
replacements={
 'Calculate the exact cost and delivery timeline to build your website, doctor clinic portal, school system, or mobile app in Assam & Northeast India. 100% transparent pricing.':'Explore an indicative budget for a website or digital system. Scope, hosting, provider charges and delivery are confirmed after review.',
 'calculate transparent, fixed pricing and exact delivery turnaround':'explore an indicative project budget and a provisional planning window',
 'Generated Project Estimate':'Indicative Project Estimate',
 'Monthly SaaS Fees:':'Hosting &amp; provider fees:',
 '₹0 Forever':'Quoted separately',
 '100% Client Owned':'Agreed license terms',
 'Lock Quote on WhatsApp':'Discuss This Estimate',
 'Transparent Pricing Guarantee':'Scope before commitment',
 'Why Our Quotes Have Zero Hidden Costs':'What the estimate includes',
 'Traditional agencies in Guwahati and Kolkata charge ₹25,000–₹50,000 for slow WordPress templates. Here is how our transparent direct engineering model works:':'This calculator uses illustrative entry-scope assumptions. Technical review, required integrations and support can change the final proposal.',
 'Fixed Price Promise':'Indicative Budget',
 'The price you see here is the exact price you pay. No extra maintenance taxes or unmentioned server onboarding markups.':'The displayed budget is not a binding quote. Hosting, domain, messaging, payment fees, tax where applicable and ongoing support are assessed separately.',
 'Sub-1s Mobile Speed':'Mobile performance review',
 'Sub-1s Speed':'Performance review',
 'Standard Fast Speed':'Standard scope',
 '⏱️ Delivery:':'Planning window (subject to scope):',
 '✓ Zero advance commitment required.<br>We engineer an interactive prototype for your review first.':'No payment is collected by this calculator. Scope, terms, milestones and any prototype work are agreed separately.'}
for before,after in replacements.items():s=s.replace(before,after)
# One non-personal event on deliberate interaction, not on initial computation.
if 'let calculatorTracked' not in s:
 s=s.replace('    function recalculate() {',"    let calculatorTracked = false;\n    function trackCalculator() { if (!calculatorTracked) { window.angsumiTrackBusiness?.('calculator_usage', {category:'digital'}); calculatorTracked = true; } }\n    function recalculate() {")
 s=s.replace("card.addEventListener('click', () => {", "card.addEventListener('click', () => {\n        trackCalculator();")
 s=s.replace("cb.addEventListener('change', recalculate)","cb.addEventListener('change', () => { trackCalculator(); recalculate(); })")
 s=s.replace("locationSelect.addEventListener('change', recalculate)","locationSelect.addEventListener('change', () => { trackCalculator(); recalculate(); })")
p.write_text(s)

# Replace confirmed broken demo destinations without removing service URLs.
for name in ['online-exam-portal-development','mobile-app-development']:
 p=ROOT/'services'/name/'index.html';s=p.read_text().replace('href="https://angsumi.online/ADRE/"','href="/portfolio/"').replace('Explore Live Case Study','Explore Project Evidence');p.write_text(s)

for relative,url in [('cv/index.html','https://angsumi.online/cv/'),('cv/download.html','https://angsumi.online/cv/download.html')]:
 p=ROOT/relative;s=p.read_text()
 if 'rel="canonical"' not in s:s=s.replace('</head>','<link rel="canonical" href="'+url+'"></head>')
 if relative=='cv/download.html':s=s.replace('href="./comprehensive_resume_data.txt" target="_blank"','href="/cv/"').replace('href="./comprehensive_resume_data.txt" download','href="/cv/"').replace('View TXT','View profile').replace('Download TXT','Read profile')
 p.write_text(s)
p=ROOT/'business/index.html';s=p.read_text().replace('rel="canonical" href="https://angsumi.online/"','rel="canonical" href="https://angsumi.online/business/"')
if 'name="description"' not in s:s=s.replace('</head>','<meta name="description" content="ANGSUMI research and digital project pathways. Discuss scoped analysis, websites and business systems."></head>')
p.write_text(s)

# Enhance the retained homepage form with the same central lead API. Native fallback remains available.
p=ROOT/'index.html';s=p.read_text()
if '/assets/home-intake.js' not in s:s=s.replace('</head>','<script defer src="/assets/lead-runtime.js"></script><script defer src="/assets/home-intake.js"></script></head>')
s=s.replace('This existing contact route uses Formspree to deliver your inquiry. Please do not include confidential records. A response time is agreed when we contact you.','We use these details to review and reply to your inquiry. Please do not include confidential records.')
p.write_text(s)
