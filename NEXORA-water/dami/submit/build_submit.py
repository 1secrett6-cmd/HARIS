"""Competition submission files: visual pitch deck + BMC, Arabic & English, as PDF and PPTX."""

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
from pptx import Presentation  # noqa: E402
from pptx.util import Emu  # noqa: E402

import art  # noqa: E402
import extra  # noqa: E402
from common import OUT, font_css  # noqa: E402

DEST = OUT / "SUBMISSION"
SHOTS = {"ar": OUT / "DAMI" / "screens", "en": OUT / "DAMI_EN" / "screens"}

TXT = {
"ar": dict(
    dir="rtl", name="دَمي", slogan="الدم يصل… قبل أن يفوت الوقت",
    sub="منصة ذكاء اصطناعي ودرونز طبية لإدارة الدم ونقله في الطوارئ", team="فريق NEXORA · الذكاء الاصطناعي وعلم البيانات",
    s2t="30–40%", s2a="من وفيات الإصابات سببها النزيف", s2b="وكل دقيقة تأخير في وصول الدم ترفع الخطر",
    s2src="المصدر: Kauvar et al., Journal of Trauma, 2006",
    s3t="نقص هنا… وهدر هناك", s3a="مستشفى ينتظر O− ولا يجد", s3b="ووحدات تنتهي صلاحيتها في مستشفى آخر",
    s3c=[("5–7 أيام", "صلاحية الصفائح فقط"), ("الزحمة", "تؤخر النقل الطارئ"), ("حملات عامة", "لا تستهدف الزمرة الناقصة")],
    s4t="الحل: دَمي", s4=[("brain", "يتنبأ ويوازن", "قبل النقص وقبل الهدر"), ("people", "يستدعي المتبرع", "المناسب والأقرب"), ("drone", "درون إسعاف الدم", "خلال دقائق")],
    s5t="كيف يعمل النظام؟", s5=[("حساسات بنك الدم", "حرارة + مخزون لحظي"), ("سحابة دَمي AI", "تنبؤ + أفضل مصدر"), ("تطبيق المستشفى", "طلب طارئ بضغطة"), ("درون مبرّدة", "GPS + حرارة حية")],
    s6t="درون إسعاف الدم", s6=[("thermo", "صندوق 2–6°م", "مراقبة حرارة كل ثانية"), ("bag", "4–6 وحدات", "في كل رحلة"), ("clock", "دقائق", "بدل نصف ساعة"), ("gps", "تتبع حي", "GPS ومسار آمن"), ("chute", "أمان", "مظلة وعودة تلقائية")],
    s7t="النموذج الأولي يعمل الآن", s7=["① يختار أفضل مصدر", "② يقارن الدرون بالسيارة", "③ ينبّه فورًا إذا ارتفعت الحرارة"],
    s8t="مثبتة عالميًا", s8a="67%", s8b="انخفاض في هدر الدم بعد التوصيل بالدرون في رواندا", s8c="79 دقيقة", s8d="أسرع في التوصيل",
    s8e="ولا يوجد نظام مشابه في الأردن حسب بحثنا المبدئي", s8src="المصدر: Nisingizwe et al., The Lancet Global Health, 2022",
    s9t="من يدفع؟", s9=[("🏥", "6,000 د.أ", "اشتراك سنوي للمستشفى"), ("🚁", "90 د.أ", "لكل رحلة طارئة"), ("🏛️", "40,000 د.أ", "عقد اللوحة الوطنية"), ("🤝", "10,000 د.أ", "رعاية تطبيق المتبرعين")],
    s9k="72% هامش إجمالي في السنة الثالثة",
    s10t="الخطة", s10=[("الآن", "نموذج أولي ✓"), ("6–12 شهرًا", "3 مستشفيات"), ("12–24 شهرًا", "أول مسار درون مرخّص"), ("24–36 شهرًا", "لوحة وطنية")],
    s11t="ما نطلبه", s11=[("money", "تمويل تأسيسي", "≈ 90,000 د.أ"), ("people", "شراكة تجريبية", "بنك دم + مستشفى"), ("drone", "دعم التصاريح", "هيئة تنظيم الطيران المدني")],
    s12a="لأن الدم الذي يصل متأخرًا…", s12b="لا يصل.",
    notes=["دَمي: منصة ذكاء اصطناعي ودرونز طبية توصل الدم قبل فوات الوقت.",
           "النزيف من أكبر أسباب الوفاة في الإصابات، وكل دقيقة تأخير مهمة.",
           "المشكلة مزدوجة: نقص في مستشفى، وهدر بانتهاء الصلاحية في مستشفى آخر.",
           "الحل ثلاث طبقات: تنبؤ وموازنة، واستدعاء متبرعين، ودرون إسعاف دم.",
           "حساسات في بنك الدم ترسل الحرارة والمخزون للسحابة، والذكاء الاصطناعي يختار أفضل مصدر، والمستشفى يطلب بضغطة، والدرون تطير بصندوق مراقَب.",
           "الدرون تحمل 4–6 وحدات في صندوق 2–6 درجات مع تتبع حي ومظلة أمان.",
           "هذا المحاكي يعمل الآن: نعرضه مباشرة أمام اللجنة.",
           "الفكرة مثبتة عالميًا: في رواندا انخفض الهدر 67% وأصبح التوصيل أسرع بـ 79 دقيقة.",
           "الدخل من اشتراكات المستشفيات ورسوم الرحلات والعقد الوطني والرعاة.",
           "نبدأ بالبرمجيات، ثم أول مسار درون مرخّص، ثم لوحة وطنية.",
           "نطلب تمويلًا تأسيسيًا وشراكة تجريبية ودعمًا في التصاريح.",
           "لأن الدم الذي يصل متأخرًا لا يصل. شكرًا."],
    bmc_t="نموذج العمل التجاري", kpi=[("الاستثمار الأولي", "58,000 د.أ"), ("إيرادات السنة 3", "325,000 د.أ"), ("الهامش الإجمالي س3", "72%")],
    bmc=dict(
        kp=("الشركاء الرئيسيون", "Key Partners", ["وزارة الصحة وبنك الدم الوطني", "المستشفيات الخاصة والحكومية", "مصنعو ومشغلو الدرونز الطبية", "هيئة تنظيم الطيران المدني", "الهلال الأحمر والرعاة"]),
        ka=("الأنشطة الرئيسية", "Key Activities", ["تطوير نماذج التنبؤ ومحرك التطابق", "تشغيل الدرونز ومركز الطوارئ", "مراقبة سلسلة التبريد", "استدعاء المتبرعين"]),
        kr=("الموارد الرئيسية", "Key Resources", ["منصة AI وبيانات المخزون", "رموز RFID لكل وحدة دم", "درونز وصناديق تبريد ذكية", "حساسات حرارة IoT", "فريق تقني وطيارون مرخّصون"]),
        vp=("القيمة المقدّمة", "Value Propositions", ["دم طارئ خلال دقائق لا نصف ساعة", "هدر أقل بموازنة المخزون", "رؤية وطنية لحظية للدم", "متبرع في الوقت المناسب"]),
        cr=("العلاقة مع العملاء", "Customer Relationships", ["عقد خدمة سنوي", "مركز طوارئ 24/7", "تقارير أثر شهرية"]),
        ch=("القنوات", "Channels", ["بيع مباشر للمستشفيات", "شراكة مع وزارة الصحة", "تطبيق جوال ولوحة ويب"]),
        cs=("شرائح العملاء", "Customer Segments", ["المستشفيات الخاصة (البداية)", "مستشفيات وزارة الصحة", "بنك الدم الوطني", "المتبرعون (مجانًا)"]),
        cost=("هيكل التكاليف", "Cost Structure", ["تطوير البرمجيات والذكاء الاصطناعي", "الدرونز والصيانة والتأمين", "التصاريح والامتثال", "رواتب الفريق والخوادم"]),
        rev=("مصادر الإيرادات", "Revenue Streams", ["اشتراك المستشفى: 6,000 د.أ/سنة", "رحلة درون طارئة: 90 د.أ", "عقد اللوحة الوطنية: 40,000 د.أ/سنة", "رعاية تطبيق المتبرعين: 10,000 د.أ/سنة"]),
    ),
    foot="الأرقام المالية افتراضات تخطيطية أولية للتحقق.",
),
"en": dict(
    dir="ltr", name="DAMI", slogan="Blood that arrives… before it's too late",
    sub="An AI platform and medical drones for managing and delivering blood in emergencies", team="Team NEXORA · AI & Data Science",
    s2t="30–40%", s2a="of trauma deaths are caused by bleeding", s2b="and every minute of delay raises the risk",
    s2src="Source: Kauvar et al., Journal of Trauma, 2006",
    s3t="Shortage here… waste there", s3a="One hospital needs O− and has none", s3b="while units expire at another",
    s3c=[("5–7 days", "platelet shelf life"), ("Traffic", "delays emergency transport"), ("Generic drives", "miss the missing type")],
    s4t="The solution: DAMI", s4=[("brain", "Forecast & balance", "before shortage or waste"), ("people", "Call the donor", "the right one, nearby"), ("drone", "Blood drone", "in minutes")],
    s5t="How the system works", s5=[("Blood-bank sensors", "temperature + live stock"), ("DAMI AI cloud", "forecast + best source"), ("Hospital app", "one-tap emergency"), ("Cooled drone", "GPS + live temperature")],
    s6t="The blood ambulance drone", s6=[("thermo", "2–6°C box", "temperature every second"), ("bag", "4–6 units", "per flight"), ("clock", "Minutes", "not half an hour"), ("gps", "Live tracking", "GPS, safe route"), ("chute", "Safety", "parachute, auto-return")],
    s7t="The prototype works today", s7=["① Picks the best source", "② Compares drone vs car", "③ Alarms instantly if temperature rises"],
    s8t="Proven worldwide", s8a="67%", s8b="drop in blood wastage after drone delivery in Rwanda", s8c="79 min", s8d="faster delivery",
    s8e="No similar system in Jordan per our preliminary research", s8src="Source: Nisingizwe et al., The Lancet Global Health, 2022",
    s9t="Who pays?", s9=[("🏥", "JOD 6,000", "hospital subscription / year"), ("🚁", "JOD 90", "per emergency flight"), ("🏛️", "JOD 40,000", "national dashboard / year"), ("🤝", "JOD 10,000", "donor-app sponsorship / year")],
    s9k="72% gross margin in year 3",
    s10t="The plan", s10=[("Now", "Prototype ✓"), ("6–12 months", "3 hospitals"), ("12–24 months", "First licensed drone route"), ("24–36 months", "National dashboard")],
    s11t="Our ask", s11=[("money", "Seed funding", "≈ JOD 90,000"), ("people", "Pilot partnership", "blood bank + hospital"), ("drone", "Permit support", "Civil Aviation Regulatory Commission")],
    s12a="Because blood that arrives late…", s12b="doesn't arrive.",
    notes=["DAMI: an AI platform and medical drones that get blood there before it's too late.",
           "Bleeding is a leading cause of trauma death, and every minute of delay matters.",
           "The problem is twofold: shortage at one hospital, expiry waste at another.",
           "Three layers: forecasting and balancing, donor call-up, and a blood ambulance drone.",
           "Blood-bank sensors stream temperature and stock to the cloud; AI picks the best source; the hospital requests in one tap; the drone flies with a monitored box.",
           "The drone carries 4–6 units in a 2–6°C box, with live tracking and a safety parachute.",
           "This simulator works today: we demo it live to the judges.",
           "It's proven: in Rwanda, wastage fell 67% and delivery got 79 minutes faster.",
           "Revenue comes from hospital subscriptions, flight fees, a national contract and sponsors.",
           "Software first, then the first licensed drone route, then a national dashboard.",
           "We ask for seed funding, a pilot partnership and permit support.",
           "Because blood that arrives late doesn't arrive. Thank you."],
    bmc_t="Business Model Canvas", kpi=[("Initial investment", "JOD 58,000"), ("Year-3 revenue", "JOD 325,000"), ("Year-3 gross margin", "72%")],
    bmc=dict(
        kp=("Key Partners", "", ["Ministry of Health & National Blood Bank", "Private & public hospitals", "Medical drone makers & operators", "Civil Aviation Regulatory Commission", "Red Crescent & sponsors"]),
        ka=("Key Activities", "", ["Forecasting models & matching engine", "Running drones & emergency center", "Cold-chain monitoring", "Donor call-ups"]),
        kr=("Key Resources", "", ["AI platform & stock data", "RFID tag on every blood unit", "Drones & smart cooling boxes", "IoT temperature sensors", "Tech team & licensed pilots"]),
        vp=("Value Propositions", "", ["Emergency blood in minutes, not half an hour", "Less waste through stock balancing", "Live national view of blood", "The right donor at the right time"]),
        cr=("Customer Relationships", "", ["Annual service contract", "24/7 emergency center", "Monthly impact reports"]),
        ch=("Channels", "", ["Direct sales to hospitals", "Ministry of Health partnership", "Mobile app & web dashboard"]),
        cs=("Customer Segments", "", ["Private hospitals (beachhead)", "Ministry of Health hospitals", "National Blood Bank", "Donors (free)"]),
        cost=("Cost Structure", "", ["Software & AI development", "Drones, maintenance & insurance", "Permits & compliance", "Team salaries & servers"]),
        rev=("Revenue Streams", "", ["Hospital subscription: JOD 6,000/yr", "Emergency drone flight: JOD 90", "National dashboard: JOD 40,000/yr", "Donor-app sponsorship: JOD 10,000/yr"]),
    ),
    foot="Financial figures are preliminary planning assumptions to be validated.",
),
}

CSS = """
* { box-sizing:border-box; margin:0; padding:0 }
body { font-family:'Cairo',sans-serif; color:#fff; background:#0C0306 }
.s { width:1920px; height:1080px; position:relative; overflow:hidden; page-break-after:always;
  background:radial-gradient(circle at 75% 30%,#4A0D14 0%,#16050A 55%,#0A0206 100%) }
.s::before { content:""; position:absolute; inset:0; background-image:linear-gradient(#ffffff07 1px,transparent 1px),linear-gradient(90deg,#ffffff07 1px,transparent 1px); background-size:80px 80px }
.light { background:linear-gradient(160deg,#FFF7F7,#FFFFFF 60%,#FEF2F2); color:#1C1917 } .light::before { display:none }
.abs { position:absolute } .row { display:flex; align-items:center }
.h { font-size:84px; font-weight:900; line-height:1.1 } .h2 { font-size:64px; font-weight:900 }
.big { font-size:260px; font-weight:900; line-height:1; color:#F87171; letter-spacing:-.02em; direction:ltr; unicode-bidi:isolate }
.l { font-size:44px; font-weight:700; line-height:1.35 } .m { font-size:34px; color:#FECACA } .light .m { color:#78716C }
.src { position:absolute; bottom:40px; font-size:20px; opacity:.6 }
.brand { position:absolute; top:44px; font-size:22px; letter-spacing:.45em; font-weight:900; opacity:.5 }
.pg { position:absolute; bottom:40px; font-size:22px; opacity:.45; font-weight:700 }
.card { background:#ffffff0f; border:2px solid #ffffff22; border-radius:36px; padding:44px 36px; text-align:center }
.card b { display:block; font-size:46px; margin-top:18px } .card span { font-size:30px; color:#FECACA }
.light .card { background:#fff; border-color:#FECACA; box-shadow:0 20px 60px #B91C1C14 } .light .card span { color:#78716C }
.chip { background:#ffffff10; border:2px solid #ffffff25; border-radius:24px; padding:22px 30px } .chip b { display:block; font-size:44px; color:#F87171 } .chip span { font-size:26px; color:#FECACA }
.red { color:#F87171 } .dk { color:#B91C1C }
.shot { border-radius:26px; overflow:hidden; box-shadow:0 40px 100px #000b, 0 0 0 3px #ffffff22 } .shot img { display:block; width:100% }
.call { background:#DC2626; border-radius:20px; padding:18px 30px; font-size:34px; font-weight:800; box-shadow:0 10px 40px #DC262666; margin-bottom:22px }
.tl { height:10px; border-radius:5px; background:linear-gradient(90deg,#B91C1C,#F87171) }
.dot { width:56px; height:56px; border-radius:50%; background:#DC2626; box-shadow:0 0 0 14px #DC262633 }
"""


def shot64(lang, name, width=1700):
    im = Image.open(SHOTS[lang] / f"{name}.png").convert("RGB")
    im.thumbnail((width, width))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def deck(lang):
    T = TXT[lang]
    rtl = T["dir"] == "rtl"
    start, end = ("right", "left") if rtl else ("left", "right")
    S, NOTES, orig = [], [], iter(T["notes"])

    def s(inner, cls="", note=None):
        NOTES.append(note if note is not None else next(orig))
        n = len(S) + 1
        S.append(f'<section class="s {cls}"><div class="brand" style="{start}:90px">NEXORA · DAMI</div>{inner}'
                 f'<div class="pg" style="{end}:90px">{n:02d}</div></section>')

    # 1 cover
    s(f"""<div class="abs" style="{end}:30px;top:200px">{art.drone(840)}</div>
<div class="abs" style="{start}:110px;top:230px;width:900px">
<div style="font-size:200px;font-weight:900;line-height:1">🩸 {T['name']}</div>
<div class="h2" style="margin-top:70px;line-height:1.3">{T['slogan']}</div>
<div class="m" style="margin-top:28px">{T['sub']}</div>
<div style="margin-top:60px;font-size:28px;font-weight:700;opacity:.8">{T['team']}</div></div>""")
    # 2 big stat
    s(f"""<div class="abs" style="{end}:220px;top:200px">{art.bag(380, .12)}</div>
<div class="abs" style="{start}:120px;top:220px;width:1100px"><div class="big">{T['s2t']}</div>
<div class="h" style="margin-top:20px">{T['s2a']}</div><div class="l red" style="margin-top:30px">{T['s2b']}</div></div>
<div class="src" style="{start}:120px">{T['s2src']}</div>""")
    # 3 shortage vs waste
    s(f"""<div class="abs h" style="left:0;right:0;top:90px;text-align:center">{T['s3t']}</div>
<div class="abs row" style="left:170px;right:170px;top:260px;justify-content:space-between">
 <div style="text-align:center;width:640px">{art.hospital(260, '#DC2626')}<div class="row" style="justify-content:center;gap:20px;margin-top:-30px">{art.bag(130, .02)}<span class="big" style="font-size:120px">0</span></div><div class="l" style="margin-top:10px">{T['s3a']}</div></div>
 <div style="text-align:center;width:640px">{art.hospital(260, '#F59E0B')}<div class="row" style="justify-content:center;gap:20px;margin-top:-30px">{art.bag(130, .9, '#F59E0B')}<span style="font-size:110px">⏳</span></div><div class="l" style="margin-top:10px">{T['s3b']}</div></div></div>
<div class="abs row" style="left:0;right:0;bottom:90px;justify-content:center;gap:30px">{''.join(f'<div class="chip"><b>{a}</b><span>{b}</span></div>' for a, b in T['s3c'])}</div>""")
    extra.causes(s, T, lang, rtl, start, end)
    # 4 solution
    s(f"""<div class="abs h" style="left:0;right:0;top:120px;text-align:center">{T['s4t']}</div>
<div class="abs" style="left:150px;right:150px;top:340px;display:grid;grid-template-columns:repeat(3,1fr);gap:50px">
{''.join(f'<div class="card"><div style="display:inline-flex;background:#DC2626;border-radius:50%;padding:30px">{art.icon(k, 150)}</div><b>{a}</b><span>{b}</span></div>' for k, a, b in T['s4'])}</div>""")
    # 5 system
    s(f"""<div class="abs h" style="left:0;right:0;top:110px;text-align:center">{T['s5t']}</div>
<div class="abs" style="left:110px;top:330px">{art.system(T['s5'], rtl=rtl)}</div>""")
    extra.modules(s, T, lang, rtl, start, end)
    extra.journey(s, T, lang, rtl, start, end)
    # 6 drone
    feats = "".join(f'<div class="row" style="gap:26px;margin-bottom:34px"><div style="background:#DC2626;border-radius:24px;padding:14px;display:flex">{art.icon(k, 80)}</div><div><div style="font-size:42px;font-weight:900">{a}</div><div class="m" style="font-size:28px">{b}</div></div></div>' for k, a, b in T['s6'])
    s(f"""<div class="abs h" style="{start}:110px;top:100px">{T['s6t']}</div>
<div class="abs" style="{end}:60px;top:220px">{art.drone(1050)}</div><div class="abs" style="{start}:120px;top:260px">{feats}</div>""")
    extra.coldchain(s, T, lang, rtl, start, end)
    extra.compat(s, T, lang, rtl, start, end)
    extra.donors(s, T, lang, rtl, start, end, shot64(lang, "donors", 1400))
    # 7 app
    s(f"""<div class="abs h" style="left:0;right:0;top:70px;text-align:center">{T['s7t']}</div>
<div class="abs shot" style="{start}:110px;top:230px;width:1180px"><img src="{shot64(lang, 'sos')}"></div>
<div class="abs" style="{end}:90px;top:330px;width:500px">{''.join(f'<div class="call">{x}</div>' for x in T['s7'])}</div>""")
    # 8 proof
    s(f"""<div class="abs h" style="left:0;right:0;top:100px;text-align:center">{T['s8t']}</div>
<div class="abs row" style="left:150px;right:150px;top:300px;justify-content:center;gap:80px">
<div class="card" style="width:720px"><div class="big" style="font-size:200px">{T['s8a']}</div><span style="font-size:36px">{T['s8b']}</span></div>
<div class="card" style="width:560px"><div class="big" style="font-size:150px;padding:25px 0">{T['s8c']}</div><span style="font-size:36px">{T['s8d']}</span></div></div>
<div class="abs l" style="left:0;right:0;top:830px;text-align:center">🇯🇴 {T['s8e']}</div>
<div class="src" style="{start}:120px">{T['s8src']}</div>""")
    # 9 who pays
    s(f"""<div class="abs h dk" style="left:0;right:0;top:100px;text-align:center">{T['s9t']}</div>
<div class="abs" style="left:130px;right:130px;top:300px;display:grid;grid-template-columns:repeat(4,1fr);gap:36px">
{''.join(f'<div class="card"><div style="font-size:100px">{i}</div><b class="dk" style="direction:ltr;unicode-bidi:isolate">{a}</b><span>{b}</span></div>' for i, a, b in T['s9'])}</div>
<div class="abs" style="left:0;right:0;top:880px;text-align:center"><span style="background:#B91C1C;color:#fff;border-radius:99px;padding:18px 50px;font-size:44px;font-weight:900">{T['s9k']}</span></div>""", "light")
    # 10 plan
    xs = [1640, 1173, 707, 240] if rtl else [240, 707, 1173, 1640]
    nodes = "".join(f'<div class="abs dot" style="left:{x - 28}px;top:532px"></div><div class="abs" style="left:{x - 220}px;width:440px;top:{300 if i % 2 == 0 else 640}px;text-align:center"><div style="font-size:44px;font-weight:900;color:#F87171">{a}</div><div class="l">{b}</div></div>' for i, ((a, b), x) in enumerate(zip(T['s10'], xs)))
    s(f"""<div class="abs h" style="left:0;right:0;top:110px;text-align:center">{T['s10t']}</div><div class="abs tl" style="left:240px;width:1400px;top:555px"></div>{nodes}""")
    # 11 ask
    s(f"""<div class="abs h" style="left:0;right:0;top:120px;text-align:center">{T['s11t']}</div>
<div class="abs" style="left:150px;right:150px;top:340px;display:grid;grid-template-columns:repeat(3,1fr);gap:50px">
{''.join(f'<div class="card"><div style="display:inline-flex;background:#DC2626;border-radius:50%;padding:30px">{art.icon(k, 140)}</div><b>{a}</b><span>{b}</span></div>' for k, a, b in T['s11'])}</div>
<div class="abs" style="left:0;right:0;bottom:110px;text-align:center;font-size:32px;font-weight:700;opacity:.85">{T['team']}</div>""")
    extra.team(s, T, lang, rtl, start, end)
    # 12 closer
    s(f"""<div class="abs" style="{end}:60px;top:300px;opacity:.9">{art.drone(760)}</div>
<div class="abs" style="{start}:120px;top:330px;width:1000px"><div class="h" style="font-size:96px">{T['s12a']}</div>
<div class="h red" style="font-size:120px;margin-top:20px">{T['s12b']}</div><div style="margin-top:70px;font-size:40px;font-weight:900">🩸 {T['name']} · NEXORA</div></div>""")
    return S, NOTES


def bmc_html(lang):
    T = TXT[lang]
    B = T["bmc"]
    ic = dict(kp="🤝", ka="⚙️", kr="🧰", vp="💎", cr="💬", ch="📣", cs="👥", cost="💸", rev="💰")
    cells = "".join(
        f'<div class="b b-{k}"><div class="bh"><span class="bi">{ic[k]}</span><div><b>{B[k][0]}</b>{f"<small>{B[k][1]}</small>" if B[k][1] else ""}</div></div>'
        f'<ul>{"".join(f"<li>{x}</li>" for x in B[k][2])}</ul></div>' for k in ("kp", "ka", "kr", "vp", "cr", "ch", "cs", "cost", "rev"))
    kpis = "".join(f'<div class="kp"><span>{a}</span><b>{b}</b></div>' for a, b in T["kpi"])
    css = """
.bmc { width:1920px; height:1358px; padding:50px 60px; background:#FFFBFB; color:#1C1917; display:flex; flex-direction:column }
.top { display:flex; align-items:center; gap:30px; background:linear-gradient(120deg,#3B0A10,#B91C1C); color:#fff; border-radius:30px; padding:26px 40px; margin-bottom:26px }
.top h1 { font-size:58px; font-weight:900; line-height:1 } .top p { font-size:26px; opacity:.85 }
.kps { margin-inline-start:auto; display:flex; gap:16px } .kp { background:#ffffff1f; border-radius:18px; padding:12px 24px; text-align:center }
.kp span { display:block; font-size:20px; opacity:.85 } .kp b { font-size:32px; direction:ltr; unicode-bidi:isolate }
.grid { flex:1; display:grid; gap:16px; grid-template-columns:repeat(10,1fr); grid-template-rows:1fr 1fr .78fr;
  grid-template-areas:"kp kp ka ka vp vp cr cr cs cs" "kp kp kr kr vp vp ch ch cs cs" "cost cost cost cost cost rev rev rev rev rev" }
.b { background:#fff; border:3px solid #F5E1E1; border-radius:26px; padding:22px 24px; overflow:hidden }
.bh { display:flex; align-items:center; gap:14px; margin-bottom:12px } .bi { font-size:44px } .bh b { display:block; font-size:30px; font-weight:900; color:#7F1D1D; line-height:1.15 }
.bh small { font-size:17px; color:#A8A29E; font-weight:700; letter-spacing:.03em }
.b ul { padding-inline-start:28px } .b li { font-size:25px; line-height:1.4; margin-bottom:8px; font-weight:600 }
.b-kp{grid-area:kp}.b-ka{grid-area:ka}.b-kr{grid-area:kr}.b-cr{grid-area:cr}.b-ch{grid-area:ch}
.b-vp{grid-area:vp;background:#FEF2F2;border-color:#F87171}.b-cs{grid-area:cs;background:#F0FDFA;border-color:#5EEAD4}
.b-cost{grid-area:cost;background:#FAFAF9}.b-rev{grid-area:rev;background:#FFFBEB;border-color:#FCD34D}
.ft { font-size:20px; color:#A8A29E; margin-top:12px }
"""
    body = f"""<div class="bmc"><div class="top"><div style="font-size:90px">🩸</div><div><h1>{T['name']} · {T['bmc_t']}</h1><p>{T['slogan']} · {T['team']}</p></div><div class="kps">{kpis}</div></div>
<div class="grid">{cells}</div><div class="ft">{" · ".join(n for n, _ in extra.TEAM[lang])} — {T['foot']}</div></div>"""
    return css, body


def page(lang, css, body):
    return (f'<!doctype html><html lang="{lang}" dir="{TXT[lang]["dir"]}"><head><meta charset="utf-8"><style>{font_css()}{CSS}{css}</style></head>'
            f"<body>{body}</body></html>")


def pptx(pngs, notes, path, w=1920, h=1080):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(int(12192000 * h / w))
    for i, png in enumerate(pngs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        sl.shapes.add_picture(str(png), 0, 0, width=prs.slide_width, height=prs.slide_height)
        if notes:
            sl.notes_slide.notes_text_frame.text = notes[i]
    prs.save(path)


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    work = DEST / "_work"
    work.mkdir(exist_ok=True)
    jobs, notes = [], {}
    for lang in ("ar", "en"):
        L = lang.upper()
        slides, notes[lang] = deck(lang)
        (work / f"deck_{lang}.html").write_text(page(lang, "", "".join(slides)), encoding="utf-8")
        css, body = bmc_html(lang)
        (work / f"bmc_{lang}.html").write_text(page(lang, css, body), encoding="utf-8")
        jobs += [dict(html=str(work / f"deck_{lang}.html"), pdf=str(DEST / f"DAMI_Pitch_Deck_{L}.pdf"), png=str(work / f"deck_{lang}"), sel=".s", w=1920, h=1080),
                 dict(html=str(work / f"bmc_{lang}.html"), pdf=str(DEST / f"DAMI_BMC_{L}.pdf"), png=str(work / f"bmc_{lang}"), sel=".bmc", w=1920, h=1358, pages="1")]
    (work / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(HERE / "render.js"), str(work / "jobs.json")], check=True, cwd="/tmp")
    for lang in ("ar", "en"):
        L = lang.upper()
        pptx(sorted(work.glob(f"deck_{lang}_*.png")), notes[lang], DEST / f"DAMI_Pitch_Deck_{L}.pptx")
        pptx(sorted(work.glob(f"bmc_{lang}_*.png")), None, DEST / f"DAMI_BMC_{L}.pptx", 1920, 1358)
    return sorted(p for p in DEST.iterdir() if p.is_file())


if __name__ == "__main__":
    for f in build():
        print(f)
