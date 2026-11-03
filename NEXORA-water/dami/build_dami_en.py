"""English edition of the DAMI submission package (same files and numbers as build_dami.py)."""

import base64
import io
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from PIL import Image  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402

import content_en as C  # noqa: E402
from build_dami import BMC_CSS, DECK_CSS, DOC_CSS  # noqa: E402
from common import BASE_CSS, OPEX_SPLIT, OUT, ROOT, by_id, cash_chart, e, font_css, model, print_pdf  # noqa: E402

P = by_id(31)
M = model(P)
OPT = model(P, volume=1.4, opex_mult=.95)
DIR = OUT / "DAMI_EN"
SHOTS = DIR / "screens"

LTR = """
body { direction:ltr } ul,ol { padding-left:5mm; padding-right:0 } .bmcg ul { padding-left:4mm; padding-right:0 }
.bmcg h4 small { text-align:left } td.n, th.n { text-align:right } th { text-align:left } td:first-child { text-align:left }
.check li { margin-right:0; margin-left:-5mm } .cover td { padding:1mm 8mm 1mm 0 }
.cover .q { border-right:none; padding-right:0; border-left:4px solid #FCA5A5; padding-left:4mm }
.foot { left:auto; right:17mm } .pg { right:auto; left:17mm }
"""


def page(title, body, css, size="A4"):
    return (f'<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><title>{e(title)}</title>'
            f"<style>{font_css()}{BASE_CSS}@page {{ size:{size}; margin:0; }}{css}{LTR}</style></head><body>{body}</body></html>")


def money(v):
    v = round(v)
    return ("−" if v < 0 else "") + f"JOD {abs(v):,}"


def price(v):
    return f"JOD {v:,.2f}".replace(".00", "")


def be(m):
    return f"Month {m['breakeven']}" if m["breakeven"] else "After year 3"


def ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def kv(rows):
    return "<table>" + "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in rows) + "</table>"


def img64(name, width=1400):
    im = Image.open(SHOTS / f"{name}.png").convert("RGB")
    im.thumbnail((width, width))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


LEGEND = ('<div style="font-size:8pt;color:#475569;margin-top:1mm"><span style="color:#0EA5E9">■</span> Annual revenue &nbsp; '
          '<span style="color:#F59E0B">■</span> Annual costs &nbsp; <span style="color:#0B6E4F">━</span> Monthly cumulative cash (dot = break-even)</div>')
ASK = [f"Seed funding of about {money(round(M['funding'], -2))} covering initial investment and the growth period; the pilot fleet (JOD 30,000) can be split out as a health grant.",
       "A pilot partnership with a blood bank and a private hospital to connect real stock.",
       "Support on the permit path with the Civil Aviation Regulatory Commission and security authorities.",
       "Mentoring in the health sector and entrepreneurship."]


def cover(doc, sub):
    return f"""<div class="cover"><div class="brand">NEXORA · AI &amp; DATA SCIENCE</div>
<div><span class="doc">{e(doc)}</span><h1 style="margin-top:6mm">🩸 {C.NAME}</h1><div class="en" style="letter-spacing:.1em">{C.NAME_AR}</div>
<div class="slogan">{e(C.SLOGAN)}</div><p style="opacity:.9;max-width:160mm">{e(sub)}</p>
<table><tr><td>Team</td><td><b>NEXORA</b></td></tr><tr><td>Field</td><td>Health · Artificial Intelligence &amp; Data Science · Drones</td></tr>
<tr><td>Competition</td><td>Jordan Students Pitch Competition — GEW Jordan</td></tr>
<tr><td>University / Supervisor</td><td>………………………………………</td></tr><tr><td>Team members</td><td>………………………………………</td></tr></table></div>
<div class="q">{e(C.CLOSER)}</div></div>"""


def kpis():
    return f"""<div class="kgrid"><div class="k"><span>Initial investment</span><b>{money(M['capex'])}</b></div>
<div class="k"><span>Funding needed</span><b>{money(M['funding'])}</b></div><div class="k"><span>Year-3 revenue</span><b>{money(M['rev'][2])}</b></div>
<div class="k"><span>Year-3 operating result</span><b>{money(M['ebitda'][2])}</b></div><div class="k"><span>Year-3 gross margin</span><b>{M['margin'] * 100:.0f}%</b></div></div>"""


def facts():
    return '<div class="facts">' + "".join(f"<div><b>{e(a)}</b>{e(b)}</div>" for a, b in C.FACTS) + "</div>"


def layers():
    return '<div class="lay">' + "".join(f"<div><i>{i}</i><b>{e(t)}</b>{e(d)}</div>" for i, t, d in C.LAYERS) + "</div>"


def mission():
    return '<div class="steps">' + "".join(f"<div><b>{e(t)}</b>{e(d)}</div>" for t, d in C.MISSION) + "</div>"


def mission_svg(width=640, height=150):
    return f"""<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Cairo" font-size="11">
<rect width="{width}" height="{height}" rx="10" fill="#FAFAF9"/>
<path d="M80 110 C 180 150, 230 60, 330 110 S 480 140, 560 105" fill="none" stroke="#A8A29E" stroke-width="5"/>
<text x="320" y="140" text-anchor="middle" fill="#78716C">🚗 By car: 34 min at peak</text>
<path d="M80 95 Q 320 0 560 90" fill="none" stroke="#B91C1C" stroke-width="3" stroke-dasharray="8 6"/>
<text x="320" y="36" text-anchor="middle" fill="#B91C1C" font-weight="700">🚁 By drone: 9 min · box at 4°C</text>
<circle cx="80" cy="100" r="22" fill="#B91C1C"/><text x="80" y="105" text-anchor="middle" fill="#fff" font-size="16">🩸</text>
<text x="80" y="138" text-anchor="middle" fill="#1C1917" font-weight="700">Blood bank</text>
<circle cx="560" cy="98" r="22" fill="#0F766E"/><text x="560" y="104" text-anchor="middle" fill="#fff" font-size="16">🏥</text>
<text x="560" y="138" text-anchor="middle" fill="#1C1917" font-weight="700">Hospital</text></svg>"""


def bmc_grid(size):
    return f'<div class="bmcg" style="font-size:{size}">' + "".join(
        f'<div class="blk b-{k}"><h4>{e(en)}</h4>{ul(C.BMC[k])}</div>' for k, en in C.BMC_BLOCKS) + "</div>"


def capex_table():
    rows = "".join(f"<tr><td>{e(n)}</td><td class='n'>{q}</td><td class='n'>{money(c)}</td><td class='n'>{money(q * c)}</td></tr>" for n, q, c in C.BOM)
    return (f"<table><tr><th>Item</th><th class='n'>Qty</th><th class='n'>Unit cost (est.)</th><th class='n'>Total</th></tr>{rows}"
            f"<tr class='hl'><td>Total</td><td></td><td></td><td class='n'>{money(sum(q * c for _, q, c in C.BOM))}</td></tr></table>")


def pl_table():
    rows = [("Revenue", M["rev"]), ("Direct costs", M["cogs"]), ("Gross profit", M["gross"]), ("Operating expenses", M["opex"]),
            ("Operating result", M["ebitda"]), ("Cumulative cash after investment", M["cum"])]
    return ("<table><tr><th>Item</th><th class='n'>Year 1</th><th class='n'>Year 2</th><th class='n'>Year 3</th></tr>"
            + "".join(f"<tr{' class=\"hl\"' if i >= 4 else ''}><td>{e(n)}</td>" + "".join(f"<td class='n'>{money(x)}</td>" for x in v) + "</tr>" for i, (n, v) in enumerate(rows))
            + "</table>")


def streams_table():
    rows = "".join(f"<tr><td>{e(nm)}</td><td>{e(u)}</td><td class='n'>{price(pr)}</td>" + "".join(f"<td class='n'>{x:,}</td>" for x in units)
                   + f"<td class='n'>{money(pr * units[2])}</td></tr>" for (nm, u), (_, _, pr, units, _) in zip(C.STREAM_NAMES, P["fin"]["streams"]))
    return f"<table><tr><th>Stream</th><th>Unit</th><th class='n'>Price</th><th class='n'>Y1</th><th class='n'>Y2</th><th class='n'>Y3</th><th class='n'>Y3 revenue</th></tr>{rows}</table>"


def scenario_table():
    rows = ""
    for name, vol, op in [("Pessimistic", .6, 1.1), ("Base", 1.0, 1.0), ("Optimistic", 1.4, .95)]:
        s = model(P, volume=vol, opex_mult=op)
        rows += f"<tr><td>{name}</td><td class='n'>×{vol}</td><td class='n'>×{op}</td><td class='n'>{money(s['rev'][2])}</td><td class='n'>{money(s['ebitda'][2])}</td><td class='n'>{money(s['funding'])}</td><td>{be(s)}</td></tr>"
    g = model(P, capex_mult=(M["capex"] - 30000) / M["capex"])
    rows += f"<tr class='hl'><td>Base + grant for pilot fleet</td><td class='n'>×1</td><td class='n'>×1</td><td class='n'>{money(g['rev'][2])}</td><td class='n'>{money(g['ebitda'][2])}</td><td class='n'>{money(g['funding'])}</td><td>{be(g)}</td></tr>"
    return f"<table><tr><th>Scenario</th><th class='n'>Volume</th><th class='n'>Costs</th><th class='n'>Y3 revenue</th><th class='n'>Y3 result</th><th class='n'>Funding needed</th><th>Break-even</th></tr>{rows}</table>"


def sensitivity_table():
    rows = ""
    for label, kw in [("Price −20%", dict(price_mult=.8)), ("Price +20%", dict(price_mult=1.2)), ("Volume −20%", dict(volume=.8)),
                      ("Volume +20%", dict(volume=1.2)), ("Costs +20%", dict(opex_mult=1.2)), ("Costs −20%", dict(opex_mult=.8))]:
        s = model(P, **kw)
        rows += f"<tr><td>{label}</td><td class='n'>{money(s['ebitda'][2])}</td><td class='n'>{money(s['cum'][2])}</td><td>{be(s)}</td></tr>"
    return f"<table><tr><th>Change</th><th class='n'>Y3 result</th><th class='n'>Y3 cumulative cash</th><th>Break-even</th></tr>{rows}</table>"


def unit_economics():
    fl, sub = P["fin"]["streams"][1], P["fin"]["streams"][0]
    d = fl[2] * fl[4]
    return f"""<table><tr><th>Metric</th><th class='n'>Value</th></tr>
<tr><td>Emergency flight price</td><td class='n'>{price(fl[2])}</td></tr>
<tr><td>Direct cost per flight (battery, maintenance, pilot time, insurance)</td><td class='n'>{price(d)}</td></tr>
<tr><td>Contribution margin per flight</td><td class='n'>{price(fl[2] - d)} ({(1 - fl[4]) * 100:.0f}%)</td></tr>
<tr><td>Annual hospital subscription / direct cost</td><td class='n'>{price(sub[2])} / {price(sub[2] * sub[4])}</td></tr>
<tr><td>Year-3 flights (assumption)</td><td class='n'>{fl[3][2]:,} ≈ {fl[3][2] / 365:.1f} per day</td></tr></table>"""


def team():
    return kv(C.TEAM)


def risks():
    return "<table><tr><th>Risk</th><th>Mitigation</th></tr>" + "".join(f"<tr><td>{e(r)}</td><td>{e(m)}</td></tr>" for r, m in C.RISKS) + "</table>"


def gtm():
    return "<table>" + "".join(f"<tr><td style='white-space:nowrap'><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in C.GTM) + "</table>"


def comp():
    return ("<table><tr><th>Alternative</th><th>What it offers</th><th>Where it falls short</th></tr>"
            + "".join(f"<tr{' class=\"hl\"' if i == 3 else ''}><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for i, (a, b, c) in enumerate(C.COMPETITION)) + "</table>")


def screens(names):
    return "".join(f'<div class="avoid"><div class="shot"><img src="{img64(k)}"></div><div class="cap"><b>{e(t)}:</b> {e(d)}</div></div>'
                   for k, t, d in C.APP_SCREENS if k in names)


def h2(n, t):
    return f'<h2><span class="n">{n}</span> {e(t)}</h2>'


VERDICT = (f"Under base assumptions the project does not break even within 3 years because drones and licensing are an early investment; "
           f"but year 3 is operationally positive ({money(M['ebitda'][2])}), and it breaks even in month {OPT['breakeven']} in the optimistic case. Funding the fleet with a grant lowers the risk.")


def proposal():
    body = cover("Full Proposal", C.ONE_LINER) + f"""
{h2(1, 'Executive summary')}<p><b>{C.NAME}</b> — {e(C.ONE_LINER)}</p>{kpis()}
<p>The prototype is already built as a complete interactive simulator. We start with software in private hospitals to generate early revenue, then run a pilot drone route once permits are granted.</p>
{h2(2, 'The problem')}<p>{e(C.PROBLEM)}</p>{facts()}{ul(C.EVIDENCE)}
{h2(3, 'The solution: three layers in one platform')}<p>{e(C.SOLUTION)}</p>{layers()}
<div class="brk"></div>{h2(4, 'The drone mission: from blood bank to hospital')}{mission_svg()}{mission()}
<div class="avoid"><h3>Drone and cooling-box specification (pilot)</h3>{kv(C.DRONE_SPEC)}</div>
<div class="dark avoid" style="margin-top:3mm"><b>⚡ Live demo for the judges:</b> {e(C.WOW)}</div>
<div class="brk"></div>{h2(5, 'The app: prototype screens')}{screens(['dash', 'sos'])}
<div class="brk"></div>{screens(['forecast', 'donors', 'mci'])}
<div class="brk"></div>{h2(6, 'AI and data')}{ul(C.AI)}<p><b>Data:</b> {e(', '.join(C.DATA))}</p>
{h2(7, 'Market and competition')}<p>{e(C.MARKET)}</p>{comp()}
<div class="brk"></div>{h2(8, 'Business Model Canvas')}{bmc_grid('9pt')}
<div class="brk"></div>{h2(9, 'Financial feasibility')}{kpis()}{pl_table()}
<div class="avoid">{cash_chart(M, 640, 170)}{LEGEND}</div>
<div class="avoid"><h3>Scenarios and path to profitability</h3>{scenario_table()}</div>
<div class="verdict avoid" style="background:#7F1D1D;margin-top:2mm">{e(VERDICT)}</div>
<div class="brk"></div>{h2(10, 'Go-to-market plan')}{gtm()}
<div class="avoid">{h2(11, 'Prototype in 12 weeks')}<table><tr><th>Weeks</th><th>Deliverables</th></tr>{''.join(f'<tr><td>{e(w)}</td><td>{e(t)}</td></tr>' for w, t in C.MVP)}</table></div>
<div class="avoid">{h2(12, 'Risks and regulation')}{risks()}<p>{e(C.LEGAL)}</p></div>
<div class="avoid">{h2(13, 'Impact metrics')}{ul(C.IMPACT)}</div>
<div class="avoid">{h2(14, 'Alignment with national priorities')}{ul(C.ALIGN)}</div>
<div class="avoid">{h2(15, 'Team')}{team()}</div>
<div class="avoid">{h2(16, 'The Ask')}{ul(ASK)}</div><p class="note">{e(C.DISC)}</p>"""
    return print_pdf(page("DAMI — Proposal", body, DOC_CSS + BMC_CSS), DIR / "01_DAMI_Proposal_EN.pdf")


def bmc_pdf():
    css = DOC_CSS.split("@page")[0] + BMC_CSS + """
@page { size:A4 landscape; margin:0 } body { font-size:9pt }
.sheet { height:209mm; padding:8mm 10mm; display:flex; flex-direction:column; break-after:page }
.hdr { display:flex; align-items:center; gap:4mm; background:linear-gradient(120deg,#450A0A,#B91C1C); color:#fff; border-radius:3mm; padding:3mm 5mm; margin-bottom:2.5mm }
.hdr h1 { font-size:22pt; font-weight:900 } .hdr p { margin:0; opacity:.9 } .hdr .kk { margin-left:auto; display:flex; gap:2mm }
.hdr .kk div { background:#ffffff22; border-radius:2mm; padding:1mm 3mm; font-size:8pt; text-align:center } .hdr .kk b { display:block; font-size:10pt }
.bmcg { flex:1; grid-template-rows:1fr 1fr .7fr }
"""
    kk = (f"<div class='kk'><div>Initial investment<b>{money(M['capex'])}</b></div><div>Year-3 revenue<b>{money(M['rev'][2])}</b></div>"
          f"<div>Year-3 gross margin<b>{M['margin'] * 100:.0f}%</b></div></div>")
    hdr = lambda sub: f'<div class="hdr"><div><h1>🩸 {C.NAME}</h1><p>{sub} · Team NEXORA</p></div>{kk}</div>'  # noqa: E731
    body = (f'<section class="sheet">{hdr("Business Model Canvas")}{bmc_grid("9pt")}</section>'
            f'<section class="sheet" style="display:block">{hdr("How the business model creates and captures value")}'
            f'<div class="two"><div><h3>Who pays and why?</h3>{ul(C.WHO_PAYS)}<h3>Unit economics</h3>{unit_economics()}</div>'
            f'<div><h3>Revenue streams in numbers</h3>{streams_table()}<h3>Growth path</h3>{gtm()}</div></div><p class="note">{e(C.DISC)}</p></section>')
    return print_pdf(page("DAMI — Business Model Canvas", body, css), DIR / "02_DAMI_Business_Model_Canvas_EN.pdf")


def feasibility():
    opex_rows = "".join(f"<tr><td>{n}</td>" + "".join(f"<td class='n'>{money(o * s)}</td>" for o in P['fin']['opex']) + "</tr>"
                        for n, (_, s) in zip(["Team salaries", "Technology & servers", "Marketing & sales", "Operations & admin"], OPEX_SPLIT))
    body = cover("Feasibility Study", "A preliminary feasibility study covering market, technical, operational, legal and 3-year financial feasibility, with scenarios, sensitivity and a recommendation.") + f"""
{h2(1, 'Summary of findings')}{kpis()}
<table><tr><th>Dimension</th><th>Rating</th><th>Why</th></tr>
<tr><td>Market</td><td>✅ High</td><td>Critical health need, clear customer (hospitals and the blood bank), no direct local competitor per our preliminary research.</td></tr>
<tr><td>Technical</td><td>✅ High</td><td>Mature technologies (forecasting, optimization, medical drones proven worldwide); the prototype works.</td></tr>
<tr><td>Operational</td><td>⚠️ Medium</td><td>Needs an operations center, licensed pilots and cold-chain management.</td></tr>
<tr><td>Legal</td><td>⚠️ Biggest challenge</td><td>Flight permits, security approvals and health-data protection.</td></tr>
<tr><td>Financial</td><td>⚠️ Long-term</td><td>Year 3 is positive; break-even after year 3 in the base case and month {OPT['breakeven']} in the optimistic case.</td></tr></table>
{h2(2, 'Market study')}<p>{e(C.PROBLEM)}</p>{facts()}<h3>Target segments</h3>{ul(C.BMC['cs'])}<h3>Growth assumptions</h3><p>{e(C.MARKET)}</p>
<h3>Competition and alternatives</h3>{comp()}
<div class="brk"></div>{h2(3, 'Technical feasibility')}{layers()}<h3>Technology stack</h3>{kv(C.STACK)}<h3>Drone and cooling specification</h3>{kv(C.DRONE_SPEC)}
{h2(4, 'Operational feasibility')}{mission()}{ul(C.OPS)}
<div class="brk"></div>{h2(5, 'Legal and regulatory feasibility')}<table><tr><th>Authority / requirement</th><th>What we need</th></tr>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in C.LICENSES)}</table>
{h2(6, 'Financial feasibility')}
<div class="two"><div class="avoid"><h3>Initial investment (CAPEX)</h3>{capex_table()}</div>
<div class="avoid"><h3>Operating expenses (OPEX)</h3><table><tr><th>Item</th><th class='n'>Y1</th><th class='n'>Y2</th><th class='n'>Y3</th></tr>{opex_rows}<tr class='hl'><td>Total</td>{''.join(f"<td class='n'>{money(o)}</td>" for o in P['fin']['opex'])}</tr></table></div></div>
<div class="avoid"><h3>Revenue streams</h3>{streams_table()}</div><div class="avoid"><h3>Projected income statement</h3>{pl_table()}</div>
<div class="brk"></div><div class="avoid"><h3>36-month cash flow</h3>{cash_chart(M, 640, 190)}{LEGEND}</div>
<div class="two"><div class="avoid"><h3>Unit economics</h3>{unit_economics()}</div><div class="avoid"><h3>Sensitivity analysis</h3>{sensitivity_table()}</div></div>
<div class="avoid"><h3>Scenarios</h3>{scenario_table()}</div>
{h2(7, 'Risks')}{risks()}
<div class="avoid">{h2(8, 'Recommendation')}<div class="verdict" style="background:#7F1D1D">The project is technically feasible with high health impact, and its financial feasibility is long-term. Recommendation: proceed in phases — software first for early revenue, fund the pilot fleet through a grant or health partner, and do not launch commercial flights before permits are complete.</div>
<h3>Assumption validation plan</h3>{ul(C.VALIDATION)}</div><p class="note">{e(C.DISC)}</p>"""
    return print_pdf(page("DAMI — Feasibility Study", body, DOC_CSS), DIR / "03_DAMI_Feasibility_Study_EN.pdf")


def requirements():
    body = cover("Requirements & Equipment", "Everything the project needs: functional and non-functional requirements, equipment and costs, technology, permits, partners, team and a submission checklist.") + f"""
{h2(1, 'Functional requirements')}<table><tr><th>ID</th><th>Requirement</th></tr>{''.join(f'<tr><td><b>{a}</b></td><td>{e(b)}</td></tr>' for a, b in C.FR)}</table>
{h2(2, 'Non-functional requirements')}{kv(C.NFR)}
<div class="brk"></div>{h2(3, 'Equipment and estimated cost')}{capex_table()}
{h2(4, 'Drone and cooling-box specification')}{kv(C.DRONE_SPEC)}{h2(5, 'Technology stack')}{kv(C.STACK)}
<div class="brk"></div>{h2(6, 'Required data')}{ul(C.DATA)}
{h2(7, 'Permits and approvals')}<table><tr><th>Authority</th><th>Required</th></tr>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in C.LICENSES)}</table>
{h2(8, 'Required partners')}{ul(C.BMC['kp'])}{h2(9, 'Team and roles')}{team()}
<div class="avoid">{h2(10, 'Submission checklist')}<ul class="check">{''.join(f'<li>{e(x)}</li>' for x in C.SUBMISSION)}</ul></div>
<div class="avoid">{h2(11, 'Demo-day preparation')}<ul class="check">{''.join(f'<li>{e(x)}</li>' for x in C.DEMO_DAY)}</ul></div><p class="note">{e(C.DISC)}</p>"""
    return print_pdf(page("DAMI — Requirements", body, DOC_CSS), DIR / "04_DAMI_Requirements_EN.pdf")


def script():
    body = cover("Pitch Script & Judge Q&A", "A 5-minute pitch script split by the second, live-demo steps, and the most likely judge questions with suggested answers.") + f"""
{h2(1, 'Pitch script (5 minutes)')}<table><tr><th>Time</th><th>Segment</th><th>What we say / do</th></tr>{''.join(f'<tr><td style="white-space:nowrap">{e(t)}</td><td><b>{e(s)}</b></td><td>{e(x)}</td></tr>' for t, s, x in C.SCRIPT)}</table>
<div class="dark avoid" style="margin-top:3mm"><b>Pitch tips:</b> Open with the story, not the tech. Have the simulator running before you walk in. Raise the regulatory challenge yourself before the judges ask. End on one strong line.</div>
<div class="brk"></div>{h2(2, 'Expected judge questions')}
{''.join(f'<div class="avoid" style="margin-bottom:2.5mm"><h3>Q: {e(q)}</h3><p style="margin:0">A: {e(a)}</p></div>' for q, a in C.QA)}<p class="note">{e(C.DISC)}</p>"""
    return print_pdf(page("DAMI — Pitch Script", body, DOC_CSS), DIR / "06_DAMI_Pitch_Script_QA_EN.pdf")


def deck_html():
    sl = []

    def s(inner, cls=""):
        sl.append(f'<section class="s {cls}">{inner}<div class="foot">NEXORA · DAMI</div><div class="pg">{len(sl) + 1}</div></section>')

    s(f"""<div class="brand">NEXORA · JORDAN STUDENTS PITCH COMPETITION</div><div style="margin-top:22mm"><h1>🩸 {C.NAME}</h1>
<p class="lead" style="font-size:22pt;max-width:250mm;margin-top:6mm">{e(C.SLOGAN)}</p></div>
<p style="position:absolute;bottom:16mm;left:20mm;font-weight:700;opacity:.9">{e(C.CLOSER)}</p>""", "cover")
    s(f"""<h2>5 p.m. — an accident on the Airport Road</h2><p class="lead">A hospital needs <b style="color:#B91C1C">6 units of O negative</b> now. The car from the blood bank needs 34 minutes in traffic.<br>In severe bleeding, every minute matters.</p>{mission_svg(900, 200)}""")
    s(f"""<h2>The problem: shortage here… waste there</h2><p class="lead" style="font-size:14pt">{e(C.PROBLEM)}</p><div class="big4">{''.join(f'<div><b>{e(a)}</b>{e(b)}</div>' for a, b in C.FACTS)}</div>""")
    s(f"""<h2>The solution: DAMI — three layers, one platform</h2>{layers()}<p class="lead" style="margin-top:6mm;font-size:14pt">{e(C.ONE_LINER)}</p>""")
    s(f"""<h2>The drone mission: blood bank to hospital in minutes</h2>{mission()}
<div class="two" style="margin-top:5mm;font-size:11pt">{kv(C.DRONE_SPEC[:4])}{kv(C.DRONE_SPEC[4:])}</div>""")
    for key in ("sos", "dash", "mci"):
        k, t, d = next(x for x in C.APP_SCREENS if x[0] == key)
        s(f"""<h2>The prototype works: {e(t)}</h2><div class="split"><div class="shot"><img src="{img64(k, 1600)}"></div>
<div><p class="lead" style="font-size:15pt">{e(d)}</p>{'<div class="dark" style="font-size:11.5pt">⚡ ' + e(C.WOW) + '</div>' if key == 'sos' else ''}</div></div>""")
    s(f"""<h2>The AI inside DAMI</h2><div class="two"><div><h3 style="font-size:15pt">Models</h3>{ul(C.AI)}</div><div><h3 style="font-size:15pt">Data</h3>{ul(C.DATA)}</div></div>
<div class="shot" style="margin-top:4mm;max-height:72mm"><img src="{img64('forecast', 1600)}"></div>""")
    s(f"""<h2>Market and competition</h2>{comp()}<p class="lead" style="font-size:14pt;margin-top:5mm">We start with private hospitals because they decide faster, then the Ministry of Health and the National Blood Bank.</p>""")
    s(f"""<h2 style="margin-bottom:3mm">Business Model Canvas</h2>{bmc_grid('8.2pt')}""")
    s(f"""<h2>The numbers: how we make money</h2><div class="split"><div>{streams_table()}<div style="margin-top:4mm">{cash_chart(M, 640, 180)}{LEGEND}</div></div>
<div class="kk"><div>Initial investment<b>{money(M['capex'])}</b></div><div>Year-3 revenue<b>{money(M['rev'][2])}</b></div>
<div>Year-3 gross margin<b>{M['margin'] * 100:.0f}%</b></div><div>Year-3 operating result<b>{money(M['ebitda'][2])}</b></div>
<div>Break-even (optimistic)<b>Month {OPT['breakeven']}</b></div><div>Margin per drone flight<b>55%</b></div></div></div>""")
    s(f"""<h2>The plan: from simulator to first licensed flight</h2>{gtm()}<div class="two" style="margin-top:5mm"><div><h3 style="font-size:15pt">Risks and mitigation</h3>{risks()}</div>
<div><h3 style="font-size:15pt">Impact metrics</h3>{ul(C.IMPACT)}</div></div>""")
    s(f"""<h2>Team and the ask</h2><div class="two"><div>{team()}</div><div><h3 style="font-size:15pt">The Ask</h3>{ul(ASK)}</div></div>""")
    s(f"""<div style="margin-top:30mm"><h1 style="font-size:58pt">{e(C.CLOSER)}</h1><p class="lead" style="margin-top:8mm">🩸 DAMI · Team NEXORA · Thank you</p></div>""", "cover")
    return page("DAMI — Pitch Deck", "".join(sl), DECK_CSS, size="338.67mm 190.5mm")


def deck_pptx(path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    W, H = prs.slide_width, prs.slide_height
    red, dark, white, ink = RGBColor(0xB9, 0x1C, 0x1C), RGBColor(0x45, 0x0A, 0x0A), RGBColor(255, 255, 255), RGBColor(0x29, 0x25, 0x24)
    blank, cm = prs.slide_layouts[6], 360000

    def text(sl, x, y, w, h, lines, size=16, color=ink, bold=False):
        tf = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)).text_frame
        tf.word_wrap = True
        for i, line in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            run = para.add_run()
            run.text = line.lstrip("■ ")
            run.font.size, run.font.bold, run.font.name = Pt(size), bold or line.startswith("■"), "Calibri"
            run.font.color.rgb = color

    def new(title=None, bg=None):
        sl = prs.slides.add_slide(blank)
        if bg:
            sl.background.fill.solid()
            sl.background.fill.fore_color.rgb = bg
        else:
            bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(cm // 2), H)
            bar.fill.solid()
            bar.fill.fore_color.rgb = red
            bar.line.fill.background()
        if title:
            text(sl, cm, int(.5 * cm), W - 2 * cm, int(1.6 * cm), [title], 28, dark, True)
        return sl

    def pic(sl, key, x, y, w):
        tmp = DIR / f"_{key}.jpg"
        Image.open(SHOTS / f"{key}.png").convert("RGB").save(tmp, "JPEG", quality=85)
        sl.shapes.add_picture(str(tmp), Emu(x), Emu(y), width=Emu(w))
        tmp.unlink()

    full, half = W - 2 * cm, int(W / 2)
    sl = new(bg=dark)
    text(sl, cm, 4 * cm, full, 3 * cm, [f"🩸 {C.NAME}"], 60, white, True)
    text(sl, cm, 7.5 * cm, full, 3 * cm, [C.SLOGAN, "", "Team NEXORA · Jordan Students Pitch Competition"], 20, RGBColor(0xFE, 0xCA, 0xCA))
    sl = new("5 p.m. — an accident on the Airport Road")
    text(sl, cm, 3 * cm, full, 8 * cm, ["A hospital needs 6 units of O negative now.", "Car from the blood bank: 34 minutes in traffic.", "Drone: 9 minutes, box steady at 4°C.", "", "In severe bleeding, every minute matters."], 24)
    sl = new("The problem: shortage here… waste there")
    text(sl, cm, 2.5 * cm, full, 5 * cm, [C.PROBLEM], 16)
    text(sl, cm, 8 * cm, full, 8 * cm, [f"■ {a}: {b}" for a, b in C.FACTS], 16)
    sl = new("The solution: three layers, one platform")
    text(sl, cm, 2.5 * cm, full, 14 * cm, sum(([f"■ {i} {t}", d, ""] for i, t, d in C.LAYERS), []), 17)
    sl = new("The drone mission: blood bank to hospital")
    text(sl, cm, 2.5 * cm, half - 2 * cm, 14 * cm, [f"■ {k + 1}. {t}" if j == 0 else d for k, (t, d) in enumerate(C.MISSION) for j in (0, 1)], 14)
    text(sl, half, 2.5 * cm, half - cm, 14 * cm, [f"■ {a}: {b}" for a, b in C.DRONE_SPEC], 12)
    for key in ("sos", "dash", "mci", "forecast"):
        _, t, d = next(x for x in C.APP_SCREENS if x[0] == key)
        sl = new(f"The prototype works: {t}")
        pic(sl, key, cm, int(2.4 * cm), int(W * .62))
        text(sl, int(W * .62) + int(1.5 * cm), int(2.6 * cm), int(W * .38) - int(2.5 * cm), 12 * cm, [d], 16)
    sl = new("Market and competition")
    text(sl, cm, 2.5 * cm, full, 14 * cm, sum(([f"■ {a}", f"Offers: {b}", f"Falls short: {c}", ""] for a, b, c in C.COMPETITION), []), 14)
    sl = new("Business Model Canvas")
    col = full // 3
    for i, (k, en) in enumerate(C.BMC_BLOCKS):
        text(sl, cm + (i % 3) * col, int(2.3 * cm) + (i // 3) * int(5.2 * cm), col - cm // 3, int(5 * cm), [f"■ {en}", *C.BMC[k]], 10.5)
    sl = new("The numbers: how we make money")
    text(sl, cm, 2.5 * cm, full, 14 * cm,
         [f"■ {nm}: {price(pr)} per {u} — volumes {un[0]:,} / {un[1]:,} / {un[2]:,}" for (nm, u), (_, _, pr, un, _) in zip(C.STREAM_NAMES, P["fin"]["streams"])]
         + ["", f"Initial investment: {money(M['capex'])}", f"Year-3 revenue: {money(M['rev'][2])}", f"Year-3 operating result: {money(M['ebitda'][2])}",
            f"Year-3 gross margin: {M['margin'] * 100:.0f}%", f"Break-even: after year 3 (base) · month {OPT['breakeven']} (optimistic)"], 16)
    sl = new("Plan and risks")
    text(sl, cm, 2.5 * cm, full, 14 * cm, [f"■ {a}: {b}" for a, b in C.GTM] + [""] + [f"■ {r}: {m}" for r, m in C.RISKS], 14)
    sl = new("Team and the ask")
    text(sl, cm, 2.5 * cm, half - 2 * cm, 14 * cm, [f"■ {r}" if j == 0 else d for r, d in C.TEAM for j in (0, 1)], 13)
    text(sl, half, 2.5 * cm, half - cm, 14 * cm, ["■ The Ask", *ASK], 14)
    sl = new(bg=dark)
    text(sl, cm, 5 * cm, full, 6 * cm, [C.CLOSER, "", "🩸 DAMI · Team NEXORA · Thank you"], 36, white, True)
    prs.save(path)
    return path


def build():
    if DIR.exists():
        shutil.rmtree(DIR)
    SHOTS.mkdir(parents=True)
    subprocess.run([sys.executable, str(HERE / "translate_app.py")], check=True)
    app = DIR / "07_DAMI_App_EN.html"
    app.write_text((ROOT / "sim" / "dami_en.html").read_text(encoding="utf-8").replace("/*FONT*/", font_css()), encoding="utf-8")
    subprocess.run(["node", str(HERE / "screens.js"), str(app), str(SHOTS)], check=True, cwd="/tmp")
    return [proposal(), bmc_pdf(), feasibility(), requirements(), print_pdf(deck_html(), DIR / "05_DAMI_Pitch_Deck_EN.pdf"),
            deck_pptx(DIR / "05_DAMI_Pitch_Deck_EN.pptx"), script(), app]


if __name__ == "__main__":
    for f in build():
        print(f)
