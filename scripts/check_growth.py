from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re

ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.labels=[];self.scripts=[];self.h1=0;self.title=0;self.canonical=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if tag in ('a','link') and d.get('href'):self.links.append(d['href'])
  if tag=='script' and d.get('src'):self.links.append(d['src'])
  if tag=='label' and d.get('for'):self.labels.append(d['for'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title+=1
  if tag=='link' and d.get('rel')=='canonical':self.canonical=True

def main():
 paths=list((ROOT/'inquiry').rglob('*.html'))+list((ROOT/'resources').rglob('*.html'))+list((ROOT/'portfolio').rglob('*.html'))+list((ROOT/'training').rglob('*.html'))
 paths += [ROOT/'services'/slug/'index.html' for slug in ['rna-seq-analysis','metagenomics-analysis','bioinformatics-consulting','scientific-data-analysis','scientific-figure-preparation','python-research-automation']]
 for path in paths:
  p=Parser();text=path.read_text();p.feed(text)
  assert len(p.ids)==len(set(p.ids)),f'Duplicate IDs: {path}'
  assert all(label in p.ids for label in p.labels),f'Unbound label: {path}'
  assert p.h1==p.title==1 and p.canonical,f'Page metadata: {path}'
  for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):json.loads(match[1])
  for link in p.links:
   u=urlparse(link)
   if u.scheme or u.netloc or not u.path:continue
   target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
   if target.is_dir():target=target/'index.html'
   assert target.is_file(),f'Missing local destination {link} in {path}'
 print(f'Checked {len(paths)} new pages: metadata, JSON-LD, unique IDs, form labels and local destinations')

if __name__=='__main__':main()
