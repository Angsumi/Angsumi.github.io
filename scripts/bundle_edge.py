from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
core=(ROOT/'supabase/functions/_shared/core.mjs').read_text().replace('export ','')
for name in ['lead-api','lead-notifications']:
 entry=(ROOT/'supabase/functions'/name/'index.js').read_text()
 entry=re.sub(r"^import .* from '\.\.?/[^']+';\n",'',entry,flags=re.M)
 handler=(ROOT/'supabase/functions/lead-api/handler.mjs').read_text() if name=='lead-api' else ''
 handler=re.sub(r"^import .*;\n",'',handler,flags=re.M).replace('export ','')
 output=Path('/tmp')/('angsumi-'+name+'.js');output.write_text(core+'\n'+handler+'\n'+entry)
 print(output)
