"""Package only intentional public files. Audit/backend/runtime material stays private."""
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.server import PUBLIC_DIRS, PUBLIC_FILES, ROOT

def build(destination=None):
    destination=Path(destination or ROOT/'dist').resolve()
    if destination==ROOT or ROOT.is_relative_to(destination):
        raise ValueError('Unsafe output directory')
    destination.mkdir(parents=True,exist_ok=True)
    # Own only this generated artifact directory; never alter source or datasets.
    if any(destination.iterdir()):
        raise ValueError('Output must be empty; choose a fresh artifact directory')
    for name in sorted(PUBLIC_FILES|PUBLIC_DIRS):
        source=ROOT/name
        if not source.exists():
            continue
        if source.is_dir():
            shutil.copytree(source,destination/name,ignore=shutil.ignore_patterns('.*','__pycache__','*.py','*.pyc','*.sqlite*','*.env'))
        else:
            shutil.copy2(source,destination/name)
    forbidden={'backend','docs','scripts','.git','.env','tests','supabase'}
    if any((destination/name).exists() for name in forbidden):
        raise RuntimeError('Private material in public artifact')
    print('Packaged public static site:',destination)
    return destination

if __name__=='__main__':
    build(sys.argv[1] if len(sys.argv)>1 else None)
