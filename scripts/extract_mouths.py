"""Extrae las fotos de bocas de la página 2 de cada PDF (posición de la consonante + sus 5 sílabas).
Salida: <letra>_0.jpg (posición) y <letra>_a.jpg ... <letra>_u.jpg; las vocales solas como voc_a.jpg ... voc_u.jpg.
Uso: python3 scripts/extract_mouths.py pdfs assets/bocas
"""
import pymupdf, sys, glob, os, io, hashlib, json
from PIL import Image
pdfdir, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
VOW='aeiou'
manifest={}
def save(doc, xref, name):
    d=doc.extract_image(xref)
    im=Image.open(io.BytesIO(d['image']))
    if im.mode!='RGB': im=im.convert('RGB')
    # normalise to 360px wide, keep aspect
    W=360
    if im.width!=W: im=im.resize((W, round(im.height*W/im.width)), Image.LANCZOS)
    p=os.path.join(outdir,name+'.jpg'); im.save(p,'JPEG',quality=82,optimize=True,progressive=True)
    return im.size
for f in sorted(glob.glob(pdfdir+'/*.pdf')):
    key=os.path.splitext(os.path.basename(f))[0]
    doc=pymupdf.open(f); pg=doc[1]
    infos=pg.get_image_info(xrefs=True)
    def bb(i): x0,y0,x1,y1=i['bbox']; return x0,y0,x1-x0,y1-y0
    if key=='vocales':
        row=sorted([i for i in infos if 150<bb(i)[1]<200 and 80<bb(i)[2]<130], key=lambda i:bb(i)[0])
        assert len(row)==5, (key,len(row))
        for v,i in zip(VOW,row): manifest[v]=save(doc,i['xref'],f'voc_{v}')
        continue
    top=[i for i in infos if bb(i)[1]<100 and bb(i)[2]>100 and bb(i)[3]>60]
    row=sorted([i for i in infos if 200<bb(i)[1]<260 and 100<bb(i)[2]<135 and bb(i)[3]>60], key=lambda i:bb(i)[0])
    assert len(top)==1 and len(row)==5, (key,len(top),len(row))
    manifest[key]=save(doc,top[0]['xref'],f'{key}_0')
    for v,i in zip(VOW,row): save(doc,i['xref'],f'{key}_{v}')
print(json.dumps(manifest))
