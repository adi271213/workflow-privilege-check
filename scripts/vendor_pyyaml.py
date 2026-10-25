"""Refresh the pinned dependency at maintenance time, never during Action execution."""
from pathlib import Path
import hashlib,io,json,urllib.request,zipfile
root=Path(__file__).resolve().parents[1]
meta=json.load(urllib.request.urlopen('https://pypi.org/pypi/PyYAML/6.0.3/json'))
wheel=next(x for x in meta['urls'] if x['filename'].endswith('cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl'))
blob=urllib.request.urlopen(wheel['url']).read();assert hashlib.sha256(blob).hexdigest()==wheel['digests']['sha256']
dest=root/'vendor/pyyaml';dest.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(io.BytesIO(blob)) as archive:
    files=[n for n in archive.namelist() if n.startswith('yaml/') and n.endswith('.py') and len(Path(n).parts)==2]
    assert len(files)>=15
    for name in files:
        path=dest/name;path.parent.mkdir(exist_ok=True);path.write_bytes(archive.read(name))
    license=next(n for n in archive.namelist() if n.endswith('/LICENSE'))
    (dest/'LICENSE').write_bytes(archive.read(license))
manifest={'name':'PyYAML','version':'6.0.3','sourceWheel':wheel['filename'],'sourceURL':wheel['url'],'sourceSha256':wheel['digests']['sha256'],'contents':'Unmodified pure-Python yaml package and MIT license; compiled optional extensions omitted.','files':{name:hashlib.sha256((dest/name).read_bytes()).hexdigest() for name in sorted(files+['LICENSE'])}}
(dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Verified upstream wheel; bundled',len(files),'Python files and license; no compiled binaries.')
