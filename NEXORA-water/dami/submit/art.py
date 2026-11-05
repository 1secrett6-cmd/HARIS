"""Inline SVG illustrations for the DAMI submission deck (drone, blood bag, hospital, sensors, system diagram)."""

RED, RED2, DARK, TEAL, ICE = "#DC2626", "#F87171", "#1C0508", "#14B8A6", "#7DD3FC"


def drone(w=900, label_box=True):
    rotors = ""
    for cx in (150, 750):
        for cy in (120, 330):
            arm_y = cy
            rotors += f'<line x1="450" y1="225" x2="{cx}" y2="{arm_y}" stroke="#E7E5E4" stroke-width="22" stroke-linecap="round"/>'
    for cx in (150, 750):
        for cy in (120, 330):
            rotors += (f'<circle cx="{cx}" cy="{cy}" r="34" fill="#F5F5F4"/>'
                       f'<ellipse cx="{cx}" cy="{cy - 30}" rx="125" ry="22" fill="#ffffff" opacity=".18"/>'
                       f'<ellipse cx="{cx}" cy="{cy - 30}" rx="125" ry="7" fill="#ffffff" opacity=".55"/>')
    box = ""
    if label_box:
        box = f"""<line x1="400" y1="300" x2="390" y2="430" stroke="#A8A29E" stroke-width="5"/><line x1="500" y1="300" x2="510" y2="430" stroke="#A8A29E" stroke-width="5"/>
<rect x="330" y="420" width="240" height="170" rx="26" fill="#F8FAFC" stroke="{ICE}" stroke-width="8"/>
<rect x="330" y="420" width="240" height="44" rx="22" fill="{ICE}"/>
<text x="450" y="452" text-anchor="middle" font-size="30" font-weight="800" fill="#0C4A6E" font-family="Cairo">2–6°C</text>
<path d="M450 490 C 420 535, 412 552, 450 572 C 488 552, 480 535, 450 490 Z" fill="{RED}"/>"""
    return f"""<svg viewBox="0 0 900 620" width="{w}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="dg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{RED}" stop-opacity=".45"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="450" cy="300" rx="430" ry="290" fill="url(#dg)"/>{rotors}
<rect x="330" y="160" width="240" height="140" rx="48" fill="#FAFAF9"/><rect x="330" y="160" width="240" height="140" rx="48" fill="none" stroke="{RED}" stroke-width="8"/>
<rect x="430" y="185" width="40" height="90" rx="6" fill="{RED}"/><rect x="405" y="210" width="90" height="40" rx="6" fill="{RED}"/>
<circle cx="450" cy="310" r="16" fill="#1E293B"/>{box}</svg>"""


def bag(w=260, level=1.0, color=RED):
    h = 300 * level
    return f"""<svg viewBox="0 0 220 360" width="{w}" style="direction:ltr" xmlns="http://www.w3.org/2000/svg">
<rect x="95" y="0" width="30" height="40" rx="8" fill="#E7E5E4"/>
<rect x="20" y="36" width="180" height="300" rx="40" fill="#ffffff22" stroke="#FECACA" stroke-width="6"/>
<clipPath id="bc{int(level * 100)}"><rect x="23" y="39" width="174" height="294" rx="37"/></clipPath>
<rect x="20" y="{336 - h}" width="180" height="{h}" fill="{color}" clip-path="url(#bc{int(level * 100)})"/>
<rect x="55" y="90" width="110" height="60" rx="10" fill="#fff" opacity=".9"/><text x="110" y="132" text-anchor="middle" font-size="34" font-weight="900" fill="{RED}" font-family="Cairo">O−</text>
<path d="M110 360 L110 336" stroke="#E7E5E4" stroke-width="10"/></svg>"""


def hospital(w=300, tint=TEAL):
    return f"""<svg viewBox="0 0 300 260" width="{w}" xmlns="http://www.w3.org/2000/svg">
<rect x="30" y="60" width="240" height="190" rx="18" fill="#F5F5F4"/><rect x="100" y="10" width="100" height="70" rx="14" fill="{tint}"/>
<rect x="140" y="20" width="20" height="50" rx="4" fill="#fff"/><rect x="125" y="35" width="50" height="20" rx="4" fill="#fff"/>
{''.join(f'<rect x="{x}" y="{y}" width="40" height="34" rx="6" fill="#CBD5E1"/>' for x in (55, 130, 205) for y in (100, 155))}
<rect x="125" y="200" width="50" height="50" rx="6" fill="{tint}"/><rect x="0" y="244" width="300" height="12" rx="6" fill="#ffffff44"/></svg>"""


def fridge(w=240):
    return f"""<svg viewBox="0 0 240 320" width="{w}" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="200" height="290" rx="22" fill="#F8FAFC"/><rect x="38" y="40" width="164" height="250" rx="12" fill="#E0F2FE"/>
{''.join(f'<rect x="{x}" y="{y}" width="34" height="46" rx="8" fill="{RED}"/>' for x in (54, 103, 152) for y in (60, 128, 196))}
<circle cx="200" cy="40" r="22" fill="{TEAL}"/><path d="M226 14 a40 40 0 0 1 0 52 M240 0 a60 60 0 0 1 0 80" stroke="{TEAL}" stroke-width="6" fill="none"/></svg>"""


def phone(img, w=300):
    return f"""<div style="width:{w}px;border-radius:{w * .13}px;background:#0F172A;padding:{w * .045}px;box-shadow:0 30px 80px #000a">
<div style="border-radius:{w * .09}px;overflow:hidden;height:{w * 1.9}px;background:#fff"><img src="{img}" style="height:100%;object-fit:cover;object-position:right top;width:100%"></div></div>"""


def icon(kind, size=110, color="#fff"):
    paths = {
        "brain": '<path d="M40 30 a18 18 0 0 1 30 -8 a18 18 0 0 1 30 8 a18 18 0 0 1 8 30 a18 18 0 0 1 -8 30 a18 18 0 0 1 -30 8 a18 18 0 0 1 -30 -8 a18 18 0 0 1 -8 -30 a18 18 0 0 1 8 -30 Z" fill="none" stroke="C" stroke-width="7"/><path d="M70 22 V98 M45 50 h18 M78 70 h20 M48 78 h14" stroke="C" stroke-width="7" stroke-linecap="round"/>',
        "people": '<circle cx="45" cy="42" r="16" fill="C"/><circle cx="90" cy="42" r="16" fill="C"/><path d="M15 100 a30 30 0 0 1 60 0 Z M60 100 a30 30 0 0 1 60 0 Z" fill="C"/>',
        "drone": '<rect x="45" y="50" width="50" height="26" rx="10" fill="C"/><path d="M45 58 L18 38 M95 58 L122 38 M45 68 L18 88 M95 68 L122 88" stroke="C" stroke-width="7"/><ellipse cx="18" cy="34" rx="18" ry="5" fill="C"/><ellipse cx="122" cy="34" rx="18" ry="5" fill="C"/><ellipse cx="18" cy="92" rx="18" ry="5" fill="C"/><ellipse cx="122" cy="92" rx="18" ry="5" fill="C"/>',
        "sensor": '<circle cx="70" cy="70" r="14" fill="C"/><path d="M45 45 a35 35 0 0 0 0 50 M95 45 a35 35 0 0 1 0 50 M28 28 a60 60 0 0 0 0 84 M112 28 a60 60 0 0 1 0 84" stroke="C" stroke-width="7" fill="none" stroke-linecap="round"/>',
        "cloud": '<path d="M38 100 a26 26 0 0 1 4 -52 a32 32 0 0 1 60 -4 a26 26 0 0 1 2 56 Z" fill="none" stroke="C" stroke-width="7"/><text x="72" y="88" text-anchor="middle" font-size="30" font-weight="900" fill="C" font-family="Cairo">AI</text>',
        "phone": '<rect x="40" y="12" width="60" height="116" rx="12" fill="none" stroke="C" stroke-width="7"/><circle cx="70" cy="110" r="5" fill="C"/>',
        "thermo": '<rect x="58" y="14" width="24" height="80" rx="12" fill="none" stroke="C" stroke-width="7"/><circle cx="70" cy="104" r="20" fill="C"/><rect x="66" y="50" width="8" height="50" fill="C"/>',
        "gps": '<path d="M70 125 C 40 85, 30 70, 30 52 a40 40 0 0 1 80 0 c0 18 -10 33 -40 73 Z" fill="C"/><circle cx="70" cy="52" r="14" fill="#1C0508"/>',
        "chute": '<path d="M20 60 a50 40 0 0 1 100 0 Z" fill="C"/><path d="M20 60 L70 115 L120 60 M70 60 V115" stroke="C" stroke-width="4" fill="none"/><rect x="58" y="108" width="24" height="20" rx="4" fill="C"/>',
        "clock": '<circle cx="70" cy="70" r="50" fill="none" stroke="C" stroke-width="8"/><path d="M70 40 V70 L92 84" stroke="C" stroke-width="8" stroke-linecap="round" fill="none"/>',
        "money": '<rect x="14" y="36" width="112" height="68" rx="12" fill="none" stroke="C" stroke-width="7"/><circle cx="70" cy="70" r="16" fill="none" stroke="C" stroke-width="7"/>',
        "drop": '<path d="M70 14 C 40 60, 28 80, 28 96 a42 42 0 0 0 84 0 c0 -16 -12 -36 -42 -82 Z" fill="C"/>',
        "bag": '<rect x="38" y="24" width="64" height="96" rx="18" fill="none" stroke="C" stroke-width="7"/><rect x="38" y="70" width="64" height="50" rx="10" fill="C"/><rect x="62" y="8" width="16" height="18" rx="4" fill="C"/>',
    }
    return f'<svg viewBox="0 0 140 140" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{paths[kind].replace("C", color)}</svg>'


def system(labels, w=1700, rtl=False):
    """Architecture: blood-bank sensors -> DAMI AI cloud -> hospital app -> drone with sensor box -> hospital."""
    kinds = ["sensor", "cloud", "phone", "drone"]
    xs = [230, 640, 1050, 1460]
    if rtl:
        kinds, labels = kinds[::-1], labels[::-1]
    nodes = [(k, lab, x) for k, lab, x in zip(kinds, labels, xs)]
    out = [f'<svg viewBox="0 0 1700 520" width="{w}" xmlns="http://www.w3.org/2000/svg" font-family="Cairo">']
    for i in range(3):
        x1, x2 = nodes[i][2] + 130, nodes[i + 1][2] - 130
        head = f'<path d="M{x1 + 6} 182 L{x1 - 20} 200 L{x1 + 6} 218 Z" fill="{RED2}"/>' if rtl else f'<path d="M{x2 - 6} 182 L{x2 + 20} 200 L{x2 - 6} 218 Z" fill="{RED2}"/>'
        out.append(f'<path d="M{x1} 200 H{x2}" stroke="{RED2}" stroke-width="8" stroke-dasharray="20 14"/>{head}')
    for kind, (title, sub), x in nodes:
        out.append(f'<circle cx="{x}" cy="200" r="120" fill="#ffffff10" stroke="#ffffff30" stroke-width="3"/>'
                   f'<g transform="translate({x - 70},130)">{icon(kind, 140)[len("<svg viewBox=\"0 0 140 140\" width=\"140\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\">"):-6]}</g>'
                   f'<text x="{x}" y="380" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">{title}</text>'
                   f'<text x="{x}" y="430" text-anchor="middle" font-size="28" fill="#FECACA">{sub}</text>')
    out.append("</svg>")
    return "".join(out)
