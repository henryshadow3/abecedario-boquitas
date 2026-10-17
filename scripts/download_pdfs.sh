#!/usr/bin/env bash
# Descarga los 21 PDFs "sin gestos" de «Introducción a los fonemas» (Comunicar_Nos / Siembra Estrellas)
# desde los enlaces de Google Drive publicados en:
# https://siembraestrellas.blogspot.com/2020/01/material-reeditado-presentacion-de-los.html
#
# Uso: scripts/download_pdfs.sh [carpeta_destino]   (por defecto: pdfs/)
set -euo pipefail
OUT="${1:-pdfs}"
mkdir -p "$OUT"

declare -A IDS=(
  [vocales]=1IlOQX0IbTUPscYuNC-ykECUMQy3lLFc8
  [b]=1K_vWZSU96XT4GIuWz-hR-v8hmL40X5Fk
  [v]=1Jv-E46AxLV4EKryEYuDC8YKVQ693TKNJ
  [z]=1Yb-JCidkezH6In7TvzjOghKqnOD5bkCS
  [c]=1Hken3oFFewfSsYGxzuxeR6vYZ3ri-OAA
  [ch]=1BzJyy_1SVUnBJWZpwa8h__CVfePEl-PA
  [d]=1TbF_ea7KOgV-7uz03OLvNTgMdJVHu9Th
  [f]=1nEAoIoPUBIeqKVGUfnvdGW7Rc97od8Zs
  [g]=15gdWE5VWpRZdK3hwgWWbfMpEwUcUtv1h
  [j]=145QYBjqpbvESOBJieSnC5iLOjPavGHWh
  [k]=1wfF_oSHi1VSxBxBkFV2xp23Og56Q2iCi
  [l]=1y5j2AqozycBde2q6lVNbFtcUiek6fv7_
  [ll]=1mKzl-RgCUJQJK9LDzFN-rJ4x3cju_8A8
  [m]=1FUhEUc9tlDX4Vjx2ofdFoaV7QQqrtcyr
  [n]=1nW4SPio0A7K8veLXwGfktZ_zxRWregOA
  [nn]=1NMnAG4WlXVvca0Lz93q8T7H6rP-6NGYA
  [p]=1aiHNEjjEYwqbrLtNj3xk_ouP7L39Q9bk
  [r]=1pJHrryYqhl4X6EqYPg8ER4jOJAfaPwww
  [rr]=1GQjDsLx-FnFXd2Wk1wMzriCoGh_T_AeW
  [s]=1ydxRzjVtzOZel6yE57QOTDt1vwqeyYgg
  [t]=1fKgo-vwbf--Hp5h_6duOjiEjihstCwn2
)

for k in "${!IDS[@]}"; do
  curl -sS -L -o "$OUT/$k.pdf" "https://drive.google.com/uc?export=download&id=${IDS[$k]}" &
done
wait
ls -1 "$OUT"/*.pdf | wc -l | xargs echo "PDFs descargados:"
