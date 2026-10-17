"""Extrae las palabras de cada PDF (palabra, sílabas y pictograma) y escribe words.json.
La G y las vocales traen el texto como imagen, por eso sus palabras están escritas a mano en MANUAL.
Uso: python3 scripts/extract_words.py pdfs assets/pictogramas
"""
import pymupdf, sys, os, json, re, unicodedata
pdfdir, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
UP = re.compile(r'^[A-ZÁÉÍÓÚÜÑ]+$')
MANUAL = {  # labels drawn as images in these PDFs: (page, [(word, syllables)...])
  'g': [(12, [('GATO',['GA','TO']), ('GOTA',['GO','TA'])]), (13, [('GAFAS',['GA','FAS']), ('GORRO',['GO','RRO'])])],
  'vocales': [(14, [('AVIÓN',['A','VIÓN']), ('UVAS',['U','VAS'])]), (15, [('ELEFANTE',['E','LE','FAN','TE'])]),
              (16, [('OVEJA',['O','VE','JA'])]), (17, [('IGLÚ',['I','GLÚ'])])],
}
CLIP={('z','ZAPATO'): pymupdf.Rect(440,62,620,184)}  # vector drawing, not an embedded image
FIX={('t','TÍA'): ['TÍ','A']}
def pic_candidates(pg, below_y):
    out=[]
    for i in pg.get_image_info(xrefs=True):
        x0,y0,x1,y1=i['bbox']; w,h=x1-x0,y1-y0
        if 50<w<300 and 50<h<300 and 0.45<w/h<2.2 and y1<=below_y+8 and y0<200:
            out.append(pymupdf.Rect(x0,y0,x1,y1))
    return out
def save_pic(pg, rect, name):
    s=330/max(rect.width,rect.height)
    pix=pg.get_pixmap(clip=rect, matrix=pymupdf.Matrix(s,s), alpha=False)
    p=os.path.join(outdir,name+'.jpg'); pix.save(p, jpg_quality=82); return p
words={}
for f in sorted(os.listdir(pdfdir)):
    key=f[:-4]; doc=pymupdf.open(os.path.join(pdfdir,f)); lst=[]
    pages = MANUAL.get(key)
    if pages is None:
        pages=[]
        for n,pg in enumerate(doc):
            toks=[(w[4],w[0],w[1],w[2]) for w in pg.get_text('words') if UP.match(w[4])]
            wt=[t for t in toks if 170<=t[2]<=262 and len(t[0])>=2]
            st=[t for t in toks if 270<=t[2]<=400]
            if not wt or not st: continue
            wt.sort(key=lambda t:t[1])
            if len(wt)==1: groups=[(wt[0],st)]
            else:
                mid=((wt[0][1]+wt[0][3])/2+(wt[1][1]+wt[1][3])/2)/2
                groups=[(wt[0],[t for t in st if (t[1]+t[3])/2<mid]),(wt[1],[t for t in st if (t[1]+t[3])/2>=mid])]
            entries=[]
            for wtok,sts in groups:
                syl=[t[0] for t in sorted(sts,key=lambda t:t[1])]
                entries.append((wtok[0],syl))
            pages.append((n,entries))
    for n,entries in pages:
        pg=doc[n]; W=pg.rect.width
        cands=pic_candidates(pg, 230)
        for k,(word,syl) in enumerate(entries):
            syl=FIX.get((key,word),syl)
            if ''.join(syl)!=word: print('SYL MISMATCH',key,word,syl); continue
            if len(entries)==1: pool=cands
            else: pool=[r for r in cands if ((r.x0+r.x1)/2 < W/2) == (k==0)]
            if (key,word) in CLIP: r=CLIP[(key,word)]
            elif not pool: print('NO PIC',key,word); continue
            else: r=max(pool,key=lambda r:r.width*r.height)
            name=f'w_{key}_{len(lst)}'; save_pic(pg,r,name)
            lst.append({'w':word,'syl':syl,'pic':name,'page':n})
    if lst: words[key]=lst
json.dump(words, open(os.path.join(outdir,'words.json'),'w'), ensure_ascii=False, indent=0)
for k,v in words.items(): print(k, [x['w']+'('+'-'.join(x['syl'])+')' for x in v])
