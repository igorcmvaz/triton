/* ── interactive figures ──────────────────────────────────────────────────────
   Each interactive figure replaces, on the section page, the static figure of
   the same file. The numbers come ready from gerar_figuras_interativas.py, which
   runs the simulator; here we only pick the cell and draw. The texts that quote
   numbers ("Try it") are built from the data, so they cannot drift from it. */

const FI = {};
const FI_D = DADOS.interativas || {};
const FI_ONDE = DADOS.onde_interativas || {};
const S = n => `var(--s${n})`;
/* A one-hue ramp, for the parts of a stacked bar. */
const R = n => `var(--r${n})`;
const menos = (v, d = 0) => (v < 0 ? "−" : "") + fmt(Math.abs(v), d);
/* Money: the currency symbol comes from the build (DADOS.i18n.moeda). */
const din = (v, d = 0) => (v < 0 ? "−" : "") + MOEDA + " " + fmt(Math.abs(v), d);
const MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const TUTORIAL = "Tutorial project: a house in New York, 150 m² of roof, runoff coefficient 0.85, 2 mm first flush, four residents using 150 L/day each, 28% of the demand suppliable by rain, 30 years of daily rain.";
const ILUSTRATIVO = "Costs and tariffs of the tutorial are illustrative, not market prices.";
const curto = t => t.replace(/ \(.*\)/, "").toLowerCase();

/* scales and axes */
function passoBonito(b) {
  if (!(b > 0)) return 1;
  const e = Math.pow(10, Math.floor(Math.log10(b))), f = b / e;
  return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * e;
}
function escala(min, max, n = 5) {
  const p = passoBonito((max - min) / n);
  const a = Math.floor(min / p + 1e-9) * p;
  let b = Math.ceil(max / p - 1e-9) * p;
  if (b <= a) b = a + p;
  const marcas = [];
  for (let v = a; v <= b + p / 1e6; v += p) marcas.push(Math.round(v / p * 1e6) / 1e6 * p);
  return {min: a, max: b, marcas};
}
function plano(o) {
  const X = v => o.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * (o.W - o.l - o.r);
  const Y = v => o.t + (1 - (v - o.y[0]) / (o.y[1] - o.y[0])) * (o.H - o.t - o.b);
  let s = "";
  (o.ym || []).forEach(v => {
    s += `<line class="g-grade" x1="${o.l}" x2="${o.W - o.r}" y1="${Y(v)}" y2="${Y(v)}"/>`;
    s += `<text class="g-t" x="${o.l - 7}" y="${Y(v) + 4}" text-anchor="end">${o.yf ? o.yf(v) : menos(v)}</text>`;
  });
  (o.xm || []).forEach(v => {
    s += `<text class="g-t" x="${X(v)}" y="${o.H - o.b + 16}" text-anchor="middle">${o.xf ? o.xf(v) : fmt(v)}</text>`;
  });
  const temZero = o.y[0] < 0 && o.y[1] > 0;
  s += `<line class="g-eixo" x1="${o.l}" x2="${o.W - o.r}" y1="${o.H - o.b}" y2="${o.H - o.b}"/>`;
  if (temZero) s += `<line class="g-zero" x1="${o.l}" x2="${o.W - o.r}" y1="${Y(0)}" y2="${Y(0)}"/>`;
  if (o.xr) s += `<text class="g-r" x="${o.W - o.r}" y="${o.H - o.b + 33}" text-anchor="end">${o.xr}</text>`;
  if (o.yr) s += `<text class="g-r" x="${o.l - 7}" y="${o.t - 11}">${o.yr}</text>`;
  if (o.painel) s += `<text class="g-painel" x="2" y="${o.t - 11}">${o.painel}</text>`;
  return {X, Y, s};
}
/* direct labels at the end of the lines, spaced so they do not overlap */
function rotulosNaPonta(itens, x, ymin, ymax) {
  const ord = itens.slice().sort((a, b) => a.y - b.y);
  for (let i = 1; i < ord.length; i++) if (ord[i].y - ord[i - 1].y < 14) ord[i].y = ord[i - 1].y + 14;
  const excesso = ord.length ? ord[ord.length - 1].y - ymax : 0;
  if (excesso > 0) ord.forEach(o => { o.y = Math.max(ymin, o.y - excesso); });
  return ord.map(o => `<text class="g-rot" x="${x}" y="${o.y + 4}" style="fill:${o.c}">${o.t}</text>`).join("");
}

/* tooltip on hover */
function dicaHTML(titulo, linhas) {
  return `<div class="d-t">${titulo}</div>` + linhas.map(([c, r, v]) =>
    `<div class="d-l"><span>${c ? `<i style="background:${c}"></i>` : ""}${r}</span><b>${v}</b></div>`).join("");
}
function pairar(svg, W, xs, conteudo, aoEscolher) {
  const dica = $("#dica");
  const indice = e => {
    const r = svg.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * W;
    let k = 0, d = Infinity;
    xs.forEach((v, i) => { const q = Math.abs(v - x); if (q < d) { d = q; k = i; } });
    return k;
  };
  svg.onpointermove = e => {
    const k = indice(e);
    dica.innerHTML = conteudo(k);
    dica.hidden = false;
    const lim = document.documentElement.clientWidth - dica.offsetWidth - 8;
    dica.style.left = Math.max(8, Math.min(e.pageX + 14, lim)) + "px";
    dica.style.top = Math.max(window.scrollY + 64, e.pageY - dica.offsetHeight - 12) + "px";
    const g = svg.querySelector(".g-guia");
    if (g) { g.setAttribute("x1", xs[k]); g.setAttribute("x2", xs[k]); g.style.display = ""; }
  };
  svg.onpointerleave = () => {
    dica.hidden = true;
    const g = svg.querySelector(".g-guia");
    if (g) g.style.display = "none";
  };
  svg.onclick = aoEscolher ? e => aoEscolher(indice(e)) : null;
  if (aoEscolher) svg.style.cursor = "pointer";
}

/* controls */
function ctlFaixa(id, rotulo, n, valor) {
  return `<div class="fi-ctl largo"><label class="fi-rot" for="${id}">${rotulo} <output id="${id}-o"></output></label>` +
    `<input id="${id}" type="range" min="0" max="${n - 1}" step="1" value="${valor}"></div>`;
}
function ctlSeg(id, rotulo, opcoes, atual) {
  return `<div class="fi-ctl"><span class="fi-rot" id="${id}-r">${rotulo}</span><div class="seg" id="${id}" role="group" aria-labelledby="${id}-r">` +
    opcoes.map(([v, t]) => `<button type="button" data-v="${v}" aria-pressed="${String(v) === String(atual)}">${t}</button>`).join("") + `</div></div>`;
}
function ctlChips(id, rotulo, itens, ativos) {
  return `<div class="fi-ctl"><span class="fi-rot" id="${id}-r">${rotulo}</span><div class="chips-t" id="${id}" role="group" aria-labelledby="${id}-r">` +
    itens.map(([k, t, c]) => `<button type="button" class="chip-t" data-v="${k}" aria-pressed="${ativos.includes(k)}" style="--c:${c}"><i></i>${t}</button>`).join("") + `</div></div>`;
}
function ligarSeg(raiz, id, cb) {
  raiz.querySelector("#" + id).addEventListener("click", e => {
    const b = e.target.closest("button");
    if (!b) return;
    raiz.querySelectorAll(`#${id} button`).forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    cb(b.dataset.v);
  });
}
function ligarChips(raiz, id, cb) {
  raiz.querySelector("#" + id).addEventListener("click", e => {
    const b = e.target.closest("button");
    if (!b) return;
    const todos = [...raiz.querySelectorAll(`#${id} button`)];
    const ligado = b.getAttribute("aria-pressed") === "true";
    if (ligado && todos.filter(x => x.getAttribute("aria-pressed") === "true").length === 1) return;
    b.setAttribute("aria-pressed", String(!ligado));
    cb(todos.filter(x => x.getAttribute("aria-pressed") === "true").map(x => x.dataset.v));
  });
}
function legenda(itens) {
  return `<div class="fi-leg">${itens.map(([c, t, tipo]) => `<span><i class="${tipo || ""}" style="--c:${c}"></i>${t}</span>`).join("")}</div>`;
}
function cartao(rotulo, valor, detalhe = "") {
  const bloco = /:/.test(detalhe) ? ' class="bl"' : "";
  return `<div><small>${rotulo}</small><b>${valor}</b>${detalhe ? ` <span${bloco}>${detalhe}</span>` : ""}</div>`;
}

/* ─── figure: the ten-day balance ───────────────────────────────────────── */
FI["fig01_dez_dias.png"] = {
  curto: "The ten-day balance",
  pergunta: "Where does each day's rain go: cistern, consumption or overflow?",
  controles: "capacity · first flush · day by day",
  experimente: D => {
    const sem0 = D.casos["2000|0"], com2 = D.casos["2000|2"];
    const d1 = D.chuva.findIndex(x => x > 0), dmax = D.chuva.indexOf(Math.max(...D.chuva));
    return `Set the first flush to 0 mm: day ${d1 + 1}, with ${fmt(D.chuva[d1], 1)} mm of rain, goes from ${fmt(com2[d1][1])} L to ${fmt(sem0[d1][1])} L collected. On day ${dmax + 1} (${fmt(D.chuva[dmax], 1)} mm) the tank overflows ${fmt(D.casos["1000|2"][dmax][5])} L at a capacity of 1,000 L and ${fmt(D.casos["3000|2"][dmax][5])} L at 3,000 L.`;
  },
  fonte: D => `The ten days of the worked example in the section: ${fmt(D.area)} m² of roof, runoff coefficient ${fmt(D.coef, 2)}, demand of ${fmt(D.demanda)} L/day with ${fmt(D.fracao * 100)}% suppliable by rain, tank starting empty. Each cell is one run of the simulator.`,
  montar(p, D, id) {
    let cap = D.padrao[0], desc = D.padrao[1], dia = 1, relogio = null;
    const W = 640, H = 390;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "c", "Cistern capacity", D.capacidades.length, D.capacidades.indexOf(cap))}
      ${ctlSeg(id + "d", "First flush", D.descartes.map(d => [d, fmt(d) + " mm"]), desc)}
      <div class="fi-ctl"><span class="fi-rot">Highlighted day</span><div class="passo">
        <button type="button" data-a="-1" aria-label="Previous day">‹</button><output id="${id}o"></output>
        <button type="button" data-a="1" aria-label="Next day">›</button>
        <button type="button" class="tocar" id="${id}p">▶ Play</button></div></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Volume collected and overflowed each day, and volume stored in the cistern at the end of each of the ten days"></svg>
      ${legenda([[S(1), "collected and kept in the cistern"], [S(2), "collected and overflowed"], [S(3), "volume stored at the end of the day", "linha"], ["var(--ink3)", "cistern capacity", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const parar = () => { clearInterval(relogio); relogio = null; p.querySelector(`#${id}p`).textContent = "▶ Play"; };
    const desenhar = () => {
      const L = D.casos[`${cap}|${desc}`];
      const ya = escala(0, Math.max(500, ...L.map(l => l[1])), 4);
      const A = plano({W, H: 190, l: 58, r: 14, t: 36, b: 24, x: [0.4, 10.6], y: [0, ya.max], ym: ya.marcas, yr: "volume collected in the day (L)", painel: "(a)"});
      const yb = escala(0, Math.max(cap, ...L.map(l => l[6])), 4);
      const B = plano({W, H, l: 58, r: 14, t: 236, b: 42, x: [0.4, 10.6], y: [0, yb.max], ym: yb.marcas, yr: "volume stored at the end of the day (L)", painel: "(b)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], xf: v => "day " + v, xr: ""});
      const passo = A.X(2) - A.X(1), w = passo * 0.56;
      let s = `<rect class="g-sel" x="${A.X(dia + 1) - passo / 2 + 3}" y="20" width="${passo - 6}" height="${H - 42 - 20 + 22}" rx="7"/>` + A.s + B.s;
      L.forEach((l, k) => {
        const x = A.X(k + 1) - w / 2, ficou = l[1] - l[5];
        if (ficou > 0) s += `<path d="M${x} ${A.Y(0)} V${A.Y(ficou) + 3} q0 -3 3 -3 h${w - 6} q3 0 3 3 V${A.Y(0)} Z" style="fill:${S(1)}"/>`;
        if (l[5] > 0) {
          const y0 = A.Y(ficou) - (ficou > 0 ? 2 : 0), y1 = A.Y(l[1]);
          if (y0 - y1 > 1) s += `<path d="M${x} ${y0} V${y1 + 3} q0 -3 3 -3 h${w - 6} q3 0 3 3 V${y0} Z" style="fill:${S(2)}"/>`;
        }
        s += `<text class="g-t" x="${A.X(k + 1)}" y="${A.Y(l[1]) - 6}" text-anchor="middle">${fmt(D.chuva[k], 1)} mm</text>`;
      });
      s += `<line class="g-ref" x1="${B.X(0.4)}" x2="${B.X(10.6)}" y1="${B.Y(cap)}" y2="${B.Y(cap)}"/>`;
      s += `<text class="g-t" x="${B.X(10.6)}" y="${B.Y(cap) - 6}" text-anchor="end">capacity: ${fmt(cap)} L</text>`;
      s += `<polyline points="${L.map((l, k) => `${B.X(k + 1)},${B.Y(l[6])}`).join(" ")}" style="fill:none;stroke:${S(3)};stroke-width:2"/>`;
      L.forEach((l, k) => { s += `<circle cx="${B.X(k + 1)}" cy="${B.Y(l[6])}" r="${k === dia ? 6.5 : 4.5}" style="fill:${S(3)};stroke:var(--surface);stroke-width:2"/>`; });
      svg.innerHTML = s;
      pairar(svg, W, L.map((_, k) => A.X(k + 1)), k => dicaHTML(`Day ${k + 1} · ${fmt(D.chuva[k], 1)} mm of rain`, [
        [S(1), "collected", fmt(L[k][1]) + " L"], [S(2), "overflowed", fmt(L[k][5]) + " L"],
        [S(3), "stored at the end of the day", fmt(L[k][6]) + " L"]]), k => { dia = k; parar(); desenhar(); });

      const l = L[dia], ini = dia ? L[dia - 1][6] : 0;
      const sat = [["nulo", "✕ none"], ["parcial", "◐ partial"], ["pleno", "✓ full"]][l[7]];
      const tot = j => L.reduce((a, x) => a + x[j], 0);
      p.querySelector(`#${id}o`).textContent = `day ${dia + 1} of 10`;
      p.querySelector(`#${id}c-o`).textContent = fmt(cap) + " L";
      leit.innerHTML = `<p class="fi-sub">Balance of day ${dia + 1}</p>
        <table class="fi-tabela"><tbody>
        <tr><td>Rain of the day</td><td class="n">${fmt(D.chuva[dia], 1)} mm</td></tr>
        <tr><td>Rain after the ${fmt(desc)} mm first flush</td><td class="n">${fmt(l[0], 1)} mm</td></tr>
        <tr><td>Collected<small>${fmt(l[0], 1)} mm × ${fmt(D.area)} m² × ${fmt(D.coef, 2)}</small></td><td class="n">${fmt(l[1])} L</td></tr>
        <tr class="sep"><td>Stored at the start of the day</td><td class="n">${fmt(ini)} L</td></tr>
        <tr><td><i style="--c:${S(1)}"></i>+ collected</td><td class="n">+${fmt(l[1])} L</td></tr>
        <tr><td>− rainwater use<small>rainwater demand of ${fmt(l[2])} L</small></td><td class="n">−${fmt(l[3])} L</td></tr>
        <tr><td><i style="--c:${S(2)}"></i>− overflowed</td><td class="n">−${fmt(l[5])} L</td></tr>
        <tr class="tot"><td><i style="--c:${S(3)}"></i>= stored at the end of the day</td><td class="n">${fmt(l[6])} L</td></tr>
        </tbody></table>
        <p class="fi-sat">Supply on the day <span class="pill ${sat[0]}">${sat[1]}</span> · potable top-up: ${fmt(l[4])} L</p>
        <p class="fi-sub">Over the ten days</p>
        <div class="fi-n">${cartao("Collected", fmt(tot(1)), "L")}${cartao("Overflowed", fmt(tot(5)), "L")}
        ${cartao("Rainwater demand met", fmt(100 * tot(3) / tot(2), 1) + "%")}${cartao("Full-supply days", L.filter(x => x[7] === 2).length, "of 10")}</div>`;
    };
    p.querySelector(`#${id}c`).addEventListener("input", e => { cap = D.capacidades[+e.target.value]; desenhar(); });
    ligarSeg(p, id + "d", v => { desc = +v; desenhar(); });
    p.querySelectorAll(".passo [data-a]").forEach(b => b.addEventListener("click", () => { parar(); dia = (dia + +b.dataset.a + 10) % 10; desenhar(); }));
    p.querySelector(`#${id}p`).addEventListener("click", e => {
      if (relogio) { parar(); return; }
      if (dia === 9) dia = -1;
      e.target.textContent = "❚❚ Pause";
      relogio = setInterval(() => {
        if (!document.body.contains(svg) || dia >= 9) { parar(); return; }
        dia += 1; desenhar();
      }, 900);
    });
    desenhar();
  }
};

/* ─── figure: the cistern level, day by day ─────────────────────────────── */
FI["fig48_programa_serie_diaria.png"] = {
  curto: "The cistern level, day by day",
  pergunta: "How does the cistern fill and empty over a year?",
  controles: "capacity · year of the series",
  experimente: "Click “Driest year” and change the capacity: see in which months the 1 m³ cistern runs empty and how much of that an 8 m³ one solves. Click a bar of the year strip to go straight to that year.",
  fonte: D => TUTORIAL + ` The year is the calendar year of the series, from ${D.inicio.split("-").reverse().join("/")}.`,
  montar(p, D, id) {
    let vol = D.padrao, yi = 0;
    const N = D.anos.length, W = 720, H = 372;
    const inicio = D.inicio.split("-").map(Number);
    const media = (v, j) => D.resumo[v].reduce((a, r) => a + r[j], 0) / N;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "v", "Cistern capacity", D.volumes.map(v => [v, fmt(v / 1000) + " m³"]), vol)}
      <div class="fi-ctl"><label class="fi-rot" for="${id}a">Year of the series</label><div class="linha-ctl">
        <select id="${id}a">${D.anos.map((a, k) => `<option value="${k}">${a}</option>`).join("")}</select>
        <button type="button" class="bt" data-q="seco">Driest year</button><button type="button" class="bt" data-q="chuvoso">Wettest year</button><button type="button" class="bt" data-q="vazio">Most empty days</button></div></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}f" class="faixa-anos" viewBox="0 0 ${W} 78" role="img" aria-label="Annual rain of each year of the series; click to choose the year"></svg>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Daily rain and volume stored in the cistern at the end of each day of the chosen year"></svg>
      ${legenda([[S(1), "daily rain"], [S(3), "stored volume"], [S(2), "day with the cistern empty (up to 5% of capacity)"], ["var(--ink3)", "capacity", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const faixa = p.querySelector(`#${id}f`), svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`), sel = p.querySelector(`#${id}a`);
    const dataDe = i => new Date(Date.UTC(inicio[0], inicio[1] - 1, inicio[2]) + i * 864e5);
    const desenhar = () => {
      const R = D.resumo[vol];
      /* year strip */
      const chuvas = R.map(r => r[0]);
      const F = plano({W, H: 78, l: 58, r: 14, t: 22, b: 20, x: [-0.5, N - 0.5], y: [0, Math.max(...chuvas)], yr: "annual rain (click a year)"});
      let f = F.s;
      const bw = (F.X(1) - F.X(0)) * 0.7;
      chuvas.forEach((c, k) => {
        f += `<rect x="${F.X(k) - bw / 2}" y="${F.Y(c)}" width="${bw}" height="${F.Y(0) - F.Y(c)}" rx="2" style="fill:${k === yi ? S(1) : "var(--line)"}"/>`;
        if (k % 5 === 0) f += `<text class="g-t" x="${F.X(k)}" y="${78 - 5}" text-anchor="middle">${D.anos[k]}</text>`;
      });
      faixa.innerHTML = f;
      pairar(faixa, W, chuvas.map((_, k) => F.X(k)), k => dicaHTML(String(D.anos[k]), [[S(1), "rain in the year", fmt(chuvas[k]) + " mm"]]), k => { yi = k; desenhar(); });

      /* the chosen year */
      const f0 = D.primeiro_dia[yi], f1 = yi + 1 < N ? D.primeiro_dia[yi + 1] : D.chuva.length, n = f1 - f0;
      const chuva = D.chuva.slice(f0, f1), niv = D.niveis[vol].slice(f0, f1);
      const ya = escala(0, Math.max(20, ...chuva), 3);
      const A = plano({W, H: 132, l: 58, r: 14, t: 30, b: 6, x: [0, n], y: [0, ya.max], ym: ya.marcas, yr: "rain (mm/day)", painel: "(a)"});
      const yb = escala(0, vol, 4);
      const inicioMes = MESES.map((_, m) => (Date.UTC(D.anos[yi], m, 1) - Date.UTC(D.anos[yi], 0, 1)) / 864e5);
      const B = plano({W, H, l: 58, r: 14, t: 170, b: 40, x: [0, n], y: [0, yb.max], ym: yb.marcas, yf: v => fmt(v), yr: "volume stored at the end of the day (L)", painel: "(b)",
        xm: inicioMes.map((d, m) => d + ((m < 11 ? inicioMes[m + 1] : n) - d) / 2), xf: v => MESES[inicioMes.filter(d => d <= v).length - 1], xr: String(D.anos[yi])});
      let s = A.s + B.s;
      inicioMes.slice(1).forEach(d => { s += `<line class="g-mes" x1="${B.X(d)}" x2="${B.X(d)}" y1="${A.Y(ya.max)}" y2="${B.Y(0)}"/>`; });
      const bw2 = Math.max(1, (A.X(1) - A.X(0)) * 0.8);
      chuva.forEach((c, k) => { if (c > 0) s += `<rect x="${A.X(k + 0.1)}" y="${A.Y(c)}" width="${bw2}" height="${A.Y(0) - A.Y(c)}" style="fill:${S(1)}"/>`; });
      const linha = niv.map((v, k) => `${B.X(k + 0.5)},${B.Y(v)}`).join(" ");
      s += `<polygon points="${B.X(0.5)},${B.Y(0)} ${linha} ${B.X(n - 0.5)},${B.Y(0)}" style="fill:${S(3)};opacity:0.16"/>`;
      s += `<polyline points="${linha}" style="fill:none;stroke:${S(3)};stroke-width:1.6"/>`;
      niv.forEach((v, k) => { if (v <= 0.05 * vol) s += `<rect x="${B.X(k)}" y="${B.Y(0) - 5}" width="${bw2}" height="5" style="fill:${S(2)}"/>`; });
      s += `<line class="g-ref" x1="${B.X(0)}" x2="${B.X(n)}" y1="${B.Y(vol)}" y2="${B.Y(vol)}"/>`;
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ya.max)}" y2="${B.Y(0)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, niv.map((_, k) => B.X(k + 0.5)), k => dicaHTML(
        dataDe(f0 + k).toLocaleDateString(LOCALE, {timeZone: "UTC", day: "numeric", month: "long", year: "numeric"}), [
          [S(1), "rain", fmt(chuva[k], 1) + " mm"], [S(3), "stored", fmt(niv[k]) + " L"],
          ["", "of capacity", fmt(100 * niv[k] / vol, 0) + "%"]]));

      sel.value = yi;
      const r = R[yi];
      leit.innerHTML = `<p class="fi-sub">${D.anos[yi]}, ${fmt(vol)} L cistern</p>
        <div class="fi-n">
        ${cartao("Rain in the year", fmt(r[0]) + " mm", `mean: ${fmt(media(vol, 0))}`)}
        ${cartao("Rainwater demand met", fmt(r[1], 1) + "%", `mean: ${fmt(media(vol, 1), 1)}%`)}
        ${cartao("Days with the cistern empty", fmt(r[3]), `mean: ${fmt(media(vol, 3), 0)}`)}
        ${cartao("Full-supply days", fmt(r[4]), `of ${r[5]}`)}
        ${cartao("Volume overflowed", fmt(r[2], 1) + " m³", `mean: ${fmt(media(vol, 2), 1)} m³`)}
        ${cartao("Daily rainwater demand", fmt(D.demanda_pluvial) + " L", "28% of 600 L")}
        </div>
        <p class="fi-nota">“Empty” is an end of day with up to 5% of capacity. “Full supply” is a day on which the cistern covered the whole rainwater demand.</p>`;
    };
    ligarSeg(p, id + "v", v => { vol = +v; desenhar(); });
    sel.addEventListener("change", () => { yi = +sel.value; desenhar(); });
    p.querySelectorAll("[data-q]").forEach(b => b.addEventListener("click", () => {
      const R = D.resumo[vol], idx = R.map((_, k) => k);
      const q = b.dataset.q;
      yi = q === "seco" ? idx.reduce((a, k) => R[k][0] < R[a][0] ? k : a, 0)
        : q === "chuvoso" ? idx.reduce((a, k) => R[k][0] > R[a][0] ? k : a, 0)
        : idx.reduce((a, k) => R[k][3] > R[a][3] ? k : a, 0);
      desenhar();
    }));
    desenhar();
  }
};

/* ─── figure: the persistence of autonomy ───────────────────────────────── */
FI["fig47_permanencia.png"] = {
  curto: "The persistence of autonomy",
  pergunta: "How many days of consumption does the cistern hold, and for how long?",
  controles: "capacity from 0.5 to 20 m³",
  experimente: D => {
    const a = D.estados["4000"], b = D.estados["8000"];
    return `Take the capacity from 4 m³ to 8 m³: the median autonomy goes from ${fmt(a[3], 1)} to ${fmt(b[3], 1)} days and the renewals fall from ${fmt(a[0], 1)} to ${fmt(b[0], 1)} a year, but the saving potential rises only from ${fmt(a[4], 2)}% to ${fmt(b[4], 2)}%.`;
  },
  fonte: D => TUTORIAL + ` Autonomy is the volume stored at the end of the day divided by the daily rainwater demand of ${fmt(D.demanda_pluvial)} L.`,
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), refs = true;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Cistern capacity", D.volumes.length, vi)}
      <div class="fi-ctl"><span class="fi-rot">Compare with</span><button type="button" class="chip-t" id="${id}r" aria-pressed="true" style="--c:var(--ink3)"><i></i>2, 4, 10 and 20 m³</button></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 320" role="img" aria-label="Persistence curve of the cistern autonomy, in days of rainwater demand"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 190" role="img" aria-label="Annual renewals of the cistern volume as a function of capacity; click to choose the capacity"></svg>
      ${legenda([[S(1), "chosen capacity", "linha"], ["var(--ink3)", "reference capacities", "linha"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), svg2 = p.querySelector(`#${id}h`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], C = D.curvas[String(v)], E = D.estados[String(v)];
      const mostrar = refs ? D.referencias.filter(r => r !== v) : [];
      const ymax = Math.max(C[0], ...mostrar.map(r => D.curvas[String(r)][0]));
      const ey = escala(0, ymax, 5);
      const A = plano({W, H: 320, l: 58, r: 14, t: 34, b: 44, x: [0, 100], y: [0, ey.max], ym: ey.marcas, yr: "autonomy (days of rainwater demand)", painel: "(a)",
        xm: [0, 20, 40, 60, 80, 100], xf: x => x + "%", xr: "share of time the autonomy is equalled or exceeded"});
      let s = A.s;
      const curva = (arr, estilo) => `<polyline points="${D.pontos.map((q, k) => `${A.X(q)},${A.Y(arr[k])}`).join(" ")}" style="${estilo}"/>`;
      mostrar.forEach(r => {
        const c = D.curvas[String(r)];
        s += curva(c, "fill:none;stroke:var(--ink3);stroke-width:1.2;opacity:0.75");
        s += `<text class="g-t" x="${A.X(1.5)}" y="${A.Y(c[1]) - 5}">${fmt(r / 1000)} m³</text>`;
      });
      s += curva(C, `fill:none;stroke:${S(1)};stroke-width:2.6`);
      s += `<text class="g-rot" x="${A.X(52)}" y="${A.Y(C[26]) - 9}" style="fill:${S(1)}">${fmt(v / 1000, v % 1000 ? 1 : 0)} m³</text>`;
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, D.pontos.map(q => A.X(q)), k => dicaHTML(`For ${D.pontos[k]}% of the time, the cistern holds at least`, [
        [S(1), `${fmt(v / 1000, v % 1000 ? 1 : 0)} m³`, fmt(C[k], 1) + " days"],
        ...mostrar.map(r => ["var(--ink3)", `${fmt(r / 1000)} m³`, fmt(D.curvas[String(r)][k], 1) + " days"])]));

      const ren = D.volumes.map(x => D.estados[String(x)][0]);
      const er = escala(0, Math.max(...ren), 3);
      const B = plano({W, H: 190, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [0, er.max], ym: er.marcas, yr: "volume renewals per year", painel: "(b)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "cistern capacity"});
      let t = B.s + `<polyline points="${D.volumes.map((x, k) => `${B.X(x)},${B.Y(ren[k])}`).join(" ")}" style="fill:none;stroke:${S(1)};stroke-width:2"/>`;
      t += `<circle cx="${B.X(v)}" cy="${B.Y(E[0])}" r="6" style="fill:${S(1)};stroke:var(--surface);stroke-width:2"/>`;
      t += `<text class="g-rot" x="${B.X(v) + 10}" y="${B.Y(E[0]) - 8}" style="fill:var(--ink)">${fmt(E[0], 1)}×</text>`;
      svg2.innerHTML = t;
      pairar(svg2, W, D.volumes.map(x => B.X(x)), k => dicaHTML(`${fmt(D.volumes[k])} L`, [[S(1), "renewals per year", fmt(ren[k], 1) + "×"]]),
        k => { vi = k; p.querySelector(`#${id}v`).value = k; desenhar(); });

      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      leit.innerHTML = `<p class="fi-sub">${fmt(v)} L cistern</p><div class="fi-n">
        ${cartao("Median autonomy", fmt(E[3], 1), "days")}
        ${cartao("Renewals per year", fmt(E[0], 1) + "×")}
        ${cartao("Time with the cistern empty", fmt(E[1], 1) + "%")}
        ${cartao("Time with the cistern full", fmt(E[2], 1) + "%")}
        ${cartao("Saving potential", fmt(E[4], 2) + "%", "of 28%")}
        ${cartao("Daily rainwater demand", fmt(D.demanda_pluvial) + " L")}</div>
        <p class="fi-nota">Curve (a) sorts the days of the 30 years from the largest to the smallest stored volume. Where it touches zero, the time with the cistern empty begins. A renewal is the year's rainwater use divided by the capacity: how many times the water in the cistern was replaced.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    p.querySelector(`#${id}r`).addEventListener("click", e => { refs = !refs; e.currentTarget.setAttribute("aria-pressed", String(refs)); desenhar(); });
    desenhar();
  }
};

/* ─── figure: the bill under three minimum-charge regimes ───────────────── */
FI["fig05_regimes.png"] = {
  curto: "The bill under three minimum-charge regimes",
  pergunta: "How much of the water saved turns into a saving on the bill?",
  controles: "consumption without and with the system",
  experimente: "In the allowance regime, lower the consumption with the system below 10 m³: the bill stops falling, because the first 10 m³ are already paid in the minimum. Under the availability charge, the same saving yields more.",
  fonte: "Three hypothetical charging structures, in currency units and not tied to any real utility: an availability charge, an allowance in the minimum, and a bill with no minimum. The water part is computed by the same function as the program; sewerage would only multiply the three curves, without changing their shape, and the shape is what tells the regimes apart. The starting point is the mean consumption of the tutorial.",
  montar(p, D, id) {
    const passo = 0.25, n = Math.round(30 / passo) + 1;
    const idx = v => Math.round(v / passo);
    let iSem = idx(D.padrao[0]), iCom = idx(D.padrao[1]);
    const W = 640, H = 350;
    const cores = [S(1), S(2), S(3)];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "s", "Consumption without the system", n, iSem)}
      ${ctlFaixa(id + "c", "Consumption with the system", n, iCom)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Monthly water bill as a function of consumption, under three charging structures"></svg>
      ${legenda(D.curvas.map((c, k) => [cores[k], c.nome, k === 1 ? "trac" : "linha"]).concat([["var(--accent-soft)", "water saved by the system"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      if (iCom > iSem) { iCom = iSem; p.querySelector(`#${id}c`).value = iCom; }
      const cs = D.consumos.slice(0, n);
      const ymax = Math.max(...D.curvas.map(c => c.fatura[n - 1]));
      const ey = escala(0, ymax, 5);
      const A = plano({W, H, l: 58, r: 150, t: 34, b: 44, x: [0, 30], y: [0, ey.max], ym: ey.marcas, yf: v => fmt(v), yr: "water part of the monthly bill (currency units)",
        xm: [0, 5, 10, 15, 20, 25, 30], xf: v => v + " m³", xr: "monthly potable water consumption"});
      let s = `<rect x="${A.X(cs[iCom])}" y="${A.Y(ey.max)}" width="${Math.max(0, A.X(cs[iSem]) - A.X(cs[iCom]))}" height="${A.Y(0) - A.Y(ey.max)}" style="fill:var(--accent-soft)"/>` + A.s;
      const rot = [];
      D.curvas.forEach((c, k) => {
        s += `<polyline points="${cs.map((x, i) => `${A.X(x)},${A.Y(c.fatura[i])}`).join(" ")}" style="fill:none;stroke:${cores[k]};stroke-width:${k === 1 ? 2.6 : 2.2}${k === 1 ? ";stroke-dasharray:7 5" : ""}"/>`;
        rot.push({y: A.Y(c.fatura[n - 1]), t: c.nome, c: cores[k]});
      });
      s += rotulosNaPonta(rot, A.X(30) + 8, A.Y(ey.max), A.Y(0));
      [[iSem, "without the system"], [iCom, "with the system"]].forEach(([i, t], j) => {
        s += `<line class="g-ref" x1="${A.X(cs[i])}" x2="${A.X(cs[i])}" y1="${A.Y(ey.max)}" y2="${A.Y(0)}"/>`;
        s += `<text class="g-t" x="${A.X(cs[i]) + (j ? -5 : 5)}" y="${A.Y(ey.max) + 12}" text-anchor="${j ? "end" : "start"}">${t}</text>`;
        D.curvas.forEach((c, k) => { s += `<circle cx="${A.X(cs[i])}" cy="${A.Y(c.fatura[i])}" r="5" style="fill:${cores[k]};stroke:var(--surface);stroke-width:2"/>`; });
      });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, cs.map(x => A.X(x)), i => dicaHTML(`Consumption of ${fmt(cs[i], 2)} m³/month · water part`,
        D.curvas.map((c, k) => [cores[k], c.nome, fmt(c.fatura[i], 2)])));
      p.querySelector(`#${id}s-o`).textContent = fmt(cs[iSem], 2) + " m³/month";
      p.querySelector(`#${id}c-o`).textContent = fmt(cs[iCom], 2) + " m³/month";
      const agua = cs[iSem] - cs[iCom];
      leit.innerHTML = `<p class="fi-sub">Potable water saved: ${fmt(agua, 2)} m³/month</p>
        <table class="fi-tabela"><thead><tr><th>Regime</th><th class="n">Without</th><th class="n">With</th><th class="n">Saving</th></tr></thead><tbody>
        ${D.curvas.map((c, k) => {
          const a = c.fatura[iSem], b = c.fatura[iCom], e = a - b;
          return `<tr><td><i style="--c:${cores[k]}"></i>${c.nome}<small>${c.exemplo}</small></td><td class="n">${fmt(a)}</td><td class="n">${fmt(b)}</td>
            <td class="n"><b>${fmt(e)}</b><small>${a > 0 ? fmt(100 * e / a, 0) + "% of the bill" : ""}${agua > 0 ? " · " + fmt(e / agua, 2) + "/m³" : ""}</small></td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">Above 10 m³, the allowance and the no-minimum structure charge the same, and the two lines overlap (the allowance is dashed); the difference between them lies entirely below 10 m³. What decides the saving is not the average price but the band in which the consumption falls and what stays fixed. A bill that does not move with the water saved can make a system unviable where, in another city, it would pay back.</p>`;
    };
    p.querySelector(`#${id}s`).addEventListener("input", e => { iSem = +e.target.value; if (iCom > iSem) iCom = iSem; desenhar(); });
    p.querySelector(`#${id}c`).addEventListener("input", e => { iCom = Math.min(+e.target.value, iSem); desenhar(); });
    desenhar();
  }
};

/* ─── figure: the cash flow ─────────────────────────────────────────────── */
FI["fig08_fluxo_de_caixa.png"] = {
  curto: "When the investment pays back",
  pergunta: "When does the investment in the cistern pay back?",
  controles: "volume · material",
  experimente: D => {
    const v = D.padrao[0];
    const itens = D.materiais.map(([k, t]) => [t, D.casos[`${v}|${k}`]]);
    const todos = itens.every(([, c]) => c.retorno === null);
    return `At ${fmt(v / 1000)} m³ the NPV over ${D.anos} years ranges from ${din(Math.max(...itens.map(([, c]) => c.vpl)))} to ${din(Math.min(...itens.map(([, c]) => c.vpl)))} depending on the material; ${todos ? "none of the four pays back within the horizon" : itens.filter(([, c]) => c.retorno !== null).map(([t]) => curto(t)).join(" and ") + " pay back, the others do not"}. Raise the volume and watch the investment grow faster than the saving. ${ILUSTRATIVO}`;
  },
  fonte: D => {
    const F = DADOS.interativas["fig07_fatura.png"];
    return TUTORIAL + ` Pumping to a 1,000 L upper tank, the New York tariff of the program's example project with the sewer at ${fmt(F.esgoto_pct)}% of the water charge, a minimum attractive rate of return of ${fmt(D.tma, 1)}% a month, a ${D.anos}-year horizon, illustrative costs (not market prices).`;
  },
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao[0]), mat = D.padrao[1];
    const W = 700, H = 370;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Cistern volume", D.volumes.length, vi)}
      ${ctlSeg(id + "m", "Cistern material", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Saving and costs of each year, and the cumulative discounted balance over ${D.anos} years"></svg>
      ${legenda([[S(4), "saving on the water and sewer bill"], [S(2), "investment (year 0) and annual running cost"], [S(3), "cumulative discounted balance", "linha"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], c = D.casos[`${v}|${mat}`], n = c.economia.length;
      const lo = Math.min(-c.custo[0], ...c.acumulado), hi = Math.max(...c.economia, ...c.acumulado, 0);
      const ey = escala(lo, hi, 6);
      const A = plano({W, H, l: 70, r: 14, t: 34, b: 44, x: [-0.7, n - 0.3], y: [ey.min, ey.max], ym: ey.marcas, yf: v => menos(v), yr: `value (${MOEDA})`,
        xm: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20].filter(a => a < n), xr: "year of operation"});
      let s = A.s;
      const w = (A.X(1) - A.X(0)) * 0.36;
      for (let a = 0; a < n; a++) {
        if (c.economia[a] > 0) s += `<rect x="${A.X(a) - w - 1}" y="${A.Y(c.economia[a])}" width="${w}" height="${A.Y(0) - A.Y(c.economia[a])}" rx="2" style="fill:${S(4)}"/>`;
        if (c.custo[a] > 0) s += `<rect x="${A.X(a) + 1}" y="${A.Y(0)}" width="${w}" height="${A.Y(-c.custo[a]) - A.Y(0)}" rx="2" style="fill:${S(2)}"/>`;
      }
      s += `<polyline points="${c.acumulado.map((x, a) => `${A.X(a)},${A.Y(x)}`).join(" ")}" style="fill:none;stroke:${S(3)};stroke-width:2.2"/>`;
      c.acumulado.forEach((x, a) => { s += `<circle cx="${A.X(a)}" cy="${A.Y(x)}" r="3.5" style="fill:${S(3)};stroke:var(--surface);stroke-width:1.5"/>`; });
      if (c.retorno) {
        const esq = c.retorno > n / 2;
        s += `<line x1="${A.X(c.retorno)}" x2="${A.X(c.retorno)}" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="stroke:${S(3)};stroke-dasharray:3 4"/>`;
        s += `<text class="g-rot" x="${A.X(c.retorno) + (esq ? -6 : 6)}" y="${A.Y(ey.min) - 8}" text-anchor="${esq ? "end" : "start"}" style="fill:var(--ink)">pays back in ${fmt(c.retorno, 1)} years</text>`;
      }
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, c.economia.map((_, a) => A.X(a)), a => dicaHTML(a ? `Year ${a}` : "Year 0 · installation", [
        [S(4), "saving", din(c.economia[a])], [S(2), a ? "running cost" : "investment", din(-c.custo[a])],
        [S(3), "cumulative discounted balance", din(c.acumulado[a])]]));
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const tma = (Math.pow(1 + D.tma / 100, 12) - 1) * 100;
      const nomeMat = D.materiais.find(m => m[0] === mat)[1];
      leit.innerHTML = `<p class="fi-sub">${fmt(v)} L, ${nomeMat.toLowerCase()}</p><div class="fi-n">
        ${cartao("Initial investment", din(c.capex))}
        ${cartao("Net saving in year 1", din(c.economia[1] - c.custo[1]))}
        ${cartao(`NPV over ${D.anos} years`, din(c.vpl), c.vpl >= 0 ? "✓ positive" : "✕ negative")}
        ${cartao("Discounted payback", c.retorno ? fmt(c.retorno, 1) + " years" : `more than ${D.anos} years`)}
        ${cartao("IRR", c.tir === null ? "—" : fmt(c.tir, 1) + "% p.a.", `MARR: ${fmt(tma, 1)}% p.a.`)}
        ${cartao("Saving potential", fmt(c.potencial, 2) + "%")}</div>
        <p class="fi-sub">NPV over ${D.anos} years, at this volume, by material</p>
        <table class="fi-tabela"><tbody>${D.materiais.map(([k, t]) => {
          const x = D.casos[`${v}|${k}`];
          return `<tr${k === mat ? ' class="atual"' : ""}><td>${t}</td><td class="n">${din(x.vpl)}</td><td class="n">${x.retorno ? fmt(x.retorno, 1) + " years" : "no payback"}</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">${ILUSTRATIVO}</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarSeg(p, id + "m", v => { mat = v; desenhar(); });
    desenhar();
  }
};

/* ─── figure: carbon over the service life ──────────────────────────────── */
FI["fig06_carbono_no_tempo.png"] = {
  curto: "The carbon payback",
  pergunta: "In how many years does the cistern give back the carbon spent to make it?",
  controles: "volume · material",
  experimente: D => {
    const v = D.padrao;
    const itens = D.materiais.map(([k, t]) => [t, D.casos[`${v}|${k}`][4]]);
    const dentro = itens.filter(([, r]) => r !== null && r <= D.anos), fora = itens.filter(([, r]) => r === null || r > D.anos);
    const lista = a => a.map(([t, r]) => `${curto(t)} (${r === null ? "never" : fmt(r, 1) + " years"})`).join(", ");
    return `At ${fmt(v / 1000)} m³, ${dentro.length ? lista(dentro) + " return the carbon within " + D.anos + " years" : "no material returns the carbon within " + D.anos + " years"}${fora.length ? "; " + lista(fora) + (dentro.length ? " do not" : "") : ""}. Reduce the volume: the embodied carbon falls, but so does the water saved.`;
  },
  fonte: TUTORIAL + " Embodied carbon of the whole system (cistern, upper tank, piping, pump and first-flush device) and annual credit for the potable water avoided, net of pumping and treatment. Positive emits, negative removes: the curve starts at the manufacturing debt and descends. Emission factors from the life cycle assessment section.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), ativos = D.materiais.map(m => m[0]);
    const W = 640, H = 350;
    const corDoMat = k => S(D.materiais.findIndex(m => m[0] === k) + 1);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Cistern volume", D.volumes.length, vi)}
      ${ctlChips(id + "m", "Materials", D.materiais.map(([k, t]) => [k, t, corDoMat(k)]), ativos)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Cumulative carbon balance over ${D.anos} years, by cistern material"></svg>
      ${legenda(D.materiais.map(([k, t]) => [corDoMat(k), t, "linha"]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], anos = D.anos;
      const casos = ativos.map(k => ({k, c: D.casos[`${v}|${k}`]}));
      // Net emissions: positive emits, negative removes. The curve starts at the
      // embodied carbon and falls with the annual credit for the water avoided.
      const lo = Math.min(0, ...casos.map(x => x.c[0] - x.c[1] * anos)), hi = Math.max(...casos.map(x => x.c[0]));
      const ey = escala(lo, hi, 6);
      const A = plano({W, H, l: 66, r: 130, t: 34, b: 44, x: [0, anos], y: [ey.min, ey.max], ym: ey.marcas, yr: "cumulative net emissions (kg CO₂e)",
        xm: [0, 5, 10, 15, 20], xr: "years of operation"});
      let s = A.s;
      const rot = [];
      let cruzou = 0;
      casos.forEach(({k, c}) => {
        const cor = corDoMat(k), fim = c[0] - c[1] * anos;
        s += `<line x1="${A.X(0)}" y1="${A.Y(c[0])}" x2="${A.X(anos)}" y2="${A.Y(fim)}" style="stroke:${cor};stroke-width:2.4"/>`;
        if (c[4] !== null && c[4] <= anos) {
          const t = c[4], acima = cruzou++ % 2 === 0;
          s += `<circle cx="${A.X(t)}" cy="${A.Y(0)}" r="6" style="fill:${cor};stroke:var(--surface);stroke-width:2"/>`;
          s += `<text class="g-rot" x="${A.X(t)}" y="${A.Y(0) + (acima ? -12 : 22)}" text-anchor="middle" style="fill:${cor}">${fmt(t, 1)} years</text>`;
        }
        rot.push({y: A.Y(fim), t: D.materiais.find(m => m[0] === k)[1], c: cor});
      });
      s += rotulosNaPonta(rot, A.X(anos) + 8, A.Y(ey.max), A.Y(ey.min));
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      svg.innerHTML = s;
      const xs = Array.from({length: anos + 1}, (_, a) => A.X(a));
      pairar(svg, W, xs, a => dicaHTML(`Year ${a}`, casos.map(({k, c}) => [corDoMat(k), D.materiais.find(m => m[0] === k)[1], menos(c[1] * a - c[0]) + " kg CO₂e"])));
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const creditos = [...new Set(D.materiais.map(([k]) => D.casos[`${v}|${k}`][1]))];
      leit.innerHTML = `<p class="fi-sub">${fmt(v)} L cistern</p>
        <table class="fi-tabela"><thead><tr><th>Material</th><th class="n">Embodied</th><th class="n">Payback</th><th class="n">At ${anos} years</th></tr></thead><tbody>
        ${D.materiais.map(([k, t]) => {
          const c = D.casos[`${v}|${k}`], ret = c[4] === null ? Infinity : c[4];
          return `<tr${ativos.includes(k) ? "" : ' class="apagado"'}><td><i style="--c:${corDoMat(k)}"></i>${t}<small>cistern of ${fmt(c[2])} kg</small></td>
            <td class="n">${fmt(c[0])} kg</td><td class="n">${ret <= anos ? fmt(ret, 1) + " years" : `more than ${anos} years`}</td><td class="n">${menos(c[1] * anos - c[0])} kg</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">${creditos.length === 1
          ? `The net credit of the operation is ${fmt(creditos[0], 1)} kg CO₂e a year for all four materials: the water saved does not depend on the material. What changes is the manufacturing carbon, and it is what decides the payback.`
          : "The net credit of the operation varies little between materials; the manufacturing carbon is what decides the payback."}
          Values in kg CO₂e; the balance starts at the embodied carbon, with a positive sign.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarChips(p, id + "m", a => { ativos = a; desenhar(); });
    desenhar();
  }
};

/* ─── figure: three cities ──────────────────────────────────────────────── */
FI["fig03_cidades.png"] = {
  curto: "Three cities, the same house",
  pergunta: "What changes when the same house is in another city?",
  controles: "cities · volume",
  experimente: D => {
    const k90 = c => { const mx = c.potencial[c.potencial.length - 1]; return D.volumes[c.potencial.findIndex(q => q >= 0.9 * mx)]; };
    const ordem = D.cidades.slice().sort((a, b) => k90(b) - k90(a));
    const a = ordem[0], b = ordem[ordem.length - 1];
    return `Compare ${a.nome} and ${b.nome}: ${a.nome} needs ${fmt(k90(a) / 1000)} m³ to reach 90% of its maximum potential, and ${b.nome} reaches it with ${fmt(k90(b) / 1000)} m³ (${fmt(a.anual)} mm and ${fmt(b.anual)} mm of rain a year). The annual total is not enough: how the rain is distributed through the year matters.`;
  },
  fonte: "The tutorial house (150 m² of roof, four residents, 28% of the demand suppliable by rain), simulated with 30 years of the series of each city. Mean monthly rain from the series itself.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), ativos = D.cidades.map(c => c.chave);
    const W = 640;
    const corDe = k => S(D.cidades.findIndex(c => c.chave === k) + 1);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlChips(id + "c", "Cities", D.cidades.map(c => [c.chave, c.nome, corDe(c.chave)]), ativos)}
      ${ctlFaixa(id + "v", "Cistern volume", D.volumes.length, vi)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}a" viewBox="0 0 ${W} 250" role="img" aria-label="Mean rain of each month in the chosen cities"></svg>
      <svg id="${id}b" viewBox="0 0 ${W} 290" role="img" aria-label="Potable water saving potential as a function of cistern volume, by city"></svg>
      ${legenda(D.cidades.map(c => [corDe(c.chave), c.nome, "linha"]).concat([["var(--ink3)", "ceiling: suppliable fraction of 28%", "trac"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const sa = p.querySelector(`#${id}a`), sb = p.querySelector(`#${id}b`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const cs = D.cidades.filter(c => ativos.includes(c.chave)), v = D.volumes[vi];
      const em = escala(0, Math.max(...cs.flatMap(c => c.mensal)), 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 30, x: [0.5, 12.5], y: [0, em.max], ym: em.marcas, yr: "mean rain of the month (mm)", painel: "(a)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xf: m => MESES[m - 1]});
      let s = A.s;
      cs.forEach(c => {
        s += `<polyline points="${c.mensal.map((x, m) => `${A.X(m + 1)},${A.Y(x)}`).join(" ")}" style="fill:none;stroke:${corDe(c.chave)};stroke-width:2.2"/>`;
        c.mensal.forEach((x, m) => { s += `<circle cx="${A.X(m + 1)}" cy="${A.Y(x)}" r="3.5" style="fill:${corDe(c.chave)};stroke:var(--surface);stroke-width:1.5"/>`; });
      });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(em.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      sa.innerHTML = s;
      pairar(sa, W, MESES.map((_, m) => A.X(m + 1)), m => dicaHTML(`Mean rain in ${MESES[m]}`, cs.map(c => [corDe(c.chave), c.nome, fmt(c.mensal[m]) + " mm"])));

      const teto = D.fracao * 100;
      const B = plano({W, H: 290, l: 58, r: 100, t: 34, b: 44, x: [0, 20000], y: [0, 30], ym: [0, 5, 10, 15, 20, 25, 30], yf: v => v + "%", yr: "potable water saving potential", painel: "(b)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "cistern volume"});
      let t = B.s + `<line class="g-ref" x1="${B.X(0)}" x2="${B.X(20000)}" y1="${B.Y(teto)}" y2="${B.Y(teto)}"/>`;
      t += `<line x1="${B.X(v)}" x2="${B.X(v)}" y1="${B.Y(30)}" y2="${B.Y(0)}" style="stroke:var(--ink3);stroke-width:1"/>`;
      const rot = [];
      cs.forEach(c => {
        const cor = corDe(c.chave);
        t += `<polyline points="${c.potencial.map((q, k) => `${B.X(D.volumes[k])},${B.Y(q)}`).join(" ")}" style="fill:none;stroke:${cor};stroke-width:2.2"/>`;
        t += `<circle cx="${B.X(v)}" cy="${B.Y(c.potencial[vi])}" r="5.5" style="fill:${cor};stroke:var(--surface);stroke-width:2"/>`;
        rot.push({y: B.Y(c.potencial[c.potencial.length - 1]), t: c.nome, c: cor});
      });
      t += rotulosNaPonta(rot, B.X(20000) + 8, B.Y(30), B.Y(0));
      sb.innerHTML = t;
      pairar(sb, W, D.volumes.map(x => B.X(x)), k => dicaHTML(`${fmt(D.volumes[k])} L`, cs.map(c => [corDe(c.chave), c.nome, fmt(c.potencial[k], 2) + "%"])),
        k => { vi = k; p.querySelector(`#${id}v`).value = k; desenhar(); });
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      leit.innerHTML = `<p class="fi-sub">${fmt(v)} L cistern</p>
        <table class="fi-tabela"><thead><tr><th>City</th><th class="n">Annual rain</th><th class="n">Potential</th><th class="n">90% of maximum at</th></tr></thead><tbody>
        ${D.cidades.map(c => {
          const max = c.potencial[c.potencial.length - 1];
          const k90 = c.potencial.findIndex(q => q >= 0.9 * max);
          return `<tr${ativos.includes(c.chave) ? "" : ' class="apagado"'}><td><i style="--c:${corDe(c.chave)}"></i>${c.nome}<small>rains on ${fmt(c.dias_chuva, 0)}% of the days</small></td>
            <td class="n">${fmt(c.anual)} mm</td><td class="n"><b>${fmt(c.potencial[vi], 2)}%</b></td><td class="n">${fmt(D.volumes[k90] / 1000)} m³</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">“90% of maximum” is the smallest volume that reaches nine tenths of the potential obtained with 20 m³. The longer the dry season, the larger the cistern for the same result.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarChips(p, id + "c", a => { ativos = a; desenhar(); });
    desenhar();
  }
};

/* ─── figure: the return curve and the ideal volume ─────────────────────── */
/* The ideal volume by the marginal-gain criterion, from the grid of the home page. */
function volumeIdealDaGrade(f, passo, lim) {
  const C = DADOS.curva, linhas = C.grade[f.toFixed(2)];
  const vol = C.volumes.filter(v => v % passo === 0);
  const pot = vol.map(v => linhas[C.volumes.indexOf(v)][0]);
  const ganho = pot.map((q, i) => i ? (q - pot[i - 1]) / ((vol[i] - vol[i - 1]) / 1000) : null);
  const i = ganho.findIndex((g, k) => k > 0 && g <= lim);
  return i < 0 ? vol[vol.length - 1] : vol[i];
}
FI["fig02_curva_de_retorno.png"] = {
  curto: "The return curve and the ideal volume",
  pergunta: "How far is it worth enlarging the cistern?",
  controles: "suppliable fraction · threshold · grid step",
  experimente: () => `With 28% and the threshold of 1 %/m³, the ideal volume is ${fmt(volumeIdealDaGrade(0.28, 1000, 1))} L on the 1,000 L grid. Change the grid step to 500 L and it becomes ${fmt(volumeIdealDaGrade(0.28, 500, 1))} L; to 2,000 L, ${fmt(volumeIdealDaGrade(0.28, 2000, 1))} L. Nothing in the project changed: it is the effect of the step that the section discusses. Raise the threshold to 5 %/m³, the value the program opens with, and the ideal becomes ${fmt(volumeIdealDaGrade(0.28, 1000, 5))} L.`,
  fonte: TUTORIAL + " One simulation per volume, from 0 to 20,000 L in steps of 500 L, for each suppliable fraction from 10% to 60%.",
  montar(p, D, id) {
    let fi = D.fracoes.findIndex(f => Math.abs(f - 0.28) < 1e-6), passo = 1000, lim = 1, vsel = 4000;
    const W = 640, LIMIARES = [0.5, 1, 2, 5];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "f", "Fraction of the demand suppliable by rain", D.fracoes.length, fi)}
      ${ctlSeg(id + "q", "Marginal-gain threshold", LIMIARES.map(x => [x, fmt(x, x < 1 ? 1 : 0) + " %/m³"]), lim)}
      ${ctlSeg(id + "p", "Grid step", [[500, "500 L"], [1000, "1,000 L"], [2000, "2,000 L"]], passo)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}a" viewBox="0 0 ${W} 280" role="img" aria-label="Saving potential as a function of cistern volume, with the ideal volume marked; click to choose a volume"></svg>
      <svg id="${id}b" viewBox="0 0 ${W} 250" role="img" aria-label="Marginal gain in potential per cubic metre, on a logarithmic scale, with the threshold"></svg>
      ${legenda([[S(1), "saving potential", "linha"], [S(2), "marginal gain per m³", "linha"], ["var(--ink3)", "ceiling and threshold", "trac"], [S(4), "ideal volume", "linha"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const sa = p.querySelector(`#${id}a`), sb = p.querySelector(`#${id}b`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const f = D.fracoes[fi], teto = f * 100, linhas = D.grade[f.toFixed(2)];
      const ks = D.volumes.map((v, k) => k).filter(k => D.volumes[k] % passo === 0);
      const vol = ks.map(k => D.volumes[k]), pot = ks.map(k => linhas[k][0]);
      const ganho = pot.map((q, i) => i ? (q - pot[i - 1]) / ((vol[i] - vol[i - 1]) / 1000) : null);
      let ii = ganho.findIndex((g, i) => i > 0 && g <= lim);
      const noLimite = ii < 0;
      if (noLimite) ii = vol.length - 1;
      const ideal = vol[ii];
      if (!vol.includes(vsel)) vsel = vol.reduce((a, v) => Math.abs(v - vsel) < Math.abs(a - vsel) ? v : a, vol[0]);
      const is = vol.indexOf(vsel), ls = linhas[D.volumes.indexOf(vsel)];

      const ey = escala(0, Math.max(teto, ...pot) * 1.08, 5);
      const A = plano({W, H: 280, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [0, ey.max], ym: ey.marcas, yf: v => fmt(v) + "%", yr: "potable water saving potential", painel: "(a)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "cistern volume"});
      let s = A.s + `<line class="g-ref" x1="${A.X(0)}" x2="${A.X(20000)}" y1="${A.Y(teto)}" y2="${A.Y(teto)}"/>`;
      s += `<text class="g-t" x="${A.X(20000)}" y="${A.Y(teto) - 6}" text-anchor="end">ceiling: suppliable fraction of ${fmt(teto)}%</text>`;
      s += `<line x1="${A.X(ideal)}" x2="${A.X(ideal)}" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="stroke:${S(4)};stroke-width:1.6;stroke-dasharray:2 3"/>`;
      s += `<text class="g-rot" x="${A.X(ideal) + 7}" y="${A.Y(ey.max * 0.2)}" style="fill:${S(4)}">ideal volume: ${fmt(ideal)} L</text>`;
      s += `<polyline points="${vol.map((v, i) => `${A.X(v)},${A.Y(pot[i])}`).join(" ")}" style="fill:none;stroke:${S(1)};stroke-width:2.2"/>`;
      vol.forEach((v, i) => { s += `<circle cx="${A.X(v)}" cy="${A.Y(pot[i])}" r="${v === vsel ? 6.5 : 3}" style="fill:${S(1)};stroke:var(--surface);stroke-width:${v === vsel ? 2 : 1}"/>`; });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      sa.innerHTML = s;
      const escolher = i => { vsel = vol[i]; desenhar(); };
      pairar(sa, W, vol.map(v => A.X(v)), i => dicaHTML(`${fmt(vol[i])} L`, [[S(1), "potential", fmt(pot[i], 2) + "%"],
        [S(2), "gain of the last step", ganho[i] === null ? "—" : fmt(ganho[i], 2) + " %/m³"]]), escolher);

      const LOGMIN = -3, LOGMAX = 2;
      const B = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [LOGMIN, LOGMAX], ym: [-3, -2, -1, 0, 1, 2], yf: e => fmt(Math.pow(10, e), Math.max(0, -e)),
        yr: "marginal gain (%/m³, logarithmic scale)", painel: "(b)", xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "cistern volume"});
      const LY = g => B.Y(Math.max(LOGMIN, Math.min(LOGMAX, Math.log10(Math.max(g, 1e-3)))));
      let t = B.s + `<line class="g-ref" x1="${B.X(0)}" x2="${B.X(20000)}" y1="${LY(lim)}" y2="${LY(lim)}"/>`;
      t += `<text class="g-t" x="${B.X(20000)}" y="${LY(lim) - 6}" text-anchor="end">threshold: ${fmt(lim, lim < 1 ? 1 : 0)} %/m³</text>`;
      t += `<line x1="${B.X(ideal)}" x2="${B.X(ideal)}" y1="${B.Y(LOGMAX)}" y2="${B.Y(LOGMIN)}" style="stroke:${S(4)};stroke-width:1.6;stroke-dasharray:2 3"/>`;
      // The potential comes with two decimals; below that the gain is zero and does not fit on a log scale.
      const gp = vol.map((v, i) => [v, ganho[i]]).filter(([, g]) => g !== null && g > 0);
      const zero = vol.find((v, i) => i > 0 && ganho[i] <= 0);
      if (zero !== undefined) t += `<text class="g-t" x="${B.X(zero)}" y="${B.Y(LOGMIN) - 8}">gain below 0.01 point from ${fmt(zero / 1000)} m³</text>`;
      t += `<polyline points="${gp.map(([v, g]) => `${B.X(v)},${LY(g)}`).join(" ")}" style="fill:none;stroke:${S(2)};stroke-width:2"/>`;
      gp.forEach(([v, g]) => { t += `<circle cx="${B.X(v)}" cy="${LY(g)}" r="${v === ideal ? 6 : 3}" style="fill:${v === ideal ? S(4) : S(2)};stroke:var(--surface);stroke-width:1.5"/>`; });
      sb.innerHTML = t;
      pairar(sb, W, vol.map(v => B.X(v)), i => dicaHTML(`${fmt(vol[i])} L`, [[S(2), "marginal gain", ganho[i] === null ? "—" : fmt(ganho[i], 3) + " %/m³"]]), escolher);

      p.querySelector(`#${id}f-o`).textContent = fmt(teto) + "%";
      leit.innerHTML = `<p class="fi-sub">Ideal volume</p><div class="fi-n">
        ${cartao("By the marginal-gain criterion", fmt(ideal) + " L", noLimite ? "grid limit" : "")}
        ${cartao("Potential at the ideal volume", fmt(pot[ii], 2) + "%", `of ${fmt(teto)}%`)}</div>
        <p class="fi-sub">Highlighted volume: ${fmt(vsel)} L <span style="text-transform:none;letter-spacing:0;font-weight:400">(click the chart to change)</span></p><div class="fi-n">
        ${cartao("Saving potential", fmt(ls[0], 2) + "%")}
        ${cartao("Gain of the last step", ganho[is] === null ? "—" : fmt(ganho[is], 2), "%/m³")}
        ${cartao("Full-supply days", fmt(ls[1], 1) + "%")}
        ${cartao("Mean overflow", fmt(ls[2]), "L/day")}</div>
        <p class="fi-nota">The ideal volume is the smallest volume on the grid whose gain per cubic metre, relative to the previous volume on the grid, has already fallen below the threshold. ${noLimite ? "In this combination no volume up to 20,000 L crosses the threshold, and the program adopts the largest volume on the grid and warns in the report." : "The criterion is hydraulic: it looks at neither cost nor carbon."}</p>`;
    };
    p.querySelector(`#${id}f`).addEventListener("input", e => { fi = +e.target.value; desenhar(); });
    ligarSeg(p, id + "q", v => { lim = +v; desenhar(); });
    ligarSeg(p, id + "p", v => { passo = +v; desenhar(); });
    desenhar();
  }
};

/* ─── TOPSIS, with the weights in the reader's hands ────────────────────── */

/** The same calculation as triton/core/topsis.py: shift by column, normalise
 *  by the vector, weight, measure the distance to the ideal and the anti-ideal. */
function topsisEscores(matriz, pesos, beneficio, volumes) {
  const n = matriz.length, m = pesos.length;
  const total = pesos.reduce((a, b) => a + b, 0);
  const w = pesos.map(x => x / total);
  const min = [], max = [];
  for (let j = 0; j < m; j++) {
    const col = matriz.map(l => l[j]);
    min.push(Math.min(...col)); max.push(Math.max(...col));
  }
  const norma = [];
  for (let j = 0; j < m; j++) {
    let s = 0;
    for (let i = 0; i < n; i++) s += Math.pow(matriz[i][j] - min[j], 2);
    norma.push(Math.sqrt(s) || 1);
  }
  const pond = matriz.map(l => l.map((x, j) => (x - min[j]) / norma[j] * w[j]));
  const ideal = [], antiideal = [];
  for (let j = 0; j < m; j++) {
    const col = pond.map(l => l[j]);
    ideal.push(beneficio[j] ? Math.max(...col) : Math.min(...col));
    antiideal.push(beneficio[j] ? Math.min(...col) : Math.max(...col));
  }
  const escores = pond.map(l => {
    const db = Math.sqrt(l.reduce((a, x, j) => a + Math.pow(x - ideal[j], 2), 0));
    const dp = Math.sqrt(l.reduce((a, x, j) => a + Math.pow(x - antiideal[j], 2), 0));
    return db + dp > 2.2e-16 ? dp / (db + dp) : 0.5;
  });
  if (n === 1) escores[0] = 1;
  // A tie is resolved by the smaller volume, as in the program.
  const ordem = escores.map((s, i) => i).sort((a, b) => escores[b] - escores[a] || volumes[a] - volumes[b]);
  const postos = new Array(n);
  ordem.forEach((i, k) => { postos[i] = k + 1; });
  // Proximity by criterion: 1 is the best observed in the column.
  const prox = matriz.map(l => l.map((x, j) => {
    const faixa = max[j] - min[j];
    if (faixa <= 0) return 1;
    return 1 - (beneficio[j] ? (max[j] - x) / faixa : (x - min[j]) / faixa);
  }));
  return {escores, postos, proximidade: prox, pesos: w};
}

/* The eight criterion weights: the weight of each dimension shared among its criteria by the
 * criterion shares, as pesos_dos_criterios in triton/core/topsis.py (only the proportion
 * within the dimension matters). */
function pesosDosCriterios(D, p4, partes) {
  const eixos = D.eixos.map(([k]) => k);
  const total = p4.reduce((a, b) => a + b, 0) || 1;
  return D.criterios.map((c, j) => {
    const soma = D.criterios.reduce((a, cc, jj) => a + (cc.eixo === c.eixo ? partes[jj] : 0), 0);
    return soma > 0 ? p4[eixos.indexOf(c.eixo)] / total * partes[j] / soma : 0;
  });
}

/* The winner for a weight on each of the four dimensions, with the default criterion shares. */
function vencedorDosEixos(D, p4) {
  const w = pesosDosCriterios(D, p4, D.partes_padrao || D.criterios.map(() => 1));
  const r = topsisEscores(D.matriz, w, D.criterios.map(c => c.beneficio), D.volumes);
  return D.volumes[r.postos.indexOf(1)];
}

/* The choice band, as faixa_de_escolha in triton/core/topsis.py: the volumes above zero whose
 * score, scaled from the worst (0) to the best (1) of those volumes, lies within the tolerance
 * of the best (5% of the score range by default). Returns the indices, by increasing volume. */
function faixaDeEscolha(volumes, escores, tol = 0.05) {
  const idx = volumes.map((v, i) => i).filter(i => volumes[i] > 0 && isFinite(escores[i]));
  if (!idx.length) return [];
  const ss = idx.map(i => escores[i]), lo = Math.min(...ss), hi = Math.max(...ss), amp = hi - lo;
  return idx.filter(i => (amp > 1e-12 ? (escores[i] - lo) / amp : 1) >= 1 - tol - 1e-12)
    .sort((a, b) => volumes[a] - volumes[b]);
}

/* The band in words: «2,000–3,000 L»; «1,000 L» with one volume; a list when a volume is missing inside it. */
function textoDaFaixa(volumes, faixa) {
  const v = faixa.map(i => volumes[i]);
  if (!v.length) return "—";
  if (v.length === 1) return `${fmt(v[0])} L`;
  const dentro = volumes.filter(x => x > 0 && x >= v[0] && x <= v[v.length - 1]).length;
  return dentro === v.length ? `${fmt(v[0])}–${fmt(v[v.length - 1])} L`
    : `${v.slice(0, -1).map(x => fmt(x)).join(", ")} and ${fmt(v[v.length - 1])} L`;
}

/* The band for a weight on each of the four dimensions, with the default criterion shares. */
function faixaDosEixos(D, p4) {
  const w = pesosDosCriterios(D, p4, D.partes_padrao || D.criterios.map(() => 1));
  const r = topsisEscores(D.matriz, w, D.criterios.map(c => c.beneficio), D.volumes);
  return textoDaFaixa(D.volumes, faixaDeEscolha(D.volumes, r.escores));
}

/* The colour of each dimension in the proximity bars. */
const COR_DO_EIXO = {technical: 3, economic: 2, environmental: 4, structural: 1};

FI["fig51_programa_topsis.png"] = {
  curto: "The multi-criteria decision",
  pergunta: "Which volumes does the multi-criteria method favour, and with what weights?",
  controles: "technical · economic · environmental · structural weight · criterion shares",
  experimente: D => `With the four dimensions equal, as the program opens, the cisterns of ${faixaDosEixos(D, [1, 1, 1, 1])} score alike: that is the choice band, with the highest score at ${fmt(vencedorDosEixos(D, [1, 1, 1, 1]))} L. Give 70% to one dimension and 10% to each of the others, and the band moves: technical, ${faixaDosEixos(D, [0.7, 0.1, 0.1, 0.1])}; economic, ${faixaDosEixos(D, [0.1, 0.7, 0.1, 0.1])}; environmental, ${faixaDosEixos(D, [0.1, 0.1, 0.7, 0.1])}; structural, ${faixaDosEixos(D, [0.1, 0.1, 0.1, 0.7])}. The technical dimension does not push the volume up: reliability rises with the volume, but storage efficiency falls. Set the share of storage efficiency to zero and watch the technical answer move.`,
  fonte: "The eight criteria of the program in four dimensions, computed for seven candidate volumes with the tutorial project and a polyethylene cistern. The score is computed on the page by the same calculation as triton/core/topsis.py, checked against the program by an automatic test.",
  montar(p, D, id) {
    const PADRAO = (D.partes_padrao || D.criterios.map(() => 1)).slice();
    const EIXOS = D.eixos, benef = D.criterios.map(c => c.beneficio), W = 640;
    const IGUAIS = EIXOS.map(() => 1 / EIXOS.length);
    let pesos = IGUAIS.slice(), partes = PADRAO.slice(), abertas = false, sel = D.volumes.indexOf(4000);
    if (sel < 0) sel = 0;
    const desenha = () => {
      const w8 = pesosDosCriterios(D, pesos, partes);
      const Res = topsisEscores(D.matriz, w8, benef, D.volumes);
      const vencedor = Res.postos.indexOf(1);
      const faixa = faixaDeEscolha(D.volumes, Res.escores);
      const ey = escala(0, Math.max(...Res.escores) * 1.12, 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: v => fmt(v, 2), yr: "TOPSIS score (1 = ideal)", painel: "(a)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "candidate volume"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.55;
      Res.escores.forEach((x, i) => {
        const cor = i === vencedor ? "var(--accent)" : faixa.includes(i) ? "var(--accent);fill-opacity:0.45" : "var(--grid)";
        const contorno = i === sel ? ";stroke:var(--ink2);stroke-width:2" : "";
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${A.Y(0) - A.Y(x)}" rx="3" style="fill:${cor}${contorno}"/>`;
        s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(x) - 6}" text-anchor="middle">${fmt(x, 3)}</text>`;
      });
      const xa = A.X(faixa[0]) - bw / 2 - 4, xb = A.X(faixa[faixa.length - 1]) + bw / 2 + 4, yb = A.Y(ey.max) - 4;
      s += `<path d="M${xa},${yb + 5} V${yb} H${xb} V${yb + 5}" style="fill:none;stroke:var(--accent);stroke-width:1.5"/>`;
      s += `<text class="g-rot" x="${(xa + xb) / 2}" y="${yb - 4}" text-anchor="middle" style="fill:var(--accent)">choice band</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, [[S(1), "score", fmt(Res.escores[i], 4)], ["", "rank", `#${Res.postos[i]}`]]),
        i => { sel = i; desenha(); });

      const H2 = 290;
      const B = plano({W, H: H2, l: 300, r: 60, t: 34, b: 36, x: [0, 1], y: [D.criterios.length - 0.4, -0.6],
        xm: [0, 0.25, 0.5, 0.75, 1], xf: v => fmt(v * 100) + "%", xr: "proximity to the best observed", painel: "(b)"});
      let t = B.s;
      D.criterios.forEach((c, j) => {
        const v = Res.proximidade[sel][j], y = B.Y(j), h = 16;
        t += `<rect x="${B.X(0)}" y="${y - h / 2}" width="${B.X(1) - B.X(0)}" height="${h}" rx="3" style="fill:var(--grid)"/>`;
        t += `<rect x="${B.X(0)}" y="${y - h / 2}" width="${Math.max(2, B.X(v) - B.X(0))}" height="${h}" rx="3" style="fill:${S(COR_DO_EIXO[c.eixo] || 1)}"/>`;
        t += `<text class="g-t" x="${B.X(0) - 8}" y="${y + 4}" text-anchor="end">${c.rotulo} · weight ${fmt(Res.pesos[j] * 100, 1)}%</text>`;
        t += `<text class="g-t" x="${B.X(1) + 8}" y="${y + 4}">${fmt(v * 100, 0)}%</text>`;
      });
      p.querySelector(`#${id}h`).innerHTML = t;

      EIXOS.forEach(([k], i) => { const o = p.querySelector(`#${id}${k}-o`); if (o) o.textContent = fmt(pesos[i] * 100, 0) + "%"; });
      if (abertas) D.criterios.forEach((c, j) => { const o = p.querySelector(`#${id}c${j}-o`); if (o) o.textContent = fmt(partes[j] * 100, 0); });
      const padrao = partes.every((x, j) => x === PADRAO[j]);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Choice band: ${textoDaFaixa(D.volumes, faixa)}</p>
        <div class="fi-n">${cartao("Highest score", fmt(D.volumes[vencedor]) + " L", `score ${fmt(Res.escores[vencedor], 3)}`)}
        ${cartao("Highlighted", fmt(D.volumes[sel]) + " L", `rank ${Res.postos[sel]}, score ${fmt(Res.escores[sel], 3)}`)}</div>
        <p class="fi-sub">The eight criteria of the highlighted volume</p>
        <table class="fi-tabela"><tbody>${D.criterios.map((c, j) => `<tr><td>${c.rotulo}<small>${c.eixo} · ${c.beneficio ? "higher is better" : "lower is better"}</small></td>
          <td class="n">${D.sem_retorno[sel] && c.chave === "payback_years" ? "no payback" : c.unidade === "US$" ? din(D.matriz[sel][j]) : menos(D.matriz[sel][j], c.casas) + " " + c.unidade}</td></tr>`).join("")}</tbody></table>
        <p class="fi-nota">The score measures the distance to two references: the ideal alternative, made of the best value of each criterion, and the anti-ideal, made of the worst. The choice band gathers the volumes whose score lies within 5% of the score range, counted from the highest, as the program reports it: they score alike, and the band, with the tolerance, is the result to report, not the highest score alone. ${D.sem_retorno.some(Boolean) ? "Volumes that do not pay back within the horizon receive the payback penalty the program applies (the worst observed plus 10%, at least 20 years); when no volume pays back, the payback column is constant and weighs nothing. " : ""}The weight of each dimension is shared among its criteria by the criterion shares; ${padrao ? "the shares are the default, equal within each dimension, and" : "with the default shares, equal within each dimension,"} equal weights on the four dimensions reproduce the program's result. ${ILUSTRATIVO}</p>`;
    };
    p.innerHTML = `<div class="fi-ctls">
      ${EIXOS.map(([k, r], i) => ctlFaixa(id + k, r + " weight", 101, Math.round(pesos[i] * 100))).join("")}
      <div class="fi-ctl"><span class="fi-rot">&nbsp;</span><div class="linha-ctl"><button type="button" class="bt" id="${id}igual">Equal weights</button><button type="button" class="bt" id="${id}abrir">Criterion shares</button></div></div>
    </div><div class="fi-ctls" id="${id}s8" hidden></div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 250" role="img" aria-label="TOPSIS score of each candidate volume"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 290" role="img" aria-label="Proximity of the highlighted volume to the best observed in each criterion"></svg>
      ${legenda([["var(--accent)", "(a) highest score; lighter: the rest of the choice band"], ["var(--ink2)", "(a) outline: highlighted volume"], [S(3), "(b) technical"], [S(2), "(b) economic"], [S(4), "(b) environmental"], [S(1), "(b) structural"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    EIXOS.forEach(([k], i) => p.querySelector(`#${id}${k}`).addEventListener("input", e => {
      pesos = pesos.map((x, j) => j === i ? +e.target.value / 100 : x);
      if (pesos.reduce((a, b) => a + b, 0) <= 0) pesos[i] = 0.01;
      desenha();
    }));
    /* A dimension needs at least one criterion with a share above zero, as in the program. */
    const ligarPartes = () => D.criterios.forEach((c, j) => p.querySelector(`#${id}c${j}`).addEventListener("input", ev => {
      partes[j] = +ev.target.value / 100;
      const soma = D.criterios.reduce((a, cc, jj) => a + (cc.eixo === c.eixo ? partes[jj] : 0), 0);
      if (soma <= 0) partes[j] = 0.01;
      desenha();
    }));
    p.querySelector(`#${id}igual`).addEventListener("click", () => {
      pesos = IGUAIS.slice();
      partes = PADRAO.slice();
      EIXOS.forEach(([k], i) => { p.querySelector(`#${id}${k}`).value = Math.round(pesos[i] * 100); });
      if (abertas) D.criterios.forEach((c, j) => { p.querySelector(`#${id}c${j}`).value = Math.round(partes[j] * 100); });
      desenha();
    });
    p.querySelector(`#${id}abrir`).addEventListener("click", e => {
      abertas = !abertas;
      const caixa = p.querySelector(`#${id}s8`);
      if (abertas) {
        caixa.innerHTML = D.criterios.map((c, j) => ctlFaixa(id + "c" + j, (c.curto || c.rotulo) + " share", 101, Math.round(partes[j] * 100))).join("");
        ligarPartes();
      }
      caixa.hidden = !abertas;
      e.target.textContent = abertas ? "Hide the criterion shares" : "Criterion shares";
      desenha();
    });
    desenha();
  }
};

/* ─── stochastic acceptability (SMAA) ───────────────────────────────────── */
FI["fig23_smaa.png"] = {
  curto: "Stochastic acceptability",
  pergunta: "If nobody can say the weights, which volume wins most often?",
  controles: "ranking method · VIKOR strategy",
  experimente: "Swap VIKOR for TOPSIS and see whether the winner survives the change of method. Move the VIKOR strategy from consensus (0.5) to minimum regret (0) and watch which volume gains stability.",
  fonte: D => `The program's own SMAA: ${fmt(D.sorteios)} draws of the eight criterion weights from a Dirichlet distribution with 25% expected on each dimension, seed ${D.semente}, with the same seven candidates as the multi-criteria decision. ${ILUSTRATIVO}`,
  montar(p, D, id) {
    let motor = D.padrao[0], v = D.padrao[1], sel = 3;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "m", "Ranking method", [["vikor", "SMAA-VIKOR"], ["topsis", "SMAA-TOPSIS"]], motor)}
      ${ctlSeg(id + "v", "VIKOR strategy", [[0, "regret (0)"], [0.5, "consensus (0.5)"], [1, "utility (1)"]], v)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 250" role="img" aria-label="First-place acceptability of each volume; click to choose a volume"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 250" role="img" aria-label="Distribution of the ranks of each volume over the ${fmt(D.sorteios)} draws"></svg>
      ${legenda([[S(4), "1st place"], [S(1), "2nd place; later ranks come in ever lighter tones"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const chave = motor === "topsis" ? "topsis|0.5" : `vikor|${v}`;
      const C = D.casos[chave] || D.casos["vikor|0.5"];
      const melhor = C.primeiro.indexOf(Math.max(...C.primeiro));
      const ey = escala(0, Math.max(...C.primeiro) * 1.15, 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x) + "%", yr: "1st-place acceptability", painel: "(a)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "candidate volume"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.55;
      C.primeiro.forEach((x, i) => {
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(x))}" rx="3" style="fill:${i === melhor ? S(4) : i === sel ? S(1) : "var(--grid)"}"/>`;
        if (x > 0.5) s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(x) - 6}" text-anchor="middle">${fmt(x, 1)}%</text>`;
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, [[S(1), "wins in", fmt(C.primeiro[i], 2) + "% of the draws"]]),
        i => { sel = i; desenha(); });

      const B = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, 100], ym: [0, 25, 50, 75, 100],
        yf: x => fmt(x) + "%", yr: `ranks over the ${fmt(D.sorteios)} draws`, painel: "(b)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "candidate volume"});
      let t = B.s;
      C.aceitabilidade.forEach((linha, i) => {
        let base = 0;
        linha.forEach((x, pos) => {
          if (x <= 0) return;
          const alto = B.Y(base) - B.Y(base + x);
          t += `<rect x="${B.X(i) - bw / 2}" y="${B.Y(base + x)}" width="${bw}" height="${Math.max(0, alto - 1)}" style="fill:${pos === 0 ? S(4) : S(1)};opacity:${pos === 0 ? 1 : Math.max(0.12, 0.62 - pos * 0.09)}"/>`;
          base += x;
        });
      });
      t += `<text class="g-t" x="${B.X(D.volumes.length - 1) + 4}" y="${B.Y(96)}">1st place in green</text>`;
      p.querySelector(`#${id}h`).innerHTML = t;
      pairar(p.querySelector(`#${id}h`), W, D.volumes.map((_, i) => B.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, C.aceitabilidade[i].map((x, pos) => [pos === 0 ? S(4) : S(1), `rank ${pos + 1}`, fmt(x, 1) + "%"]).filter((_, pos) => C.aceitabilidade[i][pos] > 0)),
        i => { sel = i; desenha(); });

      const central = C.central[sel], soma = central.reduce((a, b) => a + b, 0);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Most accepted: ${fmt(D.volumes[melhor])} L, in ${fmt(C.primeiro[melhor], 1)}% of the draws</p>
        <div class="fi-n">${cartao("Highlighted", fmt(D.volumes[sel]) + " L", `wins in ${fmt(C.primeiro[sel], 2)}% of the draws`)}
        ${cartao("Confidence factor", C.confianca[sel] >= 1 ? "✓ confirms" : "✕ does not confirm", "with its own central vector")}</div>
        ${soma > 0 ? `<p class="fi-sub">Central weight vector that elects ${fmt(D.volumes[sel])} L</p>
        <table class="fi-tabela"><tbody>${DADOS.interativas["fig51_programa_topsis.png"].criterios.map((c, j) =>
          `<tr><td>${c.rotulo}</td><td class="n">${fmt(central[j] * 100, 1)}%</td></tr>`).join("")}</tbody></table>`
        : `<p class="fi-nota">This volume won none of the ${fmt(D.sorteios)} draws, and so has no central weight vector.</p>`}
        <p class="fi-nota">Each draw takes a weight vector at random and ranks the volumes. The first-place acceptability is the share of draws in which the volume won; the central vector is the mean of the weights that elected it. It is the question inverted: instead of “which volume do these weights elect”, “which weights would elect this volume”.</p>`;
    };
    ligarSeg(p, id + "m", x => { motor = x; desenha(); });
    ligarSeg(p, id + "v", x => { v = +x; desenha(); });
    desenha();
  }
};

/* ─── the rainfall indices ──────────────────────────────────────────────── */
FI["fig16_indices.png"] = {
  curto: "The rainfall indices, year by year",
  pergunta: "What do the nine indices say about the rain of each city?",
  controles: "city · index",
  experimente: D => {
    const maxCDD = c => Math.max(...c.valores["CDD"]);
    const medSI = c => c.valores["Seasonality_Index"].reduce((a, b) => a + b, 0) / c.valores["Seasonality_Index"].length;
    const secas = D.cidades.slice().sort((a, b) => maxCDD(b) - maxCDD(a));
    const sazon = D.cidades.slice().sort((a, b) => medSI(b) - medSI(a));
    return `Choose “Longest dry spell” and compare ${secas[0].nome} with ${secas[secas.length - 1].nome}: the longest dry run reaches ${fmt(maxCDD(secas[0]))} days in ${secas[0].nome} and ${fmt(maxCDD(secas[secas.length - 1]))} in ${secas[secas.length - 1].nome}, and it is this, not the total rain, that calls for a larger cistern. Then look at the seasonality index of the three cities: ${sazon[0].nome} has the most concentrated rain (mean ${fmt(medSI(sazon[0]), 2)}).`;
  },
  fonte: "Indices computed by the program itself (triton/core/calculator.py) over 30 years of the series of each city, with the same percentile base period the program uses.",
  montar(p, D, id) {
    let cidade = D.padrao[0], indice = D.padrao[1];
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "City", D.cidades.map(c => [c.chave, c.nome]), cidade)}
      <div class="fi-ctl largo"><label class="fi-rot" for="${id}i">Index</label>
      <select id="${id}i">${D.indices.map(x => `<option value="${x.chave}"${x.chave === indice ? " selected" : ""}>${x.nome} (${x.chave.replace("Seasonality_Index", "SI")})</option>`).join("")}</select></div>
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 260" role="img" aria-label="Value of the index in each year of the series"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 190" role="img" aria-label="Mean of the index in the ${D.cidades.length} cities"></svg>
      ${legenda([[S(1), "value of the year"], ["var(--ink3)", "30-year mean", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const c = D.cidades.find(x => x.chave === cidade), meta = D.indices.find(x => x.chave === indice);
      const vals = c.valores[indice], media = vals.reduce((a, b) => a + b, 0) / vals.length;
      const un = meta.unidade === "—" ? "" : meta.unidade;
      const ey = escala(0, Math.max(...vals) * 1.1, 4);
      const A = plano({W, H: 260, l: 62, r: 14, t: 34, b: 44, x: [-0.6, vals.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x, meta.casas > 1 ? 2 : 0), yr: `${meta.nome} (${meta.unidade})`, painel: "(a)",
        xm: c.anos.map((_, i) => i).filter(i => i % 5 === 0), xf: i => c.anos[i], xr: "year"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.7;
      const maior = vals.indexOf(Math.max(...vals)), menor = vals.indexOf(Math.min(...vals));
      vals.forEach((x, i) => {
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(x))}" rx="2" style="fill:${S(1)};opacity:${i === maior || i === menor ? 1 : 0.72}"/>`;
      });
      s += `<line class="g-ref" x1="${A.X(-0.6)}" x2="${A.X(vals.length - 0.4)}" y1="${A.Y(media)}" y2="${A.Y(media)}"/>`;
      s += `<text class="g-t" x="${A.X(-0.5)}" y="${A.Y(media) - 6}">30-year mean: ${fmt(media, meta.casas)} ${un}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, vals.map((_, i) => A.X(i)),
        i => dicaHTML(`${c.nome}, ${c.anos[i]}`, [[S(1), meta.nome, fmt(vals[i], meta.casas) + " " + un]]));

      const medias = D.cidades.map(x => x.valores[indice].reduce((a, b) => a + b, 0) / x.valores[indice].length);
      const ry = escala(0, Math.max(...medias) * 1.15, 3);
      const B = plano({W, H: 190, l: 62, r: 14, t: 34, b: 40, x: [-0.6, D.cidades.length - 0.4], y: [0, ry.max], ym: ry.marcas,
        yf: x => fmt(x, meta.casas > 1 ? 2 : 0), yr: `30-year mean (${meta.unidade})`, painel: "(b)",
        xm: D.cidades.map((_, i) => i), xf: i => D.cidades[i].nome});
      let t = B.s;
      const bw2 = (B.X(1) - B.X(0)) * 0.45;
      medias.forEach((x, i) => {
        t += `<rect x="${B.X(i) - bw2 / 2}" y="${B.Y(x)}" width="${bw2}" height="${Math.max(0, B.Y(0) - B.Y(x))}" rx="3" style="fill:${D.cidades[i].chave === cidade ? S(1) : "var(--grid)"}"/>`;
        t += `<text class="g-t" x="${B.X(i)}" y="${B.Y(x) - 6}" text-anchor="middle">${fmt(x, meta.casas)}</text>`;
      });
      p.querySelector(`#${id}h`).innerHTML = t;

      const ordenado = vals.slice().sort((a, b) => a - b);
      const mediana = ordenado[Math.floor(vals.length / 2)];
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${meta.nome} in ${c.nome}</p>
        <div class="fi-n">${cartao("30-year mean", fmt(media, meta.casas), un)}
        ${cartao("Median", fmt(mediana, meta.casas), un)}
        ${cartao("Largest value", fmt(vals[maior], meta.casas), "in " + c.anos[maior])}
        ${cartao("Smallest value", fmt(vals[menor], meta.casas), "in " + c.anos[menor])}</div>
        <p class="fi-nota"><b>${meta.chave.replace("Seasonality_Index", "SI")}.</b> ${meta.texto}</p>`;
    };
    ligarSeg(p, id + "c", x => { cidade = x; desenha(); });
    p.querySelector(`#${id}i`).addEventListener("change", e => { indice = e.target.value; desenha(); });
    desenha();
  }
};

/* ─── the investment opened by item ─────────────────────────────────────── */
FI["fig21_investimento.png"] = {
  curto: "What the investment is made of",
  pergunta: "What is the initial investment made of, and what changes with the volume?",
  controles: "volume · material",
  experimente: D => {
    const tot = (v, m) => D.casos[`${v}|${m}`].reduce((a, b) => a + b, 0);
    const m = D.padrao[1], a = tot(4000, m), b = tot(8000, m);
    return `Double the volume from 4 to 8 m³: the total investment goes from ${din(a)} to ${din(b)} (${fmt(100 * (b / a - 1), 0)}% more, against 100% more volume), because only the lower tank grows. Changing the material moves only that item. ${ILUSTRATIVO}`;
  },
  fonte: "The seven items the program adds up in the initial investment, with its reference prices and the costs declared in the tutorial (illustrative, not market prices). The sum reproduces, for each volume and material, the same investment the economic analysis uses in the cash flow.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao[0]), mat = D.padrao[1];
    const W = 640, cores = [1, 2, 3, 4, 5, 6, 7].map(R);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Cistern volume", D.volumes.length, vi)}
      ${ctlSeg(id + "m", "Cistern material", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Initial investment opened by item, at each volume"></svg>
      ${legenda(D.rubricas.map((r, i) => [cores[i], r]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const v = D.volumes[vi];
      const totais = D.volumes.map(x => D.casos[`${x}|${mat}`].reduce((a, b) => a + b, 0));
      const ey = escala(0, Math.max(...totais) * 1.08, 5);
      const A = plano({W, H: 300, l: 70, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x), yr: `initial investment (${MOEDA})`,
        xm: D.volumes.map((_, i) => i).filter(i => i % 2 === 0), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "cistern volume"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.62;
      D.volumes.forEach((x, i) => {
        const partes = D.casos[`${x}|${mat}`];
        let base = 0;
        partes.forEach((valor, j) => {
          const alto = A.Y(base) - A.Y(base + valor);
          s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(base + valor)}" width="${bw}" height="${Math.max(0, alto - 1.5)}" style="fill:${cores[j]};opacity:${i === vi ? 1 : 0.38}"/>`;
          base += valor;
        });
        if (i === vi) s += `<text class="g-rot" x="${A.X(i)}" y="${A.Y(base) - 8}" text-anchor="middle" style="fill:var(--ink)">${din(base)}</text>`;
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, D.casos[`${D.volumes[i]}|${mat}`].map((x, j) => [cores[j], D.rubricas[j].split(" (")[0], din(x)])
          .concat([["", "total", din(totais[i])]])),
        i => { vi = i; p.querySelector(`#${id}v`).value = i; desenha(); });
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const partes = D.casos[`${v}|${mat}`], total = partes.reduce((a, b) => a + b, 0);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${fmt(v)} L, ${D.materiais.find(m => m[0] === mat)[1].toLowerCase()}</p>
        <table class="fi-tabela"><tbody>${D.rubricas.map((r, j) => `<tr><td><i style="--c:${cores[j]}"></i>${r}</td><td class="n">${din(partes[j])}</td><td class="n">${fmt(100 * partes[j] / total, 0)}%</td></tr>`).join("")}
        <tr class="tot"><td>Total</td><td class="n">${din(total)}</td><td class="n">100%</td></tr></tbody></table>
        <div class="fi-n">${cartao("Cost per litre of cistern", din(partes[0] / v, 2), "the tank only")}
        ${cartao("Share that does not depend on the volume", fmt(100 * (total - partes[0]) / total, 0) + "%")}</div>
        <p class="fi-nota">The sum of the seven items is the initial investment that the economic analysis uses${D.fecha_com_o_capex ? ", checked at every build of the site" : ""}. The treatment line enters through what it adds beyond the filtration allowance already built into the accessories, so that the filter is not counted twice. ${ILUSTRATIVO}</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenha(); });
    ligarSeg(p, id + "m", x => { mat = x; desenha(); });
    desenha();
  }
};

/* ─── the bill opened into parts ────────────────────────────────────────── */
FI["fig07_fatura.png"] = {
  curto: "The bill opened into parts",
  pergunta: "What is a water bill made of, and which part can the rainwater system move?",
  controles: "consumption without and with the system · sewer",
  experimente: D => `Lower the consumption with the system: the availability charge does not move, and only the water charge shrinks. Set the sewer share to zero and watch the monthly saving fall to ${fmt(100 / (1 + D.esgoto_pct / 100), 0)}% of its value: in this tariff the sewer is ${fmt(D.esgoto_pct)}% of the water charge, and it is what makes each cubic metre saved worth more.`,
  fonte: "The New York water and sewer tariff of the program's example project, opened into the parts the program computes: availability charge, consumption bands and sewer as a percentage of the water part. The starting point is the mean consumption of the tutorial project. The tariff is a published one; the costs elsewhere in the tutorial are illustrative.",
  montar(p, D, id) {
    const n = D.consumos.length, idx = v => Math.round(v / 0.25);
    let iSem = idx(D.padrao[0]), iCom = idx(D.padrao[1]), esgoto = D.esgoto_pct;
    const W = 560, ult = D.rubricas.length - 1;
    const corP = j => j === 0 ? S(2) : j === ult ? S(4) : R(Math.min(7, 2 + j));
    const escuro = j => j === 0 || j === ult || j <= 1;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "s", "Consumption without the system", n, iSem)}
      ${ctlFaixa(id + "c", "Consumption with the system", n, iCom)}
      ${ctlSeg(id + "e", "Sewer", [[0, "no sewer"], [50, "50%"], [100, "100%"], [D.esgoto_pct, fmt(D.esgoto_pct) + "%"]], esgoto)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" class="estreito" viewBox="0 0 ${W} 330" role="img" aria-label="The monthly bill opened into parts, without and with the rainwater system"></svg>
      <div class="fi-leg" id="${id}leg"></div>
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      if (iCom > iSem) { iCom = iSem; p.querySelector(`#${id}c`).value = iCom; }
      const monta = i => {
        const linha = D.parcelas[i].slice();
        linha[linha.length - 1] = linha[linha.length - 1] * esgoto / D.esgoto_pct;   // sewer on the water
        return linha;
      };
      const casos = [["without the system", monta(iSem), D.consumos[iSem]], ["with the system", monta(iCom), D.consumos[iCom]]];
      const totais = casos.map(([, l]) => l.reduce((a, b) => a + b, 0));
      const ey = escala(0, Math.max(...totais) * 1.12, 5);
      const A = plano({W, H: 330, l: 70, r: 14, t: 34, b: 52, x: [-0.6, 1.6], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x), yr: `monthly bill (${MOEDA})`, xm: [0, 1], xf: i => casos[i][0]});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.46;
      casos.forEach(([rot, linha, consumo], i) => {
        let base = 0;
        linha.forEach((valor, j) => {
          if (valor <= 0) return;
          const alto = A.Y(base) - A.Y(base + valor);
          s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(base + valor)}" width="${bw}" height="${Math.max(0, alto - 1.5)}" style="fill:${corP(j)}"/>`;
          if (alto > 18) s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(base + valor / 2) + 4}" text-anchor="middle" style="fill:${escuro(j) ? "#fff" : "var(--sobre-r7)"}">${din(valor)}</text>`;
          base += valor;
        });
        s += `<text class="g-rot" x="${A.X(i)}" y="${A.Y(base) - 8}" text-anchor="middle" style="fill:var(--ink)">${din(base)}</text>`;
        s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(0) + 32}" text-anchor="middle">${fmt(consumo, 2)} m³/month</text>`;
      });
      const xs = A.X(1) + bw / 2 + 12, y1 = A.Y(totais[0]), y2 = A.Y(totais[1]);
      s += `<line x1="${xs}" x2="${xs}" y1="${y1}" y2="${y2}" style="stroke:${S(4)};stroke-width:1.5"/>`;
      s += `<text class="g-rot" x="${xs - 4}" y="${(y1 + y2) / 2 + 4}" text-anchor="end" style="fill:${S(4)}">−${din(totais[0] - totais[1])}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      p.querySelector(`#${id}leg`).innerHTML = D.rubricas.map((r, j) => casos[0][1][j] > 0 || casos[1][1][j] > 0
        ? `<span><i style="--c:${corP(j)}"></i>${j === ult ? r.replace(/\(\d+%/, "(" + fmt(esgoto) + "%") : r}</span>` : "").join("");
      p.querySelector(`#${id}s-o`).textContent = fmt(D.consumos[iSem], 2) + " m³/month";
      p.querySelector(`#${id}c-o`).textContent = fmt(D.consumos[iCom], 2) + " m³/month";
      const agua = D.consumos[iSem] - D.consumos[iCom], economia = totais[0] - totais[1];
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Potable water saved: ${fmt(agua, 2)} m³/month</p>
        <table class="fi-tabela"><thead><tr><th>Part</th><th class="n">Without</th><th class="n">With</th><th class="n">Difference</th></tr></thead><tbody>
        ${D.rubricas.map((r, j) => {
          const a = casos[0][1][j], b = casos[1][1][j];
          if (a <= 0 && b <= 0) return "";
          return `<tr><td><i style="--c:${corP(j)}"></i>${r}</td><td class="n">${din(a)}</td><td class="n">${din(b)}</td><td class="n">${a - b > 0.005 ? "−" + din(a - b) : "—"}</td></tr>`;
        }).join("")}
        <tr class="tot"><td>Total</td><td class="n">${din(totais[0])}</td><td class="n">${din(totais[1])}</td><td class="n">−${din(economia)}</td></tr></tbody></table>
        <div class="fi-n">${cartao("Bill reduction", fmt(100 * economia / totais[0], 1) + "%", `for ${fmt(100 * agua / (D.consumos[iSem] || 1), 1)}% less consumption`)}
        ${cartao("Saving per m³ saved", agua > 0 ? din(economia / agua, 2) : "—", MOEDA + "/m³")}</div>
        <p class="fi-nota">The availability charge is the same in both cases: it is what is paid for being connected to the network. That is why the bill falls less, in proportion, than the consumption.</p>`;
    };
    p.querySelector(`#${id}s`).addEventListener("input", e => { iSem = +e.target.value; if (iCom > iSem) iCom = iSem; desenha(); });
    p.querySelector(`#${id}c`).addEventListener("input", e => { iCom = Math.min(+e.target.value, iSem); desenha(); });
    ligarSeg(p, id + "e", x => { esgoto = +x; desenha(); });
    desenha();
  }
};

/* ─── sensitivity: which assumption moves the result ────────────────────── */
FI["fig24_tornado.png"] = {
  curto: "The sensitivity tornado",
  pergunta: "Which assumption moves the project's result the most?",
  controles: "amplitude of the variation",
  experimente: D => {
    const cruza = a => Object.keys(D.casos[String(a)]).filter(k => { const [x, y] = D.casos[String(a)][k]; return Math.min(x, y) < 0 && Math.max(x, y) > 0; });
    const amps = D.amplitudes.slice().sort((a, b) => a - b);
    const a1 = amps.find(a => cruza(a).length);
    const frase = a1 === undefined ? `no single assumption changes the sign of the NPV, even at ±${amps[amps.length - 1]}%`
      : `up to ±${amps[Math.max(0, amps.indexOf(a1) - 1)]}% no single assumption changes the sign of the NPV; at ±${a1}%, ${cruza(a1).join(", ")} ${cruza(a1).length === 1 ? "alone does" : "do"}`;
    return `In this illustrative case the base NPV is ${din(D.vpl_base)}. Vary each assumption on its own: ${frase}. The assumptions at the top are the ones that need local data before the study is published.`;
  },
  fonte: D => `The program's own sensitivity analysis (run_sensitivity_analysis) over the base case of the tutorial — a ${fmt(D.volume)} L ${D.material.toLowerCase()} cistern, ${D.anos} years, the New York tariff —, the same base-case definition as the manual's figure. ${ILUSTRATIVO}`,
  montar(p, D, id) {
    let amp = D.padrao, sel = null;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "a", "Amplitude of the variation of each assumption", D.amplitudes.map(a => [a, "±" + a + "%"]), amp)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 380" role="img" aria-label="Change in the net present value when each assumption rises and falls"></svg>
      ${legenda([[S(4), "assumption up"], [S(2), "assumption down"], ["var(--ink3)", "NPV of the base case", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const C = D.casos[String(amp)];
      const itens = Object.keys(C).map(k => ({nome: k, baixo: C[k][0], alto: C[k][1]}));
      itens.forEach(x => { x.amplitude = Math.abs(x.alto - x.baixo); });
      itens.sort((a, b) => b.amplitude - a.amplitude);
      if (sel === null || !itens.some(x => x.nome === sel)) sel = itens[0].nome;
      const todos = itens.flatMap(x => [x.baixo, x.alto, D.vpl_base]);
      const ex = escala(Math.min(...todos), Math.max(...todos), 5);
      const A = plano({W, H: 380, l: 240, r: 20, t: 34, b: 48, x: [ex.min, ex.max], y: [itens.length - 0.4, -0.6],
        xm: ex.marcas, xf: v => menos(v), xr: `net present value over ${D.anos} years (${MOEDA})`});
      let s = A.s;
      const h = 18, x0 = A.X(D.vpl_base);
      itens.forEach((x, i) => {
        const y = A.Y(i);
        [[x.alto, S(4)], [x.baixo, S(2)]].forEach(([valor, cor]) => {
          const xa = Math.min(x0, A.X(valor)), largura = Math.abs(A.X(valor) - x0);
          s += `<rect x="${xa}" y="${y - h / 2}" width="${Math.max(1, largura)}" height="${h}" rx="2" style="fill:${cor};opacity:${x.nome === sel ? 1 : 0.55}"/>`;
        });
        s += `<text class="g-t" x="${A.X(ex.min) - 8}" y="${y + 4}" text-anchor="end" style="${x.nome === sel ? "font-weight:600" : ""}">${x.nome}</text>`;
      });
      s += `<line class="g-ref" x1="${x0}" x2="${x0}" y1="${A.Y(-0.6)}" y2="${A.Y(itens.length - 0.4)}"/>`;
      s += `<text class="g-t" x="${x0}" y="${A.Y(-0.6) - 6}" text-anchor="middle">base case: ${din(D.vpl_base)}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      const svg = p.querySelector(`#${id}g`);
      const linhaDe = e => {
        const r = svg.getBoundingClientRect();
        const y = (e.clientY - r.top) / r.height * 380;
        let k = 0, d = Infinity;
        itens.forEach((x, i) => { const q = Math.abs(A.Y(i) - y); if (q < d) { d = q; k = i; } });
        return k;
      };
      svg.onpointermove = e => {
        const x = itens[linhaDe(e)], dica = $("#dica");
        dica.innerHTML = dicaHTML(x.nome, [
          [S(4), `+${amp}%`, din(x.alto) + ` (${menos(x.alto - D.vpl_base)})`],
          [S(2), `−${amp}%`, din(x.baixo) + ` (${menos(x.baixo - D.vpl_base)})`]]);
        dica.hidden = false;
        const lim = document.documentElement.clientWidth - dica.offsetWidth - 8;
        dica.style.left = Math.max(8, Math.min(e.pageX + 14, lim)) + "px";
        dica.style.top = Math.max(window.scrollY + 64, e.pageY - dica.offsetHeight - 12) + "px";
      };
      svg.onpointerleave = () => { $("#dica").hidden = true; };
      svg.onclick = e => { sel = itens[linhaDe(e)].nome; desenha(); };
      const viram = itens.filter(x => Math.min(x.alto, x.baixo) < 0 && Math.max(x.alto, x.baixo) > 0);
      const s1 = itens.find(x => x.nome === sel);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Base case: ${fmt(D.volume)} L cistern, NPV of ${din(D.vpl_base)}</p>
        <div class="fi-n">${cartao("Assumption that moves the NPV most", itens[0].nome.replace(/ \(.*/, ""), `range of ${din(itens[0].amplitude)}`)}
        ${cartao("Assumptions that change the sign of the NPV", viram.length ? viram.length + " of " + itens.length : "none", viram.length ? viram.map(x => x.nome.replace(/ \(.*/, "")).join(", ") : `at ±${amp}%`)}</div>
        <p class="fi-sub">Highlighted assumption: ${s1.nome}</p>
        <table class="fi-tabela"><tbody>
        <tr><td><i style="--c:${S(4)}"></i>Assumption ${amp}% higher</td><td class="n">${din(s1.alto)}</td><td class="n">${din(s1.alto - D.vpl_base)}</td></tr>
        <tr><td>Base case</td><td class="n">${din(D.vpl_base)}</td><td class="n">—</td></tr>
        <tr><td><i style="--c:${S(2)}"></i>Assumption ${amp}% lower</td><td class="n">${din(s1.baixo)}</td><td class="n">${din(s1.baixo - D.vpl_base)}</td></tr>
        </tbody></table>
        <p class="fi-nota">The base case comes from the program's simplified economic model, which discounts an annual flow with a single marginal tariff; the NPV here is therefore not the same as that of the monthly cash flow shown in the cash-flow figure. What the tornado measures is relative sensitivity. Each bar moves one assumption at a time, keeping the others at the base case. The order is that of the amplitude: whoever is at the top decides the result, and is where it pays to spend effort to obtain local data. An assumption whose bar crosses zero can, on its own, turn the sign of the NPV.</p>`;
    };
    ligarSeg(p, id + "a", x => { amp = +x; desenha(); });
    desenha();
  }
};

/* ─── how much the roof collects ────────────────────────────────────────── */
FI["fig35_escoamento.png"] = {
  curto: "The catchment of the roof",
  pergunta: "How much water does your roof collect each month?",
  controles: "city · material · area · first flush",
  experimente: D => {
    const coef = n => (D.materiais.find(m => m[0] === n) || [0, 0])[1];
    const c = D.cidades.find(x => x.chave === D.padrao[0]);
    const perda = 100 * (1 - c.anual["3"] / c.anual["0"]);
    return `Swap the ceramic tile for the green roof: the coefficient falls from ${fmt(coef("Ceramic tile"), 2)} to ${fmt(coef("Green roofs"), 2)} and the catchment drops to about ${fmt(100 * coef("Green roofs") / coef("Ceramic tile"), 0)}% of what it was. Raise the first flush from 0 to 3 mm and see how much disappears — in ${c.nome}, ${fmt(perda, 0)}% of the year's rain.`;
  },
  fonte: "Daily rain of 30 years from the series of each city, with the first flush applied to each rain event as in the program, and the runoff coefficient of the roof material. The catchment is V = P × A × C, the same calculation as in the simulation engine.",
  montar(p, D, id) {
    let cidade = D.padrao[0], desc = D.padrao[1], area = D.padrao[2], material = D.padrao[3];
    const W = 640;
    const coefDe = () => (D.materiais.find(m => m[0] === material) || D.materiais[0])[1];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "City", D.cidades.map(c => [c.chave, c.nome]), cidade)}
      <div class="fi-ctl largo"><label class="fi-rot" for="${id}m">Roof material <output id="${id}m-o"></output></label>
      <select id="${id}m">${D.materiais.map(([n, c]) => `<option value="${esc(n)}"${n === material ? " selected" : ""}>${esc(n)} — coefficient ${fmt(c, 2)}</option>`).join("")}</select></div>
      ${ctlFaixa(id + "a", "Roof area (horizontal projection)", D.areas.length, D.areas.indexOf(area))}
      ${ctlSeg(id + "d", "First flush", D.descartes.map(d => [d, fmt(d) + " mm"]), desc)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Mean volume collected in each month of the year"></svg>
      ${legenda([[S(1), "collection of the month"], [S(2), "part held back by the first flush"], ["var(--ink3)", "rainwater demand of the tutorial", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const c = D.cidades.find(x => x.chave === cidade), coef = coefDe();
      const litros = mm => mm * area * coef;                     // 1 mm on 1 m² = 1 L
      const mensal = c.mensal[String(desc)].map(litros);
      const bruto = c.mensal["0"].map(litros);
      const demandaMes = D.demanda_pluvial_tutorial * 30.4375;
      const ey = escala(0, Math.max(...bruto, demandaMes) * 1.1, 4);
      const A = plano({W, H: 300, l: 66, r: 14, t: 34, b: 44, x: [0.4, 12.6], y: [0, ey.max], ym: ey.marcas,
        yf: v => fmt(v / 1000, 1), yr: "volume collected in the month (m³)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xf: m => MESES[m - 1]});
      let s = A.s;
      const bw = (A.X(2) - A.X(1)) * 0.62;
      mensal.forEach((v, m) => {
        const x = A.X(m + 1) - bw / 2;
        if (bruto[m] > v) s += `<rect x="${x}" y="${A.Y(bruto[m])}" width="${bw}" height="${Math.max(0, A.Y(v) - A.Y(bruto[m]) - 1)}" rx="2" style="fill:${S(2)};opacity:0.55"/>`;
        s += `<rect x="${x}" y="${A.Y(v)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(v))}" rx="2" style="fill:${S(1)}"/>`;
      });
      s += `<line class="g-ref" x1="${A.X(0.4)}" x2="${A.X(12.6)}" y1="${A.Y(demandaMes)}" y2="${A.Y(demandaMes)}"/>`;
      s += `<text class="g-t" x="${A.X(12.6)}" y="${A.Y(demandaMes) - 6}" text-anchor="end">rainwater demand of the tutorial: ${fmt(demandaMes / 1000, 1)} m³/month</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, mensal.map((_, m) => A.X(m + 1)),
        m => dicaHTML(`${MESES[m]} · 30-year mean`, [
          [S(1), "collected", fmt(mensal[m] / 1000, 2) + " m³"],
          [S(2), "held back by the first flush", fmt((bruto[m] - mensal[m]) / 1000, 2) + " m³"],
          ["", "usable depth", fmt(c.mensal[String(desc)][m], 1) + " mm"]]));
      p.querySelector(`#${id}a-o`).textContent = fmt(area) + " m²";
      p.querySelector(`#${id}m-o`).textContent = "C = " + fmt(coef, 2);
      const anual = c.anual[String(desc)] * area * coef, anualBruto = c.anual["0"] * area * coef;
      const cobertos = mensal.filter(v => v >= demandaMes).length;
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(c.nome)}, ${fmt(area)} m² of ${esc(material).toLowerCase()}</p>
        <div class="fi-n">${cartao("Mean annual collection", fmt(anual / 1000, 1) + " m³")}
        ${cartao("Daily mean", fmt(anual / 365.25) + " L/day")}
        ${cartao("Usable depth", fmt(c.anual[String(desc)]) + " mm/year", `rain of ${fmt(c.anual["0"])} mm`)}
        ${cartao("Held back by the first flush", fmt(100 * (1 - anual / anualBruto), 1) + "%", `at ${fmt(desc)} mm per event`)}
        ${cartao("Months that cover the demand", cobertos, "of 12, in the tutorial")}
        ${cartao("Runoff coefficient", fmt(coefDe(), 2), esc(material))}</div>
        <p class="fi-nota">This is the gross supply of the roof, before the cistern: what the tank manages to store depends on its volume and on the consumption, and is what the daily-balance figures show. Coefficients from the ${esc(D.fonte_coeficientes)}</p>`;
    };
    ligarSeg(p, id + "c", x => { cidade = x; desenha(); });
    ligarSeg(p, id + "d", x => { desc = +x; desenha(); });
    p.querySelector(`#${id}m`).addEventListener("change", e => { material = e.target.value; desenha(); });
    p.querySelector(`#${id}a`).addEventListener("input", e => { area = D.areas[+e.target.value]; desenha(); });
    desenha();
  }
};

/* ─── which pressuriser uses less ───────────────────────────────────────── */
FI["fig00k_energia.png"] = {
  curto: "Choosing the pressuriser",
  pergunta: "Which pump uses the least energy to pressurise rainwater?",
  controles: "pressure · volume pumped · starts",
  experimente: D => {
    const v = D.padrao[1], n = D.padrao[2];
    const p1 = D.pressoes.find(pr => D.casos[`${pr}|${v}|${n}`].some(x => !x.atende));
    if (p1 === undefined) return "Raise the working pressure and compare how the models' energy changes. Note that the most powerful model is not the one that uses most per cubic metre: what decides is the running time.";
    const fora = D.casos[`${p1}|${v}|${n}`].filter(x => !x.atende).map(x => D.modelos.find(m => m.chave === x.chave).rotulo.split(",")[0]);
    return `Raise the working pressure: from ${fmt(p1, 1)} m of head, ${fora.join(", ")} can no longer deliver the flow of the point of use and drop out of the contest. Note that the most powerful model is not the one that uses most per cubic metre: what decides is the running time.`;
  },
  fonte: D => `A set of six generic pressurisers, each with an illustrative flow-against-pressure curve and no brand. The energy is the electrical power multiplied by the running time, and the effective flow is the lesser of the pump curve and the flow of the point of use, ${fmt(D.vazao_do_ponto)} L/min. The electricity price shown is illustrative.`,
  montar(p, D, id) {
    let pi = D.pressoes.indexOf(D.padrao[0]), vol = D.padrao[1], part = D.padrao[2], sel = 0;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "p", "Working pressure", D.pressoes.length, pi)}
      ${ctlSeg(id + "v", "Volume pumped per year", D.volumes.map(v => [v, fmt(v) + " m³"]), vol)}
      ${ctlSeg(id + "n", "Starts per year", D.partidas.map(n => [n, fmt(n)]), part)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 260" role="img" aria-label="Annual energy of each model"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 260" role="img" aria-label="Flow-against-pressure curve of each model"></svg>
      ${legenda([[S(4), "model that uses least"], [S(1), "highlighted model"], [S(2), "does not deliver the flow of the point"], ["var(--ink3)", "flow of the point of use", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const pressao = D.pressoes[pi];
      const lista = D.casos[`${pressao}|${vol}|${part}`];
      const meta = c => D.modelos.find(m => m.chave === c);
      const atendem = lista.filter(x => x.atende);
      const melhor = atendem.length ? atendem[0].chave : null;
      if (sel >= lista.length) sel = 0;
      const ey = escala(0, Math.max(...lista.map(x => x.kwh)) * 1.12, 4);
      const A = plano({W, H: 260, l: 210, r: 70, t: 34, b: 44, x: [0, ey.max], y: [lista.length - 0.4, -0.6],
        xm: ey.marcas, xf: v => fmt(v), xr: "electrical energy per year (kWh)"});
      let s = A.s;
      const h = 20;
      lista.forEach((x, i) => {
        const y = A.Y(i), cor = !x.atende ? S(2) : x.chave === melhor ? S(4) : S(1);
        s += `<rect x="${A.X(0)}" y="${y - h / 2}" width="${Math.max(1, A.X(x.kwh) - A.X(0))}" height="${h}" rx="2" style="fill:${cor};opacity:${i === sel ? 1 : 0.6}"/>`;
        s += `<text class="g-t" x="${A.X(0) - 8}" y="${y + 4}" text-anchor="end" style="${i === sel ? "font-weight:600" : ""}">${esc(meta(x.chave).rotulo)}</text>`;
        s += `<text class="g-t" x="${A.X(x.kwh) + 8}" y="${y + 4}">${x.atende ? fmt(x.kwh) + " kWh" : "does not deliver"}</text>`;
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      const svg = p.querySelector(`#${id}g`);
      const linhaDoPonteiro = e => {
        const r = svg.getBoundingClientRect(), y = (e.clientY - r.top) / r.height * 260;
        let k = 0, d = Infinity;
        lista.forEach((_, i) => { const q = Math.abs(A.Y(i) - y); if (q < d) { d = q; k = i; } });
        return k;
      };
      svg.onclick = e => { sel = linhaDoPonteiro(e); desenha(); };
      svg.style.cursor = "pointer";
      svg.onpointermove = null; svg.onpointerleave = null;

      const qmax = Math.max(...D.modelos.flatMap(m => m.curva.map(c => c[0])));
      const hmax = Math.max(...D.modelos.flatMap(m => m.curva.map(c => c[1])));
      const ex = escala(0, qmax * 1.02, 5), eh = escala(0, hmax * 1.05, 4);
      const B = plano({W, H: 260, l: 66, r: 120, t: 34, b: 44, x: [0, ex.max], y: [0, eh.max], ym: eh.marcas,
        yf: v => fmt(v), yr: "pressure (m of head)", xm: ex.marcas, xf: v => fmt(v), xr: "flow (L/min)"});
      let t = B.s;
      const rot = [];
      lista.forEach((x, i) => {
        const m = meta(x.chave), pontos = m.curva.slice().sort((a, b) => a[0] - b[0]);
        const cor = i === sel ? S(1) : "var(--ink3)";
        t += `<polyline points="${pontos.map(([q, hh]) => `${B.X(q)},${B.Y(hh)}`).join(" ")}" style="fill:none;stroke:${cor};stroke-width:${i === sel ? 2.6 : 1.2};opacity:${i === sel ? 1 : 0.5}"/>`;
        if (i === sel) rot.push({y: B.Y(pontos[pontos.length - 1][1]), t: m.rotulo.split(",")[0], c: S(1)});
      });
      t += `<line class="g-ref" x1="${B.X(D.vazao_do_ponto)}" x2="${B.X(D.vazao_do_ponto)}" y1="${B.Y(eh.max)}" y2="${B.Y(0)}"/>`;
      t += `<text class="g-t" x="${B.X(D.vazao_do_ponto) + 6}" y="${B.Y(eh.max) + 12}">flow of the point: ${fmt(D.vazao_do_ponto)} L/min</text>`;
      t += `<line x1="${B.X(0)}" x2="${B.X(ex.max)}" y1="${B.Y(pressao)}" y2="${B.Y(pressao)}" style="stroke:${S(4)};stroke-dasharray:4 4"/>`;
      t += `<text class="g-t" x="${B.X(ex.max)}" y="${B.Y(pressao) - 6}" text-anchor="end" style="fill:${S(4)}">working pressure: ${fmt(pressao, 1)} m</text>`;
      t += rotulosNaPonta(rot, B.X(ex.max) + 8, B.Y(eh.max), B.Y(0));
      p.querySelector(`#${id}h`).innerHTML = t;

      p.querySelector(`#${id}p-o`).textContent = fmt(pressao, 1) + " m";
      const x = lista[sel], m = meta(x.chave);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${melhor ? "Lowest consumption: " + esc(meta(melhor).rotulo) : "No model delivers the flow of the point at this pressure"}</p>
        <div class="fi-n">${cartao("Energy of the highlighted model", x.atende ? fmt(x.kwh) + " kWh/year" : "—", esc(m.rotulo))}
        ${cartao("Specific consumption", x.atende ? fmt(x.kwh_m3, 3) + " kWh/m³" : "—")}
        ${cartao("Annual energy cost", x.atende ? din(x.kwh * D.tarifa) : "—", `price of ${din(D.tarifa, 2)}/kWh, illustrative`)}
        ${cartao("Running time", x.atende ? fmt(x.horas) + " h/year" : "—", `${fmt(part)} starts`)}</div>
        <p class="fi-sub">All models under this condition</p>
        <table class="fi-tabela"><thead><tr><th>Model</th><th class="n">Flow</th><th class="n">kWh/year</th><th class="n">kWh/m³</th></tr></thead><tbody>
        ${lista.map((y, i) => {
          const mm = meta(y.chave);
          return `<tr${i === sel ? ' class="atual"' : ""}><td>${esc(mm.rotulo)}<small>${esc(mm.controle)} · ${fmt(mm.kw_eletrico, 3)} kW electrical</small></td>
            <td class="n">${y.atende ? fmt(y.vazao, 1) + " L/min" : "does not deliver"}</td><td class="n">${y.atende ? fmt(y.kwh) : "—"}</td><td class="n">${y.atende ? fmt(y.kwh_m3, 3) : "—"}</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">The effective flow is the lesser of the pump curve and the flow of the point of use: a pump that delivers 40 L/min does not fill a cistern faster than a point that asks for ${fmt(D.vazao_do_ponto)} L/min; it merely runs for the same time at a higher power. Source of the curve: ${esc(m.fonte)}.</p>`;
    };
    p.querySelector(`#${id}p`).addEventListener("input", e => { pi = +e.target.value; desenha(); });
    ligarSeg(p, id + "v", x => { vol = +x; desenha(); });
    ligarSeg(p, id + "n", x => { part = +x; desenha(); });
    desenha();
  }
};

/* ─── the water quality classes ─────────────────────────────────────────── */
FI["fig36_classes.png"] = {
  curto: "The quality classes",
  pergunta: "What quality does each use require, and what is the reference set and what is an adaptation?",
  controles: "quality class",
  experimente: D => {
    const a = D.classes[0], b = D.classes[D.classes.length - 1];
    return `Compare class 1, which is the program's reference set, with class 4: the turbidity falls from ${fmt(a.turbidez, 0)} to ${fmt(b.turbidez, 0)} NTU and the colour from ${fmt(a.cor, 0)} to ${fmt(b.cor, 0)} HU. Note the badge on each one: only class 1 is the reference set, and the others are adaptations of the program, to be checked against the requirements that apply to your project.`;
  },
  fonte: "The four classes as the program defines them (triton/core/water_quality.py). Class 1 is the program's minimum reference set; classes 2 to 4 are adaptations of the program, and are declared as such on screen and in the report. Check the limits against the requirement that applies where the system is built.",
  montar(p, D, id) {
    let sel = D.padrao;
    const W = 640;
    const nomeCurto = c => c.nome.split(":")[0].replace(/\s*\(.*\)/, "");
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "Quality class", D.classes.map(c => [c.chave, nomeCurto(c)]), sel)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Limit of each parameter in the four classes"></svg>
      ${legenda([[S(1), "highlighted class"], ["var(--grid)", "other classes"], [S(4), "reference set (class 1)"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const c = D.classes.find(x => x.chave === sel);
      let s = "";
      D.parametros.forEach((param, k) => {
        const valores = D.classes.map(x => x[param.chave]);
        const topo = 34 + k * 92;
        const ey = escala(0, Math.max(...valores, 1) * 1.2, 3);
        const A = plano({W, H: topo + 62, l: 66, r: 14, t: topo, b: 20, x: [-0.6, D.classes.length - 0.4], y: [0, ey.max],
          ym: ey.marcas, yf: v => fmt(v, param.casas), yr: `${param.nome} (${param.unidade})`,
          xm: D.classes.map((_, i) => i), xf: i => "class " + (i + 1)});
        s += A.s;
        const bw = (A.X(1) - A.X(0)) * 0.5;
        valores.forEach((v, i) => {
          const cor = D.classes[i].chave === sel ? S(1) : D.classes[i].normativa ? S(4) : "var(--grid)";
          s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(v)}" width="${bw}" height="${Math.max(1, A.Y(0) - A.Y(v))}" rx="2" style="fill:${cor}"/>`;
          s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(v) - 5}" text-anchor="middle">${fmt(v, param.casas)}</text>`;
        });
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(nomeCurto(c))}
        <span class="pill ${c.normativa ? "pleno" : "parcial"}">${c.normativa ? "✓ reference set" : "◐ adaptation by the program"}</span></p>
        <table class="fi-tabela"><tbody>
        <tr><td>Turbidity</td><td class="n">up to ${fmt(c.turbidez, 1)} NTU</td></tr>
        <tr><td>Apparent colour</td><td class="n">up to ${fmt(c.cor, 1)} HU</td></tr>
        <tr><td>pH</td><td class="n">${fmt(c.ph[0], 1)} to ${fmt(c.ph[1], 1)}</td></tr>
        <tr><td>Free residual chlorine</td><td class="n">${fmt(c.cloro[0], 2)} to ${fmt(c.cloro[1], 2)} mg/L</td></tr>
        <tr><td>Thermotolerant coliforms</td><td class="n">${c.coliformes > 0 ? "up to " + fmt(c.coliformes) + " CFU/100 mL" : "absent"}</td></tr>
        <tr><td>Disinfection</td><td class="n">${c.desinfeccao ? "required" : "not required"}</td></tr>
        <tr><td>Fine filtration</td><td class="n">${c.filtracao ? "required" : "not required"}</td></tr>
        </tbody></table>
        <p class="fi-nota">${esc(c.descricao)}</p>
        ${D.parametros.map(x => `<p class="fi-nota"><b>${x.nome}.</b> ${x.texto}</p>`).join("")}`;
    };
    ligarSeg(p, id + "c", x => { sel = x; desenha(); });
    desenha();
  }
};

/* ─── the net present value against the volume ──────────────────────────── */
FI["fig49_programa_vpl.png"] = {
  curto: "The NPV against the volume",
  pergunta: "Which volume gives the best financial return?",
  controles: "cistern material",
  experimente: D => {
    const linha = D.casos[D.padrao];
    const j = linha.reduce((a, x, k) => k > 0 && x[0] > linha[a][0] ? k : a, 1);
    const positivo = D.materiais.some(([k]) => D.casos[k].some((x, i) => i > 0 && x[0] > 0));
    return `${positivo ? "" : "In this illustrative case no volume has a positive NPV, for any material: the curve is highest at the no-cistern point, and the least negative size is the one to compare. "}In ${D.materiais.find(m => m[0] === D.padrao)[1].toLowerCase()}, the least negative NPV among the sizes with a cistern is at ${fmt(D.volumes[j] / 1000)} m³, against 4 m³ for the marginal-gain criterion. Change the material and watch the optimum move: it is the price per litre that moves it. ${ILUSTRATIVO}`;
  },
  fonte: D => `One run of the economic analysis per volume and material, with the tutorial project, the New York tariff and a ${D.anos}-year horizon. The volume of the best NPV is read from the curve itself. ${ILUSTRATIVO}`,
  montar(p, D, id) {
    let mat = D.padrao, sel = D.volumes.indexOf(4000);
    const W = 640;
    const otimo = linha => linha.reduce((a, x, j) => j > 0 && x[0] > linha[a][0] ? j : a, 1);   // with a cistern
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "m", "Cistern material", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 320" role="img" aria-label="Net present value as a function of cistern volume, by material"></svg>
      ${legenda(D.materiais.map(([k, t], i) => [S(i + 1), t, "linha"]).concat([["var(--ink2)", "highlighted volume", "trac"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const todos = D.materiais.flatMap(([k]) => D.casos[k].map(x => x[0]));
      const ey = escala(Math.min(...todos, 0), Math.max(...todos, 0) * 1.08 + 1, 5);
      const A = plano({W, H: 320, l: 74, r: 120, t: 34, b: 46, x: [0, 20000], y: [ey.min, ey.max], ym: ey.marcas,
        yf: v => menos(v), yr: `net present value over ${D.anos} years (${MOEDA})`,
        xm: [0, 5000, 10000, 15000, 20000], xf: v => fmt(v / 1000) + " m³", xr: "cistern volume"});
      let s = A.s;
      const rot = [];
      D.materiais.forEach(([k, t], i) => {
        const linha = D.casos[k], cor = S(i + 1), atual = k === mat;
        s += `<polyline points="${linha.map((x, j) => `${A.X(D.volumes[j])},${A.Y(x[0])}`).join(" ")}" style="fill:none;stroke:${cor};stroke-width:${atual ? 2.6 : 1.4};opacity:${atual ? 1 : 0.45}"/>`;
        const melhor = otimo(linha);
        if (atual) {
          s += `<circle cx="${A.X(D.volumes[melhor])}" cy="${A.Y(linha[melhor][0])}" r="6" style="fill:${cor};stroke:var(--surface);stroke-width:2"/>`;
          s += `<text class="g-rot" x="${A.X(D.volumes[melhor])}" y="${A.Y(linha[melhor][0]) - 12}" text-anchor="middle" style="fill:${cor}">best: ${fmt(D.volumes[melhor])} L</text>`;
        }
        rot.push({y: A.Y(linha[linha.length - 1][0]), t: t.split(" (")[0], c: cor});
      });
      s += rotulosNaPonta(rot, A.X(20000) + 8, A.Y(ey.max), A.Y(ey.min));
      s += `<line class="g-ref" x1="${A.X(D.volumes[sel])}" x2="${A.X(D.volumes[sel])}" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="stroke:var(--ink2)"/>`;
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map(v => A.X(v)),
        j => dicaHTML(`${fmt(D.volumes[j])} L`, D.materiais.map(([k, t], i) => [S(i + 1), t.split(" (")[0], din(D.casos[k][j][0])])),
        j => { sel = j; desenha(); });
      const linha = D.casos[mat], melhor = otimo(linha);
      const x = linha[sel];
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(D.materiais.find(m => m[0] === mat)[1])}</p>
        <div class="fi-n">${cartao("Volume of best NPV (with a cistern)", fmt(D.volumes[melhor]) + " L", din(linha[melhor][0]))}
        ${cartao("Highlighted volume", fmt(D.volumes[sel]) + " L", "click the chart to change")}
        ${cartao("NPV", din(x[0]), x[0] >= 0 ? "✓ positive" : "✕ negative")}
        ${cartao("Payback", x[1] ? fmt(x[1], 1) + " years" : `more than ${D.anos} years`)}
        ${cartao("Saving potential", fmt(x[2], 2) + "%")}
        ${cartao("Difference from the best", din(x[0] - linha[melhor][0]))}</div>
        <p class="fi-sub">The best volume of each material</p>
        <table class="fi-tabela"><tbody>${D.materiais.map(([k, t], i) => {
          const l = D.casos[k], m = otimo(l);
          return `<tr${k === mat ? ' class="atual"' : ""}><td><i style="--c:${S(i + 1)}"></i>${t}</td><td class="n">${fmt(D.volumes[m])} L</td><td class="n">${din(l[m][0])}</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">The curve has an interior optimum because the investment grows with the volume while the water saving saturates. A volume to the right of the optimum keeps saving more water, and earning less money. The zero line is the no-cistern alternative. ${ILUSTRATIVO}</p>`;
    };
    ligarSeg(p, id + "m", x => { mat = x; desenha(); });
    desenha();
  }
};

/* ─── mounting on the pages ─────────────────────────────────────────────── */
/* A text may be a string or a function of the figure's data. */
const texto = (t, D) => (typeof t === "function" ? t(D) : t);

function montarInterativas(raiz) {
  raiz.querySelectorAll("figure.fig[data-arquivo]").forEach(fig => {
    const def = FI[fig.dataset.arquivo], bruto = FI_D[fig.dataset.arquivo];
    const dados = bruto && bruto.usa ? DADOS[bruto.usa] : bruto;
    if (!def || !dados) return;
    const num = fig.id.replace("fig-", ""), id = "fi" + num;
    const estatica = fig.querySelector(":scope > a");
    fig.classList.add("com-fi");
    const caixa = document.createElement("div");
    caixa.className = "fi";
    caixa.innerHTML = `<div class="fi-topo"><span class="fi-selo"><i></i>Figure ${num} · interactive</span>
      <div class="fi-modo" role="group" aria-label="Version of the figure"><button type="button" data-m="i" aria-pressed="true">Interactive</button><button type="button" data-m="e" aria-pressed="false">Manual figure</button></div></div>
      <p class="fi-pergunta">${def.pergunta}</p><div class="fi-palco"></div>
      <p class="fi-exp"><b>Try it.</b> ${texto(def.experimente, dados)}</p><p class="fi-fonte"><b>Where the numbers come from.</b> ${texto(def.fonte, dados)}</p>`;
    fig.insertBefore(caixa, estatica);
    estatica.hidden = true;
    const palco = caixa.querySelector(".fi-palco");
    caixa.querySelector(".fi-modo").addEventListener("click", e => {
      const b = e.target.closest("button");
      if (!b) return;
      const inter = b.dataset.m === "i";
      caixa.querySelectorAll(".fi-modo button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
      palco.hidden = !inter;
      caixa.querySelector(".fi-exp").hidden = !inter;
      caixa.querySelector(".fi-fonte").hidden = !inter;
      estatica.hidden = inter;
    });
    def.montar(palco, dados, id);
  });
}

/* Where each interactive figure is, by section, in the order of the manual. */
const INTERATIVAS_DA_SECAO = {};
Object.keys(FI_ONDE).forEach(arquivo => {
  if (!FI_D[arquivo]) return;
  const o = FI_ONDE[arquivo];
  (INTERATIVAS_DA_SECAO[o.secao] = INTERATIVAS_DA_SECAO[o.secao] || []).push({arquivo, numero: o.numero});
});
Object.values(INTERATIVAS_DA_SECAO).forEach(lista => lista.sort((a, b) => a.numero - b.numero));

/* The home page opens no figure: it points to where each one is. */
const EM_DESTAQUE = ["fig01_dez_dias.png", "fig08_fluxo_de_caixa.png", "fig35_escoamento.png",
                     "fig02_curva_de_retorno.png", "fig06_carbono_no_tempo.png",
                     "fig51_programa_topsis.png"];

function bulletsInterativas() {
  const todas = Object.keys(FI_ONDE).filter(a => FI_D[a] && FI[a]);
  if (!todas.length) return "";
  const ordem = a => {
    const partes = String(FI_ONDE[a].secao).split(".");
    return (parseFloat(partes[0]) || 99) * 100 + (parseFloat(partes[1]) || 0);
  };
  const destaque = EM_DESTAQUE.filter(a => todas.includes(a)).sort((a, b) => ordem(a) - ordem(b));
  return `<section class="faixa" id="interativas">
    <h2>Questions you answer by moving things</h2>
    <p class="sub">These figures of the manual have an interactive version. They do not open here: each one lives in the section where the subject comes up, so that the text and the chart are read together.</p>
    <ul class="perguntas">${destaque.map(a => {
      const o = FI_ONDE[a];
      return `<li><a href="#/${o.secao}/fig-${o.numero}"><b>${esc(FI[a].pergunta)}</b><small>section ${esc(o.secao)} · figure ${o.numero}</small></a></li>`;
    }).join("")}</ul>
    <p class="depois">There are ${fmt(todas.length)} in all, spread through the manual. In the contents of each page they are marked <b class="marca-i">interactive</b>, and the search finds them by name.</p>
  </section>`;
}

/* The search finds the question each interactive figure answers, and not only the
   caption of the static figure: that is how the reader arrives by what they want to know. */
Object.keys(FI_ONDE).forEach(arquivo => {
  const o = FI_ONDE[arquivo], def = FI[arquivo];
  if (!def || !FI_D[arquivo] || typeof INDICE === "undefined") return;
  const item = INDICE.find(i => i.t === "interativa" && i.id === o.secao && i.a === "fig-" + o.numero);
  if (!item) return;
  item.x = item.n + " " + def.curto + " · controls: " + def.controles;
  item.n = def.pergunta;
  item.nn = semAcento((item.r + " " + item.n + " " + item.x).toLowerCase());
  item.xn = semAcento(item.x.toLowerCase());
});
