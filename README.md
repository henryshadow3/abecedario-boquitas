# Abecedario de Boquitas

App web para terapia de lenguaje con niños. Muestra cómo se pone la boca en cada letra, sílaba y palabra del español, con juegos sencillos.

Está pensada para niños autistas: cada pantalla muestra una sola cosa, los juegos no tienen tiempo ni sonidos, y los botones de atrás y adelante siempre están en el mismo lugar.

## Qué tiene

- **Abecedario**: las 30 letras del español, incluidas CH, LL, Ñ y RR.
- **Sílabas**: una por pantalla. Se ve la boca de la consonante y luego la de la vocal (P → A = PA). Incluye un botón de movimiento y audios locales de voz femenina mexicana; si falta un audio, usa la voz del dispositivo como respaldo.
- **Palabras**: palabras cortas (dos sílabas como máximo), cada una con su pictograma; las vocales tienen tres. Salen de las láminas originales y de pictogramas de ARASAAC añadidos después (clave `extra` en `words.json`). Primero sale el dibujo y luego la boquita de cada sílaba de esa letra. Las palabras largas del material siguen en `words.json`, pero no se muestran: la lista de cada letra está en `WL` de `src/app.html`.
- **Juegos**: «¿Qué dice la boca?» y «¿Cuál es la boca?». Son 5 preguntas con 2 o 3 opciones y se pueden repetir las veces que haga falta.
- **Ajustes**: pronunciación de México y Latinoamérica o de España (cambia CE, CI y Z) y número de opciones en los juegos.

## Cómo usarla

`index.html` es la app completa en un solo archivo, con todas las imágenes incluidas. Se abre directo en el navegador, sin servidor y sin internet (salvo las fuentes de Google, que son opcionales).

## Estructura

```
index.html                 App ya construida (se genera con scripts/build.py)
src/app.html               Código fuente de la app (HTML + CSS + JS)
assets/bocas/              125 fotos de bocas extraídas de las láminas
assets/pictogramas/        126 pictogramas + words.json (palabra, sílabas, imagen)
scripts/                   Descarga de PDFs, extracción de imágenes y build
```

En `assets/bocas`, `p_0.jpg` es la posición de la P y `p_a.jpg` a `p_u.jpg` son PA a PU. Las vocales solas están en `voc_a.jpg` a `voc_u.jpg`.

## Agregar palabras con pictogramas de ARASAAC

`scripts/add_arasaac_words.sh assets/pictogramas` descarga los pictogramas listados en el script (id de ARASAAC), los recorta y los guarda como `w_extra_N.jpg`. Después registra cada palabra en `words.json` (clave `extra`, con sus sílabas) y agrégala a la lista de su letra en `WL` de `src/app.html`. Requiere `curl` y `ffmpeg`.

## Reconstruir la app

Después de editar `src/app.html`, regenera `index.html`:

```bash
python3 scripts/build.py src/app.html assets/bocas assets/pictogramas index.html assets/audio
```

## Generar los audios de ElevenLabs

La clave se lee de `ELEVENLABS_API_KEY` y nunca se guarda en el repositorio. La voz predeterminada es Jessica (femenina, cálida, brillante y juguetona), disponible en el plan gratuito de ElevenLabs.

```bash
ELEVENLABS_API_KEY=... python3 scripts/generate_audio.py assets/audio
```

## Volver a extraer las imágenes desde los PDFs

Solo hace falta si cambia el material original. Requiere `pymupdf`, `pillow` y `numpy`.

```bash
pip install pymupdf pillow numpy
scripts/download_pdfs.sh pdfs
python3 scripts/extract_mouths.py pdfs assets/bocas
python3 scripts/trim_frames.py assets/bocas
python3 scripts/extract_words.py pdfs assets/pictogramas
python3 scripts/clean_pictograms.py assets/pictogramas
python3 scripts/build.py src/app.html assets/bocas assets/pictogramas index.html assets/audio
```

## Decisiones sobre el material

- **Letras sin lámina propia** (marcadas con asterisco):
  - La H muestra las vocales, porque no suena.
  - La Y usa las boquitas de la LL.
  - La W usa U + vocal.
  - La X usa K + S + vocal.
- **G**: GE y GI usan la boca de la J, como en el material (JE/GE, JI/GI). Se agregaron GUE y GUI.
- **C y Z**: con pronunciación latinoamericana, CE, CI y Z usan la boca de la S. Con la de España, usan la lámina de la Z.
- **Palabras que se quitaron**: GUERRA, porque su pictograma es un tanque con una explosión, y CHINO, porque su pictograma es un estereotipo.

## Créditos y licencia

Las fotografías de las posiciones de la boca y las palabras vienen del material **«Introducción a los fonemas»** (versión sin gestos) de **Comunicar_Nos**, coordinado por **Belinda Haro Castilla** y publicado en el blog [Siembra Estrellas](https://siembraestrellas.blogspot.com/2020/01/material-reeditado-presentacion-de-los.html).

Los pictogramas son de **Sergio Palao**, de [ARASAAC](https://arasaac.org) (Gobierno de Aragón). Otras imágenes del material provienen de soyvisual.org, freepik y pixabay.

Todo ese material está bajo licencia **Creative Commons BY-NC-SA**: solo se puede usar sin fines comerciales, citando la fuente y compartiendo las obras derivadas con la misma licencia. Esta app y su contenido se distribuyen bajo esas mismas condiciones. Más detalles en [LICENSE.md](LICENSE.md).
