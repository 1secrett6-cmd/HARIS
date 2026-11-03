"""DAMI submission package: proposal, BMC, feasibility, requirements, pitch deck (PDF+PPTX), script & Q&A, app."""

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
from pptx.enum.text import PP_ALIGN  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402

import build_sim  # noqa: E402
from common import (BMC_BLOCKS, CHART_LEGEND, KING_QUOTE, OPEX_SPLIT, OUT, SCENARIOS, breakeven_text, by_id,  # noqa: E402
                    cash_chart, e, model, money, page, price, print_pdf)
from content import (APP_SCREENS, BOM, COMPETITION, DRONE_SPEC, FACTS, FR, GTM, LAYERS, LICENSES, MISSION,  # noqa: E402
                     NAME_AR, NAME_EN, NFR, ONE_LINER, QA, SCRIPT, SLOGAN, STACK, SUBMISSION)

P = by_id(31)
M = model(P)
DIR = OUT / "DAMI"
SHOTS = DIR / "screens"
TEAM = [("قائد المشروع / AI Lead", "المعمارية التقنية ونماذج التنبؤ والتنسيق"),
        ("Data Scientist", "بيانات المخزون والطلب، وتقييم النماذج"),
        ("مهندس أنظمة / Drones & IoT", "تكامل الدرون وصناديق التبريد والحساسات"),
        ("مطور تطبيقات", "لوحة القيادة وتطبيق المتبرع والعرض الحي"),
        ("Business & Pitch Lead", "الشراكات الصحية والتنظيمية ونموذج العمل والعرض")]

THEME = """
:root { --r:#B91C1C; --rd:#7F1D1D; --rk:#450A0A; --rs:#FEF2F2; --rb:#FECACA; }
.cover { color:#fff; background:radial-gradient(circle at 15% 20%,#DC262655,transparent 45%),linear-gradient(155deg,#2A0606,#7F1D1D 55%,#B91C1C); }
.brand { letter-spacing:.45em; font-weight:900; opacity:.75; font-size:11pt }
.drop { display:inline-block; width:16mm; height:16mm; border-radius:50% 0 50% 50%; transform:rotate(-45deg); background:#fff; margin-left:4mm; vertical-align:middle; box-shadow:0 0 0 3mm #ffffff33 }
h2 { color:var(--rd); font-size:15pt; font-weight:900; margin:5mm 0 2mm; display:flex; align-items:center; gap:2mm }
h2 .n { background:var(--r); color:#fff; border-radius:1.5mm; font-size:10pt; padding:0 2.2mm; }
h3 { color:var(--r); font-size:11pt; margin:3mm 0 1mm }
th { background:var(--rd) !important; }
.k { background:var(--rs); border:1px solid var(--rb); border-radius:2.5mm; padding:2.5mm; text-align:center }
.k span { display:block; font-size:7.8pt; color:#57534E } .k b { font-size:11pt; color:var(--rd) }
.kgrid { display:grid; gap:2mm; grid-template-columns:repeat(5,minmax(0,1fr)); margin:2mm 0 }
.lay { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:3mm }
.lay div { border:1.5px solid var(--rb); border-radius:3mm; padding:3mm; background:#fff } .lay i { font-style:normal; font-size:20pt }
.lay b { display:block; color:var(--rd); font-size:11pt }
.steps { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:2mm; counter-reset:s }
.steps div { background:var(--rs); border-top:4px solid var(--r); border-radius:2mm; padding:2.5mm; font-size:8.6pt; counter-increment:s }
.steps b { display:block; color:var(--rd); font-size:9.5pt } .steps b::before { content:counter(s) ". " }
.facts { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:2.5mm }
.facts div { background:#fff; border:1px solid var(--rb); border-radius:2.5mm; padding:2.5mm; font-size:8.4pt }
.facts b { display:block; font-size:14pt; color:var(--r); font-weight:900 }
.shot { border:1px solid #E7E5E4; border-radius:2.5mm; overflow:hidden; box-shadow:0 1mm 3mm #0002 } .shot img { width:100%; display:block }
.cap { font-size:8.4pt; color:#57534E; margin:1mm 0 3mm } .cap b { color:var(--rd) }
.dark { background:#1C1917; color:#F5F5F4; border-radius:2.5mm; padding:3mm 4mm }
.verdict { color:#fff; border-radius:2mm; padding:2.5mm 4mm; font-weight:700 }
.two { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:5mm }
.avoid { break-inside:avoid } .brk { break-before:page } ul { padding-right:5mm } li { margin:.6mm 0 }
td.n, th.n { direction:ltr; text-align:left } tr.hl td { background:var(--rs); font-weight:900 }
.note { font-size:8pt; color:#78716C; margin-top:3mm }
.check li { list-style:none; margin-right:-5mm } .check li::before { content:"☐  "; color:var(--r); font-weight:900 }
"""

DOC_CSS = THEME + """
@page { size:A4; margin:13mm 14mm 14mm; @bottom-center { content:counter(page); font-size:8pt; color:#A8A29E } }
@page :first { margin:0 }
body { font-size:9.8pt }
.cover { height:297mm; padding:22mm 18mm; display:flex; flex-direction:column; justify-content:space-between }
.cover h1 { font-size:64pt; font-weight:900; line-height:1 } .cover .en { font-size:20pt; letter-spacing:.35em; opacity:.85 }
.cover .doc { display:inline-block; background:#fff; color:var(--rd); font-weight:900; border-radius:99px; padding:1mm 6mm; font-size:13pt }
.cover .slogan { font-size:15pt; font-weight:700; margin-top:5mm; max-width:150mm }
.cover table { width:auto; font-size:10.5pt; margin-top:6mm } .cover td { color:#fff; border:none; padding:1mm 0 1mm 8mm }
.cover .q { border-right:4px solid #FCA5A5; padding-right:4mm; font-weight:700; font-size:10.5pt }
"""


def ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def img64(name, width=1400, quality=82):
    im = Image.open(SHOTS / f"{name}.png").convert("RGB")
    im.thumbnail((width, width))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def cover(doc_title, subtitle):
    return f"""<div class="cover">
  <div class="brand">NEXORA · AI &amp; DATA SCIENCE</div>
  <div>
    <span class="doc">{e(doc_title)}</span>
    <h1 style="margin-top:6mm">🩸 {NAME_AR}</h1><div class="en">{NAME_EN}</div>
    <div class="slogan">{e(SLOGAN)}</div>
    <p style="opacity:.9;max-width:160mm">{e(subtitle)}</p>
    <table><tr><td>الفريق</td><td><b>NEXORA</b></td></tr><tr><td>المجال</td><td>الصحة · الذكاء الاصطناعي وعلم البيانات · الطائرات المسيّرة</td></tr>
    <tr><td>المسابقة</td><td>Jordan Students Pitch Competition — GEW Jordan</td></tr>
    <tr><td>الجامعة / المشرف</td><td>………………………………………</td></tr><tr><td>أعضاء الفريق</td><td>………………………………………</td></tr></table>
  </div>
  <div class="q">لأن الدم الذي يصل متأخرًا… لا يصل.</div>
</div>"""


def kpis():
    return f"""<div class="kgrid">
  <div class="k"><span>الاستثمار الأولي</span><b>{money(M['capex'])}</b></div>
  <div class="k"><span>التمويل المطلوب</span><b>{money(M['funding'])}</b></div>
  <div class="k"><span>إيرادات السنة 3</span><b>{money(M['rev'][2])}</b></div>
  <div class="k"><span>صافي التشغيل س3</span><b>{money(M['ebitda'][2])}</b></div>
  <div class="k"><span>الهامش الإجمالي س3</span><b>{M['margin'] * 100:.0f}%</b></div>
</div>"""


def facts_html():
    return '<div class="facts">' + "".join(f"<div><b>{e(a)}</b>{e(b)}</div>" for a, b in FACTS) + "</div>"


def layers_html():
    return '<div class="lay">' + "".join(f"<div><i>{i}</i><b>{e(t)}</b>{e(d)}</div>" for i, t, d in LAYERS) + "</div>"


def mission_html():
    return '<div class="steps">' + "".join(f"<div><b>{e(t)}</b>{e(d)}</div>" for t, d in MISSION) + "</div>"


def mission_svg(width=640, height=150):
    """Schematic route: blood bank -> drone path vs road path -> hospital."""
    return f"""<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Cairo" font-size="11">
  <rect width="{width}" height="{height}" rx="10" fill="#FAFAF9"/>
  <path d="M80 110 C 180 150, 230 60, 330 110 S 480 140, 560 105" fill="none" stroke="#A8A29E" stroke-width="5" stroke-dasharray="2 0"/>
  <text x="320" y="140" text-anchor="middle" fill="#78716C">🚗 بالسيارة: 34 دقيقة في الذروة</text>
  <path d="M80 95 Q 320 0 560 90" fill="none" stroke="#B91C1C" stroke-width="3" stroke-dasharray="8 6"/>
  <text x="320" y="36" text-anchor="middle" fill="#B91C1C" font-weight="700">🚁 بالدرون: 9 دقائق · صندوق 4°م</text>
  <circle cx="80" cy="100" r="22" fill="#B91C1C"/><text x="80" y="105" text-anchor="middle" fill="#fff" font-size="16">🩸</text>
  <text x="80" y="138" text-anchor="middle" fill="#1C1917" font-weight="700">بنك الدم</text>
  <circle cx="560" cy="98" r="22" fill="#0F766E"/><text x="560" y="104" text-anchor="middle" fill="#fff" font-size="16">🏥</text>
  <text x="560" y="138" text-anchor="middle" fill="#1C1917" font-weight="700">المستشفى</text>
</svg>"""


def bmc_grid(size="9pt"):
    cells = "".join(
        f'<div class="blk b-{k}"><h4>{e(ar)} <small>{e(en)}</small></h4>{ul(BMC[k])}</div>' for k, ar, en in BMC_BLOCKS)
    return f'<div class="bmcg" style="font-size:{size}">{cells}</div>'


# Richer DAMI canvas than the one-line portfolio version.
BMC = dict(
    kp=["وزارة الصحة وبنك الدم الوطني", "المستشفيات الخاصة والحكومية والخدمات الطبية الملكية", "مشغّلو ومصنّعو الدرونز الطبية",
        "هيئة تنظيم الطيران المدني والجهات الأمنية", "الهلال الأحمر الأردني", "شركات اتصالات وتأمين ورعاة مسؤولية مجتمعية"],
    ka=["تطوير نماذج التنبؤ والموازنة", "تشغيل مركز عمليات الطوارئ والأسطول", "إدارة سلسلة التبريد والجودة",
        "تشغيل تطبيق المتبرعين وحملات الاستدعاء", "بناء الشراكات والحصول على التصاريح"],
    kr=["المنصة البرمجية ونماذج الذكاء الاصطناعي", "أسطول الدرونز وصناديق التبريد الذكية", "قاعدة متبرعين بموافقتهم",
        "فريق تقني وطيارون مرخّصون وخبير بنوك دم", "التصاريح والاتفاقيات"],
    vp=["للمستشفى: وحدات طارئة خلال دقائق بدل نصف ساعة", "لبنك الدم: هدر أقل بموازنة المخزون قبل انتهاء الصلاحية",
        "للوزارة: لوحة وطنية لحظية وجاهزية للحوادث الكبرى", "للمتبرع: دعوة في الوقت الصحيح ومعرفة أثر تبرعه",
        "للمريض: دم متوفر عندما يحتاجه"],
    cr=["عقد خدمة سنوي مع مدير حساب", "مركز عمليات 24/7 للطوارئ", "تقارير أثر شهرية", "مجتمع متبرعين وتحفيز وشارات"],
    ch=["بيع مباشر لإدارات المستشفيات", "شراكة مع وزارة الصحة وبنك الدم", "مؤتمرات ومعارض صحية",
        "حملات إعلامية وجامعات للمتبرعين", "تطبيق جوال ولوحة ويب"],
    cs=["المستشفيات الخاصة (البداية)", "مستشفيات وزارة الصحة والخدمات الطبية الملكية", "بنك الدم الوطني",
        "الهلال الأحمر والدفاع المدني", "المتبرعون (مستخدمون مجانيون)"],
    cost=["تطوير البرمجيات والذكاء الاصطناعي", "شراء الدرونز وصناديق التبريد وصيانتها", "التأمين والتصاريح والامتثال",
          "رواتب الفريق والطيارين", "الخوادم والاتصالات والتسويق"],
    rev=["اشتراك سنوي للمستشفى: 6,000 د.أ", "رسوم رحلة طارئة بالدرون: 90 د.أ", "عقد اللوحة الوطنية: 40,000 د.أ سنويًا",
         "رعاية مؤسسية لتطبيق المتبرعين: 10,000 د.أ سنويًا"],
)

BMC_CSS = """
.bmcg { display:grid; gap:2mm; grid-template-columns:repeat(10,minmax(0,1fr)); grid-auto-rows:minmax(0,auto);
  grid-template-areas:"kp kp ka ka vp vp cr cr cs cs" "kp kp kr kr vp vp ch ch cs cs" "cost cost cost cost cost rev rev rev rev rev"; }
.bmcg .blk { border:1.5px solid #E7E5E4; border-radius:2.5mm; padding:2mm 3mm; background:#fff }
.bmcg h4 { margin:0 0 1mm; font-size:1.08em; color:#1C1917; border-bottom:1px solid #F5F5F4; padding-bottom:1mm }
.bmcg h4 small { display:block; font-size:.72em; color:#A8A29E; direction:ltr; text-align:right; font-weight:600 }
.bmcg ul { margin:0; padding-right:4mm } .bmcg li { margin:.5mm 0; line-height:1.4 }
.b-kp{grid-area:kp}.b-ka{grid-area:ka}.b-kr{grid-area:kr}.b-cr{grid-area:cr}.b-ch{grid-area:ch}
.b-vp{grid-area:vp;background:#FEF2F2!important;border-color:#F87171!important}.b-cs{grid-area:cs;background:#F0FDFA!important;border-color:#2DD4BF!important}
.b-cost{grid-area:cost;background:#FAFAF9!important}.b-rev{grid-area:rev;background:#FFFBEB!important;border-color:#FBBF24!important}
"""


def capex_table():
    rows = "".join(f"<tr><td>{e(n)}</td><td class='n'>{q}</td><td class='n'>{money(c)}</td><td class='n'>{money(q * c)}</td></tr>" for n, q, c in BOM)
    total = sum(q * c for _, q, c in BOM)
    return f"<table><tr><th>البند</th><th class='n'>الكمية</th><th class='n'>الكلفة التقديرية</th><th class='n'>المجموع</th></tr>{rows}<tr class='hl'><td>المجموع</td><td></td><td></td><td class='n'>{money(total)}</td></tr></table>"


def pl_table():
    rows = [("الإيرادات", M["rev"]), ("الكلفة المباشرة", M["cogs"]), ("الربح الإجمالي", M["gross"]),
            ("المصاريف التشغيلية", M["opex"]), ("صافي الربح التشغيلي", M["ebitda"]), ("النقد التراكمي بعد الاستثمار", M["cum"])]
    body = "".join(f"<tr{' class=\"hl\"' if i >= 4 else ''}><td>{e(n)}</td>" + "".join(f"<td class='n'>{money(x)}</td>" for x in v) + "</tr>"
                   for i, (n, v) in enumerate(rows))
    return f"<table><tr><th>البند</th><th class='n'>السنة 1</th><th class='n'>السنة 2</th><th class='n'>السنة 3</th></tr>{body}</table>"


def streams_table():
    rows = "".join(
        f"<tr><td>{e(n)}</td><td>{e(u)}</td><td class='n'>{price(pr)}</td>" + "".join(f"<td class='n'>{x:,}</td>" for x in units)
        + f"<td class='n'>{money(pr * units[2])}</td></tr>" for n, u, pr, units, _ in P["fin"]["streams"])
    return f"<table><tr><th>المصدر</th><th>الوحدة</th><th class='n'>السعر</th><th class='n'>س1</th><th class='n'>س2</th><th class='n'>س3</th><th class='n'>إيراد س3</th></tr>{rows}</table>"


def scenario_table():
    rows = ""
    for name, vol, op in SCENARIOS:
        s = model(P, volume=vol, opex_mult=op)
        rows += f"<tr><td>{e(name)}</td><td class='n'>×{vol}</td><td class='n'>×{op}</td><td class='n'>{money(s['rev'][2])}</td><td class='n'>{money(s['ebitda'][2])}</td><td class='n'>{money(s['funding'])}</td><td>{breakeven_text(s['breakeven'])}</td></tr>"
    grant = model(P, capex_mult=(M["capex"] - 30000) / M["capex"])
    rows += (f"<tr class='hl'><td>أساسي + منحة للأسطول التجريبي</td><td class='n'>×1</td><td class='n'>×1</td><td class='n'>{money(grant['rev'][2])}</td>"
             f"<td class='n'>{money(grant['ebitda'][2])}</td><td class='n'>{money(grant['funding'])}</td><td>{breakeven_text(grant['breakeven'])}</td></tr>")
    return f"<table><tr><th>السيناريو</th><th class='n'>الكميات</th><th class='n'>التكاليف</th><th class='n'>إيراد س3</th><th class='n'>نتيجة س3</th><th class='n'>التمويل المطلوب</th><th>التعادل</th></tr>{rows}</table>"


def sensitivity_table():
    rows = ""
    for label, kw in [("السعر −20%", dict(price_mult=.8)), ("السعر +20%", dict(price_mult=1.2)), ("الكميات −20%", dict(volume=.8)),
                      ("الكميات +20%", dict(volume=1.2)), ("التكاليف +20%", dict(opex_mult=1.2)), ("التكاليف −20%", dict(opex_mult=.8))]:
        s = model(P, **kw)
        rows += f"<tr><td>{e(label)}</td><td class='n'>{money(s['ebitda'][2])}</td><td class='n'>{money(s['cum'][2])}</td><td>{breakeven_text(s['breakeven'])}</td></tr>"
    return f"<table><tr><th>التغيير</th><th class='n'>نتيجة س3</th><th class='n'>النقد التراكمي س3</th><th>التعادل</th></tr>{rows}</table>"


def unit_economics():
    fl = P["fin"]["streams"][1]
    direct = fl[2] * fl[4]
    sub = P["fin"]["streams"][0]
    return f"""<table><tr><th>المؤشر</th><th class='n'>القيمة</th></tr>
<tr><td>سعر رحلة الطوارئ</td><td class='n'>{price(fl[2])}</td></tr>
<tr><td>الكلفة المباشرة للرحلة (بطارية، صيانة، وقت الطيار، تأمين)</td><td class='n'>{price(direct)}</td></tr>
<tr><td>هامش المساهمة لكل رحلة</td><td class='n'>{price(fl[2] - direct)} ({(1 - fl[4]) * 100:.0f}%)</td></tr>
<tr><td>اشتراك المستشفى السنوي / الكلفة المباشرة</td><td class='n'>{price(sub[2])} / {price(sub[2] * sub[4])}</td></tr>
<tr><td>رحلات السنة 3 (افتراض)</td><td class='n'>{fl[3][2]:,} رحلة ≈ {fl[3][2] / 365:.1f} يوميًا</td></tr></table>"""


def team_table():
    return "<table>" + "".join(f"<tr><td><b>{e(r)}</b></td><td>{e(d)}</td></tr>" for r, d in TEAM) + "</table>"


def risks_table():
    return "<table><tr><th>الخطر</th><th>طريقة التعامل</th></tr>" + "".join(f"<tr><td>{e(r)}</td><td>{e(m)}</td></tr>" for r, m in P["risks"]) + "</table>"


def gtm_table():
    return "<table>" + "".join(f"<tr><td style='white-space:nowrap'><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in GTM) + "</table>"


def comp_table():
    return ("<table><tr><th>البديل</th><th>ماذا يقدم</th><th>أين يقصر</th></tr>"
            + "".join(f"<tr{' class=\"hl\"' if i == 3 else ''}><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for i, (a, b, c) in enumerate(COMPETITION)) + "</table>")


def screens_html(names=None, cols=1):
    items = [s for s in APP_SCREENS if names is None or s[0] in names]
    return "".join(f'<div class="avoid"><div class="shot"><img src="{img64(k)}"></div><div class="cap"><b>{e(t)}:</b> {e(d)}</div></div>' for k, t, d in items)


DISC = ("الأرقام المالية افتراضات تخطيطية أولية وضعها الفريق وليست أبحاث سوق أو عروض أسعار، ويجب التحقق منها قبل أي قرار. "
        "عبارة «غير موجود في الأردن» تعني عدم العثور على مثيل في بحث مبدئي. المحاكي يستخدم بيانات ومواقع تخطيطية.")
ASK = [f"تمويل تأسيسي بنحو {money(round(M['funding'], -2))} يغطي الاستثمار الأولي وفترة النمو، ويمكن فصل الأسطول التجريبي (30,000 د.أ) كمنحة صحية.",
       "شراكة تجريبية مع بنك دم ومستشفى خاص لربط المخزون الحقيقي.",
       "دعم في مسار التصاريح مع هيئة تنظيم الطيران المدني والجهات الأمنية.",
       "إرشاد في القطاع الصحي وريادة الأعمال."]


# ---------------------------------------------------------------- documents

def proposal():
    body = cover("المقترح الكامل · Project Proposal", ONE_LINER) + f"""
<h2><span class="n">1</span> الملخص التنفيذي</h2>
<p><b>{NAME_AR}</b> {e(ONE_LINER)}</p>{kpis()}
<p>النموذج الأولي جاهز الآن كمحاكي تفاعلي كامل. نبدأ بالبرمجيات في المستشفيات الخاصة لتوليد دخل مبكر، ثم نشغّل مسار درون تجريبي معتمد بعد الحصول على التصاريح.</p>
<h2><span class="n">2</span> المشكلة</h2><p>{e(P['problem'])}</p>{facts_html()}{ul(P['evidence'])}
<h2><span class="n">3</span> الحل: ثلاث طبقات في منصة واحدة</h2><p>{e(P['solution'])}</p>{layers_html()}
<div class="brk"></div>
<h2><span class="n">4</span> مهمة الدرون: من بنك الدم إلى المستشفى</h2>{mission_svg()}{mission_html()}
<div class="avoid"><h3>مواصفات الدرون والصندوق المبرّد (للنموذج التجريبي)</h3><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in DRONE_SPEC)}</table></div>
<div class="dark avoid" style="margin-top:3mm"><b>⚡ العرض الحي أمام اللجنة:</b> {e(P['wow'])}</div>
<div class="brk"></div>
<h2><span class="n">5</span> التطبيق: شاشات النموذج الأولي</h2>{screens_html(['dash', 'sos'])}
<div class="brk"></div>{screens_html(['forecast', 'donors', 'mci'])}
<div class="brk"></div>
<h2><span class="n">6</span> الذكاء الاصطناعي والبيانات</h2>{ul(P['ai'])}<p><b>البيانات:</b> {e('، '.join(P['data']))}</p>
<h2><span class="n">7</span> السوق والمنافسة</h2><p>{e(P['market'])}</p>{comp_table()}
<div class="brk"></div><h2><span class="n">8</span> نموذج العمل التجاري (Business Model Canvas)</h2>{bmc_grid('9pt')}
<div class="brk"></div>
<h2><span class="n">9</span> الجدوى المالية</h2>{kpis()}{pl_table()}
<div class="avoid">{cash_chart(M, 640, 170)}{CHART_LEGEND}</div>
<div class="avoid"><h3>السيناريوهات ومسار الربحية</h3>{scenario_table()}</div>
<div class="verdict avoid" style="background:#7F1D1D;margin-top:2mm">بالافتراضات الأساسية لا يتعادل المشروع خلال 3 سنوات لأن الدرونز والترخيص استثمار مبكر؛ لكن نتيجة السنة الثالثة موجبة ({money(M['ebitda'][2])})، ويتعادل في الشهر {model(P, volume=1.4, opex_mult=.95)['breakeven']} في السيناريو المتفائل. تمويل الأسطول بمنحة يخفض المخاطر.</div>
<div class="brk"></div>
<h2><span class="n">10</span> خطة الدخول للسوق</h2>{gtm_table()}
<div class="avoid"><h2><span class="n">11</span> النموذج الأولي خلال 12 أسبوعًا</h2><table><tr><th>الأسابيع</th><th>المخرجات</th></tr>{''.join(f'<tr><td>{e(w)}</td><td>{e(t)}</td></tr>' for w, t in P['mvp'])}</table></div>
<div class="avoid"><h2><span class="n">12</span> المخاطر والإطار التنظيمي</h2>{risks_table()}<p>{e(P['legal'])}</p></div>
<div class="avoid"><h2><span class="n">13</span> مؤشرات قياس الأثر</h2>{ul(P['impact'])}</div>
<div class="avoid"><h2><span class="n">14</span> الانسجام مع الأولويات الوطنية</h2>{ul(['يدعم جاهزية القطاع الصحي للطوارئ والحوادث الكبرى.', 'يتوافق مع التحول الرقمي في الخدمات الصحية وحماية البيانات.', 'يقلل الهدر في مورد صحي نادر ويحسّن العدالة في الوصول إليه بين المحافظات.', 'يبني خبرة أردنية في الطائرات المسيّرة الطبية قابلة للتصدير إقليميًا.'])}</div>
<div class="avoid"><h2><span class="n">15</span> الفريق</h2>{team_table()}</div>
<div class="avoid"><h2><span class="n">16</span> ما نحتاجه (The Ask)</h2>{ul(ASK)}</div>
<p class="note">{e(DISC)}</p>"""
    return print_pdf(page("DAMI — Proposal", body, DOC_CSS + BMC_CSS), DIR / "01_DAMI_Proposal.pdf")


def bmc_pdf():
    css = THEME + BMC_CSS + """
@page { size:A4 landscape; margin:0 } body { font-size:9pt }
.sheet { height:209mm; padding:8mm 10mm; display:flex; flex-direction:column; break-after:page }
.hdr { display:flex; align-items:center; gap:4mm; background:linear-gradient(120deg,#450A0A,#B91C1C); color:#fff; border-radius:3mm; padding:3mm 5mm; margin-bottom:2.5mm }
.hdr h1 { font-size:22pt; font-weight:900 } .hdr p { margin:0; opacity:.9 } .hdr .kk { margin-right:auto; display:flex; gap:2mm }
.hdr .kk div { background:#ffffff22; border-radius:2mm; padding:1mm 3mm; font-size:8pt; text-align:center } .hdr .kk b { display:block; font-size:10pt }
.bmcg { flex:1; grid-template-rows:1fr 1fr .7fr }
"""
    hdr = f"""<div class="hdr"><div><h1>🩸 {NAME_AR} · {NAME_EN}</h1><p>Business Model Canvas — نموذج العمل التجاري · فريق NEXORA</p></div>
<div class="kk"><div>الاستثمار الأولي<b>{money(M['capex'])}</b></div><div>إيرادات س3<b>{money(M['rev'][2])}</b></div><div>الهامش الإجمالي س3<b>{M['margin'] * 100:.0f}%</b></div></div></div>"""
    detail = f"""<section class="sheet" style="display:block">{hdr.replace('Business Model Canvas — نموذج العمل التجاري', 'شرح نموذج العمل: كيف نخلق القيمة ونحصّلها')}
<div class="two"><div><h3>من يدفع ولماذا؟</h3>{ul(['المستشفى الخاص يدفع الاشتراك لأنه يقلل الهدر في الوحدات المنتهية ويضمن توفر الزمر النادرة.', 'المستشفى يدفع رسوم الرحلة الطارئة فقط عند الحاجة، وهي أقل من كلفة تأخر علاج مريض نازف.', 'وزارة الصحة تدفع عقد اللوحة الوطنية لجاهزية الطوارئ والحوادث الكبرى.', 'الشركات ترعى تطبيق المتبرعين ضمن المسؤولية المجتمعية وتظهر علامتها فيه.'])}
<h3>اقتصاديات الوحدة</h3>{unit_economics()}</div>
<div><h3>مصادر الإيرادات بالأرقام</h3>{streams_table()}<h3>مسار النمو</h3>{gtm_table()}</div></div>
<p class="note">{e(DISC)}</p></section>"""
    body = f'<section class="sheet">{hdr}{bmc_grid("9pt")}</section>{detail}'
    return print_pdf(page("DAMI — Business Model Canvas", body, css), DIR / "02_DAMI_Business_Model_Canvas.pdf")


def feasibility():
    opex_rows = "".join(f"<tr><td>{e(n)}</td>" + "".join(f"<td class='n'>{money(o * s)}</td>" for o in P['fin']['opex']) + "</tr>" for n, s in OPEX_SPLIT)
    body = cover("دراسة الجدوى · Feasibility Study", "دراسة جدوى مبدئية: السوق، والجدوى الفنية والتشغيلية، والقانونية، والمالية لثلاث سنوات، مع السيناريوهات والحساسية والتوصية.") + f"""
<h2><span class="n">1</span> ملخص النتائج</h2>{kpis()}
<table><tr><th>الجانب</th><th>التقييم</th><th>السبب</th></tr>
<tr><td>السوق</td><td>✅ مرتفع</td><td>حاجة صحية حرجة، وزبون واضح (المستشفيات وبنك الدم)، ولا منافس مباشر محليًا حسب بحثنا المبدئي.</td></tr>
<tr><td>الفني</td><td>✅ مرتفع</td><td>التقنيات ناضجة (تنبؤ، تحسين، درونز طبية مثبتة عالميًا)، والنموذج الأولي يعمل.</td></tr>
<tr><td>التشغيلي</td><td>⚠️ متوسط</td><td>يحتاج مركز عمليات وطيارين مرخّصين وإدارة سلسلة تبريد.</td></tr>
<tr><td>القانوني</td><td>⚠️ التحدي الأكبر</td><td>تصاريح الطيران والموافقات الأمنية وحماية البيانات الصحية.</td></tr>
<tr><td>المالي</td><td>⚠️ طويل المدى</td><td>نتيجة السنة 3 موجبة، والتعادل بعد السنة الثالثة بالأساسي، والشهر {model(P, volume=1.4, opex_mult=.95)['breakeven']} بالمتفائل.</td></tr></table>
<h2><span class="n">2</span> دراسة السوق</h2><p>{e(P['problem'])}</p>{facts_html()}
<h3>الشرائح المستهدفة</h3>{ul(BMC['cs'])}<h3>افتراضات النمو</h3><p>{e(P['market'])}</p>
<h3>المنافسة والبدائل</h3>{comp_table()}
<div class="brk"></div>
<h2><span class="n">3</span> الجدوى الفنية</h2>{layers_html()}
<h3>التقنيات المستخدمة</h3><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in STACK)}</table>
<h3>مواصفات الدرون والتبريد</h3><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in DRONE_SPEC)}</table>
<h2><span class="n">4</span> الجدوى التشغيلية</h2>{mission_html()}
{ul(['مركز عمليات صغير يعمل على مدار الساعة بمشغّل وطيار مرخّص في كل وردية.', 'صيانة دورية للدرونز وفحص الصناديق ومعايرة حساسات الحرارة شهريًا.', 'إجراءات احتياطية: إذا تعذّر الطيران (طقس، عطل) يتحول الطلب تلقائيًا للنقل البري مع أقرب مصدر.', 'تدريب كوادر بنوك الدم على تعبئة الصناديق واستلام الشحنات.'])}
<div class="brk"></div>
<h2><span class="n">5</span> الجدوى القانونية والتنظيمية</h2><table><tr><th>الجهة / المتطلب</th><th>ما نحتاجه</th></tr>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in LICENSES)}</table>
<h2><span class="n">6</span> الجدوى المالية</h2>
<div class="two"><div class="avoid"><h3>الاستثمار الأولي (CAPEX)</h3>{capex_table()}</div>
<div class="avoid"><h3>المصاريف التشغيلية (OPEX)</h3><table><tr><th>البند</th><th class='n'>س1</th><th class='n'>س2</th><th class='n'>س3</th></tr>{opex_rows}<tr class='hl'><td>المجموع</td>{''.join(f"<td class='n'>{money(o)}</td>" for o in P['fin']['opex'])}</tr></table></div></div>
<div class="avoid"><h3>مصادر الإيرادات</h3>{streams_table()}</div>
<div class="avoid"><h3>قائمة الدخل المتوقعة</h3>{pl_table()}</div>
<div class="brk"></div>
<div class="avoid"><h3>التدفق النقدي لـ 36 شهرًا</h3>{cash_chart(M, 640, 190)}{CHART_LEGEND}</div>
<div class="two"><div class="avoid"><h3>اقتصاديات الوحدة</h3>{unit_economics()}</div><div class="avoid"><h3>تحليل الحساسية</h3>{sensitivity_table()}</div></div>
<div class="avoid"><h3>السيناريوهات</h3>{scenario_table()}</div>
<h2><span class="n">7</span> المخاطر</h2>{risks_table()}
<div class="avoid"><h2><span class="n">8</span> التوصية</h2>
<div class="verdict" style="background:#7F1D1D">المشروع مجدٍ فنيًا وذو أثر صحي مرتفع، وجدواه المالية طويلة المدى. التوصية: المضي على مراحل؛ البرمجيات أولًا لتوليد دخل مبكر، وتمويل الأسطول التجريبي بمنحة أو شريك صحي، وعدم إطلاق الرحلات التجارية قبل اكتمال التصاريح.</div>
<h3>خطة التحقق من الافتراضات</h3>{ul(['مقابلات مع 10–15 مديرًا لبنوك دم ومستشفيات خاصة للتحقق من الاستعداد لدفع 6,000 د.أ سنويًا.', 'جمع بيانات فعلية عن نسب الهدر بسبب انتهاء الصلاحية وأزمنة النقل الطارئ الحالية.', 'طلب عروض أسعار حقيقية لدرونين وصناديق تبريد معتمدة.', 'اجتماع تمهيدي مع هيئة تنظيم الطيران المدني لفهم مسار التصريح التجريبي.'])}</div>
<p class="note">{e(DISC)}</p>"""
    return print_pdf(page("DAMI — Feasibility Study", body, DOC_CSS), DIR / "03_DAMI_Feasibility_Study.pdf")


def requirements():
    body = cover("المتطلبات والتجهيزات · Requirements", "كل ما يحتاجه المشروع: المتطلبات الوظيفية وغير الوظيفية، والتجهيزات والكلفة، والتقنيات، والتصاريح، والشركاء، والفريق، وقائمة التسليم.") + f"""
<h2><span class="n">1</span> المتطلبات الوظيفية (Functional Requirements)</h2>
<table><tr><th>الرمز</th><th>المتطلب</th></tr>{''.join(f'<tr><td><b>{a}</b></td><td>{e(b)}</td></tr>' for a, b in FR)}</table>
<h2><span class="n">2</span> المتطلبات غير الوظيفية</h2><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in NFR)}</table>
<div class="brk"></div>
<h2><span class="n">3</span> التجهيزات والكلفة التقديرية</h2>{capex_table()}
<h2><span class="n">4</span> مواصفات الدرون وصندوق التبريد</h2><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in DRONE_SPEC)}</table>
<h2><span class="n">5</span> التقنيات (Tech Stack)</h2><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in STACK)}</table>
<div class="brk"></div>
<h2><span class="n">6</span> البيانات المطلوبة</h2>{ul(P['data'])}
<h2><span class="n">7</span> التصاريح والموافقات</h2><table><tr><th>الجهة</th><th>المطلوب</th></tr>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in LICENSES)}</table>
<h2><span class="n">8</span> الشركاء المطلوبون</h2>{ul(BMC['kp'])}
<h2><span class="n">9</span> الفريق والأدوار</h2>{team_table()}
<div class="avoid"><h2><span class="n">10</span> قائمة التسليم والعرض</h2><ul class="check">{''.join(f'<li>{e(x)}</li>' for x in SUBMISSION)}</ul></div>
<div class="avoid"><h2><span class="n">11</span> تجهيزات يوم العرض</h2><ul class="check">{''.join(f'<li>{e(x)}</li>' for x in ['لابتوب مشحون مع المحاكي مفتوحًا مسبقًا (يعمل بدون إنترنت)', 'نسخة PDF من العرض على فلاشة احتياطية', 'تجربة السيناريو الحي 3 مرات قبل الدخول', 'توزيع الأدوار: من يتكلم ومن يشغّل المحاكي', 'نسخ مطبوعة من BMC والملخص للجنة', 'ساعة توقيت للالتزام بـ 5 دقائق'])}</ul></div>
<p class="note">{e(DISC)}</p>"""
    return print_pdf(page("DAMI — Requirements", body, DOC_CSS), DIR / "04_DAMI_Requirements.pdf")


def script():
    body = cover("نص العرض وأسئلة اللجنة · Pitch Script & Q&A", "نص عرض مدته 5 دقائق مقسّم بالثواني، وخطوات العرض الحي، وأهم الأسئلة المتوقعة من لجنة التحكيم مع إجابات مقترحة.") + f"""
<h2><span class="n">1</span> نص العرض (5 دقائق)</h2>
<table><tr><th>الوقت</th><th>المقطع</th><th>ماذا نقول / نفعل</th></tr>{''.join(f'<tr><td class="n" style="white-space:nowrap">{e(t)}</td><td><b>{e(s)}</b></td><td>{e(x)}</td></tr>' for t, s, x in SCRIPT)}</table>
<div class="dark avoid" style="margin-top:3mm"><b>نصائح للعرض:</b> ابدأ بالقصة لا بالتقنية. شغّل المحاكي قبل دخولك. اذكر التحدي القانوني بنفسك قبل أن تسأله اللجنة. اختم بجملة واحدة قوية.</div>
<div class="brk"></div>
<h2><span class="n">2</span> أسئلة اللجنة المتوقعة</h2>
{''.join(f'<div class="avoid" style="margin-bottom:2.5mm"><h3>س: {e(q)}</h3><p style="margin:0">ج: {e(a)}</p></div>' for q, a in QA)}
<p class="note">{e(DISC)}</p>"""
    return print_pdf(page("DAMI — Pitch Script", body, DOC_CSS), DIR / "06_DAMI_Pitch_Script_QA.pdf")


# ---------------------------------------------------------------- deck

DECK_CSS = THEME + BMC_CSS + """
@page { size:338.67mm 190.5mm; margin:0 } body { font-size:13pt }
.s { width:338.67mm; height:190.5mm; padding:13mm 17mm; break-after:page; position:relative; overflow:hidden; background:#fff }
.s.cover { padding:16mm 20mm; color:#fff; background:radial-gradient(circle at 15% 20%,#DC262655,transparent 45%),linear-gradient(155deg,#2A0606,#7F1D1D 55%,#B91C1C) } .s h1 { font-size:72pt; font-weight:900; line-height:1 }
.s h2 { font-size:28pt; margin:0 0 5mm; color:var(--rd) } .s.cover h2 { color:#fff }
.lead { font-size:17pt; font-weight:700; color:#44403C } .cover .lead { color:#fff }
.foot { position:absolute; bottom:6mm; left:17mm; font-size:9pt; color:#A8A29E; letter-spacing:.3em }
.pg { position:absolute; bottom:6mm; right:17mm; font-size:9pt; color:#A8A29E }
.big4 { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:5mm; margin-top:6mm }
.big4 div { background:var(--rs); border-radius:4mm; padding:6mm; font-size:12pt } .big4 b { display:block; font-size:26pt; color:var(--r); font-weight:900 }
.s .lay div { font-size:12pt; padding:6mm } .s .lay b { font-size:17pt; margin:2mm 0 } .s .lay i { font-size:34pt }
.s .steps div { font-size:11pt; padding:4mm } .s .steps b { font-size:13pt }
.split { display:grid; grid-template-columns:minmax(0,1.6fr) minmax(0,1fr); gap:7mm; align-items:start }
.s table { font-size:11.5pt } .s td { padding:1.8mm 2.5mm }
.kk { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:4mm } .kk div { background:var(--rs); border-radius:3mm; padding:4mm; text-align:center; color:#57534E; font-size:11pt }
.kk b { display:block; font-size:20pt; color:var(--rd) }
"""


def deck_html():
    sl = []

    def s(inner, cls=""):
        sl.append(f'<section class="s {cls}">{inner}<div class="foot">NEXORA · DAMI</div><div class="pg">{len(sl) + 1}</div></section>')

    grant_be = model(P, volume=1.4, opex_mult=.95)["breakeven"]
    s(f"""<div class="brand">NEXORA · JORDAN STUDENTS PITCH COMPETITION</div>
<div style="margin-top:22mm"><h1>🩸 {NAME_AR} <span style="font-size:.35em;letter-spacing:.3em;opacity:.85">{NAME_EN}</span></h1>
<p class="lead" style="font-size:22pt;max-width:250mm;margin-top:6mm">{e(SLOGAN)}</p></div>
<p style="position:absolute;bottom:16mm;right:20mm;font-weight:700;opacity:.9">لأن الدم الذي يصل متأخرًا… لا يصل.</p>""", "cover")
    s(f"""<h2>الساعة 5 مساءً… حادث على طريق المطار</h2>
<p class="lead">مستشفى يحتاج <b style="color:#B91C1C">6 وحدات O سالب</b> الآن. السيارة من بنك الدم تحتاج 34 دقيقة في الزحمة.<br>في النزيف الحاد، كل دقيقة تفرق.</p>{mission_svg(900, 200)}""")
    s(f"""<h2>المشكلة: نقص هنا… وهدر هناك</h2><p class="lead">{e(P['problem'])}</p>
<div class="big4">{''.join(f'<div><b>{e(a)}</b>{e(b)}</div>' for a, b in FACTS)}</div>""")
    s(f"""<h2>الحل: دَمي — ثلاث طبقات في منصة واحدة</h2>{layers_html()}
<p class="lead" style="margin-top:6mm;font-size:14pt">{e(ONE_LINER)}</p>""")
    s(f"""<h2>مهمة الدرون: من بنك الدم إلى المستشفى خلال دقائق</h2>{mission_html()}
<div class="two" style="margin-top:5mm;font-size:11pt"><table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in DRONE_SPEC[:4])}</table>
<table>{''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in DRONE_SPEC[4:])}</table></div>""")
    for key in ("sos", "dash", "mci"):
        k, t, d = next(x for x in APP_SCREENS if x[0] == key)
        s(f"""<h2>النموذج الأولي يعمل: {e(t)}</h2><div class="split"><div class="shot"><img src="{img64(k, 1600)}"></div>
<div><p class="lead" style="font-size:15pt">{e(d)}</p>{'<div class="dark" style="font-size:11.5pt">⚡ ' + e(P['wow']) + '</div>' if key == 'sos' else ''}</div></div>""")
    s(f"""<h2>الذكاء الاصطناعي داخل دَمي</h2><div class="two"><div><h3 style="font-size:15pt">النماذج</h3>{ul(P['ai'])}</div>
<div><h3 style="font-size:15pt">البيانات</h3>{ul(P['data'])}</div></div>
<div class="shot" style="margin-top:4mm;max-height:72mm"><img src="{img64('forecast', 1600)}"></div>""")
    s(f"""<h2>السوق والمنافسة</h2>{comp_table()}<p class="lead" style="font-size:14pt;margin-top:5mm">نبدأ بالمستشفيات الخاصة لأن قرارها أسرع، ثم وزارة الصحة وبنك الدم الوطني.</p>""")
    s(f"""<h2 style="margin-bottom:3mm">نموذج العمل التجاري</h2>{bmc_grid('8.2pt')}""")
    s(f"""<h2>الأرقام: كيف نربح</h2><div class="split"><div>{streams_table()}<div style="margin-top:4mm">{cash_chart(M, 640, 180)}{CHART_LEGEND}</div></div>
<div class="kk"><div>الاستثمار الأولي<b>{money(M['capex'])}</b></div><div>إيرادات س3<b>{money(M['rev'][2])}</b></div>
<div>الهامش الإجمالي س3<b>{M['margin'] * 100:.0f}%</b></div><div>صافي التشغيل س3<b>{money(M['ebitda'][2])}</b></div>
<div>التعادل (متفائل)<b>الشهر {grant_be}</b></div><div>هامش رحلة الدرون<b>55%</b></div></div></div>""")
    s(f"""<h2>الخطة: من المحاكي إلى أول رحلة مرخّصة</h2>{gtm_table()}
<div class="two" style="margin-top:5mm"><div><h3 style="font-size:15pt">المخاطر وكيف نتعامل معها</h3>{risks_table()}</div>
<div><h3 style="font-size:15pt">مؤشرات الأثر</h3>{ul(P['impact'])}</div></div>""")
    s(f"""<h2>الفريق وما نحتاجه</h2><div class="two"><div>{team_table()}</div><div><h3 style="font-size:15pt">The Ask</h3>{ul(ASK)}</div></div>""")
    s(f"""<div style="margin-top:30mm"><h1 style="font-size:58pt">لأن الدم الذي يصل متأخرًا… لا يصل.</h1>
<p class="lead" style="margin-top:8mm">🩸 دَمي · فريق NEXORA · شكرًا</p></div>""", "cover")
    return page("DAMI — Pitch Deck", "".join(sl), DECK_CSS, size="338.67mm 190.5mm")


def deck_pptx(path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    W, H = prs.slide_width, prs.slide_height
    red, dark, white, ink = RGBColor(0xB9, 0x1C, 0x1C), RGBColor(0x45, 0x0A, 0x0A), RGBColor(255, 255, 255), RGBColor(0x29, 0x25, 0x24)
    blank = prs.slide_layouts[6]
    cm = 360000

    def text(sl, x, y, w, h, lines, size=16, color=ink, bold=False):
        tf = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)).text_frame
        tf.word_wrap = True
        for i, line in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = PP_ALIGN.RIGHT
            para._pPr.set("rtl", "1")
            b = bold or line.startswith("■")
            run = para.add_run()
            run.text = line.lstrip("■ ")
            run.font.size, run.font.bold, run.font.name = Pt(size), b, "Cairo"
            run.font.color.rgb = color

    def new(title=None, bg=None):
        sl = prs.slides.add_slide(blank)
        if bg:
            sl.background.fill.solid()
            sl.background.fill.fore_color.rgb = bg
        else:
            bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, W - Emu(cm // 2), 0, Emu(cm // 2), H)
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

    full = W - 2 * cm
    sl = new(bg=dark)
    text(sl, cm, 4 * cm, full, 3 * cm, [f"🩸 {NAME_AR} · {NAME_EN}"], 60, white, True)
    text(sl, cm, 7.5 * cm, full, 3 * cm, [SLOGAN, "", "فريق NEXORA · Jordan Students Pitch Competition"], 20, RGBColor(0xFE, 0xCA, 0xCA))
    sl = new("الساعة 5 مساءً… حادث على طريق المطار")
    text(sl, cm, 3 * cm, full, 8 * cm, ["مستشفى يحتاج 6 وحدات O سالب الآن.", "السيارة من بنك الدم: 34 دقيقة في الزحمة.", "الدرون: 9 دقائق، والصندوق ثابت على 4°م.", "", "في النزيف الحاد، كل دقيقة تفرق."], 24)
    sl = new("المشكلة: نقص هنا… وهدر هناك")
    text(sl, cm, 2.5 * cm, full, 5 * cm, [P["problem"]], 16)
    text(sl, cm, 8 * cm, full, 8 * cm, [f"■ {a}: {b}" for a, b in FACTS], 16)
    sl = new("الحل: ثلاث طبقات في منصة واحدة")
    text(sl, cm, 2.5 * cm, full, 14 * cm, sum(([f"■ {i} {t}", d, ""] for i, t, d in LAYERS), []), 17)
    sl = new("مهمة الدرون: من بنك الدم إلى المستشفى")
    text(sl, int(W / 2), 2.5 * cm, int(W / 2) - cm, 14 * cm, [f"■ {k + 1}. {t}" if j == 0 else d for k, (t, d) in enumerate(MISSION) for j in (0, 1)], 14)
    text(sl, cm, 2.5 * cm, int(W / 2) - 2 * cm, 14 * cm, [f"■ {a}: {b}" for a, b in DRONE_SPEC], 12)
    for key in ("sos", "dash", "mci", "forecast"):
        _, t, d = next(x for x in APP_SCREENS if x[0] == key)
        sl = new(f"النموذج الأولي يعمل: {t}")
        pic(sl, key, cm, int(2.4 * cm), int(W * .62))
        text(sl, int(W * .62) + int(1.5 * cm), int(2.6 * cm), int(W * .38) - int(2.5 * cm), 12 * cm, [d], 16)
    sl = new("السوق والمنافسة")
    text(sl, cm, 2.5 * cm, full, 14 * cm, sum(([f"■ {a}", f"يقدّم: {b}", f"يقصر: {c}", ""] for a, b, c in COMPETITION), []), 14)
    sl = new("نموذج العمل التجاري (BMC)")
    col = full // 3
    for i, (k, ar, en) in enumerate(BMC_BLOCKS):
        x = cm + (2 - i % 3) * col
        y = int(2.3 * cm) + (i // 3) * int(5.2 * cm)
        text(sl, x, y, col - cm // 3, int(5 * cm), [f"■ {ar} · {en}", *BMC[k]], 10.5)
    sl = new("الأرقام: كيف نربح")
    text(sl, cm, 2.5 * cm, full, 14 * cm,
         [f"■ {n}: {price(pr)} لكل {u} — الكميات {units[0]:,} / {units[1]:,} / {units[2]:,}" for n, u, pr, units, _ in P["fin"]["streams"]]
         + ["", f"الاستثمار الأولي: {money(M['capex'])}", f"إيرادات السنة 3: {money(M['rev'][2])}", f"صافي التشغيل س3: {money(M['ebitda'][2])}",
            f"الهامش الإجمالي س3: {M['margin'] * 100:.0f}%", f"التعادل: بعد السنة الثالثة (أساسي) · الشهر {model(P, volume=1.4, opex_mult=.95)['breakeven']} (متفائل)"], 16)
    sl = new("الخطة والمخاطر")
    text(sl, cm, 2.5 * cm, full, 14 * cm, [f"■ {a}: {b}" for a, b in GTM] + [""] + [f"■ {r}: {m}" for r, m in P["risks"]], 14)
    sl = new("الفريق وما نحتاجه")
    text(sl, int(W / 2), 2.5 * cm, int(W / 2) - cm, 14 * cm, [f"■ {r}" if j == 0 else d for r, d in TEAM for j in (0, 1)], 13)
    text(sl, cm, 2.5 * cm, int(W / 2) - 2 * cm, 14 * cm, ["■ The Ask", *ASK], 14)
    sl = new(bg=dark)
    text(sl, cm, 5 * cm, full, 6 * cm, ["لأن الدم الذي يصل متأخرًا… لا يصل.", "", "🩸 دَمي · فريق NEXORA · شكرًا"], 36, white, True)
    prs.save(path)
    return path


def build():
    if DIR.exists():
        shutil.rmtree(DIR)
    SHOTS.mkdir(parents=True)
    build_sim.build()
    app = DIR / "07_DAMI_App.html"
    shutil.copy(OUT / "simulators" / "dami.html", app)
    subprocess.run(["node", str(HERE / "screens.js"), str(app), str(SHOTS)], check=True, cwd="/tmp")
    out = [proposal(), bmc_pdf(), feasibility(), requirements(), print_pdf(deck_html(), DIR / "05_DAMI_Pitch_Deck.pdf"),
           deck_pptx(DIR / "05_DAMI_Pitch_Deck.pptx"), script(), app]
    return out


if __name__ == "__main__":
    for f in build():
        print(f)
