"""01 — the detailed ideas book for all 31 projects."""

from common import (AXES, DISCLAIMER, KING_QUOTE, OUT, PROJECTS, SCORE_LABELS, SCORES, breakeven_text, e,
                    model, money, page, print_pdf, score, verdict)

SOURCES = [
    ("الجزيرة — خطاب العرش 2026 وأمن المياه", "https://www.aljazeera.net/news/2026/11/2/"),
    ("الأنباط — الملك: المياه أولوية وطنية لا مساومة فيها", "https://alanbatnews.net/article/485641"),
    ("عمون — تحليل محور المياه في خطاب الملك", "https://www.ammonnews.net/article/1041745"),
    ("صندوق المناخ الأخضر — مشروع الناقل الوطني FP288", "https://www.greenclimate.fund/project/FP288"),
    ("Climate Policy Radar — مشروع تحلية ونقل مياه العقبة–عمّان", "https://app.climatepolicyradar.org/document/jordan-aqaba-amman-water-desalination-and-conveyance-project-aawdcp_3633"),
    ("Arab News — إنفاق الأردن على مشاريع المياه في 2025", "https://www.arabnews.pk/node/2627657"),
    ("FAO WaPOR — بيانات التبخر والنتح المفتوحة", "https://www.fao.org/in-action/remote-sensing-for-water-productivity/en"),
]

CSS = """
@page { size:A4; margin:13mm 12mm; }
@page :first { margin:0; }
body { font-size:9.8pt; }
.cover { height:297mm; padding:24mm 18mm; color:#fff; display:flex; flex-direction:column; justify-content:space-between;
  background: radial-gradient(circle at 80% 15%, #38BDF8 0, transparent 40%), radial-gradient(circle at 10% 90%, #0B6E4F 0, transparent 45%), linear-gradient(160deg,#04223A,#075985 55%,#0C4A6E); }
.cover .team { letter-spacing:.4em; font-weight:900; direction:ltr; text-align:right; opacity:.85 }
.cover h1 { font-size:58pt; font-weight:900; line-height:1.08 }
.cover h1 span { color:#7DD3FC }
.cover .sub { font-size:15pt; font-weight:600; margin-top:5mm }
.cover .q { margin-top:9mm; border-right:4px solid #7DD3FC; padding-right:5mm; font-size:13pt; font-weight:700 }
.cover .q small { display:block; font-size:9.5pt; font-weight:400; opacity:.8 }
.pills { display:flex; gap:3mm; flex-wrap:wrap; margin-top:8mm } .pill { border:1px solid #ffffff60; background:#ffffff14; border-radius:99px; padding:1mm 4.5mm; font-size:9.5pt }
.brk { break-before:page; }
.band { background:linear-gradient(135deg,#075985,#0369A1); color:#fff; border-radius:4mm; padding:5mm 7mm; margin-bottom:4mm }
.band h2 { font-size:19pt; font-weight:900 } .band p { margin:1mm 0 0; opacity:.92 }
.box { background:var(--bg); border:1px solid var(--line); border-radius:3mm; padding:3.5mm 5mm; margin:3mm 0 }
.box h3 { color:var(--w); font-size:12pt; margin-bottom:1mm }
.facts { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:3mm; margin:3mm 0 }
.fact { background:#E0F2FE; border-radius:3mm; padding:3mm 4mm } .fact b { display:block; font-size:18pt; color:#075985; font-weight:900 }
.idx td, .idx th { font-size:8.6pt; padding:1mm 1.6mm } .idx td:nth-child(2) { white-space:nowrap; font-weight:700 }
.ph { display:flex; gap:4mm; align-items:center; border-bottom:3px solid var(--w2); padding-bottom:3mm }
.badge { font-size:24pt; font-weight:900; color:#fff; background:linear-gradient(135deg,#0369A1,#075985); border-radius:3mm; min-width:17mm; text-align:center; line-height:1.45 }
.badge.new { background:linear-gradient(135deg,#B8860B,#7a5a00) }
.pname { font-size:21pt; font-weight:900; line-height:1.2 } .ptag { color:var(--w); font-weight:700; font-size:11pt }
.scores { display:flex; gap:2mm; margin:2.5mm 0 } .sc { flex:1; background:var(--bg); border:1px solid var(--line); border-radius:2mm; padding:.8mm 2.5mm; display:flex; justify-content:space-between; font-size:8.3pt; color:var(--mute) }
.sc b { color:var(--w); letter-spacing:1px } .sc i { color:#CBD5E1; font-style:normal } .tot { background:var(--w); color:#fff; border-radius:2mm; padding:0 3mm; font-weight:900; font-size:13pt; display:flex; align-items:center }
h4 { color:var(--w); font-size:11pt; margin:3mm 0 1mm; }
p { margin:.6mm 0 }
.two { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:5mm }
.steps { counter-reset:s; list-style:none; padding:0 } .steps li { counter-increment:s; position:relative; padding-right:8mm; margin:1.2mm 0 }
.steps li::before { content:counter(s); position:absolute; right:0; top:.3mm; width:5.5mm; height:5.5mm; border-radius:50%; background:var(--w2); color:#fff; font-size:8pt; font-weight:900; text-align:center; line-height:5.5mm }
.wow { background:var(--ink); color:#F1F5F9; border-radius:3mm; padding:3mm 5mm; margin-top:3mm } .wow h4 { color:#7DD3FC; margin-top:0 }
.risk th { background:#475569 } .risk td { font-size:9pt; vertical-align:top }
.mvp th { background:#0B6E4F } .mvp td:first-child { white-space:nowrap; font-weight:700; color:#0B6E4F }
.finmini { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:2mm; margin-top:2mm }
.k { background:#F0F9FF; border:1px solid #BAE6FD; border-radius:2mm; padding:2mm; text-align:center } .k span { display:block; font-size:7.8pt; color:var(--mute) } .k b { font-size:10.5pt; color:#075985 }
.verdict { border-radius:2mm; color:#fff; padding:2mm 4mm; margin-top:2mm; font-weight:700 }
.avoid { break-inside:avoid }
.rank td, .rank th { font-size:8.8pt; padding:1mm 1.6mm; text-align:center } .rank td:nth-child(2) { text-align:right } .rank tr.top td { background:#E0F2FE; font-weight:700 }
.picks { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:3mm } .pk { border-radius:3mm; padding:4mm; color:#fff; background:#075985 } .pk:nth-child(2){background:#0B6E4F} .pk:nth-child(3){background:#7C3AED}
.pk h3 { font-size:14pt } .pk p { font-size:9pt; opacity:.95 }
a { color:#0369A1; word-break:break-all }
"""


def score_bar(p):
    s = SCORES[p["id"]]
    cells = "".join(f'<div class="sc"><span>{lab}</span><b>{"●" * v}<i>{"●" * (5 - v)}</i></b></div>' for lab, v in zip(SCORE_LABELS, s))
    return f'<div class="scores">{cells}<div class="tot">{sum(s)}/20</div></div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def project(p):
    axis, color = AXES[p["axis"]]
    m = model(p)
    v_label, v_color, v_text = verdict(m["breakeven"])
    risks = "".join(f"<tr><td>{e(r)}</td><td>{e(mit)}</td></tr>" for r, mit in p["risks"])
    mvp = "".join(f"<tr><td>الأسابيع {e(w)}</td><td>{e(t)}</td></tr>" for w, t in p["mvp"])
    new = " new" if p.get("new") else ""
    return f"""
<section class="brk">
  <div class="ph"><div class="badge{new}">{p['id']:02d}</div>
    <div><div class="pname">{p['emoji']} {e(p['ar'])} <span class="en" style="font-size:.55em">{e(p['en'])}</span>
      <span class="chip" style="background:{color};vertical-align:middle">{e(axis)}</span>{' <span class="chip" style="background:#B8860B">⭐ جديد</span>' if p.get('new') else ''}</div>
    <div class="ptag">{e(p['tag'])}</div></div></div>
  {score_bar(p)}
  <h4>المشكلة</h4><p>{e(p['problem'])}</p>
  <h4>السياق والأدلة</h4>{ul(p['evidence'])}
  <h4>الحل</h4><p>{e(p['solution'])}</p>
  <div class="two">
    <div><h4>كيف يعمل خطوة بخطوة</h4><ol class="steps">{''.join(f'<li>{e(s)}</li>' for s in p['how'])}</ol></div>
    <div><h4>المميزات</h4>{ul(p['features'])}</div>
  </div>
  <div class="two">
    <div><h4>الذكاء الاصطناعي المستخدم</h4>{ul(p['ai'])}</div>
    <div><h4>مصادر البيانات</h4>{ul(p['data'])}</div>
  </div>
  <div class="wow avoid"><h4>⚡ لحظة الإبهار أمام اللجنة</h4><p>{e(p['wow'])}</p></div>
  <h4>التميّز والمنافسة</h4>{ul(p['diff'])}
  <div class="avoid"><h4>المخاطر وطرق التعامل</h4><table class="risk"><tr><th>الخطر</th><th>التعامل</th></tr>{risks}</table></div>
  <h4>الإطار التنظيمي والقانوني</h4><p>{e(p['legal'])}</p>
  <div class="two">
    <div class="avoid"><h4>مؤشرات قياس الأثر</h4>{ul(p['impact'])}</div>
    <div class="avoid"><h4>خطة النموذج الأولي (12 أسبوعًا)</h4><table class="mvp">{mvp}</table></div>
  </div>
  <div class="avoid"><h4>الخلاصة المالية (افتراضات أساسية)</h4>
    <div class="finmini">
      <div class="k"><span>الاستثمار الأولي</span><b>{money(m['capex'])}</b></div>
      <div class="k"><span>التمويل المطلوب</span><b>{money(m['funding'])}</b></div>
      <div class="k"><span>إيرادات السنة 3</span><b>{money(m['rev'][2])}</b></div>
      <div class="k"><span>نتيجة السنة 3</span><b>{money(m['ebitda'][2])}</b></div>
      <div class="k"><span>نقطة التعادل</span><b>{breakeven_text(m['breakeven'])}</b></div>
    </div>
    <div class="verdict" style="background:{v_color}">{e(v_label)}: {e(v_text)}</div>
  </div>
</section>"""


def build():
    ranked = sorted(PROJECTS, key=lambda p: (-score(p), p["id"]))
    index_rows = "".join(
        f"<tr><td>{p['id']}</td><td>{p['emoji']} {e(p['ar'])}</td><td>{e(AXES[p['axis']][0])}</td><td>{e(p['tag'])}</td><td>{score(p)}</td></tr>"
        for p in PROJECTS)
    rank_rows = "".join(
        f"<tr{' class=\"top\"' if i < 7 else ''}><td>{i + 1}</td><td>{p['emoji']} {e(p['ar'])} <span class='en'>{e(p['en'])}</span></td>"
        + "".join(f"<td>{v}</td>" for v in SCORES[p['id']])
        + f"<td><b>{score(p)}</b></td><td>{breakeven_text(model(p)['breakeven'])}</td></tr>"
        for i, p in enumerate(ranked))
    head = "".join(f"<th>{x}</th>" for x in ("#", "المشروع", *SCORE_LABELS, "المجموع", "التعادل"))
    sources = "".join(f'<li>{e(t)}: <a href="{u}">{e(u)}</a></li>' for t, u in SOURCES)

    sections, current = [], None
    for p in PROJECTS:
        if p["axis"] != current:
            current = p["axis"]
        sections.append(project(p))

    body = f"""
<div class="cover">
  <div class="team">NEXORA</div>
  <div>
    <h1>31 مشروعًا<br><span>لأمن الأردن المائي</span></h1>
    <div class="sub">الكتاب التفصيلي: 30 فكرة مائية بالذكاء الاصطناعي + مشروع دَمي<br>مُعدّ لمسابقة Jordan Students Pitch Competition — GEW Jordan</div>
    <div class="q">«{e(KING_QUOTE)}»<small>جلالة الملك عبدالله الثاني — خطاب العرش، 2 تشرين الثاني 2026</small></div>
    <div class="pills"><span class="pill">31 مشروعًا مفصّلًا</span><span class="pill">7 محاور</span><span class="pill">⭐ 5 أفكار جديدة</span><span class="pill">خلاصة مالية لكل مشروع</span></div>
  </div>
  <div style="font-size:9.5pt;opacity:.8">فريق NEXORA · تخصص Artificial Intelligence &amp; Data Science · تشرين الثاني 2026</div>
</div>

<section>
  <div class="band"><h2>لماذا المياه؟ ولماذا الآن؟</h2><p>المياه في قلب أولويات الدولة الأردنية، وهذه أقوى لحظة لتقديم حلول ريادية لها.</p></div>
  <div class="facts">
    <div class="fact"><b>×3</b>كرر جلالة الملك كلمة "المياه" في خطاب العرش 2026، ووجّه إلى "خطط استباقية".</div>
    <div class="fact"><b>~50%</b>نسبة الفاقد المائي التي تستهدف الاستراتيجية الوطنية خفضها لأقل من 25% بحلول 2040.</div>
    <div class="fact"><b>&lt;48 ساعة</b>أسبوعيًا: مدة وصول المياه لمعظم الأسر حسب تقارير منشورة.</div>
  </div>
  <div class="box"><h3>الناقل الوطني يغيّر المعادلة</h3><p>مشروع تحلية ونقل مياه العقبة–عمّان يستهدف نحو 300 مليون متر مكعب سنويًا، تغطي قرابة 40% من الاحتياجات البلدية بحلول 2030. هذا يفتح فرصًا ضخمة لحلول الكفاءة والطاقة والتحلية وإدارة الشبكات، وهي محاور كثير من مشاريع هذا الكتاب.</p></div>
  <div class="box"><h3>كيف تقرأ هذا الكتاب؟</h3>
    <ul><li>كل مشروع مقدّم بالتفصيل: المشكلة، والأدلة، والحل، وطريقة العمل، والمميزات، والتقنيات، والبيانات، ولحظة الإبهار، والمنافسة، والمخاطر، والإطار القانوني، ومؤشرات الأثر، وخطة النموذج الأولي، وخلاصة مالية.</li>
    <li>كل مشروع مقيّم على 4 معايير من 5: {"، ".join(SCORE_LABELS)}. التقييمات تقديرات أولية من الفريق.</li>
    <li>ملفات مرافقة: لوحات نموذج العمل (Business Model Canvas)، ودراسات الجدوى، والبروبوزلات، والعرض التقديمي، والمحاكي التفاعلي.</li></ul></div>
  <div class="disc"><b>تنبيه مهم:</b> {e(DISCLAIMER)} وكذلك عبارة "غير موجود في الأردن" تعني أننا لم نجد مثيلًا في بحث مبدئي، ويجب التحقق من المنافسين قبل الاعتماد.</div>
</section>

<section class="brk">
  <div class="band"><h2>فهرس المشاريع الـ 31</h2><p>مرتبة حسب المحاور: البيت، الشبكة، الزراعة، الصناعة، المستقبل، الخمسة الجديدة، الصحة.</p></div>
  <table class="idx"><tr><th>#</th><th>المشروع</th><th>المحور</th><th>الفكرة</th><th>التقييم</th></tr>{index_rows}</table>
</section>

{''.join(sections)}

<section class="brk">
  <div class="band"><h2>الترتيب النهائي</h2><p>حسب مجموع التقييم من 20، مع نقطة التعادل حسب الافتراضات الأساسية. المظلّل: أفضل 7.</p></div>
  <table class="rank"><tr>{head}</tr>{rank_rows}</table>
</section>

<section class="brk">
  <div class="band"><h2>🏆 توصيتنا</h2><p>إذا أردنا أعلى فرصة فوز في مسابقة تعتمد نموذج العمل والعرض:</p></div>
  <div class="picks">
    <div class="pk"><h3>🥇 خزّاني</h3><p>كل بيت أردني لديه خزان؛ نموذج أولي رخيص، وعرض حي مبهر، وزبونان (الأسرة وشركة المياه).</p></div>
    <div class="pk"><h3>🥈 وفّرلك</h3><p>نموذج العمل نفسه هو الإبهار: "ما بتدفع إلا من التوفير".</p></div>
    <div class="pk"><h3>🥉 عين العدّاد / نبض المضخّات</h3><p>حلول مباشرة لأكبر مشكلتين: الفاقد وكلفة الطاقة، بعائد مالي واضح.</p></div>
  </div>
  <div class="box"><h3>💡 الأقوى: منظومة بدل فكرة</h3><p><b>خزّاني + دور المي + عين العدّاد</b> = منصة واحدة تربط البيت بشركة المياه: "من خزان السطح لغرفة القرار، المي ما بتضيع". ومعها <b>استباق</b> كطبقة قرار وطنية تتجاوب مع توجيه جلالة الملك بالخطط الاستباقية.</p></div>
  <div class="box"><h3>المصادر</h3><ul>{sources}</ul></div>
</section>
"""
    return print_pdf(page("NEXORA — 31 مشروعًا لأمن الأردن المائي", body, CSS), OUT / "01_Water_Projects_Book.pdf")


if __name__ == "__main__":
    print(build())
