"""Genera index.html: inserta en src/app.html las imágenes (como data URI) y las palabras.
Uso: python3 scripts/build.py src/app.html assets/bocas assets/pictogramas index.html
"""
import sys, os, json, base64
tpl, imgdir, wdir, out = sys.argv[1:5]
def uris(d, ext):
    return {f[:-len(ext)]:'data:image/jpeg;base64,'+base64.b64encode(open(os.path.join(d,f),'rb').read()).decode()
            for f in sorted(os.listdir(d)) if f.endswith(ext)}
words=json.load(open(os.path.join(wdir,'words.json')))
for v in words.values():
    for w in v: w.pop('page',None)
s=open(tpl).read()
for ph,val in [('/*__IMAGES__*/{}',uris(imgdir,'.jpg')),('/*__PICS__*/{}',uris(wdir,'.jpg')),('/*__WORDS__*/{}',words)]:
    assert s.count(ph)==1, ph; s=s.replace(ph, json.dumps(val, ensure_ascii=False, separators=(',',':')))
open(out,'w').write(s)
print(round(os.path.getsize(out)/1024/1024,2),'MB')
