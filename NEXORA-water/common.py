"""Shared data loading, the 3-year financial model, formatting and PDF printing."""

import base64
import html
import re
import subprocess
from pathlib import Path

from data import p01_08, p09_16, p17_24, p25_31

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PROJECTS = p01_08.PROJECTS + p09_16.PROJECTS + p17_24.PROJECTS + p25_31.PROJECTS
assert [p["id"] for p in PROJECTS] == list(range(1, 32))

AXES = {
    "home": ("البيت والمواطن", "#0E7490"),
    "network": ("الشبكة وشركات المياه", "#1D4ED8"),
    "agri": ("الزراعة", "#15803D"),
    "industry": ("المؤسسات والصناعة", "#7C3AED"),
    "future": ("المستقبل والمجتمع", "#C2410C"),
    "new": ("الخمسة الجديدة", "#B8860B"),
    "health": ("الصحة", "#B91C1C"),
}

# impact, wow, MVP ease, revenue clarity (1–5): team estimates to guide the choice, not measurements
SCORES = {
    1: (4, 5, 5, 4), 2: (4, 4, 5, 3), 3: (4, 4, 4, 3), 4: (3, 3, 5, 3), 5: (4, 4, 4, 4),
    6: (5, 4, 4, 4), 7: (5, 3, 4, 3), 8: (4, 5, 3, 4), 9: (4, 3, 3, 3), 10: (5, 4, 3, 5),
    11: (5, 4, 4, 3), 12: (4, 3, 4, 3), 13: (3, 4, 3, 4), 14: (3, 4, 5, 3), 15: (4, 4, 4, 2),
    16: (4, 5, 4, 5), 17: (3, 3, 4, 4), 18: (5, 3, 4, 3), 19: (4, 3, 4, 4), 20: (4, 4, 2, 2),
    21: (5, 5, 4, 2), 22: (4, 4, 2, 3), 23: (3, 3, 5, 4), 24: (3, 4, 4, 3), 25: (3, 4, 5, 3),
    26: (4, 5, 3, 2), 27: (5, 5, 3, 2), 28: (5, 4, 3, 4), 29: (4, 5, 4, 3), 30: (5, 4, 2, 2),
    31: (5, 3, 4, 3),
}
SCORE_LABELS = ("الأثر", "الإبهار", "سهولة النموذج", "وضوح الدخل")

BMC_BLOCKS = [
    ("kp", "الشركاء الرئيسيون", "Key Partnerships"),
    ("ka", "الأنشطة الرئيسية", "Key Activities"),
    ("kr", "الموارد الرئيسية", "Key Resources"),
    ("vp", "القيمة المقدّمة", "Value Propositions"),
    ("cr", "العلاقة مع العملاء", "Customer Relationships"),
    ("ch", "القنوات", "Channels"),
    ("cs", "شرائح العملاء", "Customer Segments"),
    ("cost", "هيكل التكاليف", "Cost Structure"),
    ("rev", "مصادر الإيرادات", "Revenue Streams"),
]

OPEX_SPLIT = [("رواتب الفريق", 0.60), ("التقنية والخوادم", 0.10), ("التسويق والمبيعات", 0.15), ("التشغيل والإدارة", 0.15)]

SCENARIOS = [("متشائم", 0.6, 1.10), ("أساسي", 1.0, 1.0), ("متفائل", 1.4, 0.95)]

DISCLAIMER = ("جميع الأرقام المالية افتراضات تخطيطية أولية وضعها الفريق لتقدير الجدوى، "
              "وليست نتائج أبحاث سوق أو عروض أسعار فعلية. يجب التحقق منها بالمقابلات والتجارب قبل أي قرار استثماري.")

KING_QUOTE = "أمننا المائي أولوية وطنية… ولن نسمح بأن يكون ظمأ الأردنيين رهينة لأي ظرف"


def by_id(pid):
    return PROJECTS[pid - 1]


def score(p):
    return sum(SCORES[p["id"]])


def e(text):
    return html.escape(str(text), quote=False)


def money(v, unit=True):
    v = round(v)
    s = f"{abs(v):,}"
    if v < 0:
        s = "−" + s
    return s + (" د.أ" if unit else "")


def price(v):
    return (f"{v:,.2f}" if v < 1 else f"{v:,.0f}") + " د.أ"


def model(p, volume=1.0, opex_mult=1.0, price_mult=1.0, capex_mult=1.0):
    """Three-year projection. Returns dict of yearly lists and summary KPIs."""
    fin = p["fin"]
    capex = sum(v for _, v in fin["capex"]) * capex_mult
    rev, cogs = [0.0] * 3, [0.0] * 3
    for _, _, unit_price, units, cogs_pct in fin["streams"]:
        for y in range(3):
            r = unit_price * price_mult * units[y] * volume
            rev[y] += r
            cogs[y] += r * cogs_pct
    gross = [rev[y] - cogs[y] for y in range(3)]
    opex = [o * opex_mult for o in fin["opex"]]
    ebitda = [gross[y] - opex[y] for y in range(3)]

    cash, low, breakeven = -capex, -capex, None
    curve = [cash]
    for m in range(36):
        cash += ebitda[m // 12] / 12
        curve.append(cash)
        low = min(low, cash)
        if breakeven is None and cash >= 0:
            breakeven = m + 1
    cum = [-capex + sum(ebitda[: y + 1]) for y in range(3)]
    return dict(
        capex=capex, rev=rev, cogs=cogs, gross=gross, opex=opex, ebitda=ebitda, cum=cum,
        curve=curve, funding=-low, breakeven=breakeven,
        margin=(gross[2] / rev[2]) if rev[2] else 0.0,
        roi=(cum[2] / -low) if low < 0 else 0.0,
    )


def breakeven_text(m):
    return f"الشهر {m}" if m else "بعد السنة الثالثة"


def verdict(m):
    if m and m <= 24:
        return ("جدوى مبدئية مرتفعة", "#15803D", "يسترد الاستثمار ضمن سنتين حسب الافتراضات الأساسية.")
    if m and m <= 36:
        return ("جدوى مبدئية متوسطة", "#B45309", "يصل لنقطة التعادل خلال السنة الثالثة، ويحتاج تمويلًا يغطي فترة النمو.")
    return ("جدوى طويلة المدى", "#B91C1C", "لا يتعادل خلال 3 سنوات بالافتراضات الحالية؛ يحتاج منحًا أو شريكًا مؤسسيًا أو مراجعة نموذج الدخل.")


def font_css():
    css = (ROOT / "cairo-local.css").read_text(encoding="utf-8")

    def embed(match):
        data = (ROOT / match.group(1)).read_bytes()
        return "url(data:font/woff2;base64," + base64.b64encode(data).decode() + ")"

    return re.sub(r"url\((fonts/[^)]+)\)", embed, css)


BASE_CSS = """
:root { --g:#0B6E4F; --w:#0369A1; --w2:#0EA5E9; --gold:#B8860B; --ink:#0F172A; --mute:#475569; --line:#E2E8F0; --bg:#F8FAFC; }
* { box-sizing: border-box; }
body { font-family:'Cairo','DejaVu Sans',sans-serif; color:var(--ink); direction:rtl; margin:0; background:#fff; line-height:1.65; }
.en { direction:ltr; unicode-bidi:isolate; font-weight:600; color:var(--mute); letter-spacing:.05em; }
h1,h2,h3,h4 { margin:0; }
ul,ol { margin:1mm 0; padding-right:5mm; padding-left:0; }
li { margin:.5mm 0; }
table { border-collapse:collapse; width:100%; }
th { background:var(--w); color:#fff; font-weight:700; padding:1.4mm 2mm; }
td { border-bottom:1px solid var(--line); padding:1.2mm 2mm; }
.num { direction:ltr; unicode-bidi:isolate; }
.chip { display:inline-block; border-radius:99px; padding:.3mm 3mm; font-size:8.5pt; font-weight:700; color:#fff; }
.disc { font-size:8.5pt; color:var(--mute); background:#FFF7ED; border:1px solid #FED7AA; border-radius:2mm; padding:2mm 3mm; }
"""


def page(title, body, css, size="A4"):
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{e(title)}</title>'
            f"<style>{font_css()}{BASE_CSS}@page {{ size:{size}; margin:0; }}{css}</style></head><body>{body}</body></html>")


def print_pdf(html_text, pdf_path):
    pdf_path = Path(pdf_path)
    html_path = pdf_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", html_path.as_uri()],
        check=True, capture_output=True, timeout=300,
    )
    html_path.unlink()
    return pdf_path


def cash_chart(m, width=520, height=170):
    """SVG: yearly revenue/opex bars plus the 36-month cumulative cash line."""
    pad_l, pad_r, pad_t, pad_b = 54, 12, 14, 26
    w, h = width - pad_l - pad_r, height - pad_t - pad_b
    vals = m["curve"] + m["rev"] + [m["opex"][y] + m["cogs"][y] for y in range(3)]
    hi, lo = max(vals + [0]), min(vals + [0])
    span = (hi - lo) or 1

    def y(v):
        return pad_t + (hi - v) / span * h

    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" direction="ltr" font-family="Cairo, DejaVu Sans" font-size="9">']
    for t in range(5):
        v = lo + span * t / 4
        parts.append(f'<line x1="{pad_l}" x2="{width - pad_r}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#E2E8F0"/>'
                     f'<text x="{pad_l - 4}" y="{y(v) + 3:.1f}" text-anchor="end" fill="#64748B">{money(v / 1000, False)}k</text>')
    parts.append(f'<line x1="{pad_l}" x2="{width - pad_r}" y1="{y(0):.1f}" y2="{y(0):.1f}" stroke="#94A3B8"/>')
    yw = w / 3
    for i in range(3):
        x0 = pad_l + i * yw
        bw = yw * 0.22
        cost = m["opex"][i] + m["cogs"][i]
        for j, (v, c) in enumerate(((m["rev"][i], "#0EA5E9"), (cost, "#F59E0B"))):
            bx = x0 + yw * 0.25 + j * (bw + 3)
            parts.append(f'<rect x="{bx:.1f}" y="{min(y(v), y(0)):.1f}" width="{bw:.1f}" height="{abs(y(v) - y(0)):.1f}" fill="{c}" rx="2"/>')
        parts.append(f'<text x="{x0 + yw / 2:.1f}" y="{height - 8}" text-anchor="middle" fill="#334155">Y{i + 1}</text>')
    pts = " ".join(f"{pad_l + k / 36 * w:.1f},{y(v):.1f}" for k, v in enumerate(m["curve"]))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="#0B6E4F" stroke-width="2.2"/>')
    if m["breakeven"]:
        bx = pad_l + m["breakeven"] / 36 * w
        parts.append(f'<circle cx="{bx:.1f}" cy="{y(0):.1f}" r="4" fill="#0B6E4F"/>')
    parts.append("</svg>")
    return "".join(parts)


CHART_LEGEND = ('<div style="font-size:8pt;color:#475569;margin-top:1mm">'
                '<span style="color:#0EA5E9">■</span> الإيرادات السنوية &nbsp; '
                '<span style="color:#F59E0B">■</span> التكاليف السنوية &nbsp; '
                '<span style="color:#0B6E4F">━</span> النقد التراكمي شهريًا (النقطة = التعادل)</div>')
