"""Builds the Arabic and English DAMI motion videos. Usage: build_video.py [ar|en|stills]"""

import base64
import io
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NX = HERE.parent.parent
sys.path.insert(0, str(NX))

from PIL import Image  # noqa: E402

from common import OUT, font_css  # noqa: E402

SHOT_DIRS = {"ar": OUT / "DAMI" / "screens", "en": OUT / "DAMI_EN" / "screens"}


def shots(lang):
    res = []
    for name in ("sos", "dash", "mci"):
        im = Image.open(SHOT_DIRS[lang] / f"{name}.png").convert("RGB")
        im.thumbnail((1600, 1600))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85)
        res.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
    return res


def page(lang, work):
    html = (HERE / "motion.html").read_text(encoding="utf-8")
    html = html.replace("/*FONT*/", font_css()).replace("__LANG__", json.dumps(lang)).replace("__SHOTS__", json.dumps(shots(lang)))
    path = work / f"motion_{lang}.html"
    path.write_text(html, encoding="utf-8")
    return path


def build(lang, work):
    wav = work / "music.wav"
    if not wav.exists():
        subprocess.run([sys.executable, str(HERE / "music.py"), str(wav)], check=True)
    folder = OUT / ("DAMI" if lang == "ar" else "DAMI_EN")
    out = folder / ("08_DAMI_Video_AR.mp4" if lang == "ar" else "08_DAMI_Video_EN.mp4")
    subprocess.run(["node", str(HERE / "capture.js"), str(page(lang, work)), str(wav), str(out)], check=True, cwd="/tmp")
    return out


if __name__ == "__main__":
    work = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "_work"
    work.mkdir(parents=True, exist_ok=True)
    print(build(sys.argv[1], work))
