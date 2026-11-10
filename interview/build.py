"""Builds the bilingual (English ↔ Arabic) accreditation interview sheet as a PDF."""

import html
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "NEXORA-water"))

from common import CHROME, font_css  # noqa: E402
from content import CLOSING, INTRO, PHRASES, SECTIONS, TIPS  # noqa: E402

CSS = """
@page { size:A4; margin:13mm 12mm 14mm; @bottom-center { content:counter(page); font-size:8pt; color:#94A3B8 } }
* { box-sizing:border-box } body { font-family:'Cairo',sans-serif; color:#0F172A; margin:0; font-size:10.3pt; line-height:1.5 }
.cover { background:linear-gradient(135deg,#0C1E3D,#1D4ED8); color:#fff; border-radius:4mm; padding:9mm 10mm; margin-bottom:5mm }
.cover h1 { margin:0; font-size:22pt } .cover .ar { direction:rtl; text-align:right; font-size:16pt; font-weight:800; margin-top:1mm }
h2 { margin:6mm 0 2mm; padding:2mm 4mm; border-radius:2.5mm; background:#1D4ED8; color:#fff; font-size:12.5pt; display:flex; justify-content:space-between; break-after:avoid }
h2 span:last-child { direction:rtl }
.q { margin:3mm 0 1mm; padding:1.5mm 3mm; background:#EFF6FF; border-left:4px solid #1D4ED8; border-radius:1.5mm; display:flex; justify-content:space-between; gap:5mm; font-weight:800; break-after:avoid }
.q span:last-child { direction:rtl; text-align:right; color:#1E3A8A }
table { width:100%; border-collapse:collapse; break-inside:auto } tr { break-inside:avoid }
td { width:50%; padding:1.3mm 2.5mm; vertical-align:top; border-bottom:1px dashed #E2E8F0 }
td.en { direction:ltr; font-weight:600 } td.ar { direction:rtl; text-align:right; color:#334155; border-right:none }
.box { border:1.5px solid #BFDBFE; border-radius:3mm; padding:1mm 2mm; margin-bottom:3mm; break-inside:avoid }
.box .t { font-weight:900; color:#1D4ED8; padding:1.5mm 2.5mm; display:flex; justify-content:space-between }
.note { font-size:8.5pt; color:#64748B; margin-top:2mm }
"""


def e(s):
    return html.escape(s, quote=False).replace("[", '<mark style="background:#FEF3C7">[').replace("]", "]</mark>")


def rows(pairs):
    return "<table>" + "".join(f'<tr><td class="en">{e(a)}</td><td class="ar">{e(b)}</td></tr>' for a, b in pairs) + "</table>"


def box(t_en, t_ar, pairs):
    return f'<div class="box"><div class="t"><span>{t_en}</span><span dir="rtl">{t_ar}</span></div>{rows(pairs)}</div>'


def build(out):
    body = ('<div class="cover"><h1>Accreditation Interview — Software Engineering</h1>'
            '<div class="ar">مقابلة الاعتماد — هندسة البرمجيات: كل جملة إنجليزية وترجمتها بجانبها</div></div>')
    body += box("Tips", "نصائح", TIPS) + box("Introduce yourself", "عرّف بنفسك", INTRO) + box("Useful phrases", "عبارات مفيدة", PHRASES)
    for en, ar, qs in SECTIONS:
        body += f"<h2><span>{en}</span><span>{ar}</span></h2>"
        for q_en, q_ar, ans in qs:
            body += f'<div class="q"><span>{html.escape(q_en)}</span><span>{html.escape(q_ar)}</span></div>' + rows(ans)
    body += box("Closing", "الختام", CLOSING)
    body += '<p class="note">The yellow [brackets] are placeholders: replace them with your real details (advisor name, courses, tools, year). Never guess facts about the university. · الأقواس الصفراء تُستبدل بمعلوماتك الحقيقية.</p>'
    page = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>{body}</body></html>'
    src = out.with_suffix(".html")
    src.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True)
    src.unlink()
    return out


if __name__ == "__main__":
    print(build(HERE / "Accreditation_Interview_SE_EN_AR.pdf"))
