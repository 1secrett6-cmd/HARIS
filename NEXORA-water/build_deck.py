"""05 — the pitch deck: 16:9 PDF (designed) and an editable PPTX with the same storyline."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

from common import (AXES, KING_QUOTE, OUT, PROJECTS, SCORE_LABELS, SCORES, breakeven_text, e, model, money, page,
                    print_pdf, score)

TOP = [1, 16, 6, 10, 31, 21, 29]

CSS = """
@page { size:338.67mm 190.5mm; margin:0 }
body { font-size:13pt }
.s { width:338.67mm; height:190.5mm; padding:14mm 18mm; break-after:page; position:relative; overflow:hidden; background:#fff }
.dark { color:#fff; background:linear-gradient(150deg,#04223A,#075985 60%,#0B6E4F) }
.s h1 { font-size:46pt; font-weight:900; line-height:1.1 } .s h2 { font-size:28pt; font-weight:900; color:#075985; margin-bottom:5mm }
.dark h2 { color:#7DD3FC }
.big { font-size:20pt; font-weight:700 }
.grid3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:6mm }
.card { border-radius:4mm; padding:6mm; background:#F0F9FF; border:1px solid #BAE6FD } .card b { display:block; font-size:30pt; color:#075985; font-weight:900 }
.foot { position:absolute; bottom:6mm; left:18mm; font-size:9pt; color:#94A3B8; letter-spacing:.3em }
.pnum { font-size:60pt; font-weight:900; color:#E0F2FE; position:absolute; top:6mm; left:16mm }
.ptitle { font-size:34pt; font-weight:900 } .ptag { font-size:15pt; color:#0369A1; font-weight:700; margin:2mm 0 5mm }
.cols { display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:8mm }
.blk h4 { color:#0369A1; font-size:12pt; margin:2mm 0 1mm } .blk p, .blk li { font-size:11pt; line-height:1.55 }
.kp { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:3mm; margin-top:3mm }
.kp div { background:#F0F9FF; border-radius:3mm; padding:3mm; text-align:center; font-size:10pt; color:#475569 } .kp b { display:block; font-size:16pt; color:#075985 }
.wow { background:#0F172A; color:#F1F5F9; border-radius:3mm; padding:4mm 5mm; font-size:11pt; margin-top:3mm }
.axes { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:4mm }
.ax { border-radius:3mm; padding:4mm; color:#fff } .ax b { font-size:24pt; display:block }
table { font-size:11pt } th { background:#075985 } td { padding:1.6mm 2mm }
"""


def slide(inner, cls=""):
    return f'<section class="s {cls}">{inner}<div class="foot">NEXORA · 2026</div></section>'


def project_slide(p):
    m = model(p)
    return slide(f"""<div class="pnum">{p['id']:02d}</div>
  <div class="ptitle">{p['emoji']} {e(p['ar'])} <span class="en" style="font-size:.45em">{e(p['en'])}</span>
    <span class="chip" style="background:{AXES[p['axis']][1]};font-size:10pt;vertical-align:middle">{e(AXES[p['axis']][0])}</span></div>
  <div class="ptag">{e(p['tag'])}</div>
  <div class="cols">
    <div class="blk"><h4>المشكلة</h4><p>{e(p['problem'])}</p><h4>الحل</h4><p>{e(p['solution'])}</p></div>
    <div class="blk"><h4>الزبون ومصادر الدخل</h4><ul>{''.join(f'<li>{e(x)}</li>' for x in p['bmc']['cs'][:2] + p['bmc']['rev'][:2])}</ul>
      <div class="kp"><div>الاستثمار الأولي<b>{money(m['capex'])}</b></div><div>إيرادات س3<b>{money(m['rev'][2])}</b></div>
      <div>التعادل<b>{breakeven_text(m['breakeven'])}</b></div><div>التقييم<b>{score(p)}/20</b></div></div>
      <div class="wow">⚡ {e(p['wow'])}</div></div>
  </div>""")


def html_deck():
    axes_count = {}
    for p in PROJECTS:
        axes_count[p["axis"]] = axes_count.get(p["axis"], 0) + 1
    axes = "".join(f'<div class="ax" style="background:{c}"><b>{axes_count.get(k, 0)}</b>{e(n)}</div>' for k, (n, c) in AXES.items())
    ranked = sorted(PROJECTS, key=lambda p: (-score(p), p["id"]))[:10]
    rank_rows = "".join(f"<tr><td>{i + 1}</td><td>{p['emoji']} {e(p['ar'])}</td>" + "".join(f"<td>{v}</td>" for v in SCORES[p['id']]) + f"<td><b>{score(p)}</b></td></tr>" for i, p in enumerate(ranked))
    head = "".join(f"<th>{x}</th>" for x in ("#", "المشروع", *SCORE_LABELS, "المجموع"))
    slides = [
        slide(f"""<div style="letter-spacing:.4em;font-weight:900;opacity:.8">NEXORA</div><div style="height:22mm"></div>
<h1>31 مشروعًا لأمن الأردن المائي<br><span style="color:#7DD3FC">بالذكاء الاصطناعي</span></h1>
<p class="big" style="margin-top:8mm;opacity:.9">من خزان السطح… لغرفة القرار الوطني</p>
<p style="margin-top:14mm;font-size:14pt">«{e(KING_QUOTE)}»<br><span style="font-size:10pt;opacity:.8">جلالة الملك عبدالله الثاني — خطاب العرش 2026</span></p>""", "dark"),
        slide("""<h2>المشكلة: المياه أولوية وطنية</h2><div class="grid3">
<div class="card"><b>×3</b>كرر جلالة الملك كلمة "المياه" في خطاب العرش، ووجّه إلى خطط استباقية</div>
<div class="card"><b>~50%</b>فاقد تستهدف الاستراتيجية الوطنية خفضه لأقل من 25% بحلول 2040</div>
<div class="card"><b>&lt;48 ساعة</b>أسبوعيًا: وصول المياه لمعظم الأسر حسب تقارير منشورة</div></div>
<p class="big" style="margin-top:10mm">التحدي ليس فقط إنتاج مياه أكثر، بل ألا نخسر ما ننتجه، وأن نقرر أسرع وأذكى.</p>"""),
        slide(f"""<h2>محفظتنا: 31 مشروعًا في 7 محاور</h2><div class="axes">{axes}</div>
<p class="big" style="margin-top:8mm">كل مشروع جاهز بـ: بروبوزل، نموذج عمل، دراسة جدوى، ومحاكي تفاعلي.</p>"""),
        *[project_slide(p) for p in PROJECTS],
        slide(f"""<h2>الترتيب: أقوى 10 مشاريع</h2><table><tr>{head}</tr>{rank_rows}</table>"""),
        slide("""<h2>💡 الأقوى: منظومة بدل فكرة</h2>
<p class="big">خزّاني + دور المي + عين العدّاد = منصة تربط البيت بشركة المياه</p>
<p style="font-size:15pt;margin-top:6mm">المواطن يعرف متى تصل المياه ومتى يفرغ خزانه. وشركة المياه تحصل على أول خريطة لحظية للاستهلاك والفاقد.</p>
<p style="font-size:15pt">ومعها <b>استباق</b> كطبقة قرار وطنية، و<b>دَمي</b> كنموذج إنقاذ أرواح بالدرون.</p>"""),
        slide("""<h2>خارطة الطريق</h2><div class="grid3">
<div class="card"><b>0–3 أشهر</b>نموذج أولي ومقابلات عملاء وأول تجربة ميدانية</div>
<div class="card"><b>3–12 شهرًا</b>أول عملاء يدفعون وشراكة مع جهة رسمية</div>
<div class="card"><b>1–3 سنوات</b>توسع وطني ثم إقليمي في الدول الجافة</div></div>"""),
        slide("""<h2>ما نحتاجه</h2><ul style="font-size:17pt;line-height:1.9">
<li>إرشاد في ريادة الأعمال والشراكات الحكومية</li><li>شريك تجريبي (شركة مياه، مستشفى، بلدية، جامعة)</li>
<li>تمويل أولي للنموذج الأولي والتجارب الميدانية</li><li>منصة لعرض المشاريع على صناع القرار</li></ul>"""),
        slide("""<div style="height:40mm"></div><h1 style="text-align:center">شكرًا</h1><p class="big" style="text-align:center;margin-top:6mm">NEXORA · نحوّل كل نقطة مي إلى قرار ذكي</p>""", "dark"),
    ]
    return page("NEXORA Pitch Deck", "".join(slides), CSS, size="338.67mm 190.5mm")


def pptx_deck(path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    navy, sky, white = RGBColor(0x07, 0x59, 0x85), RGBColor(0x7D, 0xD3, 0xFC), RGBColor(0xFF, 0xFF, 0xFF)

    def text(s, x, y, w, h, lines, size=18, color=None, bold=False):
        tb = s.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, line in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = PP_ALIGN.RIGHT
            para._pPr.set("rtl", "1")
            run = para.add_run()
            run.text = line
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.name = "Cairo"
            if color is not None:
                run.font.color.rgb = color
        return tb

    def bg(s, color):
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = color

    W = 12192000
    s = prs.slides.add_slide(blank)
    bg(s, navy)
    text(s, 600000, 1500000, W - 1200000, 1500000, ["31 مشروعًا لأمن الأردن المائي بالذكاء الاصطناعي"], 40, white, True)
    text(s, 600000, 3200000, W - 1200000, 1200000, [f"«{KING_QUOTE}»", "فريق NEXORA · Jordan Students Pitch Competition"], 18, sky)
    for p in PROJECTS:
        m = model(p)
        s = prs.slides.add_slide(blank)
        text(s, 500000, 300000, W - 1000000, 700000, [f"{p['id']:02d} · {p['ar']} · {p['en']}"], 30, navy, True)
        text(s, 500000, 950000, W - 1000000, 500000, [p["tag"]], 16, RGBColor(0x03, 0x69, 0xA1), True)
        text(s, 6400000, 1500000, 5300000, 4300000, ["المشكلة", p["problem"], "", "الحل", p["solution"]], 12)
        text(s, 500000, 1500000, 5600000, 4300000,
             ["الزبون", *p["bmc"]["cs"][:2], "", "مصادر الدخل", *p["bmc"]["rev"][:3], "",
              f"الاستثمار الأولي: {money(m['capex'])}", f"إيرادات السنة 3: {money(m['rev'][2])}",
              f"التعادل: {breakeven_text(m['breakeven'])}", "", "العرض الحي: " + p["wow"]], 12)
    s = prs.slides.add_slide(blank)
    bg(s, navy)
    text(s, 600000, 2500000, W - 1200000, 1500000, ["شكرًا · NEXORA"], 44, white, True)
    prs.save(path)
    return path


def build():
    pdf = print_pdf(html_deck(), OUT / "05_Pitch_Deck.pdf")
    pptx = pptx_deck(OUT / "05_Pitch_Deck.pptx")
    return pdf, pptx


if __name__ == "__main__":
    print(build())
