"""02 — one Business Model Canvas page (A4 landscape) per project."""

from common import AXES, BMC_BLOCKS, DISCLAIMER, OUT, PROJECTS, breakeven_text, e, model, money, page, print_pdf

ICONS = {"kp": "🤝", "ka": "⚙️", "kr": "🧰", "vp": "💎", "cr": "💬", "ch": "📣", "cs": "👥", "cost": "💸", "rev": "💰"}

CSS = """
@page { size:A4 landscape; margin:9mm 10mm; }
@page :first { margin:0; }
body { font-size:9.2pt; }
.cover { height:210mm; padding:20mm 22mm; color:#fff; display:flex; flex-direction:column; justify-content:center;
  background:linear-gradient(150deg,#04223A,#0369A1 60%,#0B6E4F); }
.cover h1 { font-size:44pt; font-weight:900; line-height:1.15 } .cover p { font-size:13pt; opacity:.9; margin-top:4mm }
.sheet { break-before:page; height:189mm; display:flex; flex-direction:column; }
.top { display:flex; align-items:center; gap:4mm; margin-bottom:2.5mm }
.num { background:#0369A1; color:#fff; font-weight:900; font-size:17pt; border-radius:2mm; padding:0 3mm }
.name { font-size:17pt; font-weight:900 } .tag { color:#0369A1; font-weight:700; font-size:9.5pt }
.kpis { margin-right:auto; display:flex; gap:2mm } .kpis div { background:#F0F9FF; border:1px solid #BAE6FD; border-radius:2mm; padding:1mm 2.5mm; font-size:8pt; text-align:center }
.kpis b { display:block; color:#075985; font-size:9.5pt }
.canvas { flex:1; display:grid; gap:2mm; grid-template-columns:repeat(10,minmax(0,1fr)); grid-template-rows:1fr 1fr .82fr;
  grid-template-areas:"kp kp ka ka vp vp cr cr cs cs" "kp kp kr kr vp vp ch ch cs cs" "cost cost cost cost cost rev rev rev rev rev"; }
.blk { border:1.5px solid #CBD5E1; border-radius:2.5mm; padding:2mm 3mm; overflow:hidden; background:#fff }
.blk h3 { font-size:10pt; color:#0F172A; display:flex; justify-content:space-between; gap:2mm; border-bottom:1px solid #E2E8F0; padding-bottom:1mm; margin-bottom:1mm }
.blk h3 small { font-size:7pt; color:#64748B; direction:ltr; font-weight:600 }
.blk ul { padding-right:4mm; margin:0 } .blk li { margin:.6mm 0; line-height:1.4 }
.vp { background:#F0F9FF; border-color:#0EA5E9 } .cs { background:#F0FDF4; border-color:#22C55E } .rev { background:#FFFBEB; border-color:#F59E0B } .cost { background:#FEF2F2; border-color:#F87171 }
.foot { font-size:7.5pt; color:#64748B; margin-top:1.5mm }
"""


def block(p, key, ar, en):
    items = "".join(f"<li>{e(x)}</li>" for x in p["bmc"][key])
    return f'<div class="blk {key}" style="grid-area:{key}"><h3><span>{ICONS[key]} {e(ar)}</span><small>{e(en)}</small></h3><ul>{items}</ul></div>'


def sheet(p):
    m = model(p)
    blocks = "".join(block(p, k, ar, en) for k, ar, en in BMC_BLOCKS)
    return f"""<section class="sheet">
  <div class="top"><div class="num">{p['id']:02d}</div>
    <div><div class="name">{p['emoji']} {e(p['ar'])} <span class="en" style="font-size:.6em">{e(p['en'])}</span> <span class="chip" style="background:{AXES[p['axis']][1]}">{e(AXES[p['axis']][0])}</span></div>
    <div class="tag">{e(p['tag'])}</div></div>
    <div class="kpis"><div>الاستثمار الأولي<b>{money(m['capex'])}</b></div><div>إيرادات السنة 3<b>{money(m['rev'][2])}</b></div><div>التعادل<b>{breakeven_text(m['breakeven'])}</b></div></div>
  </div>
  <div class="canvas">{blocks}</div>
  <div class="foot">Business Model Canvas · فريق NEXORA · الأرقام افتراضات تخطيطية أولية للتحقق.</div>
</section>"""


def build():
    body = f"""<div class="cover"><div style="letter-spacing:.4em;font-weight:900;opacity:.8">NEXORA</div>
  <h1>نموذج العمل التجاري<br>Business Model Canvas</h1>
  <p>31 لوحة نموذج عمل: لكل مشروع الخانات التسع كاملة.<br>Key Partnerships · Key Activities · Key Resources · Value Propositions · Customer Relationships · Channels · Customer Segments · Cost Structure · Revenue Streams</p>
  <p style="font-size:9pt">{e(DISCLAIMER)}</p></div>
{''.join(sheet(p) for p in PROJECTS)}"""
    return print_pdf(page("NEXORA — Business Model Canvas", body, CSS), OUT / "02_Business_Model_Canvas.pdf")


if __name__ == "__main__":
    print(build())
