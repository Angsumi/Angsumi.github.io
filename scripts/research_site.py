"""Research-only shared pages and deterministic retirement/sitemap policy."""
from pathlib import Path
from html import escape
import json
from research_content import build_guides, GUIDES
from xml.etree.ElementTree import Element, SubElement, tostring
ROOT=Path(__file__).resolve().parents[1]

def finish(page, services):
    cards=''.join(f'<article class="card"><h3><a href="/services/{slug}/">{escape(title)}</a></h3><p>{escape(desc)}</p></article>' for slug,title,_,desc,*_ in services)
    page('', 'Bioinformatics & scientific data analysis for research labs',
         'Discuss outsourced bioinformatics and scientific data analysis. Scope your question, inputs, reproducible outputs, figures and interpretation with ANGSUMI.', '''
<div class="eyebrow">For scientists · PIs · assistant professors · PhD scholars</div>
<h1>Bioinformatics and scientific data analysis for busy research labs.</h1>
<p class="intro">Stay focused on your experiments. Bring us your research question and dataset; discuss a scoped analysis, interpretable results and reproducible workflows.</p>
<div class="actions"><a class="btn" href="/inquiry/?category=research" data-growth-event="cta_click" data-category="research">Discuss my dataset →</a><a class="btn secondary" href="/portfolio/">View example analysis deliverables</a></div>
<p class="help">Feasibility, supported methods, deliverables and timelines are agreed before work begins.</p>
<section><h2>When the experiment is done, the analysis still needs a plan.</h2><div class="grid"><article class="card"><h3>Data waiting for analysis</h3><p>Start with your biological question, study design and the files you have. We review what can be answered.</p></article><article class="card"><h3>Results that need interpretation</h3><p>Discuss unexplained plots, uncertain comparisons or reviewer requests, with assumptions and limitations made explicit.</p></article><article class="card"><h3>A workflow to repeat</h3><p>Scope documented scripts and a clear handover so your team can understand and revisit the work.</p></article></div></section>
<section><h2>Choose a starting point.</h2><p>These are requests we can review. Each project needs a feasibility assessment before methods or delivery are confirmed.</p><div class="grid">'''+cards+'''</div></section>
<section id="deliverables"><h2>What a scoped handover can contain.</h2><div class="grid"><article class="card"><h3>Quality and provenance</h3><p>Input inventory, sample and metadata checks, QC summary and exclusions with reasons.</p></article><article class="card"><h3>Results and interpretation</h3><p>Analysis tables, readable figures, methods notes, assumptions and limits on what the data support.</p></article><article class="card"><h3>Materials to revisit</h3><p>Agreed scripts, configuration, software versions, reference identifiers and instructions for rerunning.</p></article></div><p>Exact contents, compute costs, code rights, revisions and support are written into your scope.</p><a href="/portfolio/">Inspect the deliverable example and research repositories →</a></section>
<section><h2>From question to handover.</h2><ol><li><strong>Feasibility review:</strong> describe your question and input stage without sending sensitive files.</li><li><strong>Written scope and quote:</strong> agree methods, outputs, costs, milestones and acceptance checks.</li><li><strong>Analysis checkpoints:</strong> review data quality, design choices and interpretation as agreed.</li><li><strong>Handover:</strong> receive the agreed outputs, documentation and support arrangements.</li></ol></section>
<section><h2>Practical questions before you begin.</h2><details><summary>What should I send first?</summary><p>Your research question, assay or data type, approximate sample count, study groups and current stage. Do not upload participant identifiers or raw confidential data.</p></details><details><summary>What will it cost, and how long will it take?</summary><p>Input readiness, design, data scale, compute, interpretation and revision needs determine the quote and milestones. A short inquiry is enough to start the scope discussion.</p></details><details><summary>Will the results be significant or publishable?</summary><p>No analysis can promise significance, biological validation or publication. Conclusions must reflect study design, data quality and uncertainty.</p></details><details><summary>How are data transfer and ownership handled?</summary><p>Agree a suitable transfer method, access, data rights, code licensing and retention arrangements before sharing files. The public inquiry form accepts no uploads.</p></details></section>
<section id="cta"><h2>Tell us where your analysis stands.</h2><p>Start with a short question. No dataset upload is needed.</p><a class="btn" href="/inquiry/?category=research" data-growth-event="cta_click" data-category="research">Discuss my dataset →</a></section>''')
    page('services','Bioinformatics & scientific analysis services','Review research analysis options, inputs, deliverables and feasibility before requesting a scoped quote.', '<div class="eyebrow">Research analysis</div><h1>A clear question. An agreed analysis.</h1><p class="intro">Start with the closest data type or task. Supported assays, tools and capacity are confirmed during feasibility review.</p><div class="grid">'+cards+'</div><section><h2>Not sure where to start?</h2><p>Describe your research question and available files. We can review the scope before choosing a method.</p><a class="btn" href="/inquiry/">Discuss my dataset →</a></section>')
    page('about','About ANGSUMI research analysis','Research-focused analysis, clear project scopes and reproducible handovers.', '''<div class="eyebrow">About ANGSUMI</div><h1>Research questions deserve clear analysis.</h1><p class="intro">ANGSUMI focuses on bioinformatics and scientific data analysis for researchers who need computational support alongside their experimental work.</p><section><h2>Know who you are working with.</h2><p>The existing <a href="/cv/">Angsuman Das academic profile</a> provides background for your review. Discuss the contributor, relevant experience and availability for your particular project during scoping.</p><p>Research repository links are available in the <a href="/portfolio/">methods index</a>. A repository is not proof of a client endorsement, a validated clinical workflow or a publication outcome.</p></section><section><h2>Agree the work before it starts.</h2><p>We begin with the question, input readiness and design. Methods, deliverables, compute, revisions, data arrangements and acceptance checks belong in a written scope.</p><a class="btn" href="/inquiry/">Discuss my dataset →</a></section>''')
    # Illustrative output structure, clearly distinguished from evidence of completed work.
    example='''<section><h2>An illustrative analysis handover.</h2><p>This is an example of folder structure, not a completed analysis or client result. Contents depend on the agreed scope.</p><pre>project/\n  README — question, design and rerun instructions\n  metadata/ — data dictionary and sample manifest\n  qc/ — input checks and documented exclusions\n  results/ — annotated tables and figure exports\n  methods/ — assumptions, references and limitations\n  workflow/ — scripts, configuration and software versions</pre><p>A useful README explains input provenance, commands, expected outputs and any steps requiring external compute or licensed resources.</p><a href="/inquiry/?category=research">Discuss your required deliverables →</a></section>'''
    p=ROOT/'portfolio/index.html';p.write_text(p.read_text().replace('</main>',example+'</main>'))
    page('404','Page not found','This page is unavailable. Browse current research services or contact ANGSUMI.', '<h1>Page not found.</h1><p>This address is unavailable. Browse our current research services or describe the dataset you need help with.</p><div class="actions"><a class="btn" href="/services/">Research services</a><a class="btn secondary" href="/inquiry/">Discuss my dataset</a></div>')
    (ROOT/'404.html').write_text((ROOT/'404/index.html').read_text().replace('<head>','<head><meta name="robots" content="noindex">'))
    (ROOT/'404/index.html').unlink();(ROOT/'404').rmdir()
    # Existing policy body is retained as an authored template, independent of old agency generators.
    for slug,title in [('privacy-policy','Privacy policy'),('terms','Terms of service')]:
        body=(ROOT/'scripts/content'/f'{slug}.html').read_text()
        page(slug,title, f'{title} for ANGSUMI research inquiries and analysis projects.',body)
    for name in json.loads((ROOT/'scripts/retired_urls.json').read_text())['retired_files']:
        target=ROOT/name
        if target.is_file():target.unlink()
    for family in ['business','locations','tools','learning']:
        base=ROOT/family
        if base.exists():
            for directory in sorted(base.rglob('*'),key=lambda p:len(p.parts),reverse=True):
                if directory.is_dir() and not any(directory.iterdir()):directory.rmdir()
            if not any(base.iterdir()):base.rmdir()
    build_guides(page)
    p=ROOT/'resources/index.html'
    guides='<section><h2>Prepare your analysis brief.</h2><div class="grid">'+''.join('<article class="card"><h3><a href="/resources/'+slug+'/">'+escape(title)+'</a></h3><p>Inputs, scope decisions and interpretation limits.</p></article>' for slug,title,*_ in GUIDES)+'</div></section>'
    p.write_text(p.read_text().replace('</main>',guides+'</main>'))
    # Indexable pages only. Private owner/unsubscribe routes and custom 404 are excluded.
    paths=['','cv']+[p.parent.relative_to(ROOT).as_posix() for family in ['about','services','resources','portfolio','training','inquiry','privacy-policy','terms'] for p in (ROOT/family).rglob('index.html')]
    paths += ['bioinformatics','MD_RNAseq']  # Existing independently served research projects, HTTP 200 in baseline crawl.
    urls=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in sorted(set(paths)):
        SubElement(SubElement(urls,'url'),'loc').text='https://angsumi.online/'+(path+'/' if path else '')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="utf-8"?>\n'+tostring(urls,encoding='unicode')+'\n')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://angsumi.online/sitemap.xml\n')
