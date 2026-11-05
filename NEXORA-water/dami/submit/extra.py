"""Deeper DAMI slides: shortage causes, 8 system modules, emergency journey, cold chain, compatibility engine, donors, team."""

import art

TEAM = {
    "ar": [("عبد الرحمن بلال أبورمان", "هندسة البرمجيات"), ("مرح يوسف القيسي", "الذكاء الاصطناعي"), ("ندين محمد الصمادي", "الذكاء الاصطناعي"),
           ("داريا علي الشقاقحة", "الذكاء الاصطناعي"), ("عبد المنعم فادي قعدان", "الذكاء الاصطناعي")],
    "en": [("Abdulrahman Bilal Aburumman", "Software Engineer"), ("Marah Yousef Al-Qaisi", "AI Engineer"), ("Nadeen Mohammad Al-Smadi", "AI Engineer"),
           ("Darya Ali Al-Shaqaqha", "AI Engineer"), ("Abdulmonem Fadi Qadan", "AI Engineer")],
}

X = {
"ar": dict(
    causes_t="لماذا ينقص الدم؟",
    causes=[("📉", "تبرع موسمي", "ينخفض في الصيف ورمضان والامتحانات"), ("⏳", "صلاحية قصيرة", "الصفائح 5–7 أيام والكريات 35–42 يومًا"),
            ("🩸", "زمر نادرة", "O− مطلوبة دائمًا ومتوفرة قليلًا"), ("🗺️", "توزيع غير متوازن", "مخزون في المركز والأطراف تنتظر"),
            ("🚨", "طوارئ مفاجئة", "حادث واحد يستهلك مخزون أيام"), ("📞", "تنسيق يدوي", "اتصالات هاتفية بلا رؤية لحظية")],
    mods_t="النظام بالتفصيل: 8 وحدات ذكية",
    mods=[("🏷️", "مخزون ذكي", "رمز RFID لكل وحدة وصلاحيتها"), ("🧠", "التنبؤ بالطلب", "لكل زمرة ومستشفى لـ 14 يومًا"),
          ("⚖️", "الموازنة الذكية", "نقل الوحدات قبل انتهاء صلاحيتها"), ("🔎", "محرك التطابق", "الزمرة المتوافقة وأقرب مصدر"),
          ("🚁", "إدارة الأسطول", "مسار آمن وموافقة طيار مرخّص"), ("🌡️", "سلسلة التبريد", "حرارة كل ثانية وإنذار فوري"),
          ("🫂", "محرك المتبرعين", "استدعاء موجّه للزمرة الناقصة"), ("🏛️", "لوحة وطنية", "رؤية لحظية لوزارة الصحة")],
    jr_t="الطلب الطارئ: من الضغطة إلى الوصول",
    jr=[("0 ث", "المستشفى يطلب 6 وحدات O−"), ("5 ث", "الذكاء الاصطناعي يفحص المخزون والتوافق"), ("10 ث", "اختيار أفضل مصدر: درون أم سيارة"),
        ("1 د", "موافقة الطيار وتعبئة الصندوق"), ("≈ 9 د", "طيران مع تتبع الحرارة والموقع"), ("✓", "تسليم واستدعاء متبرعين للتعويض")],
    jr_note="الأزمنة من المحاكاة لمسافة نموذجية داخل عمّان",
    cc_t="الحساسات وسلسلة التبريد",
    cc=[("sensor", "ثلاجة بنك الدم", "حساس حرارة ومخزون لحظي"), ("bag", "كل وحدة دم", "رمز تعريف وتاريخ صلاحية"),
        ("thermo", "صندوق الدرون", "2–6°م كل ثانية + GPS"), ("clock", "إنذار فوري", "تبريد احتياطي وإبلاغ المستشفى"),
        ("phone", "سجل كامل", "تقرير حرارة مع كل شحنة")],
    cm_t="محرك التطابق: الزمرة الصحيحة دائمًا", cm_d="المتبرع", cm_r="المريض",
    cm=["O− يعطي الجميع", "AB+ يستقبل من الجميع", "إذا نفدت الزمرة يقترح البديل المتوافق فورًا"],
    dn_t="المتبرع الذكي",
    dn=[("✅", "مؤهل", "آخر تبرع قبل 90 يومًا أو أكثر"), ("📍", "قريب", "ضمن 12 كم من المستشفى"),
        ("🎯", "موجّه", "للزمرة الناقصة فقط"), ("❤️", "أثر واضح", "يعرف أين ذهبت وحدته")],
    tm_t="فريق دَمي", tm_s="هندسة البرمجيات + الذكاء الاصطناعي",
    notes=dict(causes="الدم ينقص لأسباب كثيرة: التبرع موسمي، والصلاحية قصيرة، والزمر النادرة، والتوزيع غير المتوازن، والطوارئ المفاجئة، والتنسيق اليدوي.",
               mods="النظام ليس درونز فقط: ثماني وحدات تبدأ من تتبع كل وحدة دم وتنتهي بلوحة وطنية لوزارة الصحة.",
               jr="من لحظة الطلب حتى الوصول: ثوانٍ لاتخاذ القرار، ودقائق للتوصيل.",
               cc="الحساسات تراقب الحرارة في الثلاجة والصندوق كل ثانية، وأي خلل يطلق إنذارًا فوريًا.",
               cm="محرك التطابق يعرف قواعد التوافق بين الزمر، ويقترح البديل الآمن إذا نفدت الزمرة.",
               dn="بدل حملات عامة، نستدعي المتبرع المؤهل القريب للزمرة الناقصة بالذات.",
               tm="نحن فريق دَمي: مهندس برمجيات وأربعة متخصصين في الذكاء الاصطناعي."),
),
"en": dict(
    causes_t="Why does blood run short?",
    causes=[("📉", "Seasonal donation", "drops in summer, Ramadan and exams"), ("⏳", "Short shelf life", "platelets 5–7 days, red cells 35–42"),
            ("🩸", "Rare types", "O− always needed, rarely available"), ("🗺️", "Uneven distribution", "stock in the center, outskirts wait"),
            ("🚨", "Sudden emergencies", "one accident uses days of stock"), ("📞", "Manual coordination", "phone calls, no live view")],
    mods_t="The system in depth: 8 smart modules",
    mods=[("🏷️", "Smart inventory", "RFID per unit with expiry"), ("🧠", "Demand forecasting", "per type & hospital, 14 days"),
          ("⚖️", "Smart balancing", "move units before they expire"), ("🔎", "Matching engine", "compatible type, nearest source"),
          ("🚁", "Fleet management", "safe route, licensed pilot approval"), ("🌡️", "Cold chain", "temperature every second, alarms"),
          ("🫂", "Donor engine", "targeted call-up for missing type"), ("🏛️", "National dashboard", "live view for the Ministry")],
    jr_t="Emergency request: from tap to arrival",
    jr=[("0 s", "Hospital requests 6 units O−"), ("5 s", "AI checks stock & compatibility"), ("10 s", "Best source: drone or car"),
        ("1 min", "Pilot approval, box packed"), ("≈ 9 min", "Flight with live temperature & GPS"), ("✓", "Delivered, donors called to restock")],
    jr_note="Times from the simulation for a typical distance in Amman",
    cc_t="Sensors & the cold chain",
    cc=[("sensor", "Blood-bank fridge", "temperature & live stock sensor"), ("bag", "Every blood unit", "ID tag and expiry date"),
        ("thermo", "Drone box", "2–6°C every second + GPS"), ("clock", "Instant alarm", "backup cooling, hospital notified"),
        ("phone", "Full log", "temperature report with every shipment")],
    cm_t="Matching engine: always the right type", cm_d="Donor", cm_r="Patient",
    cm=["O− gives to everyone", "AB+ receives from everyone", "If a type runs out, it proposes a compatible alternative instantly"],
    dn_t="The smart donor",
    dn=[("✅", "Eligible", "last donation 90+ days ago"), ("📍", "Nearby", "within 12 km of the hospital"),
        ("🎯", "Targeted", "only for the missing type"), ("❤️", "Visible impact", "knows where their unit went")],
    tm_t="Team DAMI", tm_s="Software Engineering + Artificial Intelligence",
    notes=dict(causes="Blood runs short for many reasons: seasonal donation, short shelf life, rare types, uneven distribution, sudden emergencies and manual coordination.",
               mods="It's not just drones: eight modules, from tracking every unit to a national dashboard for the Ministry of Health.",
               jr="From request to arrival: seconds to decide, minutes to deliver.",
               cc="Sensors watch temperature in the fridge and the box every second; any fault triggers an instant alarm.",
               cm="The matching engine knows blood compatibility rules and proposes a safe alternative if a type runs out.",
               dn="Instead of generic drives, we call eligible nearby donors for exactly the missing type.",
               tm="We are Team DAMI: one software engineer and four AI engineers."),
),
}

TYPES = ["O−", "O+", "A−", "A+", "B−", "B+", "AB−", "AB+"]


def compatible(donor, patient):
    d, p = donor.rstrip("−+"), patient.rstrip("−+")
    abo = d == "O" or d == p or p == "AB"
    rh = donor.endswith("−") or patient.endswith("+")
    return abo and rh


def matrix():
    cell = 74
    out = [f'<svg viewBox="0 0 {cell * 9 + 20} {cell * 9 + 20}" width="{cell * 9 + 20}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg" font-family="Cairo">']
    for i, t in enumerate(TYPES):
        out.append(f'<text x="{cell * (i + 1) + cell / 2}" y="{cell / 2 + 12}" text-anchor="middle" font-size="26" font-weight="900" fill="#F87171">{t}</text>')
        out.append(f'<text x="{cell / 2}" y="{cell * (i + 1) + cell / 2 + 10}" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">{t}</text>')
    for r, p in enumerate(TYPES):
        for c, d in enumerate(TYPES):
            x, y = cell * (c + 1), cell * (r + 1)
            ok = compatible(d, p)
            out.append(f'<rect x="{x + 4}" y="{y + 4}" width="{cell - 8}" height="{cell - 8}" rx="12" fill="{"#DC2626" if ok else "#ffffff0d"}"/>')
            if ok:
                out.append(f'<text x="{x + cell / 2}" y="{y + cell / 2 + 11}" text-anchor="middle" font-size="30" fill="#fff">✓</text>')
    out.append("</svg>")
    return "".join(out)


def tiles(items, cols, size="big"):
    fs = (60, 38, 27) if size == "big" else (56, 34, 25)
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:30px">'
            + "".join(f'<div class="card" style="padding:30px 24px"><div style="font-size:{fs[0]}px">{i}</div><b style="font-size:{fs[1]}px;margin-top:8px">{a}</b><span style="font-size:{fs[2]}px">{b}</span></div>' for i, a, b in items)
            + "</div>")


def causes(s, T, lang, rtl, start, end):
    x = X[lang]
    s(f"""<div class="abs h" style="left:0;right:0;top:90px;text-align:center">{x['causes_t']}</div>
<div class="abs" style="left:150px;right:150px;top:270px">{tiles(x['causes'], 3)}</div>""", note=x["notes"]["causes"])


def modules(s, T, lang, rtl, start, end):
    x = X[lang]
    s(f"""<div class="abs h" style="left:0;right:0;top:80px;text-align:center">{x['mods_t']}</div>
<div class="abs" style="left:110px;right:110px;top:260px">{tiles(x['mods'], 4, 'small')}</div>""", note=x["notes"]["mods"])


def journey(s, T, lang, rtl, start, end):
    x = X[lang]
    n = len(x["jr"])
    xs = [1700 - i * 1480 / (n - 1) for i in range(n)] if rtl else [220 + i * 1480 / (n - 1) for i in range(n)]
    nodes = "".join(
        f'<div class="abs dot" style="left:{px - 28}px;top:512px;{"background:#16A34A;box-shadow:0 0 0 14px #16A34A33" if i == n - 1 else ""}"></div>'
        f'<div class="abs" style="left:{px - 150}px;width:300px;top:{290 if i % 2 == 0 else 610}px;text-align:center">'
        f'<div style="font-size:52px;font-weight:900;color:#F87171;direction:ltr;unicode-bidi:isolate">{a}</div><div style="font-size:31px;font-weight:700;line-height:1.35">{b}</div></div>'
        for i, ((a, b), px) in enumerate(zip(x["jr"], xs)))
    s(f"""<div class="abs h" style="left:0;right:0;top:100px;text-align:center">{x['jr_t']}</div>
<div class="abs tl" style="left:220px;width:1480px;top:535px"></div>{nodes}<div class="src" style="{start}:120px">{x['jr_note']}</div>""", note=x["notes"]["jr"])


def coldchain(s, T, lang, rtl, start, end):
    x = X[lang]
    rows = "".join(f'<div class="row" style="gap:26px;margin-bottom:30px"><div style="background:#DC2626;border-radius:24px;padding:14px;display:flex">{art.icon(k, 78)}</div>'
                   f'<div><div style="font-size:40px;font-weight:900">{a}</div><div class="m" style="font-size:28px">{b}</div></div></div>' for k, a, b in x["cc"])
    s(f"""<div class="abs h" style="{start}:110px;top:90px">{x['cc_t']}</div>
<div class="abs row" style="{end}:110px;top:270px;gap:40px;align-items:flex-end">{art.fridge(300)}<div style="font-size:90px;color:#F87171">{"←" if rtl else "→"}</div>{art.drone(520)}</div>
<div class="abs" style="{start}:120px;top:250px">{rows}</div>""", note=x["notes"]["cc"])


def compat(s, T, lang, rtl, start, end):
    x = X[lang]
    s(f"""<div class="abs h" style="left:0;right:0;top:70px;text-align:center">{x['cm_t']}</div>
<div class="abs" style="{end}:150px;top:200px">{matrix()}<div class="m" style="text-align:center;font-size:26px;direction:ltr">↑ {x['cm_r']} · {x['cm_d']} →</div></div>
<div class="abs" style="{start}:130px;top:330px;width:760px">{''.join(f'<div class="call" style="font-size:40px;padding:24px 34px;margin-bottom:34px">{t}</div>' for t in x['cm'])}</div>""", note=x["notes"]["cm"])


def donors(s, T, lang, rtl, start, end, shot):
    x = X[lang]
    s(f"""<div class="abs h" style="left:0;right:0;top:70px;text-align:center">{x['dn_t']}</div>
<div class="abs shot" style="{end}:110px;top:230px;width:1000px"><img src="{shot}"></div>
<div class="abs" style="{start}:120px;top:240px;width:640px">{''.join(f'<div class="row" style="gap:24px;margin-bottom:40px"><div style="font-size:64px">{i}</div><div><div style="font-size:42px;font-weight:900">{a}</div><div class="m" style="font-size:29px">{b}</div></div></div>' for i, a, b in x['dn'])}</div>""", note=x["notes"]["dn"])


def team(s, T, lang, rtl, start, end):
    x = X[lang]
    cards = "".join(
        f'<div class="card" style="padding:40px 26px;"><div style="display:inline-flex;background:#DC2626;border-radius:50%;padding:22px">{art.icon("people", 90)}</div>'
        f'<b style="font-size:34px;line-height:1.3">{n}</b><span>{role or "&nbsp;"}</span></div>' for n, role in TEAM[lang])
    s(f"""<div class="abs h" style="left:0;right:0;top:120px;text-align:center">{x['tm_t']}</div>
<div class="abs l red" style="left:0;right:0;top:250px;text-align:center">{x['tm_s']}</div>
<div class="abs" style="left:110px;right:110px;top:400px;display:grid;grid-template-columns:repeat(5,1fr);gap:26px">{cards}</div>""", note=x["notes"]["tm"])
