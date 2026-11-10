"""Business & finance slides for the DAMI deck: market size, competition, revenue, costs, budget, financial summary.
All numbers come from the shared 3-year model (common.model) so deck, BMC and guide agree."""

import math

from common import by_id, model

P = by_id(31)
M = model(P)
OPT = model(P, volume=1.4, opex_mult=.95)
STREAMS = P["fin"]["streams"]  # (name, unit, price, [units y1..y3], cogs share)
REV_BY = [[pr * u[y] for (_, _, pr, u, _) in STREAMS] for y in range(3)]  # per year, per stream
OPEX = P["fin"]["opex"]
OPEX_SPLIT = [0.60, 0.10, 0.15, 0.15]
BUDGET = [30000, 23000, 5000, round(M["funding"]) - 58000]  # hardware, software, compliance, runway
BE_BASE = next(m for m in range(1, 61) if -M["capex"] + sum(M["ebitda"][min(2, (k) // 12)] / 12 for k in range(m)) >= 0)
HOSP = dict(total=121, private=71, moh=33, rms=15, uni=2)
SRC_HOSP = "trade.gov — Jordan Country Commercial Guide: Healthcare"
RCOL = ["#B91C1C", "#F87171", "#7F1D1D", "#FDA4AF"]
CCOL = ["#7F1D1D", "#B91C1C", "#F87171", "#FDA4AF", "#A8A29E"]

L = {
"en": dict(
    k="k", cur="JOD", y=["Year 1", "Year 2", "Year 3"],
    mk_t="Market size", mk=[("TAM", "121 hospitals in Jordan", "JOD 726K / year"), ("SAM", "71 private hospitals", "JOD 426K / year"), ("SOM", "20 hospitals by year 3", "JOD 120K / year")],
    mk_side=["+ National dashboard contract", "+ Emergency flights", "+ Region: Gulf & Iraq later"], mk_src="Hospital counts: " + SRC_HOSP + " (121 = 71 private, 33 MoH, 15 RMS, 2 university)",
    cp_t="Competition", cp_cols=["Today (manual)", "Blood-bank software", "Zipline", "DAMI"],
    cp_rows=["Demand forecasting", "Stock balancing", "Targeted donors", "Drone delivery", "Live cold-chain", "Built for Jordan"],
    cp=[["✗", "~", "✗", "✓"], ["✗", "✗", "✗", "✓"], ["✗", "~", "✗", "✓"], ["✗", "✗", "✓", "✓"], ["✗", "~", "✓", "✓"], ["~", "~", "✗", "✓"]],
    cp_src="Based on our preliminary research; ~ = partial",
    rv_t="Revenue: 4 streams, growing", rv_leg=["Hospital subscriptions", "Emergency drone flights", "National dashboard", "Sponsorship"],
    rv_side=[("JOD 6,000", "per hospital / year"), ("JOD 90", "per flight · 55% margin"), ("3 → 10 → 20", "hospitals"), ("0 → 400 → 1,500", "flights")],
    cs_t="Costs: where the money goes", cs_leg=["Salaries", "Tech & servers", "Marketing", "Operations", "Direct costs"],
    cs_side=[("60%", "of OPEX is the team"), ("≈ JOD 40", "direct cost per flight"), ("15%", "direct cost per subscription")],
    bd_t="Budget: we need JOD 89,900", bd_leg=["Drones, cold boxes & ground station", "Platform & donor app", "Security & compliance", "Operating runway (to month 24)"],
    bd_note="Covers the initial investment (JOD 58,000) + operating losses until monthly cash flow turns positive in month 25",
    fs_t="Financial summary", fs_rows=["Revenue", "Direct costs", "Gross profit", "Operating costs", "Operating result"],
    fs_k=[("Gross margin Y3", f"{M['margin'] * 100:.0f}%"), ("Cash-positive from", "Month 25"), ("Break-even", f"Month {BE_BASE}"), ("Optimistic case", f"Month {OPT['breakeven']}")],
    fs_cash="Cumulative cash (36 months)", fs_note="Planning assumptions — to be validated with hospitals and suppliers",
    notes=dict(mk="Jordan has 121 hospitals. If all subscribed, that's JOD 726K a year. We focus first on the 71 private hospitals, and target 20 by year 3.",
               cp="Today it's phone calls. Blood-bank software records stock but doesn't forecast or deliver. Zipline delivers but isn't here and doesn't manage stock. DAMI does it all.",
               rv="Revenue grows from JOD 28K to 325K in three years, from four streams. Subscriptions are the base; drone flights grow after licensing.",
               cs="Most of our cost is the team. Each drone flight costs about JOD 40 directly and sells for 90.",
               bd="We need JOD 89,900: 30K hardware, 23K software, 5K compliance, and 32K to run until we're cash-positive in month 25.",
               fs="Year 3 is profitable with a 72% gross margin. We become cash-positive in month 25 and break even around month 37, or month 27 in the optimistic case.")),
"ar": dict(
    k="ألف", cur="د.أ", y=["السنة 1", "السنة 2", "السنة 3"],
    mk_t="حجم السوق", mk=[("TAM", "121 مستشفى في الأردن", "726 ألف د.أ سنويًا"), ("SAM", "71 مستشفى خاصًا", "426 ألف د.أ سنويًا"), ("SOM", "20 مستشفى بحلول السنة 3", "120 ألف د.أ سنويًا")],
    mk_side=["+ عقد اللوحة الوطنية", "+ رحلات الطوارئ", "+ لاحقًا: الخليج والعراق"], mk_src="أعداد المستشفيات: " + SRC_HOSP + " (121 = 71 خاص، 33 وزارة الصحة، 15 الخدمات الطبية، 2 جامعي)",
    cp_t="المنافسة", cp_cols=["الوضع الحالي", "برامج بنوك الدم", "Zipline", "دَمي"],
    cp_rows=["التنبؤ بالطلب", "موازنة المخزون", "متبرعون موجّهون", "توصيل بالدرون", "تبريد مراقَب لحظيًا", "مصمم للأردن"],
    cp=[["✗", "~", "✗", "✓"], ["✗", "✗", "✗", "✓"], ["✗", "~", "✗", "✓"], ["✗", "✗", "✓", "✓"], ["✗", "~", "✓", "✓"], ["~", "~", "✗", "✓"]],
    cp_src="حسب بحثنا المبدئي؛ ~ = جزئي",
    rv_t="الإيرادات: 4 مصادر تنمو", rv_leg=["اشتراكات المستشفيات", "رحلات الدرون الطارئة", "اللوحة الوطنية", "الرعاية"],
    rv_side=[("6,000 د.أ", "لكل مستشفى سنويًا"), ("90 د.أ", "لكل رحلة · هامش 55%"), ("3 → 10 → 20", "مستشفى"), ("0 → 400 → 1,500", "رحلة")],
    cs_t="التكاليف: أين تذهب الأموال؟", cs_leg=["الرواتب", "التقنية والخوادم", "التسويق", "التشغيل", "تكاليف مباشرة"],
    cs_side=[("60%", "من التكاليف للفريق"), ("≈ 40 د.أ", "كلفة مباشرة لكل رحلة"), ("15%", "كلفة مباشرة للاشتراك")],
    bd_t="الميزانية: نحتاج 89,900 د.أ", bd_leg=["درونز وصناديق تبريد ومحطة تحكم", "المنصة وتطبيق المتبرع", "الأمن والامتثال", "تشغيل حتى الشهر 24"],
    bd_note="تغطي الاستثمار الأولي (58,000 د.أ) والخسائر التشغيلية حتى يصبح التدفق النقدي الشهري موجبًا في الشهر 25",
    fs_t="الملخص المالي", fs_rows=["الإيرادات", "التكاليف المباشرة", "الربح الإجمالي", "التكاليف التشغيلية", "النتيجة التشغيلية"],
    fs_k=[("الهامش الإجمالي س3", f"{M['margin'] * 100:.0f}%"), ("تدفق نقدي موجب من", "الشهر 25"), ("نقطة التعادل", f"الشهر {BE_BASE}"), ("السيناريو المتفائل", f"الشهر {OPT['breakeven']}")],
    fs_cash="النقد التراكمي (36 شهرًا)", fs_note="افتراضات تخطيطية تُختبر مع المستشفيات والموردين",
    notes=dict(mk="في الأردن 121 مستشفى؛ لو اشتركت كلها فهذا 726 ألف دينار سنويًا. نبدأ بالمستشفيات الخاصة الـ 71 ونستهدف 20 منها بحلول السنة الثالثة.",
               cp="اليوم يتم كل شيء بالهاتف. برامج بنوك الدم تسجل المخزون فقط. Zipline توصل لكنها غير موجودة هنا ولا تدير المخزون. دَمي تجمع كل ذلك.",
               rv="الإيرادات تنمو من 28 ألفًا إلى 325 ألف دينار خلال ثلاث سنوات من أربعة مصادر.",
               cs="أكبر تكلفة هي الفريق. كل رحلة درون تكلف نحو 40 دينارًا وتباع بـ 90.",
               bd="نحتاج 89,900 دينار: 30 ألفًا للأجهزة، و23 ألفًا للبرمجيات، و5 آلاف للامتثال، و32 ألفًا للتشغيل حتى الشهر 25.",
               fs="السنة الثالثة رابحة بهامش 72%. التدفق النقدي يصبح موجبًا في الشهر 25، ونقطة التعادل قرابة الشهر 37، أو الشهر 27 في السيناريو المتفائل.")),
}


def k(v, lang):
    return f"{v / 1000:,.0f}{'K' if lang == 'en' else ' ألف'}" if abs(v) >= 1000 else f"{v:,.0f}"


def legend(names, cols):
    return '<div style="display:flex;flex-wrap:wrap;gap:22px 36px;font-size:26px;font-weight:700">' + "".join(
        f'<span><i style="display:inline-block;width:26px;height:26px;border-radius:6px;background:{c};vertical-align:middle;margin-inline-end:10px"></i>{n}</span>' for n, c in zip(names, cols)) + "</div>"


def stacked(series, colors, labels, lang, w=1000, h=560, total_fmt=None):
    """series[year][part] -> stacked bars with totals on top (always LTR)."""
    tot = [sum(s) for s in series]
    hi = max(tot) * 1.18
    bw, gap, base, top = 190, (w - 3 * 190) / 4, h - 70, 40
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg" font-family="Cairo">',
           f'<line x1="0" x2="{w}" y1="{base}" y2="{base}" stroke="#D6D3D1" stroke-width="3"/>']
    for i, parts in enumerate(series):
        x, y = gap + i * (bw + gap), base
        for v, c in zip(parts, colors):
            hh = v / hi * (base - top)
            if hh > 0:
                out.append(f'<rect x="{x}" y="{y - hh}" width="{bw}" height="{hh}" fill="{c}" rx="6"/>')
            y -= hh
        out.append(f'<text x="{x + bw / 2}" y="{y - 16}" text-anchor="middle" font-size="40" font-weight="900" fill="#1C1917">{(total_fmt or (lambda v: k(v, lang)))(tot[i])}</text>')
        out.append(f'<text x="{x + bw / 2}" y="{base + 50}" text-anchor="middle" font-size="30" font-weight="700" fill="#57534E">{labels[i]}</text>')
    out.append("</svg>")
    return "".join(out)


def donut(values, colors, size=560, center=("JOD", "89,900")):
    r, sw, c = size / 2 - 50, 90, size / 2
    tot, ang, out = sum(values), -math.pi / 2, []
    out.append(f'<svg viewBox="0 0 {size} {size}" width="{size}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg" font-family="Cairo">')
    for v, col in zip(values, colors):
        a2 = ang + v / tot * 2 * math.pi
        large = 1 if a2 - ang > math.pi else 0
        x1, y1, x2, y2 = c + r * math.cos(ang), c + r * math.sin(ang), c + r * math.cos(a2), c + r * math.sin(a2)
        out.append(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 {large} 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        mid = (ang + a2) / 2
        out.append(f'<text x="{c + r * math.cos(mid):.1f}" y="{c + r * math.sin(mid) + 12:.1f}" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">{v / tot * 100:.0f}%</text>')
        ang = a2
    out.append(f'<text x="{c}" y="{c - 10}" text-anchor="middle" font-size="36" fill="#78716C" font-weight="700">{center[0]}</text>'
               f'<text x="{c}" y="{c + 50}" text-anchor="middle" font-size="64" fill="#7F1D1D" font-weight="900">{center[1]}</text></svg>')
    return "".join(out)


def cash_line(w=820, h=380, lang="en"):
    pts, lo, hi = M["curve"], min(M["curve"]), max(max(M["curve"]), 10000)
    sx, base = lambda i: 60 + i / 36 * (w - 90), lambda v: 30 + (hi - v) / (hi - lo) * (h - 90)
    path = " ".join(f"{sx(i):.1f},{base(v):.1f}" for i, v in enumerate(pts))
    low_i = pts.index(lo)
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg" font-family="Cairo">',
           f'<line x1="60" x2="{w - 30}" y1="{base(0):.1f}" y2="{base(0):.1f}" stroke="#A8A29E" stroke-width="2" stroke-dasharray="8 8"/>',
           f'<polyline points="{path}" fill="none" stroke="#B91C1C" stroke-width="7" stroke-linejoin="round"/>',
           f'<circle cx="{sx(low_i):.1f}" cy="{base(lo):.1f}" r="11" fill="#7F1D1D"/>',
           f'<text x="{sx(low_i):.1f}" y="{base(lo) - 26:.1f}" text-anchor="middle" font-size="26" font-weight="800" fill="#7F1D1D">−89.9K</text>']
    for m in (0, 12, 24, 36):
        out.append(f'<text x="{sx(m):.1f}" y="{h - 12}" text-anchor="middle" font-size="24" fill="#78716C">M{m}</text>')
    out.append(f'<text x="{sx(36) - 4:.1f}" y="{base(pts[-1]) - 18:.1f}" text-anchor="end" font-size="26" font-weight="800" fill="#B91C1C">{pts[-1] / 1000:,.1f}K</text></svg>')
    return "".join(out)


def slides(s, lang, rtl, start, end, part):
    t = L[lang]
    if part == 2:
        return money(s, t, lang, rtl, start, end)
    # market size
    circ = (f'<div class="abs" style="{end}:170px;top:230px;width:660px;height:660px">'
            f'<div class="abs" style="left:0;top:0;width:660px;height:660px;border-radius:50%;background:#FEE2E2"></div>'
            f'<div class="abs" style="left:100px;top:200px;width:460px;height:460px;border-radius:50%;background:#FCA5A5"></div>'
            f'<div class="abs" style="left:205px;top:410px;width:250px;height:250px;border-radius:50%;background:#B91C1C"></div>'
            f'<div class="abs" style="left:0;right:0;top:70px;text-align:center;font-size:40px;font-weight:900;color:#7F1D1D">TAM</div>'
            f'<div class="abs" style="left:0;right:0;top:280px;text-align:center;font-size:40px;font-weight:900;color:#7F1D1D">SAM</div>'
            f'<div class="abs" style="left:0;right:0;top:500px;text-align:center;font-size:40px;font-weight:900;color:#fff">SOM</div></div>')
    rows = "".join(f'<div style="margin-bottom:22px"><div style="font-size:30px;font-weight:900;color:#B91C1C">{a}</div><div style="font-size:46px;font-weight:900">{c}</div><div style="font-size:30px;color:#57534E">{b}</div></div>' for a, b, c in t["mk"])
    s(f"""<div class="abs h dk" style="{start}:120px;top:90px">{t['mk_t']}</div>{circ}
<div class="abs" style="{start}:130px;top:220px;width:860px">{rows}<div style="font-size:26px;font-weight:700;color:#7F1D1D;line-height:1.5;margin-top:6px">{' · '.join(t['mk_side'])}</div></div>
<div class="src" style="{start}:120px;opacity:.7;font-size:19px">{t['mk_src']}</div>""", "light", note=t["notes"]["mk"])
    # competition
    head = "".join(f'<th style="padding:22px 18px;font-size:30px;{"background:#B91C1C;color:#fff;border-radius:18px 18px 0 0" if i == 3 else "color:#57534E"}">{c}</th>' for i, c in enumerate(t["cp_cols"]))
    body = "".join(f'<tr><td style="padding:18px 24px;font-size:32px;font-weight:800;text-align:start">{r}</td>' + "".join(
        f'<td style="text-align:center;font-size:44px;font-weight:900;{"background:#FEF2F2;" if j == 3 else ""}color:{"#16A34A" if v == "✓" else "#DC2626" if v == "✗" else "#D97706"}">{v}</td>' for j, v in enumerate(row)) + "</tr>"
        for r, row in zip(t["cp_rows"], t["cp"]))
    s(f"""<div class="abs h dk" style="left:0;right:0;top:80px;text-align:center">{t['cp_t']}</div>
<div class="abs" style="left:170px;right:170px;top:230px"><table style="width:100%;border-collapse:collapse;background:#fff;border-radius:24px;box-shadow:0 20px 60px #B91C1C14"><tr><th></th>{head}</tr>{body}</table></div>
<div class="src" style="{start}:120px;opacity:.7">{t['cp_src']}</div>""", "light", note=t["notes"]["cp"])


def money(s, t, lang, rtl, start, end):
    # revenue
    side = "".join(f'<div class="card" style="padding:22px;margin-bottom:22px;text-align:start"><b class="dk" style="margin:0;font-size:40px;direction:ltr;unicode-bidi:isolate">{a}</b><span>{b}</span></div>' for a, b in t["rv_side"])
    s(f"""<div class="abs h dk" style="{start}:120px;top:80px">{t['rv_t']}</div>
<div class="abs" style="{start}:110px;top:230px">{stacked(REV_BY, RCOL, t['y'], lang)}<div style="margin-top:20px">{legend(t['rv_leg'], RCOL)}</div></div>
<div class="abs" style="{end}:120px;top:230px;width:520px">{side}</div>""", "light", note=t["notes"]["rv"])
    # costs
    cost_series = [[OPEX[y] * f for f in OPEX_SPLIT] + [M["cogs"][y]] for y in range(3)]
    side = "".join(f'<div class="card" style="padding:26px;margin-bottom:26px;text-align:start"><b class="dk" style="margin:0;font-size:48px;direction:ltr;unicode-bidi:isolate">{a}</b><span>{b}</span></div>' for a, b in t["cs_side"])
    s(f"""<div class="abs h dk" style="{start}:120px;top:80px">{t['cs_t']}</div>
<div class="abs" style="{start}:110px;top:230px">{stacked(cost_series, CCOL, t['y'], lang)}<div style="margin-top:20px">{legend(t['cs_leg'], CCOL)}</div></div>
<div class="abs" style="{end}:120px;top:250px;width:520px">{side}</div>""", "light", note=t["notes"]["cs"])
    # budget
    lg = "".join(f'<div class="row" style="gap:22px;margin-bottom:34px"><i style="width:40px;height:40px;border-radius:10px;background:{c};flex:none"></i>'
                 f'<div><div style="font-size:44px;font-weight:900;direction:ltr;unicode-bidi:isolate;text-align:start">{v:,} {"JOD" if lang == "en" else "د.أ"}</div><div style="font-size:30px;color:#57534E">{n}</div></div></div>'
                 for n, v, c in zip(t["bd_leg"], BUDGET, RCOL))
    s(f"""<div class="abs h dk" style="left:0;right:0;top:80px;text-align:center">{t['bd_t']}</div>
<div class="abs" style="{end}:180px;top:230px">{donut(BUDGET, RCOL, center=("JOD" if lang == "en" else "د.أ", f"{sum(BUDGET):,}"))}</div>
<div class="abs" style="{start}:170px;top:250px;width:820px">{lg}</div>
<div class="abs" style="left:150px;right:150px;bottom:80px;text-align:center;font-size:28px;font-weight:700;color:#7F1D1D">{t['bd_note']}</div>""", "light", note=t["notes"]["bd"])
    # financial summary
    vals = [M["rev"], M["cogs"], M["gross"], M["opex"], M["ebitda"]]
    trs = "".join(f'<tr style="{"background:#FEF2F2;font-weight:900" if i in (2, 4) else ""}"><td style="padding:14px 20px;font-size:28px;font-weight:800;text-align:start">{n}</td>'
                  + "".join(f'<td style="padding:14px 20px;font-size:30px;text-align:center;direction:ltr;color:{"#DC2626" if v < 0 else "#1C1917"}">{v / 1000:,.1f}K</td>' for v in row) + "</tr>"
                  for i, (n, row) in enumerate(zip(t["fs_rows"], vals)))
    kp = "".join(f'<div class="card" style="padding:18px 10px"><b class="dk" style="margin:0;font-size:34px;white-space:nowrap">{b}</b><span style="font-size:22px;display:block;line-height:1.3">{a}</span></div>' for a, b in t["fs_k"])
    s(f"""<div class="abs h dk" style="{start}:120px;top:70px">{t['fs_t']}</div>
<div class="abs" style="{start}:100px;top:210px;width:860px"><table style="width:100%;border-collapse:collapse;background:#fff;border-radius:20px;box-shadow:0 20px 60px #B91C1C14">
<tr><th></th>{''.join(f'<th style="padding:16px;font-size:26px;color:#57534E">{y}</th>' for y in t['y'])}</tr>{trs}</table>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:30px">{kp}</div></div>
<div class="abs" style="{end}:70px;top:210px;width:780px"><div style="font-size:30px;font-weight:900;color:#7F1D1D;margin-bottom:10px">{t['fs_cash']}</div>{cash_line(w=780, lang=lang)}</div>
<div class="src" style="{start}:120px;opacity:.7">{t['fs_note']}</div>""", "light", note=t["notes"]["fs"])
