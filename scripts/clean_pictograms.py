"""Borra líneas sueltas del recuadro del PDF que quedaron al pie de algunos pictogramas.
Uso: python3 scripts/clean_pictograms.py assets/pictogramas
"""
import sys, os, numpy as np
from PIL import Image
d=sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith('.jpg'): continue
    p=os.path.join(d,f); im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int)
    h=a.shape[0]; nonwhite=(a.min(axis=2)<200)
    frac=nonwhite.mean(axis=1)
    rows=[y for y in range(int(h*0.85),h) if frac[y]>0.45]
    # a thin full-width rule near the bottom = leftover box border from the PDF, not the drawing
    if rows and len(rows)<=6 and frac[max(0,min(rows)-6):min(rows)].mean()<0.25:
        a=a.copy(); a[max(0,min(rows)-1):min(h,max(rows)+2),:,:]=255
        Image.fromarray(a.astype('uint8')).save(p,'JPEG',quality=82); print('cleaned',f,rows)
