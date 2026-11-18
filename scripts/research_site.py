"""Research-only shared pages and deterministic retirement/sitemap policy."""
from pathlib import Path
from html import escape
import json
from research_content import build_guides, GUIDES
import urllib.request
from xml.etree.ElementTree import Element, SubElement, tostring
import re
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
SITE='https://angsumi.online/'

# One identity graph, referenced by @id on every page so search and answer engines resolve a single entity.
ORG={'@type':'Organization','@id':SITE+'#organization','name':'ANGSUMI','url':SITE,'logo':SITE+'logo.png',
     'email':'angudas62@gmail.com','founder':{'@id':SITE+'#person'},'sameAs':['https://github.com/Angsumi']}
PERSON={'@type':'Person','@id':SITE+'#person','name':'Angsuman Das','url':SITE+'cv/',
        'description':'CSIR-UGC NET JRF qualified life-science researcher and bioinformatician.',
        'worksFor':{'@id':SITE+'#organization'},
        'knowsAbout':['Bioinformatics','RNA-seq analysis','Metagenomics','Scientific data analysis','Python'],
        'sameAs':['https://orcid.org/0000-0001-8146-7697','https://www.linkedin.com/in/angsumi/',
                  'https://www.researchgate.net/profile/Angsuman-Das-2','https://github.com/Angsumi']}
PREVIEWS=[('RNA-seq analysis','md-rnaseq','https://angsumi.online/MD_RNAseq/','Explore the existing transcriptomic analysis dashboard.'),
          ('Shruti — de novo RNA-seq','shruti-rnaseq-denovo','https://angsumi.online/Shruti_RNAseq_DeNovo/','Explore the existing de novo transcriptome analysis project.'),
          ('Sahil — metagenomics','sahil-metagenome','https://angsumi.online/Sahil_Metagenome/','Explore the existing environmental metabarcoding project.')]
SECTIONS={'services':'Services','resources':'Resources'}
BLOG='https://blog.angsumi.online/'
LEARN='https://learn.angsumi.online/'

def blog_posts():
    """Posts published by the blog repo (blog.angsumi.online/posts.json), cached so offline builds stay deterministic."""
    cache=ROOT/'scripts/blog_posts.json'
    try:
        posts=json.load(urllib.request.urlopen(BLOG+'posts.json',timeout=20))
        cache.write_text(json.dumps(posts,indent=1)+'\n')
    except Exception:
        posts=json.loads(cache.read_text()) if cache.exists() else []
    return posts

def blog_stubs(posts):
    """Old /blog/ URLs forward to the blog subdomain (GitHub Pages cannot send 301s)."""
    for path,target in [('blog',BLOG)]+[('blog/'+q['slug'],q['url']) for q in posts]:
        out=ROOT/path/'index.html';out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved to the ANGSUMI blog</title><meta name="robots" content="noindex"><link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0; url={target}"></head><body><p>This article is now at <a href="{target}">{target}</a>.</p></body></html>\n')

def cluster_links(posts):
    """Each service page and planning guide links to its blog posts."""
    for q in posts:
        link=f'<li><a href="{q["url"]}">{escape(q["title"])}</a></li>'
        for target in (ROOT/'services'/q['service']/'index.html',ROOT/'resources'/q['guide']/'index.html'):
            if not target.exists():continue
            html=target.read_text()
            if '<section id="further-reading">' not in html:
                html=html.replace('</main>','<section id="further-reading"><h2>Further reading</h2><ul></ul></section></main>')
            target.write_text(html.replace('<section id="further-reading"><h2>Further reading</h2><ul>','<section id="further-reading"><h2>Further reading</h2><ul>'+link,1))

def text(fragment):
    return ' '.join(unescape(re.sub(r'<[^>]+>',' ',fragment)).split())

def faq(html):
    return [{'@type':'Question','name':text(q),'acceptedAnswer':{'@type':'Answer','text':text(a)}}
            for q,a in re.findall(r'<details><summary>(.*?)</summary>(.*?)</details>',html,re.S)]

def structured_data(path,title,description,html):
    """JSON-LD @graph for a generated page: identity, page, breadcrumbs, FAQ and type-specific nodes."""
    url=SITE+(path+'/' if path else '')
    webpage={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,
             'isPartOf':{'@id':SITE+'#website'},'publisher':{'@id':SITE+'#organization'},'inLanguage':'en'}
    graph=[ORG,{'@type':'WebSite','@id':SITE+'#website','name':'ANGSUMI','url':SITE,'publisher':{'@id':SITE+'#organization'}},webpage]
    questions=faq(html)
    if questions:
        webpage['@type']=['WebPage','FAQPage'];webpage['mainEntity']=questions
    parts=path.split('/') if path else []
    if parts:
        crumbs=[('Home',SITE)]+[(SECTIONS[p],SITE+p+'/') for p in parts[:-1] if p in SECTIONS]+[(title,url)]
        webpage['breadcrumb']={'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i,'name':n,'item':u} for i,(n,u) in enumerate(crumbs,1)]}
    services=json.loads((ROOT/'scripts/services.json').read_text())
    if not path:
        graph+=[PERSON,{'@type':'ProfessionalService','@id':SITE+'#service','name':'ANGSUMI','url':SITE,
            'description':description,'image':SITE+'og-icon.png','logo':SITE+'logo.png','email':'angudas62@gmail.com',
            'telephone':'+91-7896595109','parentOrganization':{'@id':SITE+'#organization'},'founder':{'@id':SITE+'#person'},
            'knowsAbout':PERSON['knowsAbout'],'sameAs':ORG['sameAs'],
            'hasOfferCatalog':{'@type':'OfferCatalog','name':'Research analysis services','itemListElement':[
                {'@type':'Offer','itemOffered':{'@type':'Service','name':s[1],'url':SITE+'services/'+s[0]+'/'}} for s in services]}}]
    elif path in ('about','cv'):
        graph.append(PERSON);webpage['about']={'@id':SITE+'#person'}
    elif path.startswith('services/'):
        graph.append({'@type':'Service','@id':url+'#service','name':title,'description':description,'url':url,
                      'serviceType':title,'provider':{'@id':SITE+'#organization'}})
    return {'@context':'https://schema.org','@graph':graph}

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
    home=ROOT/'index.html'
    html=home.read_text()
    # Static thumbnails (assets/previews, captured from the live projects) replace heavy cross-site iframes.
    previews='<section id="client-work"><h2>Client research work previews</h2><div class="grid">'
    for name,slug,url,description in PREVIEWS:
        previews+=f'<article class="card project-preview"><a href="{url}"><img src="/assets/previews/{slug}.webp" alt="" width="640" height="400" loading="lazy" decoding="async"><h3>{escape(name)}</h3></a><p>{description}</p></article>'
    previews+='</div></section>'
    html=html.replace('<section id="deliverables">',previews+'<section id="deliverables">')
    html=html.replace('</main>',(ROOT/'scripts/content/home-form.html').read_text()+'</main>')
    html=html.replace('</head>','<script defer src="/assets/lead-runtime.js"></script><script defer src="/assets/home-intake.js"></script></head>')
    home.write_text(html)
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
    posts=blog_posts();blog_stubs(posts);cluster_links(posts)
    latest='<section id="blog"><h2>From the blog.</h2><div class="grid">'+''.join(f'<article class="card"><h3><a href="{q["url"]}">{escape(q["title"])}</a></h3><p>{escape(q["description"])}</p></article>' for q in posts[:3])+'</div><a href="'+BLOG+'">All articles →</a></section>'
    home.write_text(home.read_text().replace('<section id="deliverables">',latest+'<section id="deliverables">',1))
    # Indexable pages only. Private owner/unsubscribe routes and custom 404 are excluded.
    paths=['','cv']+[p.parent.relative_to(ROOT).as_posix() for family in ['about','services','resources','portfolio','training','inquiry','privacy-policy','terms'] for p in (ROOT/family).rglob('index.html')]
    paths += ['MD_RNAseq']  # Independently served research project on this host.
    urls=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in sorted(set(paths)):
        SubElement(SubElement(urls,'url'),'loc').text='https://angsumi.online/'+(path+'/' if path else '')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="utf-8"?>\n'+tostring(urls,encoding='unicode')+'\n')
    write_robots_and_llms(services,posts)

# Search and answer-engine crawlers named explicitly so a future blanket rule cannot silently block them.
AI_CRAWLERS=['Googlebot','Bingbot','GPTBot','OAI-SearchBot','ChatGPT-User','PerplexityBot','ClaudeBot','Claude-SearchBot','Google-Extended','Applebot']

def write_robots_and_llms(services,posts):
    robots=''.join(f'User-agent: {bot}\nAllow: /\n\n' for bot in AI_CRAWLERS)
    robots+='User-agent: *\nAllow: /\n\nSitemap: https://angsumi.online/sitemap.xml\n'
    (ROOT/'robots.txt').write_text(robots)
    # llms.txt (https://llmstxt.org): a plain summary answer engines can read; facts only, no outcome claims.
    lines=['# ANGSUMI — bioinformatics and scientific data analysis','',
           '> ANGSUMI provides scoped, reproducible bioinformatics and scientific data analysis for research labs, PIs and PhD scholars: RNA-seq, metagenomics and microbiome analysis, research automation in Python, and publication figures. Every project starts with a feasibility review and a written scope. Run by Angsuman Das.','',
           '## Services']
    lines+=[f'- [{title}](https://angsumi.online/services/{slug}/): {desc}' for slug,title,_,desc,*_ in services]
    lines+=['','## Planning guides']
    lines+=[f'- [{title}](https://angsumi.online/resources/{slug}/)' for slug,title,*_ in GUIDES]
    lines+=['','## Blog']
    lines+=[f'- [{q["title"]}]({q["url"]}): {q["description"]}' for q in posts]
    lines+=['','## Research projects',
            '- [Bioinformatics & multi-omics learning hub](https://learn.angsumi.online/): interactive guides and workflows for genomics, transcriptomics, proteomics and microbiome data.',
            '- [RNA-seq transcriptomic analysis dashboard](https://angsumi.online/MD_RNAseq/): example transcriptome analysis project.',
            '- [De novo transcriptome analysis](https://angsumi.online/Shruti_RNAseq_DeNovo/): example de novo RNA-seq project.',
            '- [Environmental metabarcoding](https://angsumi.online/Sahil_Metagenome/): example environmental metabarcoding project.',
            '','## About',
            '- [About ANGSUMI](https://angsumi.online/about/)',
            '- [Angsuman Das — academic profile](https://angsumi.online/cv/)',
            '- [Research portfolio](https://angsumi.online/portfolio/)',
            '- [Start an inquiry](https://angsumi.online/inquiry/)',
            '- [GitHub](https://github.com/Angsumi)','']
    (ROOT/'llms.txt').write_text('\n'.join(lines))
