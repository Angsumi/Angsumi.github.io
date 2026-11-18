"""Blog: Markdown posts in scripts/content/blog/*.md -> /blog/<slug>/ pages, index, RSS feed and cluster links.

Front-matter (between --- lines): title, description, date, updated (optional), cluster, service, guide,
and faq as a list of `- q:` / `  a:` pairs. The first paragraph is the 40–60-word direct answer.
Markdown subset: ## and ### headings, paragraphs, - and 1. lists, | tables |, **bold**, `code`, [links](url).
"""
from pathlib import Path
from html import escape
from datetime import date
import re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'scripts/content/blog'
SITE='https://angsumi.online/'
FEED='<link rel="alternate" type="application/rss+xml" title="ANGSUMI blog" href="/blog/feed.xml">'

def front_matter(raw):
    _,head,body=raw.split('---\n',2)
    meta,faq={},[]
    for line in head.splitlines():
        if line.startswith('  - q:'):faq.append([line[6:].strip(),''])
        elif line.startswith('    a:'):faq[-1][1]=line[6:].strip()
        elif ':' in line and not line.startswith(' '):
            key,value=line.split(':',1);meta[key.strip()]=value.strip()
    meta['faq']=faq
    return meta,body.strip()

def inline(s):
    s=escape(s,quote=False)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def render(markdown):
    html=[]
    for block in re.split(r'\n\s*\n',markdown):
        lines=block.strip().splitlines()
        first=lines[0]
        if first.startswith('### '):html.append(f'<h3 id="{slug(first[4:])}">{inline(first[4:])}</h3>')
        elif first.startswith('## '):html.append(f'<h2 id="{slug(first[3:])}">{inline(first[3:])}</h2>')
        elif first.startswith('- '):html.append('<ul>'+''.join(f'<li>{inline(l[2:])}</li>' for l in lines)+'</ul>')
        elif re.match(r'\d+\. ',first):html.append('<ol>'+''.join(f'<li>{inline(l.split(". ",1)[1])}</li>' for l in lines)+'</ol>')
        elif first.startswith('|'):
            rows=[[c.strip() for c in l.strip('|').split('|')] for l in lines if not re.match(r'^\|[\s:|-]+\|$',l)]
            head=''.join(f'<th scope="col">{inline(c)}</th>' for c in rows[0])
            body=''.join('<tr>'+f'<th scope="row">{inline(r[0])}</th>'+''.join(f'<td>{inline(c)}</td>' for c in r[1:])+'</tr>' for r in rows[1:])
            html.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
        else:html.append('<p>'+inline(' '.join(lines))+'</p>')
    return '\n'.join(html)

def human(d):
    return date.fromisoformat(d).strftime('%-d %B %Y')

def load():
    posts=[]
    for path in sorted(SOURCE.glob('*.md')):
        meta,body=front_matter(path.read_text())
        answer,rest=body.split('\n\n',1)
        meta.update(slug=path.stem,answer=' '.join(answer.split()),body=rest,
                    citations=sorted(set(re.findall(r'\]\((https?://[^)\s]+)\)',body))))
        posts.append(meta)
    return sorted(posts,key=lambda p:p['date'],reverse=True)

def build(page,guides):
    """Generate posts, index and feed; return posts for sitemap and llms.txt."""
    posts=load()
    guide_titles={g[0]:g[1] for g in guides}
    for p in posts:
        updated=p.get('updated',p['date'])
        byline=f'<p class="byline">By <a href="/about/">Angsuman Das</a> · Published <time datetime="{p["date"]}">{human(p["date"])}</time>'+(f' · Updated <time datetime="{updated}">{human(updated)}</time>' if updated!=p['date'] else '')+'</p>'
        faq=''.join(f'<details><summary>{inline(q)}</summary><p>{inline(a)}</p></details>' for q,a in p['faq'])
        body=(f'<article class="post"><div class="eyebrow"><a href="/blog/">Blog</a> · {escape(p["cluster"])}</div><h1>{escape(p["title"])}</h1>{byline}'
              f'<p class="intro answer">{inline(p["answer"])}</p>{render(p["body"])}'
              +(f'<section><h2>Common questions</h2>{faq}</section>' if faq else '')+
              f'<section class="notice"><h2>Plan your analysis</h2><p>Read the <a href="/resources/{p["guide"]}/">{escape(guide_titles[p["guide"]])}</a> guide, or see the matching <a href="/services/{p["service"]}/">analysis service</a>.</p>'
              f'<a class="btn" href="/inquiry/?category=research&amp;service={p["service"]}&amp;campaign=blog-{p["slug"]}">Discuss my dataset →</a></section></article>')
        page('blog/'+p['slug'],p['title'],p['description'],body,FEED,
             article={'date':p['date'],'updated':updated,'cluster':p['cluster'],'service':p['service'],'citations':p['citations']})
    cards=''.join(f'<article class="card"><span class="tag">{escape(p["cluster"])}</span><h2 style="font-size:28px"><a href="/blog/{p["slug"]}/">{escape(p["title"])}</a></h2><p>{escape(p["description"])}</p><p class="help"><time datetime="{p["date"]}">{human(p["date"])}</time></p></article>' for p in posts)
    page('blog','Bioinformatics analysis blog','Practical, source-cited explanations of RNA-seq, metagenomics and research data analysis decisions.',
         f'<div class="eyebrow">Blog</div><h1>Analysis decisions, explained.</h1><p class="intro">Practical explanations of bioinformatics methods and choices, with links to the primary documentation behind each claim.</p><div class="grid">{cards}</div>',FEED)
    items=''.join(f'<item><title>{escape(p["title"])}</title><link>{SITE}blog/{p["slug"]}/</link><guid>{SITE}blog/{p["slug"]}/</guid><pubDate>{date.fromisoformat(p["date"]).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate><description>{escape(p["description"])}</description></item>' for p in posts)
    (ROOT/'blog/feed.xml').write_text(f'<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel><title>ANGSUMI blog</title><link>{SITE}blog/</link><description>Bioinformatics and research data analysis, explained.</description><language>en</language>{items}</channel></rss>\n')
    # Topic-cluster links: each service and planning guide points back to its posts.
    for p in posts:
        link=f'<li><a href="/blog/{p["slug"]}/">{escape(p["title"])}</a></li>'
        for target in (ROOT/'services'/p['service']/'index.html',ROOT/'resources'/p['guide']/'index.html'):
            html=target.read_text()
            if '<section id="further-reading">' not in html:
                html=html.replace('</main>','<section id="further-reading"><h2>Further reading</h2><ul></ul></section></main>')
            target.write_text(html.replace('<section id="further-reading"><h2>Further reading</h2><ul>','<section id="further-reading"><h2>Further reading</h2><ul>'+link,1))
    return posts
