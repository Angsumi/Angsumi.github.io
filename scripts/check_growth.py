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
 paths=[ROOT/'index.html', ROOT/'404.html']+[p for family in ['about','services','inquiry','resources','portfolio','training','privacy-policy','terms'] for p in (ROOT/family).rglob('*.html')]
 retired=json.loads((ROOT/'scripts/retired_urls.json').read_text())['retired_files']
 assert all(not (ROOT/name).exists() for name in retired),'Retired file regenerated'
 from xml.etree import ElementTree
 sitemap=ElementTree.parse(ROOT/'sitemap.xml')
 for loc in sitemap.findall('.//{*}loc'):
  url=urlparse(loc.text)
  assert not url.query and url.netloc=='angsumi.online','Invalid canonical sitemap URL'
  assert not any(url.path.startswith('/'+family+'/') for family in ['business','locations','tools','learning']),'Retired sitemap family'
  local=ROOT/url.path.lstrip('/')/'index.html'
  assert local.is_file() or url.path in ['/bioinformatics/','/MD_RNAseq/'],f'Sitemap destination missing: {loc.text}'
 home=(ROOT/'index.html').read_text()
 assert 'id="requirementsForm"' in home and '/assets/home-intake.js' in home,'Homepage lead form missing'
 for field in ['form_name','form_email','form_phone','form_represent','form_service','form_budget','form_details','legacy-consent']:
  assert 'id="'+field+'"' in home,'Homepage field missing: '+field
 for project in ['MD_RNAseq','Shruti_RNAseq_DeNovo','Sahil_Metagenome']:
  assert 'src="https://angsumi.online/'+project+'/' in home,'Client preview missing: '+project
 inquiry=(ROOT/'inquiry/index.html').read_text()
 assert 'value="digital"' not in inquiry and 'data-category="digital"' not in inquiry,'Legacy public inquiry category'
 assert 'type="file"' not in inquiry,'Public inquiry must not accept uploads'
 for required in ['contact_consent','marketing_consent','lead-runtime.js','intake.js','name="website"']:
  assert required in inquiry,f'Inquiry contract missing: {required}'
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
 print(f'Checked {len(paths)} public pages: retirement, sitemap, inquiry, metadata, JSON-LD, unique IDs, form labels and local destinations')

if __name__=='__main__':main()
