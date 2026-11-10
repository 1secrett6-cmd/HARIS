"""Builds the bilingual team guide PDFs (DAMI_Team_Guide_AR.pdf / _EN.pdf)."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, str(HERE))

from common import OUT, e, font_css, print_pdf  # noqa: E402
from guide_content import G, SOURCES, SPEAKERS  # noqa: E402
from extra import TEAM  # noqa: E402

CSS = """
@page { size:A4; margin:14mm 15mm 15mm; @bottom-center { content:counter(page); font-size:8pt; color:#A8A29E } }
@page :first { margin:0 }
* { box-sizing:border-box } body { font-family:'Cairo',sans-serif; color:#1C1917; font-size:10.2pt; line-height:1.65; margin:0 }
.cover { height:297mm; padding:24mm 20mm; color:#fff; display:flex; flex-direction:column; justify-content:space-between;
  background:radial-gradient(circle at 20% 15%,#DC262655,transparent 45%),linear-gradient(155deg,#2A0606,#7F1D1D 55%,#B91C1C) }
.cover h1 { font-size:58pt; font-weight:900; line-height:1.05; margin:4mm 0 } .cover .tag { display:inline-block; background:#fff; color:#7F1D1D; border-radius:99px; padding:1mm 6mm; font-weight:900 }
.cover .sub { font-size:15pt; font-weight:700; max-width:160mm } .cover table { margin-top:8mm; border-collapse:collapse } .cover td { padding:1mm 0; padding-inline-end:10mm; font-size:11pt }
h2 { color:#7F1D1D; font-size:15pt; margin:7mm 0 2.5mm; display:flex; gap:2.5mm; align-items:center; break-after:avoid }
h2 .n { background:#B91C1C; color:#fff; border-radius:1.5mm; padding:0 2.4mm; font-size:10.5pt }
table.t { width:100%; border-collapse:collapse; margin:1.5mm 0 2mm; font-size:9.4pt; break-inside:auto } table.t th { background:#7F1D1D; color:#fff; padding:1.6mm 2mm; text-align:start }
table.t td { border-bottom:1px solid #F1E4E4; padding:1.5mm 2mm; vertical-align:top } table.t tr:nth-child(even) td { background:#FFFBFB } table.t tr { break-inside:avoid }
.call { background:#FEF2F2; border-inline-start:4px solid #B91C1C; border-radius:2mm; padding:2.5mm 4mm; margin:2.5mm 0; font-weight:700; break-inside:avoid }
ul, ol { padding-inline-start:5.5mm; margin:1mm 0 } li { margin:1mm 0 }
.qa { break-inside:avoid; margin-bottom:2.5mm } .qa b { color:#B91C1C; display:block } .check li { list-style:none; margin-inline-start:-5mm } .check li::before { content:"☐  "; color:#B91C1C; font-weight:900 }
.src { font-size:8.5pt; color:#57534E }
"""


def block(kind, data, lang):
    if kind == "p":
        return f"<p>{e(data)}</p>"
    if kind == "call":
        return f'<div class="call">{e(data)}</div>'
    if kind in ("ul", "ol"):
        return f"<{kind}>" + "".join(f"<li>{e(x)}</li>" for x in data) + f"</{kind}>"
    if kind == "check":
        return '<ul class="check">' + "".join(f"<li>{e(x)}</li>" for x in data) + "</ul>"
    if kind == "table":
        head, rows = data
        return ('<table class="t"><tr>' + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr>"
                + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
    if kind == "qa":
        q, a = ("Q", "A") if lang == "en" else ("س", "ج")
        return "".join(f'<div class="qa"><b>{q}: {e(x)}</b>{a}: {e(y)}</div>' for x, y in data)
    if kind == "speakers":
        head = ["Who", "Topic", "Slides"] if lang == "en" else ["من", "الموضوع", "الشرائح"]
        note = ("A suggested split for a 5-minute pitch (~1 minute each). Adjust to the competition's time limit; everyone should still be able to answer finance questions."
                if lang == "en" else "تقسيم مقترح لعرض مدته 5 دقائق (دقيقة تقريبًا لكل عضو). عدّلوه حسب وقت المسابقة، وكل عضو يجب أن يستطيع الإجابة عن الأسئلة المالية.")
        return f"<p>{e(note)}</p>" + block("table", (head, [list(r) for r in SPEAKERS[lang]]), lang)
    raise ValueError(kind)


def html(lang):
    g = G[lang]
    names = "".join(f"<tr><td>{e(n)}</td><td>{e(r)}</td></tr>" for n, r in TEAM[lang])
    cover = f"""<div class="cover"><div style="letter-spacing:.4em;font-weight:900;opacity:.75">TEAM DAMI</div>
<div><span class="tag">{e(g['title'])}</span><h1>🩸 {'دَمي' if lang == 'ar' else 'DAMI'}</h1><div class="sub">{e(g['sub'])}</div><table>{names}</table></div>
<div style="font-weight:700">{'Jordan Students Pitch Competition — GEW Jordan' if lang == 'en' else 'Jordan Students Pitch Competition — GEW Jordan'}</div></div>"""
    body = cover + "".join(f'<h2><span class="n">{i}</span>{e(t)}</h2>' + "".join(block(b[0], b[1:] if len(b) > 2 else b[1], lang) for b in blocks)
                           for i, (t, blocks) in enumerate(g["sections"], 1))
    body += f'<h2><span class="n">★</span>{"Sources" if lang == "en" else "المصادر"}</h2><ol class="src">' + "".join(f"<li>{e(s)}</li>" for s in SOURCES) + "</ol>"
    d = "rtl" if lang == "ar" else "ltr"
    return f'<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>{body}</body></html>'


def build():
    dest = OUT / "SUBMISSION"
    return [print_pdf(html(lang), dest / f"DAMI_Team_Guide_{lang.upper()}.pdf") for lang in ("ar", "en")]


if __name__ == "__main__":
    for f in build():
        print(f)
