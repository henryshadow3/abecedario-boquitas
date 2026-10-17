"""Genera index.html: inserta imágenes, palabras y audios como data URI.
Uso: python3 scripts/build.py src/app.html assets/bocas assets/pictogramas index.html [assets/audio]
"""
import sys, os, json, base64
tpl, imgdir, wdir, out = sys.argv[1:5]
audiodir = sys.argv[5] if len(sys.argv) > 5 else None
def uris(d, ext):
    return {f[:-len(ext)]:'data:image/jpeg;base64,'+base64.b64encode(open(os.path.join(d,f),'rb').read()).decode()
            for f in sorted(os.listdir(d)) if f.endswith(ext)}
def audio_uris(d):
    if not d or not os.path.isdir(d): return {}
    return {f[:-4]:'data:audio/mpeg;base64,'+base64.b64encode(open(os.path.join(d,f),'rb').read()).decode()
            for f in sorted(os.listdir(d)) if f.endswith('.mp3')}
words=json.load(open(os.path.join(wdir,'words.json')))
for v in words.values():
    for w in v: w.pop('page',None)
s=open(tpl).read()
for ph,val in [('/*__IMAGES__*/{}',uris(imgdir,'.jpg')),('/*__PICS__*/{}',uris(wdir,'.jpg')),('/*__WORDS__*/{}',words),('/*__AUDIO__*/{}',audio_uris(audiodir))]:
    assert s.count(ph)==1, ph; s=s.replace(ph, json.dumps(val, ensure_ascii=False, separators=(',',':')))
open(out,'w').write(s)
print(round(os.path.getsize(out)/1024/1024,2),'MB')
