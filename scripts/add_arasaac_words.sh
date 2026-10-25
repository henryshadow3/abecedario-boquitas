#!/bin/bash
# Descarga pictogramas de ARASAAC (https://arasaac.org, CC BY-NC-SA, autor Sergio Palao, Gobierno de Aragón),
# los recorta, los pone sobre fondo blanco y los guarda como assets/pictogramas/w_extra_N.jpg.
# Requiere curl y ffmpeg. Después hay que registrar las palabras en words.json (clave "extra") y en WL de src/app.html.
# Uso: scripts/add_arasaac_words.sh assets/pictogramas
set -euo pipefail
out=${1:?directorio de salida}
# N:id_arasaac:palabra
WORDS="0:2248:AGUA 1:5368:ALA 2:6923:AVE 3:36388:ELFO 4:8348:ESQUÍ 5:36989:ECO 6:8138:IMÁN 7:2966:ISLA 8:2488:OSO 9:4706:OLA 10:2627:UNO 11:2783:UÑA 12:11461:JUGO 13:2435:JARRA 14:7138:KILO 15:6540:KÉTCHUP 16:2859:PARQUE 17:34227:WAFLE"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
for e in $WORDS; do
  n=${e%%:*}; r=${e#*:}; id=${r%%:*}; w=${r#*:}
  curl -fsS -m 30 -o "$tmp/$id.png" "https://static.arasaac.org/pictograms/$id/${id}_500.png"
  # caja del dibujo según el canal alfa (cropdetect sobre la máscara), con un margen pequeño
  crop=$(ffmpeg -hide_banner -i "$tmp/$id.png" -vf "format=rgba,alphaextract,cropdetect=limit=0.05:round=2:reset=0:skip=0" -f null - 2>&1 | grep -o 'crop=[0-9:]*' | tail -1)
  ffmpeg -loglevel error -y -i "$tmp/$id.png" -vf "format=rgba,${crop},pad=iw+24:ih+24:12:12:color=0x00000000,format=rgba" "$tmp/c$id.png"
  ffmpeg -loglevel error -y -i "$tmp/c$id.png" -f lavfi -i color=white:s=16x16 \
    -filter_complex "[1]scale=iw:ih[b];[b][0]scale2ref[bg][fg];[bg][fg]overlay=format=auto:shortest=1,scale=340:340:force_original_aspect_ratio=decrease,pad=340:340:(ow-iw)/2:(oh-ih)/2:white,format=yuvj420p" \
    -frames:v 1 -q:v 3 "$out/w_extra_$n.jpg"
  echo "$w -> w_extra_$n.jpg (ARASAAC $id)"
done
