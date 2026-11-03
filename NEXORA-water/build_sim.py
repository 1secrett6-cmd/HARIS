"""06 — self-contained interactive simulators: the 31-project hub and the DAMI app."""

import json

from common import AXES, BMC_BLOCKS, DISCLAIMER, KING_QUOTE, OUT, PROJECTS, ROOT, font_css, score
from demos import DEMOS

KEYS = ("id", "ar", "en", "emoji", "axis", "tag", "problem", "solution", "features", "diff", "wow", "bmc", "fin")


def data():
    projects = [dict({k: p[k] for k in KEYS}, score=score(p), demo=DEMOS[p["id"]]) for p in PROJECTS]
    return dict(projects=projects, axes=AXES, bmc=BMC_BLOCKS, disclaimer=DISCLAIMER, quote=KING_QUOTE)


def build():
    folder = OUT / "simulators"
    folder.mkdir(exist_ok=True)
    css = font_css() + (ROOT / "sim" / "style.css").read_text(encoding="utf-8")
    js = (ROOT / "sim" / "engine.js").read_text(encoding="utf-8")
    payload = json.dumps(data(), ensure_ascii=False).replace("</", "<\\/")
    (folder / "index.html").write_text(
        f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>NEXORA Simulators</title><style>{css}</style></head><body><div id=\"app\"></div>"
        f"<script>window.DATA={payload};</script><script>{js}</script></body></html>", encoding="utf-8")
    dami = (ROOT / "sim" / "dami.html").read_text(encoding="utf-8").replace("/*FONT*/", font_css())
    (folder / "dami.html").write_text(dami, encoding="utf-8")
    return folder


if __name__ == "__main__":
    print(build())
