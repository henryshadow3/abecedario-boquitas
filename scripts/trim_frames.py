"""Recorta el marco negro que traen algunas fotos de bocas y las deja a 360 px de ancho.
Uso: python3 scripts/trim_frames.py assets/bocas
"""
import sys, os, numpy as np
from PIL import Image
d=sys.argv[1]; n=0
for f in sorted(os.listdir(d)):
    p=os.path.join(d,f); im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int).mean(axis=2)
    t,b,l,r=0,a.shape[0],0,a.shape[1]
    for _ in range(14):
        ch=False
        if a[t,l:r].mean()<110: t+=1; ch=True
        if a[b-1,l:r].mean()<110: b-=1; ch=True
        if a[t:b,l].mean()<110: l+=1; ch=True
        if a[t:b,r-1].mean()<110: r-=1; ch=True
        if not ch: break
    if (t,b,l,r)!=(0,a.shape[0],0,a.shape[1]):
        m=2  # shave a little extra past the frame (anti-aliasing)
        im=im.crop((l+m,t+m,r-m,b-m)); im=im.resize((360,round(im.height*360/im.width)),Image.LANCZOS)
        im.save(p,'JPEG',quality=82,optimize=True,progressive=True); n+=1
print('trimmed',n)
