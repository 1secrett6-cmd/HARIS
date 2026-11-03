"""04 — one submission-ready proposal PDF per project, plus a combined volume."""

from common import (AXES, BMC_BLOCKS, CHART_LEGEND, KING_QUOTE, OUT, PROJECTS, breakeven_text, cash_chart, e, model,
                    money, page, print_pdf, verdict)

ALIGNMENT = {
    "health": [
        "يدعم جاهزية القطاع الصحي للطوارئ والحوادث الكبرى.",
        "يتوافق مع توجه التحول الرقمي في الخدمات الصحية وحماية البيانات.",
        "يقلل الهدر في مورد صحي نادر ويحسّن العدالة في الوصول إليه.",
    ],
}
ALIGNMENT_WATER = [
    "يستجيب مباشرة لخطاب العرش 2026 الذي جعل الأمن المائي أولوية وطنية ووجّه لخطط استباقية.",
    "يدعم أهداف الاستراتيجية الوطنية للمياه 2023–2040، ومنها خفض الفاقد إلى أقل من 25%.",
    "يكمّل مشاريع التزويد الكبرى مثل الناقل الوطني بحلول الكفاءة وإدارة الطلب والبيانات.",
]
TEAM = [("قائد المشروع / AI Lead", "المعمارية التقنية ونماذج الذكاء الاصطناعي والتنسيق"),
        ("Data Scientist", "البيانات والتحليل والتقييم"),
        ("مهندس أنظمة / IoT", "الحساسات والتكامل الميداني أو المحاكاة"),
        ("مطور تطبيقات ولوحات", "التطبيق ولوحة التحكم والعرض الحي"),
        ("Business & Pitch Lead", "نموذج العمل والشراكات والعرض أمام اللجنة")]

CSS = """
@page { size:A4; margin:14mm 14mm; }
@page :first { margin:0; }
body { font-size:10pt; }
.cover { height:297mm; padding:24mm 18mm; color:#fff; display:flex; flex-direction:column; justify-content:space-between; background:linear-gradient(160deg,#04223A,#0369A1 58%,#0B6E4F) }
.cover h1 { font-size:46pt; font-weight:900; line-height:1.1 } .cover .en2 { font-size:16pt; letter-spacing:.15em; opacity:.85; direction:ltr; text-align:right }
.cover .tag { font-size:15pt; font-weight:700; margin-top:4mm }
.cover table { width:auto; margin-top:8mm; font-size:10.5pt } .cover td { border:none; padding:1mm 0 1mm 8mm; color:#fff }
.cover .q { border-right:4px solid #7DD3FC; padding-right:4mm; font-weight:700 }
h2 { color:#075985; font-size:14pt; border-bottom:2px solid #BAE6FD; padding-bottom:1mm; margin:5mm 0 2mm }
.brk { break-before:page }
.kgrid { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:2mm; margin:2mm 0 }
.k { background:#F0F9FF; border:1px solid #BAE6FD; border-radius:2mm; padding:2mm; text-align:center } .k span { display:block; font-size:7.8pt; color:#475569 } .k b { color:#075985 }
.bmc { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr); gap:2mm }
.bmc div { border:1px solid #CBD5E1; border-radius:2mm; padding:2mm 3mm; font-size:8.6pt } .bmc h5 { margin:0 0 1mm; color:#0F172A; font-size:9pt }
.bmc ul { margin:0; padding-right:4mm }
.wow { background:#0F172A; color:#F1F5F9; border-radius:2mm; padding:3mm 4mm; margin-top:2mm }
.verdict { color:#fff; border-radius:2mm; padding:2.5mm 4mm; font-weight:700 }
.avoid { break-inside:avoid } ul { padding-right:5mm }
"""


def ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def proposal_body(p):
    m = model(p)
    v_label, v_color, v_text = verdict(m["breakeven"])
    align = ALIGNMENT.get(p["axis"], ALIGNMENT_WATER)
    bmc = "".join(f"<div><h5>{e(ar)} <small style='color:#64748B'>{e(en)}</small></h5>{ul(p['bmc'][k])}</div>" for k, ar, en in BMC_BLOCKS)
    mvp = "".join(f"<tr><td>الأسابيع {e(w)}</td><td>{e(t)}</td></tr>" for w, t in p["mvp"])
    risks = "".join(f"<tr><td>{e(r)}</td><td>{e(mm)}</td></tr>" for r, mm in p["risks"])
    team = "".join(f"<tr><td><b>{e(r)}</b></td><td>{e(d)}</td></tr>" for r, d in TEAM)
    first_capex = max(p["fin"]["capex"], key=lambda x: x[1])[0]
    return f"""
<div class="cover">
  <div style="letter-spacing:.4em;font-weight:900;opacity:.8">NEXORA</div>
  <div>
    <div style="font-size:12pt;opacity:.85">مقترح مشروع ريادي · Project Proposal</div>
    <h1>{p['emoji']} {e(p['ar'])}</h1><div class="en2">{e(p['en'])}</div>
    <div class="tag">{e(p['tag'])}</div>
    <table><tr><td>الفريق</td><td><b>NEXORA</b></td></tr><tr><td>المجال</td><td>{e(AXES[p['axis']][0])} · Artificial Intelligence &amp; Data Science</td></tr>
    <tr><td>المسابقة</td><td>Jordan Students Pitch Competition — GEW Jordan</td></tr><tr><td>الجامعة / المشرف</td><td>………………………………</td></tr></table>
  </div>
  <div class="q">«{e(KING_QUOTE)}»<div style="font-weight:400;font-size:9pt;opacity:.8">جلالة الملك عبدالله الثاني — خطاب العرش 2026</div></div>
</div>

<h2>1. الملخص التنفيذي</h2>
<p><b>{e(p['ar'])}</b> {e(p['tag'])}. {e(p['solution'])}</p>
<div class="kgrid">
  <div class="k"><span>الاستثمار الأولي</span><b>{money(m['capex'])}</b></div>
  <div class="k"><span>التمويل المطلوب</span><b>{money(m['funding'])}</b></div>
  <div class="k"><span>إيرادات السنة 3</span><b>{money(m['rev'][2])}</b></div>
  <div class="k"><span>نتيجة السنة 3</span><b>{money(m['ebitda'][2])}</b></div>
  <div class="k"><span>التعادل</span><b>{breakeven_text(m['breakeven'])}</b></div>
</div>
<h2>2. المشكلة</h2><p>{e(p['problem'])}</p>{ul(p['evidence'])}
<h2>3. الحل المقترح</h2><p>{e(p['solution'])}</p>
<div class="avoid"><h2>4. كيف يعمل</h2><ol>{''.join(f'<li>{e(x)}</li>' for x in p['how'])}</ol></div>
<div class="avoid"><h2>5. المميزات والتقنيات</h2>{ul(p['features'])}<p><b>الذكاء الاصطناعي:</b> {e('؛ '.join(p['ai']))}</p><p><b>البيانات:</b> {e('، '.join(p['data']))}</p></div>
<div class="wow avoid"><b>⚡ العرض الحي أمام اللجنة:</b> {e(p['wow'])}</div>
<div class="avoid"><h2>6. الابتكار والتميّز</h2>{ul(p['diff'])}</div>

<div class="brk"></div>
<h2>7. نموذج العمل التجاري (Business Model Canvas)</h2><div class="bmc">{bmc}</div>
<div class="avoid"><h2>8. الجدوى المالية</h2><p>{e(p['market'])}</p>{cash_chart(m, 640, 170)}{CHART_LEGEND}
<div class="verdict" style="background:{v_color};margin-top:2mm">{e(v_label)}: {e(v_text)}</div></div>

<div class="brk"></div>
<div class="avoid"><h2>9. خطة التنفيذ (النموذج الأولي خلال 12 أسبوعًا)</h2><table><tr><th>المرحلة</th><th>المخرجات</th></tr>{mvp}</table></div>
<div class="avoid"><h2>10. مؤشرات قياس الأثر</h2>{ul(p['impact'])}</div>
<div class="avoid"><h2>11. المخاطر والإطار التنظيمي</h2><table><tr><th>الخطر</th><th>التعامل</th></tr>{risks}</table><p>{e(p['legal'])}</p></div>
<div class="avoid"><h2>12. الانسجام مع الأولويات الوطنية</h2>{ul(align)}</div>
<div class="avoid"><h2>13. الفريق</h2><table>{team}</table></div>
<div class="avoid"><h2>14. ما نحتاجه (The Ask)</h2>{ul([
    f"تمويل أولي بقيمة تقريبية {money(m['funding'])} يغطي الاستثمار الأولي وفترة النمو حتى التعادل.",
    f"شريك تجريبي من شريحة \"{p['bmc']['cs'][0]}\" لاختبار النموذج الأولي.",
    f"دعم في تأمين أكبر بند في الاستثمار الأولي: {first_capex}.",
    "إرشاد في ريادة الأعمال والتعامل مع الجهات الحكومية والمانحين.",
])}</div>
<p style="font-size:8pt;color:#64748B;margin-top:4mm">الأرقام المالية افتراضات تخطيطية أولية للتحقق، وليست نتائج أبحاث سوق. عبارة "غير موجود في الأردن" تعني عدم العثور على مثيل في بحث مبدئي.</p>
"""


def build():
    folder = OUT / "proposals"
    folder.mkdir(exist_ok=True)
    for p in PROJECTS:
        print_pdf(page(f"Proposal — {p['en']}", proposal_body(p), CSS), folder / f"{p['id']:02d}_{p['slug']}_proposal.pdf")
    return folder


if __name__ == "__main__":
    print(build())
