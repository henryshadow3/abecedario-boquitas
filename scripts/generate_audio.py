#!/usr/bin/env python3
"""Genera las pronunciaciones locales con ElevenLabs.

Requiere ELEVENLABS_API_KEY en el entorno. La clave nunca se escribe en disco.
"""
import argparse
import json
import os
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_VOICE = "cgSgspJ2msm6clMCkdW9"  # Jessica, voz femenina cálida y brillante

LETTER_NAMES = {
    "a": "a", "b": "be", "c": "ce", "ch": "che", "d": "de", "e": "e",
    "f": "efe", "g": "ge", "h": "hache", "i": "i", "j": "jota", "k": "ka",
    "l": "ele", "ll": "elle", "m": "eme", "n": "ene", "nn": "eñe", "o": "o",
    "p": "pe", "q": "cu", "r": "erre", "rr": "erre fuerte", "s": "ese", "t": "te",
    "u": "u", "v": "uve", "w": "doble u", "x": "equis", "y": "ye", "z": "zeta",
}

STANDARD = ["b", "ch", "d", "f", "j", "k", "l", "ll", "m", "n", "ñ", "p", "r", "rr", "s", "t", "v", "y", "z"]
VOWELS = ["a", "e", "i", "o", "u"]


def slug(text: str) -> str:
    text = text.lower().replace("ñ", "nn")
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return "_".join("".join(c if c.isalnum() else " " for c in text).split())


def clips():
    result = {f"letter_{key}": value for key, value in LETTER_NAMES.items()}
    syllables = set(VOWELS)
    for consonant in STANDARD:
        syllables.update(consonant + vowel for vowel in VOWELS)
    syllables.update(["ca", "ce", "ci", "co", "cu", "ga", "ge", "gi", "go", "gu", "gue", "gui", "que", "qui"])
    syllables.update(["ua", "ue", "ui", "uo"])
    syllables.update(["ksa", "kse", "ksi", "kso", "ksu"])
    result.update({f"syl_{slug(text)}": text for text in sorted(syllables)})
    return result


def synthesize(api_key: str, voice_id: str, text: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    body = json.dumps({
        "text": text,
        "model_id": "eleven_flash_v2_5",
        "language_code": "es",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True},
    }).encode()
    request = urllib.request.Request(url, data=body, method="POST", headers={
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="assets/audio")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE)
    parser.add_argument("--only", help="Genera solo una clave, para probar la voz")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("Falta ELEVENLABS_API_KEY en el entorno")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    manifest = clips()
    if args.only:
        manifest = {args.only: manifest[args.only]}
    generated = 0
    for index, (key, text) in enumerate(manifest.items(), 1):
        target = output / f"{key}.mp3"
        if target.exists() and not args.force:
            continue
        try:
            target.write_bytes(synthesize(api_key, args.voice_id, text))
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise SystemExit(f"ElevenLabs rechazo {key} ({error.code}): {detail}") from error
        generated += 1
        print(f"[{index}/{len(manifest)}] {key}: {text}")
        time.sleep(0.08)
    (output / "manifest.json").write_text(json.dumps(clips(), ensure_ascii=False, indent=2) + "\n")
    print(f"Listo: {generated} audios nuevos en {output}")


if __name__ == "__main__":
    main()
