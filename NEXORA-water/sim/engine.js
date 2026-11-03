/* NEXORA simulators: hub, per-project live demos, feasibility simulator. Synthetic data only. */
(function () {
  "use strict";
  const D = window.DATA;
  const $ = (sel, root) => (root || document).querySelector(sel);
  const timers = [];
  const every = (ms, fn) => { const t = setInterval(fn, ms); timers.push(t); return t; };
  const stopAll = () => { while (timers.length) clearInterval(timers.pop()); };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const fmt = (v, d = 0) => Number(v).toLocaleString("en-US", { maximumFractionDigits: d, minimumFractionDigits: d });
  const money = (v) => (v < 0 ? "−" : "") + fmt(Math.abs(Math.round(v))) + " د.أ";
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

  /* ---------- tiny SVG charts ---------- */
  function lineChart(series, opt) {
    const W = 640, H = opt.h || 220, pl = 46, pr = 10, pt = 12, pb = 24;
    const all = series.flatMap((s) => s.data).concat(opt.extra || []);
    let lo = opt.min !== undefined ? opt.min : Math.min(...all), hi = opt.max !== undefined ? opt.max : Math.max(...all);
    if (hi === lo) hi = lo + 1;
    const n = Math.max(...series.map((s) => s.data.length));
    const x = (i) => pl + (i / Math.max(1, n - 1)) * (W - pl - pr);
    const y = (v) => pt + (hi - v) / (hi - lo) * (H - pt - pb);
    let g = "";
    for (let t = 0; t <= 4; t++) {
      const v = lo + (hi - lo) * t / 4;
      g += `<line x1="${pl}" x2="${W - pr}" y1="${y(v)}" y2="${y(v)}" class="grid"/><text x="${pl - 6}" y="${y(v) + 4}" class="ax" text-anchor="end">${fmt(v, Math.abs(hi - lo) < 10 ? 1 : 0)}</text>`;
    }
    (opt.thr || []).forEach((t) => { g += `<line x1="${pl}" x2="${W - pr}" y1="${y(t.v)}" y2="${y(t.v)}" stroke="${t.c}" stroke-dasharray="5 4"/><text x="${W - pr}" y="${y(t.v) - 4}" class="ax" text-anchor="end" fill="${t.c}">${esc(t.l)}</text>`; });
    (opt.xl || []).forEach((l, i, a) => { g += `<text x="${x(i * (n - 1) / Math.max(1, a.length - 1))}" y="${H - 6}" class="ax" text-anchor="middle">${esc(l)}</text>`; });
    series.forEach((s) => {
      if (s.bars) {
        const bw = (W - pl - pr) / n * 0.7;
        s.data.forEach((v, i) => { g += `<rect x="${x(i) - bw / 2}" y="${Math.min(y(v), y(Math.max(lo, 0)))}" width="${bw}" height="${Math.abs(y(v) - y(Math.max(lo, 0)))}" fill="${s.c}" rx="2" opacity="${s.o || 1}"/>`; });
      } else {
        const pts = s.data.map((v, i) => `${x(i)},${y(v)}`).join(" ");
        if (s.fill) g += `<polygon points="${x(0)},${y(lo)} ${pts} ${x(s.data.length - 1)},${y(lo)}" fill="${s.c}" opacity=".15"/>`;
        g += `<polyline points="${pts}" fill="none" stroke="${s.c}" stroke-width="${s.w || 2.4}" ${s.dash ? 'stroke-dasharray="6 5"' : ""} stroke-linejoin="round"/>`;
      }
    });
    const legend = series.filter((s) => s.l).map((s) => `<span><i style="background:${s.c}"></i>${esc(s.l)}</span>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" class="chart" direction="ltr">${g}</svg><div class="legend">${legend}</div>`;
  }

  /* ---------- financial model (mirrors common.model) ---------- */
  function model(fin, k) {
    const capex = fin.capex.reduce((a, c) => a + c[1], 0) * k.capex;
    const rev = [0, 0, 0], cogs = [0, 0, 0];
    fin.streams.forEach(([, , price, units, c]) => units.forEach((u, y) => { const r = price * k.price * u * k.volume; rev[y] += r; cogs[y] += r * c; }));
    const opex = fin.opex.map((o) => o * k.opex);
    const ebitda = rev.map((r, y) => r - cogs[y] - opex[y]);
    let cash = -capex, low = cash, be = null; const curve = [cash];
    for (let m = 0; m < 36; m++) { cash += ebitda[Math.floor(m / 12)] / 12; curve.push(cash); low = Math.min(low, cash); if (be === null && cash >= 0) be = m + 1; }
    return { capex, rev, cogs, opex, ebitda, curve, funding: -low, be };
  }

  function financePanel(p, host) {
    const k = { price: 1, volume: 1, opex: 1, capex: 1 };
    const sliders = [["price", "الأسعار"], ["volume", "عدد العملاء والكميات"], ["opex", "التكاليف التشغيلية"], ["capex", "الاستثمار الأولي"]];
    host.innerHTML = `<div class="row2"><div class="card"><h3>🎚️ حرّك الافتراضات</h3>${sliders.map(([key, l]) =>
      `<label class="sl">${l} <b id="v-${key}">×1.00</b><input type="range" min="0.4" max="1.8" step="0.05" value="1" data-k="${key}"></label>`).join("")}
      <button class="btn ghost" id="reset">إرجاع الافتراضات الأساسية</button>
      <p class="muted">الأرقام افتراضات تخطيطية أولية للتحقق، والمحاكي يوضح حساسية المشروع لها.</p></div>
      <div class="card"><div id="kpis" class="kpis"></div><div id="fchart"></div></div></div>
      <div class="card"><h3>📊 قائمة الدخل المتوقعة</h3><div id="pl"></div></div>`;
    const draw = () => {
      const m = model(p.fin, k);
      $("#kpis", host).innerHTML = [["الاستثمار الأولي", money(m.capex)], ["التمويل المطلوب", money(m.funding)], ["إيرادات السنة 3", money(m.rev[2])],
        ["نتيجة السنة 3", money(m.ebitda[2])], ["نقطة التعادل", m.be ? "الشهر " + m.be : "بعد 3 سنوات"]].map(([a, b]) => `<div><span>${a}</span><b>${b}</b></div>`).join("");
      $("#fchart", host).innerHTML = lineChart([{ data: m.curve, c: "#0B6E4F", l: "النقد التراكمي (36 شهرًا)", fill: true }], { h: 230, thr: [{ v: 0, c: "#94A3B8", l: "التعادل" }], xl: ["البداية", "س1", "س2", "س3"] });
      const rows = [["الإيرادات", m.rev], ["الكلفة المباشرة", m.cogs], ["المصاريف التشغيلية", m.opex], ["صافي الربح التشغيلي", m.ebitda]];
      $("#pl", host).innerHTML = `<table><tr><th>البند</th><th>السنة 1</th><th>السنة 2</th><th>السنة 3</th></tr>${rows.map(([l, v]) => `<tr><td>${l}</td>${v.map((x) => `<td class="n">${money(x)}</td>`).join("")}</tr>`).join("")}</table>`;
    };
    host.querySelectorAll("input[type=range]").forEach((r) => r.addEventListener("input", () => { k[r.dataset.k] = +r.value; $("#v-" + r.dataset.k, host).textContent = "×" + (+r.value).toFixed(2); draw(); }));
    $("#reset", host).onclick = () => { host.querySelectorAll("input[type=range]").forEach((r) => { r.value = 1; k[r.dataset.k] = 1; $("#v-" + r.dataset.k, host).textContent = "×1.00"; }); draw(); };
    draw();
  }

  /* ---------- demo archetypes ---------- */
  function alertBox(host) {
    const box = document.createElement("div"); box.className = "log"; host.appendChild(box);
    return (msg, kind) => { const d = document.createElement("div"); d.className = "item " + (kind || ""); d.innerHTML = `<b>${new Date().toLocaleTimeString("ar-JO", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}</b> ${msg}`; box.prepend(d); while (box.children.length > 8) box.lastChild.remove(); };
  }

  function demoMonitor(c, host) {
    host.innerHTML = `<div class="row2"><div class="card"><h3>📡 ${esc(c.metric)} (لحظي)</h3><div id="ch"></div><div class="btns" id="ev"></div></div>
      <div class="card"><div class="kpis" id="mk"></div><h3>🔔 تنبيهات النظام الذكي</h3><div id="lg"></div></div></div>`;
    const log = alertBox($("#lg", host));
    const data = []; let t = 0, saved = 0, state = { leak: 0, overflow: false, supply: 0, slope: c.slope || 0, spike: 0, tamper: 0 };
    let v = c.pattern === "tank" ? 70 : (c.base || 0);
    const daily = (h) => 0.35 + 0.65 * (Math.exp(-((h - 7) ** 2) / 6) + Math.exp(-((h - 20) ** 2) / 8));
    (c.events || []).forEach((ev) => { const b = document.createElement("button"); b.className = "btn"; b.textContent = ev.label; b.onclick = () => {
      if (ev.kind === "leak") state.leak = 1; if (ev.kind === "overflow") { state.overflow = true; state.supply = 10; }
      if (ev.kind === "supply") state.supply = 10; if (ev.kind === "foul") state.slope *= 3; if (ev.kind === "clean") { v = c.base; state.slope = c.slope; }
      if (ev.kind === "spike") state.spike = 14; if (ev.kind === "tamper") state.tamper = 6;
      log(ev.alert, "warn"); }; $("#ev", host).appendChild(b); });
    const step = () => {
      const h = t % 24; t++;
      if (c.pattern === "tank") {
        v -= 2.2 * daily(h) + (state.leak && h < 5 ? 1.4 : 0);
        if (state.supply > 0) { state.supply--; v += 9; }
        if (v >= 100) { v = 100; if (state.overflow) { saved += 180; state.overflow = false; state.supply = 0; log("🤖 الذكاء الاصطناعي أطفأ المضخة ومنع الفيضان", "ok"); } }
        if (state.leak && h === 4) { log("💧 تأكيد: هبوط ليلي بلا استخدام، أرسلنا تنبيهًا على واتساب", "warn"); saved += 90; state.leak = 0; }
        if (v < c.thr_lo && t % 6 === 0) log(`⏳ خزانك بيخلص خلال ~${Math.max(1, Math.round(v / 2))} ساعة، والدور القادم بعد 30 ساعة`, "warn");
        v = clamp(v, 0, 100);
      } else if (c.pattern === "flow") {
        v = c.base + c.amp * daily(h) + (rnd() - .5) * c.base * .4 + (state.leak ? c.thr : 0);
        if (state.tamper > 0) { state.tamper--; v = 0; }
        if (state.leak && h >= 1 && h <= 4) { if (h === 3) { log("🔍 التدفق الليلي الأدنى أعلى من الطبيعي 3 ساعات متتالية: تسريب مؤكد", "warn"); saved++; } }
        saved++;
      } else if (c.pattern === "drift") {
        v += state.slope * (c.base || 1) + (rnd() - .5) * (c.base || 1) * .01;
        if (v > c.thr && t % 5 === 0) log(`⚠️ ${esc(c.metric)} تجاوز الحد: الإجراء المقترح الآن`, "warn");
        saved += 1;
      } else {
        v = c.base + (rnd() - .5) * c.base * .3 + (state.spike > 0 ? (c.thr - c.base) * 1.6 * Math.sin((14 - state.spike) / 14 * Math.PI) : 0);
        if (state.spike > 0) { state.spike--; if (state.spike === 7) { log("📍 تم تأكيد الإشارة وتحديد الموقع", "ok"); saved++; } }
      }
      data.push(v); if (data.length > 72) data.shift();
      const proj = c.pattern === "drift" && state.slope > 0 ? Math.max(0, Math.round((c.thr - v) / (state.slope * (c.base || 1)))) : null;
      const thr = [];
      if (c.thr) thr.push({ v: c.thr, c: "#DC2626", l: "حد الإنذار" });
      if (c.thr_lo) thr.push({ v: c.thr_lo, c: "#F59E0B", l: "مستوى منخفض" });
      $("#ch", host).innerHTML = lineChart([{ data, c: "#0369A1", l: c.metric, fill: true }], { h: 230, min: c.min, max: c.max, thr });
      $("#mk", host).innerHTML = `<div><span>القراءة الحالية</span><b>${fmt(v, 1)} ${esc(c.unit)}</b></div>` +
        (proj !== null ? `<div><span>الوصول للحد المتوقع</span><b>${proj} ساعة</b></div>` : "") +
        `<div><span>${esc(c.counter)}</span><b>${fmt(saved)}</b></div>`;
    };
    for (let i = 0; i < 30; i++) step();
    every(700, step);
  }

  function demoZones(c, host) {
    host.innerHTML = `<div class="row2"><div class="card"><h3>🗺️ ${esc(c.metric)}</h3><div class="zones" id="zg"></div>
      <div class="legendbar"><span>${c.good_high ? "منخفض" : "آمن"}</span><i></i><span>${c.good_high ? "مرتفع" : "خطر"}</span></div></div>
      <div class="card"><h3>🎚️ السيناريو</h3><div id="zs"></div><h3>🎯 الأولويات المقترحة</h3><div id="zt"></div></div></div>`;
    seed = 11; const base = c.items.map(() => 0.25 + rnd() * 0.5), sens = c.items.map(() => 0.6 + rnd() * 0.8);
    const s = {}; c.sliders.forEach((x) => { s[x.k] = x.v; });
    $("#zs", host).innerHTML = c.sliders.map((x) => `<label class="sl">${esc(x.l)} <b id="z-${x.k}">${x.v}%</b><input type="range" min="${x.min}" max="${x.max}" value="${x.v}" data-k="${x.k}"></label>`).join("");
    let jitter = c.items.map(() => 0);
    const draw = () => {
      const vals = c.items.map((_, i) => clamp(base[i] + jitter[i] + c.sliders.reduce((a, x) => a + x.w * (s[x.k] / 100 - 0.5) * sens[i], 0), 0.02, 0.98));
      $("#zg", host).innerHTML = c.items.map((n, i) => { const v = vals[i]; const bad = c.good_high ? 1 - v : v;
        const col = `hsl(${(1 - bad) * 120},70%,${88 - bad * 30}%)`; return `<div class="zone" style="background:${col}"><b>${fmt(v * 100)}${esc(c.unit)}</b><span>${esc(n)}</span></div>`; }).join("");
      const order = vals.map((v, i) => [v, i]).sort((a, b) => c.good_high ? b[0] - a[0] : b[0] - a[0]).slice(0, 5);
      $("#zt", host).innerHTML = order.map(([v, i], r) => `<div class="pri"><b>${r + 1}</b> ${esc(c.items[i])} <span>${fmt(v * 100)}${esc(c.unit)}</span><small>${esc(c.action)}</small></div>`).join("");
    };
    host.querySelectorAll("input[type=range]").forEach((r) => r.addEventListener("input", () => { s[r.dataset.k] = +r.value; $("#z-" + r.dataset.k, host).textContent = r.value + "%"; draw(); }));
    draw();
    every(1600, () => { jitter = jitter.map((j) => clamp(j + (rnd() - .5) * .06, -.08, .08)); draw(); });
  }

  function demoMatch(c, host) {
    host.innerHTML = `<div class="row2"><div class="card"><h3>📍 الخريطة</h3><canvas id="mc" width="640" height="380"></canvas>
      <div class="btns"><button class="btn" id="m1">توزيع تقليدي</button><button class="btn primary" id="m2">🤖 توزيع ذكي</button><button class="btn ghost" id="m3">طلبات جديدة</button></div></div>
      <div class="card"><div class="kpis" id="mk"></div><div class="legend"><span><i style="background:#0369A1"></i>${esc(c.supplier)}</span><span><i style="background:#F59E0B"></i>${esc(c.request)}</span></div>
      <p class="muted">التوزيع الذكي يطابق كل ${esc(c.request)} مع أقرب ${esc(c.supplier)} متاح ضمن السعة.</p></div></div>`;
    const cv = $("#mc", host), g = cv.getContext("2d"); let S = [], R = [], base = null;
    const gen = () => { S = Array.from({ length: c.ns }, () => ({ x: 40 + rnd() * 560, y: 30 + rnd() * 320 })); R = Array.from({ length: c.nr }, () => ({ x: 30 + rnd() * 580, y: 20 + rnd() * 340 })); base = null; draw([]); };
    const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y) / 20;
    const draw = (pairs) => {
      g.clearRect(0, 0, 640, 380); g.fillStyle = "#F1F5F9"; g.fillRect(0, 0, 640, 380);
      g.strokeStyle = "#94A3B8"; pairs.forEach(([r, s]) => { g.beginPath(); g.moveTo(r.x, r.y); g.lineTo(s.x, s.y); g.stroke(); });
      R.forEach((r) => { g.fillStyle = "#F59E0B"; g.beginPath(); g.arc(r.x, r.y, 5, 0, 7); g.fill(); });
      S.forEach((s) => { g.fillStyle = "#0369A1"; g.fillRect(s.x - 8, s.y - 8, 16, 16); });
    };
    const total = (pairs) => pairs.reduce((a, [r, s]) => a + dist(r, s), 0);
    const show = (pairs, smart) => { draw(pairs); const tot = total(pairs); if (!smart) base = tot;
      $("#mk", host).innerHTML = `<div><span>${esc(c.metric)}</span><b>${fmt(tot)} كم</b></div>` + (smart && base ? `<div><span>التوفير مقابل التقليدي</span><b>${fmt((1 - tot / base) * 100)}%</b></div>` : "") + `<div><span>عدد الطلبات</span><b>${R.length}</b></div>`; };
    $("#m1", host).onclick = () => show(R.map((r) => [r, S[Math.floor(rnd() * S.length)]]), false);
    $("#m2", host).onclick = () => { if (base === null) $("#m1", host).click(); const cap = S.map(() => Math.ceil(R.length / S.length) + 1);
      show(R.map((r) => { let bi = -1, bd = 1e9; S.forEach((s, i) => { const d = dist(r, s); if (cap[i] > 0 && d < bd) { bd = d; bi = i; } }); cap[bi]--; return [r, S[bi]]; }), true); };
    $("#m3", host).onclick = gen; gen(); $("#m1", host).click();
  }

  const PROFILES = {
    home: (h) => 10 + 60 * Math.exp(-((h - 7) ** 2) / 4) + 45 * Math.exp(-((h - 20) ** 2) / 6),
    pressure: (h) => 3 + 1.4 * (h < 6 || h > 22 ? 1 : 0.4),
    pump: (h) => 120 + 40 * Math.sin(h / 24 * 6.28),
    irrigation: (h) => (h >= 5 && h <= 9 ? 90 : h >= 16 && h <= 19 ? 70 : 5),
    hotel: (h) => 20 + 40 * Math.exp(-((h - 8) ** 2) / 5) + 30 * Math.exp(-((h - 19) ** 2) / 6),
  };
  function demoOptimize(c, host) {
    host.innerHTML = `<div class="row2"><div class="card"><h3>📈 ${esc(c.series)} خلال 24 ساعة</h3><div id="oc"></div>
      <label class="sl">${esc(c.slider.l)} <b id="ov">0%</b><input type="range" min="0" max="${c.slider.max}" value="0" id="or"></label></div>
      <div class="card"><div class="kpis" id="ok"></div><p class="muted">${esc(c.note)}</p></div></div>`;
    const base = Array.from({ length: 24 }, (_, h) => PROFILES[c.profile](h));
    const tariff = Array.from({ length: 24 }, (_, h) => (h >= 17 && h <= 22 ? 0.16 : h >= 23 || h <= 6 ? 0.07 : 0.11));
    const draw = (pct) => {
      let opt;
      if (c.mode === "shift") {
        const peak = base.map((b, h) => (tariff[h] > 0.1 ? b * pct / 100 : 0)); const moved = peak.reduce((a, b) => a + b, 0);
        const cheap = tariff.filter((t) => t < 0.1).length; opt = base.map((b, h) => (tariff[h] > 0.1 ? b - peak[h] : b + moved / cheap));
      } else {
        const wgt = c.profile === "pressure" ? (h) => (h < 6 || h > 22 ? 1 : 0.25) : () => 1;
        opt = base.map((b, h) => b * (1 - pct / 100 * wgt(h)));
      }
      const sum = (a) => a.reduce((x, y) => x + y, 0);
      const cost = (a) => (c.mode === "shift" ? a.reduce((x, y, h) => x + y * tariff[h] * 4, 0) : c.profile === "pressure" ? a.reduce((x, y) => x + Math.pow(y, 1.15), 0) : sum(a) * (c.cost_unit.includes("شهر") ? 30 : 1));
      const b = cost(base), o = cost(opt);
      $("#oc", host).innerHTML = lineChart([{ data: base, c: "#94A3B8", l: "الوضع الحالي", dash: true }, { data: opt, c: "#0B6E4F", l: "مع الذكاء الاصطناعي", fill: true }],
        { h: 230, min: 0, xl: ["00", "06", "12", "18", "23"] });
      $("#ok", host).innerHTML = `<div><span>الحالي</span><b>${fmt(b)} ${esc(c.cost_unit)}</b></div><div><span>بعد التحسين</span><b>${fmt(o)} ${esc(c.cost_unit)}</b></div><div><span>التوفير</span><b>${fmt((1 - o / b) * 100, 1)}%</b></div>`;
    };
    $("#or", host).addEventListener("input", (ev) => { $("#ov", host).textContent = ev.target.value + "%"; draw(+ev.target.value); });
    draw(0);
  }

  function demoCalc(c, host) {
    host.innerHTML = `<div class="row2"><div class="card"><h3>🧮 المدخلات</h3>${c.inputs.map((x) => `<label class="sl">${esc(x.l)} <b id="c-${x.k}">${fmt(x.v, x.step < 1 ? 1 : 0)} ${esc(x.u)}</b><input type="range" min="${x.min}" max="${x.max}" step="${x.step}" value="${x.v}" data-k="${x.k}"></label>`).join("")}</div>
      <div class="card"><h3>📋 النتائج</h3><div class="kpis big" id="co"></div><p class="muted">حسابات توضيحية بمعاملات تقريبية تُضبط ببيانات حقيقية في النموذج الأولي.</p></div></div>`;
    const v = {}; c.inputs.forEach((x) => { v[x.k] = x.v; });
    const fns = c.outputs.map((o) => new Function(...c.inputs.map((x) => x.k), "return " + o.f));
    const draw = () => { $("#co", host).innerHTML = c.outputs.map((o, i) => { const r = fns[i](...c.inputs.map((x) => v[x.k])); return `<div><span>${esc(o.l)}</span><b>${typeof r === "number" ? fmt(r, o.d) : esc(r)} ${esc(o.u)}</b></div>`; }).join(""); };
    host.querySelectorAll("input[type=range]").forEach((r) => r.addEventListener("input", () => { v[r.dataset.k] = +r.value; const x = c.inputs.find((i) => i.k === r.dataset.k); $("#c-" + x.k, host).textContent = fmt(+r.value, x.step < 1 ? 1 : 0) + " " + x.u; draw(); }));
    draw();
  }

  function demoBalance(c, host) {
    const S = [["pop", "النمو السكاني السنوي", 0, 5, 2.2, 0.1, "%"], ["rain", "تغير الأمطار", -40, 20, -10, 5, "%"], ["carrier", "سنة تشغيل الناقل الوطني", 2028, 2034, 2030, 1, ""],
      ["nrw", "خفض الفاقد بحلول 2040", 0, 30, 15, 1, "نقطة"], ["agri", "تحسين كفاءة الري", 0, 30, 10, 1, "%"]];
    host.innerHTML = `<div class="row2"><div class="card"><h3>🎛️ قرارات وسيناريوهات</h3>${S.map(([k, l, a, b, v, st, u]) => `<label class="sl">${l} <b id="b-${k}">${v} ${u}</b><input type="range" min="${a}" max="${b}" step="${st}" value="${v}" data-k="${k}"></label>`).join("")}
      <p class="muted">نموذج مبسط بأرقام توضيحية (مليون م³) لعرض فكرة التوأم الرقمي، وليس بيانات رسمية.</p></div>
      <div class="card"><div class="kpis" id="bk"></div><div id="bc"></div></div></div>`;
    const v = {}; S.forEach((x) => { v[x[0]] = x[4]; });
    const draw = () => {
      const yrs = [], sup = [], dem = [];
      for (let y = 2026; y <= 2040; y++) {
        const i = y - 2026; const pop = Math.pow(1 + v.pop / 100, i);
        const nrw = 0.5 - v.nrw / 100 * i / 14;
        const muni = 520 * pop / (1 - nrw) * 0.5; const ag = 560 * (1 - v.agri / 100 * i / 14); const ind = 60 * pop;
        const s = 600 - 6 * i + 250 * (1 + v.rain / 100) + 160 + (y >= v.carrier ? Math.min(300, (y - v.carrier + 1) * 150) : 0);
        yrs.push(y); sup.push(s); dem.push(muni + ag + ind);
      }
      const gap = dem.map((d, i) => d - sup[i]);
      $("#bc", host).innerHTML = lineChart([{ data: dem, c: "#DC2626", l: "الطلب" }, { data: sup, c: "#0369A1", l: "المتاح", fill: true }], { h: 240, xl: ["2026", "2030", "2035", "2040"] });
      $("#bk", host).innerHTML = [["العجز 2030", gap[4]], ["العجز 2035", gap[9]], ["العجز 2040", gap[14]]].map(([l, x]) => `<div class="${x > 0 ? "bad" : "good"}"><span>${l}</span><b>${x > 0 ? fmt(x) + " عجز" : fmt(-x) + " فائض"}</b></div>`).join("");
    };
    host.querySelectorAll("input[type=range]").forEach((r) => r.addEventListener("input", () => { v[r.dataset.k] = +r.value; const x = S.find((s) => s[0] === r.dataset.k); $("#b-" + x[0], host).textContent = r.value + " " + x[6]; draw(); }));
    draw();
  }

  function demoDami(c, host) {
    host.innerHTML = `<div class="card hero"><h3>🩸 تطبيق دَمي الكامل</h3><p>تطبيق مستقل يشمل: لوحة مخزون الدم في المستشفيات، والتنبؤ بالطلب، وتنبيهات الصلاحية، والطوارئ مع <b>توصيل الدم بالدرون</b> على الخريطة ومراقبة حرارة الصندوق، واستدعاء المتبرعين، ووضع الحوادث الكبرى.</p>
      <a class="btn primary" href="dami.html">افتح تطبيق دَمي ←</a></div>`;
  }

  const DEMO = { monitor: demoMonitor, zones: demoZones, match: demoMatch, optimize: demoOptimize, calc: demoCalc, balance: demoBalance, dami: demoDami };

  /* ---------- views ---------- */
  function hub() {
    const axes = Object.entries(D.axes);
    const app = $("#app");
    app.innerHTML = `<header class="top"><div><div class="brand">NEXORA</div><h1>محاكيات المشاريع الـ 31</h1><p>لكل مشروع: محاكاة تفاعلية للفكرة، ومحاكي جدوى مالي، ونموذج العمل.</p></div>
      <div class="quote">«${esc(D.quote)}»</div></header>
      <div class="filters"><input id="q" placeholder="ابحث عن مشروع…"><div class="chips"><button class="chip on" data-a="">الكل</button>${axes.map(([k, [n, col]]) => `<button class="chip" data-a="${k}" style="--c:${col}">${esc(n)}</button>`).join("")}</div></div>
      <div class="grid" id="grid"></div><p class="muted foot">${esc(D.disclaimer)} جميع المحاكيات تعمل ببيانات اصطناعية لأغراض العرض.</p>`;
    let axis = "", q = "";
    const draw = () => { $("#grid").innerHTML = D.projects.filter((p) => (!axis || p.axis === axis) && (!q || (p.ar + p.en + p.tag).includes(q))).map((p) => {
      const m = model(p.fin, { price: 1, volume: 1, opex: 1, capex: 1 });
      return `<a class="pcard" href="#/p/${p.id}" style="--c:${D.axes[p.axis][1]}"><div class="pn">${String(p.id).padStart(2, "0")}</div><div class="pe">${p.emoji}</div><h3>${esc(p.ar)} <small>${esc(p.en)}</small></h3><p>${esc(p.tag)}</p>
        <div class="meta"><span>${esc(D.axes[p.axis][0])}</span><span>⭐ ${p.score}/20</span><span>${m.be ? "تعادل: الشهر " + m.be : "تعادل: بعد 3 سنوات"}</span></div></a>`; }).join(""); };
    $("#q").addEventListener("input", (e) => { q = e.target.value.trim(); draw(); });
    document.querySelectorAll(".chip").forEach((b) => b.onclick = () => { document.querySelectorAll(".chip").forEach((x) => x.classList.remove("on")); b.classList.add("on"); axis = b.dataset.a; draw(); });
    draw();
  }

  function project(id) {
    const p = D.projects.find((x) => x.id === id); if (!p) return hub();
    const tabs = [["demo", "🎮 المحاكاة التفاعلية"], ["fin", "💹 محاكي الجدوى"], ["bmc", "🧩 نموذج العمل"], ["idea", "💡 الفكرة"]];
    $("#app").innerHTML = `<a class="back" href="#/">→ كل المشاريع</a>
      <header class="ph" style="--c:${D.axes[p.axis][1]}"><div class="pn">${String(p.id).padStart(2, "0")}</div><div><h1>${p.emoji} ${esc(p.ar)} <small>${esc(p.en)}</small></h1><p>${esc(p.tag)}</p></div></header>
      <nav class="tabs">${tabs.map(([k, l], i) => `<button class="tab ${i ? "" : "on"}" data-t="${k}">${l}</button>`).join("")}</nav><div id="pane"></div>
      <p class="muted foot">محاكاة توضيحية ببيانات اصطناعية. ${esc(D.disclaimer)}</p>`;
    const show = (k) => { stopAll(); const pane = $("#pane");
      if (k === "demo") { pane.innerHTML = `<div class="wow">⚡ ${esc(p.wow)}</div><div id="dh"></div>`; DEMO[p.demo.type](p.demo, $("#dh")); }
      if (k === "fin") financePanel(p, pane);
      if (k === "bmc") pane.innerHTML = `<div class="bmc">${D.bmc.map(([key, ar, en]) => `<div class="b b-${key}"><h4>${esc(ar)} <small>${esc(en)}</small></h4><ul>${p.bmc[key].map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`).join("")}</div>`;
      if (k === "idea") pane.innerHTML = `<div class="row2"><div class="card"><h3>المشكلة</h3><p>${esc(p.problem)}</p><h3>الحل</h3><p>${esc(p.solution)}</p></div><div class="card"><h3>المميزات</h3><ul>${p.features.map((x) => `<li>${esc(x)}</li>`).join("")}</ul><h3>التميّز</h3><ul>${p.diff.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div></div>`;
    };
    document.querySelectorAll(".tab").forEach((b) => b.onclick = () => { document.querySelectorAll(".tab").forEach((x) => x.classList.remove("on")); b.classList.add("on"); show(b.dataset.t); });
    show("demo"); window.scrollTo(0, 0);
  }

  function route() { stopAll(); const m = location.hash.match(/^#\/p\/(\d+)/); if (m) project(+m[1]); else hub(); }
  window.addEventListener("hashchange", route); route();
})();
