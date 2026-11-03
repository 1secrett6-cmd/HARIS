"""03 — a feasibility study per project: market, costs, revenues, 3-year P&L, scenarios, verdict."""

from common import (AXES, CHART_LEGEND, DISCLAIMER, OPEX_SPLIT, OUT, PROJECTS, SCENARIOS, breakeven_text, cash_chart,
                    e, model, money, page, price, print_pdf, verdict)

CSS = """
@page { size:A4; margin:12mm 12mm; }
@page :first { margin:0; }
body { font-size:9.4pt; }
.cover { height:297mm; padding:26mm 18mm; color:#fff; display:flex; flex-direction:column; justify-content:center; background:linear-gradient(160deg,#0F172A,#075985 60%,#0B6E4F) }
.cover h1 { font-size:46pt; font-weight:900; line-height:1.1 } .cover p { font-size:12.5pt; opacity:.9 }
.brk { break-before:page; }
.band { background:linear-gradient(135deg,#075985,#0369A1); color:#fff; border-radius:3mm; padding:4mm 6mm; margin-bottom:3mm }
.band h2 { font-size:17pt; font-weight:900 } .band p { margin:.5mm 0 0; opacity:.92 }
h4 { color:#0369A1; font-size:10.5pt; margin:3mm 0 1mm }
.kgrid { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:2mm }
.k { background:#F0F9FF; border:1px solid #BAE6FD; border-radius:2mm; padding:2mm; text-align:center } .k span { display:block; font-size:7.6pt; color:#475569 } .k b { font-size:10pt; color:#075985 }
table { font-size:8.8pt } td.n, th.n { text-align:left; direction:ltr }
.pl td:first-child { font-weight:700 } .pl tr.hl td { background:#F0F9FF; font-weight:900 }
.two { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:5mm }
.verdict { color:#fff; border-radius:2mm; padding:2.5mm 4mm; font-weight:700; margin-top:2mm }
.box { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:2mm; padding:2.5mm 4mm; margin-top:2mm }
ul { padding-right:5mm } .avoid { break-inside:avoid }
.sum td, .sum th { font-size:8.3pt; padding:1mm 1.5mm; text-align:center } .sum td:nth-child(2) { text-align:right; white-space:nowrap }
"""


def validation_plan(p):
    first = p["fin"]["streams"][0]
    return [
        f"تحقق من استعداد العميل للدفع: {first[0]} بسعر {price(first[2])} لكل {first[1]}، عبر 15–20 مقابلة مع شريحة \"{p['bmc']['cs'][0]}\".",
        f"اختبر افتراض الكميات للسنة الأولى ({first[3][0]:,} {first[1]}) بخطاب نوايا أو تجربة مدفوعة صغيرة.",
        "اطلب عروض أسعار حقيقية لأكبر بندين في الاستثمار الأولي وحدّث الجدول.",
        "قِس الأثر في النموذج الأولي (مؤشرات الأثر) واستخدم الأرقام المقاسة في العرض بدل الافتراضات.",
    ]


def study(p):
    m = model(p)
    fin = p["fin"]
    v_label, v_color, v_text = verdict(m["breakeven"])
    capex_rows = "".join(f"<tr><td>{e(n)}</td><td class='n'>{money(v)}</td></tr>" for n, v in fin["capex"])
    stream_rows = "".join(
        f"<tr><td>{e(n)}</td><td>{e(u)}</td><td class='n'>{price(pr)}</td>"
        + "".join(f"<td class='n'>{x:,}</td>" for x in units)
        + f"<td class='n'>{money(pr * units[2])}</td><td class='n'>{int(c * 100)}%</td></tr>"
        for n, u, pr, units, c in fin["streams"])
    opex_rows = "".join(
        f"<tr><td>{e(n)}</td>" + "".join(f"<td class='n'>{money(o * share)}</td>" for o in fin["opex"]) + "</tr>"
        for n, share in OPEX_SPLIT)
    pl = [("الإيرادات", m["rev"]), ("كلفة الإيرادات المباشرة", m["cogs"]), ("الربح الإجمالي", m["gross"]),
          ("المصاريف التشغيلية", m["opex"]), ("صافي الربح التشغيلي", m["ebitda"]), ("النقد التراكمي (بعد الاستثمار)", m["cum"])]
    pl_rows = "".join(
        f"<tr{' class=\"hl\"' if lab.startswith(('صافي', 'النقد')) else ''}><td>{e(lab)}</td>" + "".join(f"<td class='n'>{money(x)}</td>" for x in vals) + "</tr>"
        for lab, vals in pl)
    sc_rows = ""
    for name, vol, op in SCENARIOS:
        s = model(p, volume=vol, opex_mult=op)
        sc_rows += f"<tr><td>{e(name)}</td><td class='n'>×{vol}</td><td class='n'>×{op}</td><td class='n'>{money(s['rev'][2])}</td><td class='n'>{money(s['ebitda'][2])}</td><td class='n'>{money(s['funding'])}</td><td>{breakeven_text(s['breakeven'])}</td></tr>"
    risks = "".join(f"<li><b>{e(r)}:</b> {e(mit)}</li>" for r, mit in p["risks"])
    return f"""
<section class="brk">
  <div class="band"><h2>{p['id']:02d} · {p['emoji']} {e(p['ar'])} <span style="font-size:.6em;opacity:.8">{e(p['en'])}</span></h2><p>{e(p['tag'])} · {e(AXES[p['axis']][0])}</p></div>
  <div class="kgrid">
    <div class="k"><span>الاستثمار الأولي</span><b>{money(m['capex'])}</b></div>
    <div class="k"><span>التمويل المطلوب</span><b>{money(m['funding'])}</b></div>
    <div class="k"><span>إيرادات السنة 1</span><b>{money(m['rev'][0])}</b></div>
    <div class="k"><span>إيرادات السنة 3</span><b>{money(m['rev'][2])}</b></div>
    <div class="k"><span>الهامش الإجمالي س3</span><b>{m['margin'] * 100:.0f}%</b></div>
    <div class="k"><span>نقطة التعادل</span><b>{breakeven_text(m['breakeven'])}</b></div>
  </div>
  <h4>1. السوق والافتراضات</h4><p>{e(p['market'])}</p>
  <div class="two">
    <div class="avoid"><h4>2. الاستثمار الأولي (CAPEX)</h4><table><tr><th>البند</th><th class="n">القيمة</th></tr>{capex_rows}<tr class="hl"><td><b>المجموع</b></td><td class="n"><b>{money(m['capex'])}</b></td></tr></table></div>
    <div class="avoid"><h4>3. المصاريف التشغيلية السنوية (OPEX)</h4><table><tr><th>البند</th><th class="n">س1</th><th class="n">س2</th><th class="n">س3</th></tr>{opex_rows}</table></div>
  </div>
  <div class="avoid"><h4>4. مصادر الإيرادات</h4><table><tr><th>المصدر</th><th>الوحدة</th><th class="n">السعر</th><th class="n">س1</th><th class="n">س2</th><th class="n">س3</th><th class="n">إيراد س3</th><th class="n">الكلفة المباشرة</th></tr>{stream_rows}</table></div>
  <div class="avoid"><h4>5. قائمة الدخل المتوقعة (3 سنوات)</h4><table class="pl"><tr><th>البند</th><th class="n">السنة 1</th><th class="n">السنة 2</th><th class="n">السنة 3</th></tr>{pl_rows}</table></div>
</section>
<section class="brk">
  <div class="avoid"><h4>6. التدفق النقدي ونقطة التعادل</h4>{cash_chart(m, 640, 190)}{CHART_LEGEND}</div>
  <div class="avoid"><h4>7. تحليل السيناريوهات</h4><table><tr><th>السيناريو</th><th class="n">الكميات</th><th class="n">التكاليف</th><th class="n">إيراد س3</th><th class="n">نتيجة س3</th><th class="n">التمويل المطلوب</th><th>التعادل</th></tr>{sc_rows}</table></div>
  <div class="two">
    <div class="avoid"><h4>8. الجدوى الفنية</h4><ul>{''.join(f'<li>{e(x)}</li>' for x in p['ai'])}</ul><p><b>البيانات:</b> {e('، '.join(p['data']))}</p></div>
    <div class="avoid"><h4>9. الجدوى القانونية والتنظيمية</h4><p>{e(p['legal'])}</p></div>
  </div>
  <div class="avoid"><h4>10. المخاطر وطرق التخفيف</h4><ul>{risks}</ul></div>
  <div class="avoid"><h4>11. خطة التحقق من الافتراضات</h4><ul>{''.join(f'<li>{e(x)}</li>' for x in validation_plan(p))}</ul></div>
  <div class="verdict" style="background:{v_color}">الخلاصة: {e(v_label)}. {e(v_text)}</div>
</section>"""


def build():
    rows = ""
    for p in PROJECTS:
        m = model(p)
        rows += (f"<tr><td>{p['id']}</td><td>{p['emoji']} {e(p['ar'])}</td><td>{money(m['capex'])}</td><td>{money(m['funding'])}</td>"
                 f"<td>{money(m['rev'][2])}</td><td>{money(m['ebitda'][2])}</td><td>{breakeven_text(m['breakeven'])}</td>"
                 f"<td style='color:{verdict(m['breakeven'])[1]};font-weight:700'>{e(verdict(m['breakeven'])[0])}</td></tr>")
    body = f"""<div class="cover"><div style="letter-spacing:.4em;font-weight:900;opacity:.8">NEXORA</div>
  <h1>دراسات الجدوى المبدئية<br>للمشاريع الـ 31</h1>
  <p>لكل مشروع: السوق والافتراضات، الاستثمار الأولي، المصاريف التشغيلية، مصادر الإيرادات، قائمة الدخل لثلاث سنوات، التدفق النقدي ونقطة التعادل، السيناريوهات، الجدوى الفنية والقانونية، المخاطر، وخطة التحقق.</p>
  <p style="font-size:9.5pt;opacity:.8">{e(DISCLAIMER)}</p></div>
<section><div class="band"><h2>ملخص مقارن</h2><p>نتائج النموذج المالي بالافتراضات الأساسية (بالدينار الأردني).</p></div>
<table class="sum"><tr><th>#</th><th>المشروع</th><th>الاستثمار</th><th>التمويل المطلوب</th><th>إيراد س3</th><th>نتيجة س3</th><th>التعادل</th><th>الحكم المبدئي</th></tr>{rows}</table></section>
{''.join(study(p) for p in PROJECTS)}"""
    return print_pdf(page("NEXORA — دراسات الجدوى", body, CSS), OUT / "03_Feasibility_Studies.pdf")


if __name__ == "__main__":
    print(build())
