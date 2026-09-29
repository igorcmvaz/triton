/* ── figuras interativas ──────────────────────────────────────────────────────
   Cada figura interativa substitui, na página da seção, a figura estática de
   mesmo arquivo. Os números vêm prontos de gerar_figuras_interativas.py, que
   roda o simulador; aqui só se escolhe a célula e se desenha. */

const FI = {};
const FI_D = DADOS.interativas || {};
const FI_ONDE = DADOS.onde_interativas || {};
const S = n => `var(--s${n})`;
/* Rampa de um tom só, para as parcelas de uma barra empilhada. */
const R = n => `var(--r${n})`;
const menos = (v, d = 0) => (v < 0 ? "−" : "") + fmt(Math.abs(v), d);
const reais = (v, d = 0) => (v < 0 ? "−" : "") + "R$ " + fmt(Math.abs(v), d);
const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
const TUTORIAL = "Projeto do tutorial: casa em Florianópolis, 150 m² de cobertura, coeficiente de escoamento 0,85, descarte de 2 mm, quatro moradores com 150 L/dia cada, 28% da demanda atendível por chuva, 30 anos de chuva diária.";

/* escalas e eixos */
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
/* rótulos diretos na ponta das linhas, afastados para não se sobreporem */
function rotulosNaPonta(itens, x, ymin, ymax) {
  const ord = itens.slice().sort((a, b) => a.y - b.y);
  for (let i = 1; i < ord.length; i++) if (ord[i].y - ord[i - 1].y < 14) ord[i].y = ord[i - 1].y + 14;
  const excesso = ord.length ? ord[ord.length - 1].y - ymax : 0;
  if (excesso > 0) ord.forEach(o => { o.y = Math.max(ymin, o.y - excesso); });
  return ord.map(o => `<text class="g-rot" x="${x}" y="${o.y + 4}" style="fill:${o.c}">${o.t}</text>`).join("");
}

/* dica ao passar o ponteiro */
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

/* controles */
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

/* ─── figura: o balanço de dez dias ─────────────────────────────────────── */
FI["fig01_dez_dias.png"] = {
  curto: "O balanço de dez dias",
  pergunta: "Para onde vai a chuva de cada dia: cisterna, consumo ou extravasor?",
  controles: "capacidade · descarte · dia a dia",
  experimente: "Zere o descarte: o dia 3, com 1,6 mm de chuva, passa a render 136 L. Suba a capacidade para 3.000 L e o dia 6 deixa de extravasar; desça para 1.000 L e ele extravasa 1.774 L.",
  fonte: "Os dez dias do exemplo da seção: 100 m² de cobertura, coeficiente de escoamento 0,85, demanda de 200 L/dia com 40% atendível por chuva, cisterna começando vazia. Cada célula é uma rodada do simulador.",
  montar(p, D, id) {
    let cap = D.padrao[0], desc = D.padrao[1], dia = 1, relogio = null;
    const W = 640, H = 390;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "c", "Capacidade da cisterna", D.capacidades.length, D.capacidades.indexOf(cap))}
      ${ctlSeg(id + "d", "Descarte de primeiras águas", D.descartes.map(d => [d, fmt(d) + " mm"]), desc)}
      <div class="fi-ctl"><span class="fi-rot">Dia em destaque</span><div class="passo">
        <button type="button" data-a="-1" aria-label="Dia anterior">‹</button><output id="${id}o"></output>
        <button type="button" data-a="1" aria-label="Próximo dia">›</button>
        <button type="button" class="tocar" id="${id}p">▶ Reproduzir</button></div></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Volume captado e extravasado por dia, e volume armazenado na cisterna ao fim de cada um dos dez dias"></svg>
      ${legenda([[S(1), "captado que ficou na cisterna"], [S(2), "captado que extravasou"], [S(3), "volume armazenado ao fim do dia", "linha"], ["var(--ink3)", "capacidade da cisterna", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const parar = () => { clearInterval(relogio); relogio = null; p.querySelector(`#${id}p`).textContent = "▶ Reproduzir"; };
    const desenhar = () => {
      const L = D.casos[`${cap}|${desc}`];
      const ya = escala(0, Math.max(500, ...L.map(l => l[1])), 4);
      const A = plano({W, H: 190, l: 58, r: 14, t: 36, b: 24, x: [0.4, 10.6], y: [0, ya.max], ym: ya.marcas, yr: "volume captado no dia (L)", painel: "(a)"});
      const yb = escala(0, Math.max(cap, ...L.map(l => l[6])), 4);
      const B = plano({W, H, l: 58, r: 14, t: 236, b: 42, x: [0.4, 10.6], y: [0, yb.max], ym: yb.marcas, yr: "volume armazenado ao fim do dia (L)", painel: "(b)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], xf: v => "dia " + v, xr: ""});
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
      s += `<text class="g-t" x="${B.X(10.6)}" y="${B.Y(cap) - 6}" text-anchor="end">capacidade: ${fmt(cap)} L</text>`;
      s += `<polyline points="${L.map((l, k) => `${B.X(k + 1)},${B.Y(l[6])}`).join(" ")}" style="fill:none;stroke:${S(3)};stroke-width:2"/>`;
      L.forEach((l, k) => { s += `<circle cx="${B.X(k + 1)}" cy="${B.Y(l[6])}" r="${k === dia ? 6.5 : 4.5}" style="fill:${S(3)};stroke:var(--surface);stroke-width:2"/>`; });
      svg.innerHTML = s;
      pairar(svg, W, L.map((_, k) => A.X(k + 1)), k => dicaHTML(`Dia ${k + 1} · chuva de ${fmt(D.chuva[k], 1)} mm`, [
        [S(1), "captado", fmt(L[k][1]) + " L"], [S(2), "extravasado", fmt(L[k][5]) + " L"],
        [S(3), "armazenado ao fim do dia", fmt(L[k][6]) + " L"]]), k => { dia = k; parar(); desenhar(); });

      const l = L[dia], ini = dia ? L[dia - 1][6] : 0;
      const sat = [["nulo", "✕ nulo"], ["parcial", "◐ parcial"], ["pleno", "✓ pleno"]][l[7]];
      const tot = j => L.reduce((a, x) => a + x[j], 0);
      p.querySelector(`#${id}o`).textContent = `dia ${dia + 1} de 10`;
      p.querySelector(`#${id}c-o`).textContent = fmt(cap) + " L";
      leit.innerHTML = `<p class="fi-sub">Balanço do dia ${dia + 1}</p>
        <table class="fi-tabela"><tbody>
        <tr><td>Chuva do dia</td><td class="n">${fmt(D.chuva[dia], 1)} mm</td></tr>
        <tr><td>Chuva depois do descarte de ${fmt(desc)} mm</td><td class="n">${fmt(l[0], 1)} mm</td></tr>
        <tr><td>Captado<small>${fmt(l[0], 1)} mm × ${fmt(D.area)} m² × ${fmt(D.coef, 2)}</small></td><td class="n">${fmt(l[1])} L</td></tr>
        <tr class="sep"><td>Armazenado no início do dia</td><td class="n">${fmt(ini)} L</td></tr>
        <tr><td><i style="--c:${S(1)}"></i>+ captado</td><td class="n">+${fmt(l[1])} L</td></tr>
        <tr><td>− consumo pluvial<small>demanda pluvial de ${fmt(l[2])} L</small></td><td class="n">−${fmt(l[3])} L</td></tr>
        <tr><td><i style="--c:${S(2)}"></i>− extravasado</td><td class="n">−${fmt(l[5])} L</td></tr>
        <tr class="tot"><td><i style="--c:${S(3)}"></i>= armazenado no fim do dia</td><td class="n">${fmt(l[6])} L</td></tr>
        </tbody></table>
        <p class="fi-sat">Atendimento do dia <span class="pill ${sat[0]}">${sat[1]}</span> · água potável complementar: ${fmt(l[4])} L</p>
        <p class="fi-sub">Nos dez dias</p>
        <div class="fi-n">${cartao("Captado", fmt(tot(1)), "L")}${cartao("Extravasado", fmt(tot(5)), "L")}
        ${cartao("Demanda pluvial atendida", fmt(100 * tot(3) / tot(2), 1) + "%")}${cartao("Dias de atendimento pleno", L.filter(x => x[7] === 2).length, "de 10")}</div>`;
    };
    p.querySelector(`#${id}c`).addEventListener("input", e => { cap = D.capacidades[+e.target.value]; desenhar(); });
    ligarSeg(p, id + "d", v => { desc = +v; desenhar(); });
    p.querySelectorAll(".passo [data-a]").forEach(b => b.addEventListener("click", () => { parar(); dia = (dia + +b.dataset.a + 10) % 10; desenhar(); }));
    p.querySelector(`#${id}p`).addEventListener("click", e => {
      if (relogio) { parar(); return; }
      if (dia === 9) dia = -1;
      e.target.textContent = "❚❚ Pausar";
      relogio = setInterval(() => {
        if (!document.body.contains(svg) || dia >= 9) { parar(); return; }
        dia += 1; desenhar();
      }, 900);
    });
    desenhar();
  }
};

/* ─── figura: o nível da cisterna, dia a dia ───────────────────────────── */
FI["fig48_programa_serie_diaria.png"] = {
  curto: "O nível da cisterna, dia a dia",
  pergunta: "Como a cisterna enche e esvazia ao longo de um ano?",
  controles: "capacidade · ano da série",
  experimente: "Clique em «Ano mais seco» e troque a capacidade: veja em que meses a cisterna de 1 m³ passa vazia e quanto disso uma de 8 m³ resolve. Clique numa barra da faixa de anos para ir direto a ele.",
  fonte: TUTORIAL + " O ano é o do calendário da série, a partir de 1º de janeiro de 1980.",
  montar(p, D, id) {
    let vol = D.padrao, yi = 0;
    const N = D.anos.length, W = 720, H = 372;
    const media = (v, j) => D.resumo[v].reduce((a, r) => a + r[j], 0) / N;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "v", "Capacidade da cisterna", D.volumes.map(v => [v, fmt(v / 1000) + " m³"]), vol)}
      <div class="fi-ctl"><label class="fi-rot" for="${id}a">Ano da série</label><div class="linha-ctl">
        <select id="${id}a">${D.anos.map((a, k) => `<option value="${k}">${a}</option>`).join("")}</select>
        <button type="button" class="bt" data-q="seco">Ano mais seco</button><button type="button" class="bt" data-q="chuvoso">Ano mais chuvoso</button><button type="button" class="bt" data-q="vazio">Mais dias vazia</button></div></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}f" class="faixa-anos" viewBox="0 0 ${W} 78" role="img" aria-label="Chuva anual de cada ano da série; clique para escolher o ano"></svg>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Chuva diária e volume armazenado na cisterna ao fim de cada dia do ano escolhido"></svg>
      ${legenda([[S(1), "chuva diária"], [S(3), "volume armazenado"], [S(2), "dia com a cisterna vazia (até 5% da capacidade)"], ["var(--ink3)", "capacidade", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const faixa = p.querySelector(`#${id}f`), svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`), sel = p.querySelector(`#${id}a`);
    const dataDe = i => new Date(Date.UTC(1980, 0, 1) + i * 864e5);
    const desenhar = () => {
      const R = D.resumo[vol];
      /* faixa dos anos */
      const chuvas = R.map(r => r[0]);
      const F = plano({W, H: 78, l: 58, r: 14, t: 22, b: 20, x: [-0.5, N - 0.5], y: [0, Math.max(...chuvas)], yr: "chuva anual (clique num ano)"});
      let f = F.s;
      const bw = (F.X(1) - F.X(0)) * 0.7;
      chuvas.forEach((c, k) => {
        f += `<rect x="${F.X(k) - bw / 2}" y="${F.Y(c)}" width="${bw}" height="${F.Y(0) - F.Y(c)}" rx="2" style="fill:${k === yi ? S(1) : "var(--line)"}"/>`;
        if (k % 5 === 0) f += `<text class="g-t" x="${F.X(k)}" y="${78 - 5}" text-anchor="middle">${D.anos[k]}</text>`;
      });
      faixa.innerHTML = f;
      pairar(faixa, W, chuvas.map((_, k) => F.X(k)), k => dicaHTML(String(D.anos[k]), [[S(1), "chuva no ano", fmt(chuvas[k]) + " mm"]]), k => { yi = k; desenhar(); });

      /* o ano escolhido */
      const f0 = D.primeiro_dia[yi], f1 = yi + 1 < N ? D.primeiro_dia[yi + 1] : D.chuva.length, n = f1 - f0;
      const chuva = D.chuva.slice(f0, f1), niv = D.niveis[vol].slice(f0, f1);
      const ya = escala(0, Math.max(20, ...chuva), 3);
      const A = plano({W, H: 132, l: 58, r: 14, t: 30, b: 6, x: [0, n], y: [0, ya.max], ym: ya.marcas, yr: "chuva (mm/dia)", painel: "(a)"});
      const yb = escala(0, vol, 4);
      const inicioMes = MESES.map((_, m) => (Date.UTC(D.anos[yi], m, 1) - Date.UTC(D.anos[yi], 0, 1)) / 864e5);
      const B = plano({W, H, l: 58, r: 14, t: 170, b: 40, x: [0, n], y: [0, yb.max], ym: yb.marcas, yf: v => fmt(v), yr: "volume armazenado ao fim do dia (L)", painel: "(b)",
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
        dataDe(f0 + k).toLocaleDateString("pt-BR", {timeZone: "UTC", day: "numeric", month: "long", year: "numeric"}), [
          [S(1), "chuva", fmt(chuva[k], 1) + " mm"], [S(3), "armazenado", fmt(niv[k]) + " L"],
          ["", "da capacidade", fmt(100 * niv[k] / vol, 0) + "%"]]));

      sel.value = yi;
      const r = R[yi];
      leit.innerHTML = `<p class="fi-sub">${D.anos[yi]}, cisterna de ${fmt(vol)} L</p>
        <div class="fi-n">
        ${cartao("Chuva no ano", fmt(r[0]) + " mm", `média: ${fmt(media(vol, 0))}`)}
        ${cartao("Demanda pluvial atendida", fmt(r[1], 1) + "%", `média: ${fmt(media(vol, 1), 1)}%`)}
        ${cartao("Dias com a cisterna vazia", fmt(r[3]), `média: ${fmt(media(vol, 3), 0)}`)}
        ${cartao("Dias de atendimento pleno", fmt(r[4]), `de ${r[5]}`)}
        ${cartao("Volume extravasado", fmt(r[2], 1) + " m³", `média: ${fmt(media(vol, 2), 1)} m³`)}
        ${cartao("Demanda pluvial diária", fmt(D.demanda_pluvial) + " L", "28% de 600 L")}
        </div>
        <p class="fi-nota">«Vazia» é o fim de dia com até 5% da capacidade. «Atendimento pleno» é o dia em que a cisterna cobriu toda a demanda pluvial.</p>`;
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

/* ─── figura: a permanência da autonomia ───────────────────────────────── */
FI["fig47_permanencia.png"] = {
  curto: "A permanência da autonomia",
  pergunta: "Quantos dias de consumo a cisterna guarda, e durante quanto tempo?",
  controles: "capacidade de 0,5 a 20 m³",
  experimente: "Leve a capacidade de 4 m³ para 8 m³: a autonomia mediana passa de 19,8 para 43,3 dias e as renovações caem de 14,9 para 7,6 por ano, mas o potencial de economia sobe só de 27,12% para 27,92%.",
  fonte: TUTORIAL + " Autonomia é o volume guardado ao fim do dia dividido pela demanda pluvial diária de 168 L.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), refs = true;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Capacidade da cisterna", D.volumes.length, vi)}
      <div class="fi-ctl"><span class="fi-rot">Comparar com</span><button type="button" class="chip-t" id="${id}r" aria-pressed="true" style="--c:var(--ink3)"><i></i>2, 4, 10 e 20 m³</button></div>
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 320" role="img" aria-label="Curva de permanência da autonomia da cisterna, em dias de demanda pluvial"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 190" role="img" aria-label="Renovações anuais do volume da cisterna em função da capacidade; clique para escolher a capacidade"></svg>
      ${legenda([[S(1), "capacidade escolhida", "linha"], ["var(--ink3)", "capacidades de referência", "linha"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), svg2 = p.querySelector(`#${id}h`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], C = D.curvas[String(v)], E = D.estados[String(v)];
      const mostrar = refs ? D.referencias.filter(r => r !== v) : [];
      const ymax = Math.max(C[0], ...mostrar.map(r => D.curvas[String(r)][0]));
      const ey = escala(0, ymax, 5);
      const A = plano({W, H: 320, l: 58, r: 14, t: 34, b: 44, x: [0, 100], y: [0, ey.max], ym: ey.marcas, yr: "autonomia (dias de demanda pluvial)", painel: "(a)",
        xm: [0, 20, 40, 60, 80, 100], xf: x => x + "%", xr: "tempo em que a autonomia é igualada ou superada"});
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
      pairar(svg, W, D.pontos.map(q => A.X(q)), k => dicaHTML(`Em ${D.pontos[k]}% do tempo, a cisterna guarda pelo menos`, [
        [S(1), `${fmt(v / 1000, v % 1000 ? 1 : 0)} m³`, fmt(C[k], 1) + " dias"],
        ...mostrar.map(r => ["var(--ink3)", `${fmt(r / 1000)} m³`, fmt(D.curvas[String(r)][k], 1) + " dias"])]));

      const ren = D.volumes.map(x => D.estados[String(x)][0]);
      const er = escala(0, Math.max(...ren), 3);
      const B = plano({W, H: 190, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [0, er.max], ym: er.marcas, yr: "renovações do volume por ano", painel: "(b)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "capacidade da cisterna"});
      let t = B.s + `<polyline points="${D.volumes.map((x, k) => `${B.X(x)},${B.Y(ren[k])}`).join(" ")}" style="fill:none;stroke:${S(1)};stroke-width:2"/>`;
      t += `<circle cx="${B.X(v)}" cy="${B.Y(E[0])}" r="6" style="fill:${S(1)};stroke:var(--surface);stroke-width:2"/>`;
      t += `<text class="g-rot" x="${B.X(v) + 10}" y="${B.Y(E[0]) - 8}" style="fill:var(--ink)">${fmt(E[0], 1)}×</text>`;
      svg2.innerHTML = t;
      pairar(svg2, W, D.volumes.map(x => B.X(x)), k => dicaHTML(`${fmt(D.volumes[k])} L`, [[S(1), "renovações por ano", fmt(ren[k], 1) + "×"]]),
        k => { vi = k; p.querySelector(`#${id}v`).value = k; desenhar(); });

      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      leit.innerHTML = `<p class="fi-sub">Cisterna de ${fmt(v)} L</p><div class="fi-n">
        ${cartao("Autonomia mediana", fmt(E[3], 1), "dias")}
        ${cartao("Renovações por ano", fmt(E[0], 1) + "×")}
        ${cartao("Tempo com a cisterna vazia", fmt(E[1], 1) + "%")}
        ${cartao("Tempo com a cisterna cheia", fmt(E[2], 1) + "%")}
        ${cartao("Potencial de economia", fmt(E[4], 2) + "%", "de 28%")}
        ${cartao("Demanda pluvial diária", fmt(D.demanda_pluvial) + " L")}</div>
        <p class="fi-nota">A curva (a) ordena os 30 anos de dias do maior para o menor volume guardado. Onde ela toca o zero, começa o tempo de cisterna vazia. Renovação é o consumo pluvial do ano dividido pela capacidade: quantas vezes a água da cisterna foi trocada.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    p.querySelector(`#${id}r`).addEventListener("click", e => { refs = !refs; e.currentTarget.setAttribute("aria-pressed", String(refs)); desenhar(); });
    desenhar();
  }
};

/* ─── figura: a fatura nos três regimes ────────────────────────────────── */
FI["fig05_regimes.png"] = {
  curto: "A fatura em três regimes de mínimo",
  pergunta: "Quanto da água economizada vira economia na fatura?",
  controles: "consumo sem e com o sistema",
  experimente: "No regime de franquia, baixe o consumo com o sistema para menos de 10 m³: a fatura para de cair, porque os primeiros 10 m³ já estão pagos no valor mínimo. No regime de disponibilidade, a mesma economia rende mais.",
  fonte: "Estruturas tarifárias reais: disponibilidade como na CASAN (Florianópolis), franquia como em Floriano (PI), e a de Floriano sem a franquia, para isolar o efeito dela. Parcela de água calculada pela mesma função do programa; o esgoto é cobrado como percentual dela e apenas multiplica as três curvas, sem mudar o formato — é o formato que distingue os regimes. A figura 28, na seção 2.7, abre a fatura inteira. O ponto de partida é o consumo médio do tutorial.",
  montar(p, D, id) {
    const passo = 0.25, n = Math.round(30 / passo) + 1;
    const idx = v => Math.round(v / passo);
    let iSem = idx(D.padrao[0]), iCom = idx(D.padrao[1]);
    const W = 640, H = 350;
    const cores = [S(1), S(2), S(3)];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "s", "Consumo sem o sistema", n, iSem)}
      ${ctlFaixa(id + "c", "Consumo com o sistema", n, iCom)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Fatura mensal de água e esgoto em função do consumo, em três estruturas tarifárias"></svg>
      ${legenda(D.curvas.map((c, k) => [cores[k], c.nome, k === 1 ? "trac" : "linha"]).concat([["var(--accent-soft)", "água economizada pelo sistema"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      if (iCom > iSem) { iCom = iSem; p.querySelector(`#${id}c`).value = iCom; }
      const cs = D.consumos.slice(0, n);
      const ymax = Math.max(...D.curvas.map(c => c.fatura[n - 1]));
      const ey = escala(0, ymax, 5);
      const A = plano({W, H, l: 58, r: 150, t: 34, b: 44, x: [0, 30], y: [0, ey.max], ym: ey.marcas, yf: v => "R$ " + fmt(v), yr: "parcela de água da fatura mensal",
        xm: [0, 5, 10, 15, 20, 25, 30], xf: v => v + " m³", xr: "consumo mensal de água potável"});
      let s = `<rect x="${A.X(cs[iCom])}" y="${A.Y(ey.max)}" width="${Math.max(0, A.X(cs[iSem]) - A.X(cs[iCom]))}" height="${A.Y(0) - A.Y(ey.max)}" style="fill:var(--accent-soft)"/>` + A.s;
      const rot = [];
      D.curvas.forEach((c, k) => {
        s += `<polyline points="${cs.map((x, i) => `${A.X(x)},${A.Y(c.fatura[i])}`).join(" ")}" style="fill:none;stroke:${cores[k]};stroke-width:${k === 1 ? 2.6 : 2.2}${k === 1 ? ";stroke-dasharray:7 5" : ""}"/>`;
        rot.push({y: A.Y(c.fatura[n - 1]), t: c.nome, c: cores[k]});
      });
      s += rotulosNaPonta(rot, A.X(30) + 8, A.Y(ey.max), A.Y(0));
      [[iSem, "sem o sistema"], [iCom, "com o sistema"]].forEach(([i, t], j) => {
        s += `<line class="g-ref" x1="${A.X(cs[i])}" x2="${A.X(cs[i])}" y1="${A.Y(ey.max)}" y2="${A.Y(0)}"/>`;
        s += `<text class="g-t" x="${A.X(cs[i]) + (j ? -5 : 5)}" y="${A.Y(ey.max) + 12}" text-anchor="${j ? "end" : "start"}">${t}</text>`;
        D.curvas.forEach((c, k) => { s += `<circle cx="${A.X(cs[i])}" cy="${A.Y(c.fatura[i])}" r="5" style="fill:${cores[k]};stroke:var(--surface);stroke-width:2"/>`; });
      });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, cs.map(x => A.X(x)), i => dicaHTML(`Consumo de ${fmt(cs[i], 2)} m³/mês · parcela de água`,
        D.curvas.map((c, k) => [cores[k], c.nome, reais(c.fatura[i], 2)])));
      p.querySelector(`#${id}s-o`).textContent = fmt(cs[iSem], 2) + " m³/mês";
      p.querySelector(`#${id}c-o`).textContent = fmt(cs[iCom], 2) + " m³/mês";
      const agua = cs[iSem] - cs[iCom];
      leit.innerHTML = `<p class="fi-sub">Água potável economizada: ${fmt(agua, 2)} m³/mês</p>
        <table class="fi-tabela"><thead><tr><th>Regime</th><th class="n">Sem</th><th class="n">Com</th><th class="n">Economia</th></tr></thead><tbody>
        ${D.curvas.map((c, k) => {
          const a = c.fatura[iSem], b = c.fatura[iCom], e = a - b;
          return `<tr><td><i style="--c:${cores[k]}"></i>${c.nome}<small>${c.exemplo}</small></td><td class="n">${reais(a)}</td><td class="n">${reais(b)}</td>
            <td class="n"><b>${reais(e)}</b><small>${a > 0 ? fmt(100 * e / a, 0) + "% da fatura" : ""}${agua > 0 ? " · " + reais(e / agua, 2) + "/m³" : ""}</small></td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">Acima de 10 m³, a franquia e a tarifa sem mínimo cobram o mesmo, e as duas linhas se sobrepõem (a franquia está tracejada); a diferença entre elas está toda abaixo de 10 m³. O que decide a economia não é o preço médio, e sim a faixa em que o consumo cai e o que fica fixo. Uma fatura que não se mexe com a economia de água torna inviável um sistema que, noutra cidade, se pagaria.</p>`;
    };
    p.querySelector(`#${id}s`).addEventListener("input", e => { iSem = +e.target.value; if (iCom > iSem) iCom = iSem; desenhar(); });
    p.querySelector(`#${id}c`).addEventListener("input", e => { iCom = Math.min(+e.target.value, iSem); desenhar(); });
    desenhar();
  }
};

/* ─── figura: o fluxo de caixa ─────────────────────────────────────────── */
FI["fig08_fluxo_de_caixa.png"] = {
  curto: "Quando o investimento se paga",
  pergunta: "Quando o investimento na cisterna se paga?",
  controles: "volume · material",
  experimente: "Com 4 m³, troque o concreto pelo polietileno: o VPL dobra, de R$ 2.745 para R$ 5.524. Em aço inoxidável, o investimento não se paga em 20 anos. Aumente o volume e veja o investimento crescer mais depressa que a economia.",
  fonte: TUTORIAL + " Recalque para caixa superior de 1.000 L, tarifa da CASAN, esgoto a 100% da água, taxa mínima de atratividade de 0,5% ao mês, horizonte de 20 anos, preços de referência do programa.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao[0]), mat = D.padrao[1];
    const W = 700, H = 370;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Volume da cisterna", D.volumes.length, vi)}
      ${ctlSeg(id + "m", "Material da cisterna", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Economia e custos de cada ano, e o saldo acumulado descontado ao longo de 20 anos"></svg>
      ${legenda([[S(4), "economia na fatura de água e esgoto"], [S(2), "investimento (ano 0) e custeio anual"], [S(3), "saldo acumulado descontado", "linha"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], c = D.casos[`${v}|${mat}`], n = c.economia.length;
      const lo = Math.min(-c.custo[0], ...c.acumulado), hi = Math.max(...c.economia, ...c.acumulado, 0);
      const ey = escala(lo, hi, 6);
      const A = plano({W, H, l: 70, r: 14, t: 34, b: 44, x: [-0.7, n - 0.3], y: [ey.min, ey.max], ym: ey.marcas, yf: v => menos(v), yr: "valor (R$)",
        xm: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20].filter(a => a < n), xr: "ano de operação"});
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
        s += `<text class="g-rot" x="${A.X(c.retorno) + (esq ? -6 : 6)}" y="${A.Y(ey.min) - 8}" text-anchor="${esq ? "end" : "start"}" style="fill:var(--ink)">se paga em ${fmt(c.retorno, 1)} anos</text>`;
      }
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      svg.innerHTML = s;
      pairar(svg, W, c.economia.map((_, a) => A.X(a)), a => dicaHTML(a ? `Ano ${a}` : "Ano 0 · instalação", [
        [S(4), "economia", reais(c.economia[a])], [S(2), a ? "custeio" : "investimento", reais(-c.custo[a])],
        [S(3), "saldo acumulado descontado", reais(c.acumulado[a])]]));
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const tma = (Math.pow(1 + D.tma / 100, 12) - 1) * 100;
      const nomeMat = D.materiais.find(m => m[0] === mat)[1];
      leit.innerHTML = `<p class="fi-sub">${fmt(v)} L em ${nomeMat.toLowerCase()}</p><div class="fi-n">
        ${cartao("Investimento inicial", reais(c.capex))}
        ${cartao("Economia líquida no 1º ano", reais(c.economia[1] - c.custo[1]))}
        ${cartao("VPL em 20 anos", reais(c.vpl), c.vpl >= 0 ? "✓ positivo" : "✕ negativo")}
        ${cartao("Tempo de retorno descontado", c.retorno ? fmt(c.retorno, 1) + " anos" : "mais de 20 anos")}
        ${cartao("TIR", c.tir === null ? "—" : fmt(c.tir, 1) + "% a.a.", `TMA: ${fmt(tma, 1)}% a.a.`)}
        ${cartao("Potencial de economia", fmt(c.potencial, 2) + "%")}</div>
        <p class="fi-sub">VPL em 20 anos, neste volume, por material</p>
        <table class="fi-tabela"><tbody>${D.materiais.map(([k, t]) => {
          const x = D.casos[`${v}|${k}`];
          return `<tr${k === mat ? ' class="atual"' : ""}><td>${t}</td><td class="n">${reais(x.vpl)}</td><td class="n">${x.retorno ? fmt(x.retorno, 1) + " anos" : "não se paga"}</td></tr>`;
        }).join("")}</tbody></table>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarSeg(p, id + "m", v => { mat = v; desenhar(); });
    desenhar();
  }
};

/* ─── figura: o carbono ao longo da vida útil ──────────────────────────── */
FI["fig06_carbono_no_tempo.png"] = {
  curto: "O retorno de carbono",
  pergunta: "Em quantos anos a cisterna devolve o carbono gasto para fabricá-la?",
  controles: "volume · material",
  experimente: "Com 4 m³, o polietileno e a fibra de vidro devolvem o carbono antes dos 20 anos; concreto e aço inoxidável, não. Diminua o volume: o carbono de fabricação cai, mas a água economizada também.",
  fonte: TUTORIAL + " Carbono incorporado de todo o sistema (cisterna, caixa superior, tubulações, motobomba e descarte) e crédito anual da água potável evitada, descontados o bombeamento e o tratamento. Positivo emite, negativo retira: a curva parte da dívida de fabricação e desce. Fatores de emissão da seção de avaliação de ciclo de vida.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), ativos = D.materiais.map(m => m[0]);
    const W = 640, H = 350;
    const corDoMat = k => S(D.materiais.findIndex(m => m[0] === k) + 1);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Volume da cisterna", D.volumes.length, vi)}
      ${ctlChips(id + "m", "Materiais", D.materiais.map(([k, t]) => [k, t, corDoMat(k)]), ativos)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} ${H}" role="img" aria-label="Saldo de carbono acumulado ao longo de 20 anos, por material da cisterna"></svg>
      ${legenda(D.materiais.map(([k, t]) => [corDoMat(k), t, "linha"]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const svg = p.querySelector(`#${id}g`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const v = D.volumes[vi], anos = D.anos;
      const casos = ativos.map(k => ({k, c: D.casos[`${v}|${k}`]}));
      // Emissoes liquidas: positivo emite, negativo retira. A curva parte do
      // carbono incorporado e desce com o credito anual da agua evitada.
      const lo = Math.min(0, ...casos.map(x => x.c[0] - x.c[1] * anos)), hi = Math.max(...casos.map(x => x.c[0]));
      const ey = escala(lo, hi, 6);
      const A = plano({W, H, l: 66, r: 130, t: 34, b: 44, x: [0, anos], y: [ey.min, ey.max], ym: ey.marcas, yr: "emissões líquidas acumuladas (kg CO₂e)",
        xm: [0, 5, 10, 15, 20], xr: "anos de operação"});
      let s = A.s;
      const rot = [];
      let cruzou = 0;
      casos.forEach(({k, c}) => {
        const cor = corDoMat(k), fim = c[0] - c[1] * anos;
        s += `<line x1="${A.X(0)}" y1="${A.Y(c[0])}" x2="${A.X(anos)}" y2="${A.Y(fim)}" style="stroke:${cor};stroke-width:2.4"/>`;
        if (c[4] !== null && c[4] <= anos) {
          const t = c[4], acima = cruzou++ % 2 === 0;
          s += `<circle cx="${A.X(t)}" cy="${A.Y(0)}" r="6" style="fill:${cor};stroke:var(--surface);stroke-width:2"/>`;
          s += `<text class="g-rot" x="${A.X(t)}" y="${A.Y(0) + (acima ? -12 : 22)}" text-anchor="middle" style="fill:${cor}">${fmt(t, 1)} anos</text>`;
        }
        rot.push({y: A.Y(fim), t: D.materiais.find(m => m[0] === k)[1], c: cor});
      });
      s += rotulosNaPonta(rot, A.X(anos) + 8, A.Y(ey.max), A.Y(ey.min));
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      svg.innerHTML = s;
      const xs = Array.from({length: anos + 1}, (_, a) => A.X(a));
      pairar(svg, W, xs, a => dicaHTML(`Ano ${a}`, casos.map(({k, c}) => [corDoMat(k), D.materiais.find(m => m[0] === k)[1], menos(c[1] * a - c[0]) + " kg CO₂e"])));
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const creditos = [...new Set(D.materiais.map(([k]) => D.casos[`${v}|${k}`][1]))];
      leit.innerHTML = `<p class="fi-sub">Cisterna de ${fmt(v)} L</p>
        <table class="fi-tabela"><thead><tr><th>Material</th><th class="n">Incorporado</th><th class="n">Retorno</th><th class="n">Em 20 anos</th></tr></thead><tbody>
        ${D.materiais.map(([k, t]) => {
          const c = D.casos[`${v}|${k}`], ret = c[4] === null ? Infinity : c[4];
          return `<tr${ativos.includes(k) ? "" : ' class="apagado"'}><td><i style="--c:${corDoMat(k)}"></i>${t}<small>cisterna de ${fmt(c[2])} kg</small></td>
            <td class="n">${fmt(c[0])} kg</td><td class="n">${ret <= anos ? fmt(ret, 1) + " anos" : "mais de 20 anos"}</td><td class="n">${menos(c[1] * anos - c[0])} kg</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">${creditos.length === 1
          ? `O crédito líquido da operação é de ${fmt(creditos[0], 1)} kg CO₂e por ano para os quatro materiais: a água economizada não depende do material. O que muda é o carbono de fabricação, e é ele que decide o retorno.`
          : "O crédito líquido da operação varia pouco entre os materiais; o carbono de fabricação é o que decide o retorno."}
          Valores em kg CO₂e; o saldo parte do carbono incorporado, com sinal negativo.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarChips(p, id + "m", a => { ativos = a; desenhar(); });
    desenhar();
  }
};

/* ─── figura: quatro capitais ──────────────────────────────────────────── */
FI["fig03_cidades.png"] = {
  curto: "Quatro capitais, a mesma casa",
  pergunta: "O que muda quando a mesma casa está noutra cidade?",
  controles: "cidades · volume",
  experimente: "Compare Brasília e Florianópolis: Brasília quase não tem chuva de maio a setembro e precisa de 15 m³ para chegar a 90% do seu potencial máximo; Florianópolis chega lá com 3 m³. Chover mais no ano, como em Manaus, não basta: conta como a chuva se distribui.",
  fonte: "A casa do tutorial (150 m² de cobertura, quatro moradores, 28% da demanda atendível por chuva), simulada com 30 anos da série de cada capital. Chuva mensal média da própria série.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao), ativos = D.cidades.map(c => c.chave);
    const W = 640;
    const corDe = k => S(D.cidades.findIndex(c => c.chave === k) + 1);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlChips(id + "c", "Cidades", D.cidades.map(c => [c.chave, c.nome, corDe(c.chave)]), ativos)}
      ${ctlFaixa(id + "v", "Volume da cisterna", D.volumes.length, vi)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}a" viewBox="0 0 ${W} 250" role="img" aria-label="Chuva média de cada mês nas cidades escolhidas"></svg>
      <svg id="${id}b" viewBox="0 0 ${W} 290" role="img" aria-label="Potencial de economia de água potável em função do volume da cisterna, por cidade"></svg>
      ${legenda(D.cidades.map(c => [corDe(c.chave), c.nome, "linha"]).concat([["var(--ink3)", "teto: fração atendível de 28%", "trac"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const sa = p.querySelector(`#${id}a`), sb = p.querySelector(`#${id}b`), leit = p.querySelector(`#${id}l`);
    const desenhar = () => {
      const cs = D.cidades.filter(c => ativos.includes(c.chave)), v = D.volumes[vi];
      const em = escala(0, Math.max(...cs.flatMap(c => c.mensal)), 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 30, x: [0.5, 12.5], y: [0, em.max], ym: em.marcas, yr: "chuva média do mês (mm)", painel: "(a)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xf: m => MESES[m - 1]});
      let s = A.s;
      cs.forEach(c => {
        s += `<polyline points="${c.mensal.map((x, m) => `${A.X(m + 1)},${A.Y(x)}`).join(" ")}" style="fill:none;stroke:${corDe(c.chave)};stroke-width:2.2"/>`;
        c.mensal.forEach((x, m) => { s += `<circle cx="${A.X(m + 1)}" cy="${A.Y(x)}" r="3.5" style="fill:${corDe(c.chave)};stroke:var(--surface);stroke-width:1.5"/>`; });
      });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(em.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      sa.innerHTML = s;
      pairar(sa, W, MESES.map((_, m) => A.X(m + 1)), m => dicaHTML(`Chuva média de ${MESES[m]}`, cs.map(c => [corDe(c.chave), c.nome, fmt(c.mensal[m]) + " mm"])));

      const teto = D.fracao * 100;
      const B = plano({W, H: 290, l: 58, r: 100, t: 34, b: 44, x: [0, 20000], y: [0, 30], ym: [0, 5, 10, 15, 20, 25, 30], yf: v => v + "%", yr: "potencial de economia de água potável", painel: "(b)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "volume da cisterna"});
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
      leit.innerHTML = `<p class="fi-sub">Cisterna de ${fmt(v)} L</p>
        <table class="fi-tabela"><thead><tr><th>Cidade</th><th class="n">Chuva anual</th><th class="n">Potencial</th><th class="n">90% do máximo com</th></tr></thead><tbody>
        ${D.cidades.map(c => {
          const max = c.potencial[c.potencial.length - 1];
          const k90 = c.potencial.findIndex(q => q >= 0.9 * max);
          return `<tr${ativos.includes(c.chave) ? "" : ' class="apagado"'}><td><i style="--c:${corDe(c.chave)}"></i>${c.nome}<small>chove em ${fmt(c.dias_chuva, 0)}% dos dias</small></td>
            <td class="n">${fmt(c.anual)} mm</td><td class="n"><b>${fmt(c.potencial[vi], 2)}%</b></td><td class="n">${fmt(D.volumes[k90] / 1000)} m³</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">«90% do máximo» é o menor volume que alcança nove décimos do potencial obtido com 20 m³. Quanto mais longa a estação seca, maior a cisterna para o mesmo resultado.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenhar(); });
    ligarChips(p, id + "c", a => { ativos = a; desenhar(); });
    desenhar();
  }
};

/* ─── figura: a curva de retorno e o volume ideal ──────────────────────── */
FI["fig02_curva_de_retorno.png"] = {
  curto: "A curva de retorno e o volume ideal",
  pergunta: "Até onde vale aumentar a cisterna?",
  controles: "fração atendível · limiar · passo da grade",
  experimente: "Com 28% e o limiar de 1 %/m³, o volume ideal é 4.000 L. Troque o passo da grade para 500 L e ele vira 3.500 L; para 2.000 L, vira 6.000 L. Nada no projeto mudou: é o efeito do passo que a seção discute. Suba o limiar para 5 %/m³, o valor com que o programa abre, e o ideal cai para 2.000 L.",
  fonte: TUTORIAL + " Uma simulação por volume, de 0 a 20.000 L em passos de 500 L, para cada fração atendível de 10% a 60%.",
  montar(p, D, id) {
    let fi = D.fracoes.findIndex(f => Math.abs(f - 0.28) < 1e-6), passo = 1000, lim = 1, vsel = 4000;
    const W = 640, LIMIARES = [0.5, 1, 2, 5];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "f", "Fração da demanda atendível por chuva", D.fracoes.length, fi)}
      ${ctlSeg(id + "q", "Limiar de ganho marginal", LIMIARES.map(x => [x, fmt(x, x < 1 ? 1 : 0) + " %/m³"]), lim)}
      ${ctlSeg(id + "p", "Passo da grade", [[500, "500 L"], [1000, "1.000 L"], [2000, "2.000 L"]], passo)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}a" viewBox="0 0 ${W} 280" role="img" aria-label="Potencial de economia em função do volume da cisterna, com o volume ideal marcado; clique para escolher um volume"></svg>
      <svg id="${id}b" viewBox="0 0 ${W} 250" role="img" aria-label="Ganho marginal de potencial por metro cúbico, em escala logarítmica, com o limiar"></svg>
      ${legenda([[S(1), "potencial de economia", "linha"], [S(2), "ganho marginal por m³", "linha"], ["var(--ink3)", "teto e limiar", "trac"], [S(4), "volume ideal", "linha"]])}
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
      const A = plano({W, H: 280, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [0, ey.max], ym: ey.marcas, yf: v => fmt(v) + "%", yr: "potencial de economia de água potável", painel: "(a)",
        xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "volume da cisterna"});
      let s = A.s + `<line class="g-ref" x1="${A.X(0)}" x2="${A.X(20000)}" y1="${A.Y(teto)}" y2="${A.Y(teto)}"/>`;
      s += `<text class="g-t" x="${A.X(20000)}" y="${A.Y(teto) - 6}" text-anchor="end">teto: fração atendível de ${fmt(teto)}%</text>`;
      s += `<line x1="${A.X(ideal)}" x2="${A.X(ideal)}" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="stroke:${S(4)};stroke-width:1.6;stroke-dasharray:2 3"/>`;
      s += `<text class="g-rot" x="${A.X(ideal) + 7}" y="${A.Y(ey.max * 0.2)}" style="fill:${S(4)}">volume ideal: ${fmt(ideal)} L</text>`;
      s += `<polyline points="${vol.map((v, i) => `${A.X(v)},${A.Y(pot[i])}`).join(" ")}" style="fill:none;stroke:${S(1)};stroke-width:2.2"/>`;
      vol.forEach((v, i) => { s += `<circle cx="${A.X(v)}" cy="${A.Y(pot[i])}" r="${v === vsel ? 6.5 : 3}" style="fill:${S(1)};stroke:var(--surface);stroke-width:${v === vsel ? 2 : 1}"/>`; });
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(0)}" style="display:none"/>`;
      sa.innerHTML = s;
      const escolher = i => { vsel = vol[i]; desenhar(); };
      pairar(sa, W, vol.map(v => A.X(v)), i => dicaHTML(`${fmt(vol[i])} L`, [[S(1), "potencial", fmt(pot[i], 2) + "%"],
        [S(2), "ganho do último passo", ganho[i] === null ? "—" : fmt(ganho[i], 2) + " %/m³"]]), escolher);

      const LOGMIN = -3, LOGMAX = 2;
      const B = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [0, 20000], y: [LOGMIN, LOGMAX], ym: [-3, -2, -1, 0, 1, 2], yf: e => fmt(Math.pow(10, e), Math.max(0, -e)),
        yr: "ganho marginal (%/m³, escala logarítmica)", painel: "(b)", xm: [0, 5000, 10000, 15000, 20000], xf: x => fmt(x / 1000) + " m³", xr: "volume da cisterna"});
      const LY = g => B.Y(Math.max(LOGMIN, Math.min(LOGMAX, Math.log10(Math.max(g, 1e-3)))));
      let t = B.s + `<line class="g-ref" x1="${B.X(0)}" x2="${B.X(20000)}" y1="${LY(lim)}" y2="${LY(lim)}"/>`;
      t += `<text class="g-t" x="${B.X(20000)}" y="${LY(lim) - 6}" text-anchor="end">limiar: ${fmt(lim, lim < 1 ? 1 : 0)} %/m³</text>`;
      t += `<line x1="${B.X(ideal)}" x2="${B.X(ideal)}" y1="${B.Y(LOGMAX)}" y2="${B.Y(LOGMIN)}" style="stroke:${S(4)};stroke-width:1.6;stroke-dasharray:2 3"/>`;
      // O potencial vem com duas casas; abaixo disso o ganho é zero e não cabe no log.
      const gp = vol.map((v, i) => [v, ganho[i]]).filter(([, g]) => g !== null && g > 0);
      const zero = vol.find((v, i) => i > 0 && ganho[i] <= 0);
      if (zero !== undefined) t += `<text class="g-t" x="${B.X(zero)}" y="${B.Y(LOGMIN) - 8}">ganho abaixo de 0,01 ponto a partir de ${fmt(zero / 1000)} m³</text>`;
      t += `<polyline points="${gp.map(([v, g]) => `${B.X(v)},${LY(g)}`).join(" ")}" style="fill:none;stroke:${S(2)};stroke-width:2"/>`;
      gp.forEach(([v, g]) => { t += `<circle cx="${B.X(v)}" cy="${LY(g)}" r="${v === ideal ? 6 : 3}" style="fill:${v === ideal ? S(4) : S(2)};stroke:var(--surface);stroke-width:1.5"/>`; });
      sb.innerHTML = t;
      pairar(sb, W, vol.map(v => B.X(v)), i => dicaHTML(`${fmt(vol[i])} L`, [[S(2), "ganho marginal", ganho[i] === null ? "—" : fmt(ganho[i], 3) + " %/m³"]]), escolher);

      p.querySelector(`#${id}f-o`).textContent = fmt(teto) + "%";
      leit.innerHTML = `<p class="fi-sub">Volume ideal</p><div class="fi-n">
        ${cartao("Pelo critério do ganho marginal", fmt(ideal) + " L", noLimite ? "limite da grade" : "")}
        ${cartao("Potencial no volume ideal", fmt(pot[ii], 2) + "%", `de ${fmt(teto)}%`)}</div>
        <p class="fi-sub">Volume em destaque: ${fmt(vsel)} L <span style="text-transform:none;letter-spacing:0;font-weight:400">(clique no gráfico para trocar)</span></p><div class="fi-n">
        ${cartao("Potencial de economia", fmt(ls[0], 2) + "%")}
        ${cartao("Ganho do último passo", ganho[is] === null ? "—" : fmt(ganho[is], 2), "%/m³")}
        ${cartao("Dias de atendimento pleno", fmt(ls[1], 1) + "%")}
        ${cartao("Extravasamento médio", fmt(ls[2]), "L/dia")}</div>
        <p class="fi-nota">O volume ideal é o menor volume da grade cujo ganho por metro cúbico, em relação ao volume anterior da grade, já caiu abaixo do limiar. ${noLimite ? "Nesta combinação, nenhum volume até 20.000 L cruza o limiar, e o programa adota o maior volume da grade e avisa no relatório." : "O critério é hidráulico: não olha custo nem carbono."}</p>`;
    };
    p.querySelector(`#${id}f`).addEventListener("input", e => { fi = +e.target.value; desenhar(); });
    ligarSeg(p, id + "q", v => { lim = +v; desenhar(); });
    ligarSeg(p, id + "p", v => { passo = +v; desenhar(); });
    desenhar();
  }
};

/* ─── o TOPSIS, com os pesos na mão do leitor ──────────────────────────── */

/** O mesmo cálculo de netuno/core/topsis.py: desloca pela coluna, normaliza
 *  pelo vetor, pondera, mede a distância ao ideal e ao anti-ideal. */
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
  // Empate resolvido pelo menor volume, como no programa.
  const ordem = escores.map((s, i) => i).sort((a, b) => escores[b] - escores[a] || volumes[a] - volumes[b]);
  const postos = new Array(n);
  ordem.forEach((i, k) => { postos[i] = k + 1; });
  // Proximidade por critério: 1 é o ótimo observado na coluna.
  const prox = matriz.map(l => l.map((x, j) => {
    const faixa = max[j] - min[j];
    if (faixa <= 0) return 1;
    return 1 - (beneficio[j] ? (max[j] - x) / faixa : (x - min[j]) / faixa);
  }));
  return {escores, postos, proximidade: prox, pesos: w};
}

FI["fig51_programa_topsis.png"] = {
  curto: "A decisão multicritério",
  pergunta: "Que volume o multicritério elege, e com que pesos?",
  controles: "peso técnico · econômico · ambiental",
  experimente: "Com os três eixos iguais, como o programa abre, vence a cisterna de 4.000 L. Leve o peso ambiental ao máximo e veja a escolha subir de volume; leve o econômico e ela desce. O critério que muda a decisão fica visível nas barras de proximidade.",
  fonte: "Os sete critérios do programa, calculados para sete volumes candidatos com o projeto do tutorial e cisterna de polietileno. O escore é calculado na página pela mesma conta de netuno/core/topsis.py, conferida contra o programa por teste automático.",
  montar(p, D, id) {
    let pesos = [1 / 3, 1 / 3, 1 / 3], sete = false, pc = null, sel = D.volumes.indexOf(4000);
    const W = 640, EIXOS = D.eixos, benef = D.criterios.map(c => c.beneficio);
    const desenha = () => {
      const w7 = sete ? pc.slice() : [pesos[0] / 2, pesos[0] / 2, pesos[1] / 3, pesos[1] / 3, pesos[1] / 3, pesos[2] / 2, pesos[2] / 2];
      const Res = topsisEscores(D.matriz, w7, benef, D.volumes);
      const vencedor = Res.postos.indexOf(1);
      const ey = escala(0, Math.max(...Res.escores) * 1.12, 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: v => fmt(v, 2), yr: "escore TOPSIS (1 = ideal)", painel: "(a)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "volume candidato"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.55;
      Res.escores.forEach((x, i) => {
        const cor = i === vencedor ? "var(--accent)" : "var(--grid)";
        const contorno = i === sel ? ";stroke:var(--ink2);stroke-width:2" : "";
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${A.Y(0) - A.Y(x)}" rx="3" style="fill:${cor}${contorno}"/>`;
        s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(x) - 6}" text-anchor="middle">${fmt(x, 3)}</text>`;
      });
      s += `<text class="g-rot" x="${A.X(vencedor)}" y="${A.Y(ey.max) + 2}" text-anchor="middle" style="fill:var(--accent)">eleito</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, [[S(1), "escore", fmt(Res.escores[i], 4)], ["", "posição", `${Res.postos[i]}º`]]),
        i => { sel = i; desenha(); });

      const B = plano({W, H: 250, l: 268, r: 60, t: 34, b: 36, x: [0, 1], y: [D.criterios.length - 0.4, -0.6],
        xm: [0, 0.25, 0.5, 0.75, 1], xf: v => fmt(v * 100) + "%", xr: "proximidade do ótimo observado", painel: "(b)"});
      let t = B.s;
      D.criterios.forEach((c, j) => {
        const v = Res.proximidade[sel][j], y = B.Y(j), h = 16;
        t += `<rect x="${B.X(0)}" y="${y - h / 2}" width="${B.X(1) - B.X(0)}" height="${h}" rx="3" style="fill:var(--grid)"/>`;
        t += `<rect x="${B.X(0)}" y="${y - h / 2}" width="${Math.max(2, B.X(v) - B.X(0))}" height="${h}" rx="3" style="fill:${S(c.eixo === "technical" ? 3 : c.eixo === "economic" ? 2 : 4)}"/>`;
        t += `<text class="g-t" x="${B.X(0) - 8}" y="${y + 4}" text-anchor="end">${c.rotulo} · peso ${fmt(Res.pesos[j] * 100, 1)}%</text>`;
        t += `<text class="g-t" x="${B.X(1) + 8}" y="${y + 4}">${fmt(v * 100, 0)}%</text>`;
      });
      p.querySelector(`#${id}h`).innerHTML = t;

      EIXOS.forEach(([k], i) => { const o = p.querySelector(`#${id}${k}-o`); if (o) o.textContent = fmt(pesos[i] * 100, 0) + "%"; });
      if (sete) D.criterios.forEach((c, j) => { const o = p.querySelector(`#${id}c${j}-o`); if (o) o.textContent = fmt(Res.pesos[j] * 100, 1) + "%"; });
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Eleito: ${fmt(D.volumes[vencedor])} L</p>
        <div class="fi-n">${cartao("Escore do eleito", fmt(Res.escores[vencedor], 3))}
        ${cartao("Em destaque", fmt(D.volumes[sel]) + " L", `${Res.postos[sel]}º lugar, escore ${fmt(Res.escores[sel], 3)}`)}</div>
        <p class="fi-sub">Os sete critérios do volume em destaque</p>
        <table class="fi-tabela"><tbody>${D.criterios.map((c, j) => `<tr><td>${c.rotulo}<small>${c.beneficio ? "maior é melhor" : "menor é melhor"}</small></td>
          <td class="n">${c.unidade === "R$" ? reais(D.matriz[sel][j]) : menos(D.matriz[sel][j], c.casas) + " " + c.unidade}</td></tr>`).join("")}</tbody></table>
        <p class="fi-nota">O escore mede a distância a duas referências: a alternativa ideal, feita do melhor valor de cada critério, e a anti-ideal, feita do pior. ${D.sem_retorno.some(Boolean) ? "Os volumes que não se pagam no horizonte recebem a penalidade de retorno que o programa aplica, e não ficam de fora da conta. " : ""}Pesos iguais nos três eixos reproduzem o resultado do programa.</p>`;
    };
    p.innerHTML = `<div class="fi-ctls">
      ${EIXOS.map(([k, r], i) => ctlFaixa(id + k, "Peso " + r.toLowerCase(), 101, Math.round(pesos[i] * 100))).join("")}
      <div class="fi-ctl"><span class="fi-rot">&nbsp;</span><div class="linha-ctl"><button type="button" class="bt" id="${id}igual">Pesos iguais</button><button type="button" class="bt" id="${id}sete">Abrir nos sete critérios</button></div></div>
    </div><div class="fi-ctls" id="${id}s7" hidden></div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 250" role="img" aria-label="Escore TOPSIS de cada volume candidato"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 250" role="img" aria-label="Proximidade do volume em destaque ao ótimo observado em cada critério"></svg>
      ${legenda([["var(--accent)", "(a) volume eleito"], ["var(--ink2)", "(a) contorno: volume em destaque"], [S(3), "(b) eixo técnico"], [S(2), "(b) eixo econômico"], [S(4), "(b) eixo ambiental"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const ajustar = () => {
      const soma = pesos.reduce((a, b) => a + b, 0);
      if (soma <= 0) pesos = [1 / 3, 1 / 3, 1 / 3];
      else pesos = pesos.map(x => x / soma);
    };
    EIXOS.forEach(([k], i) => p.querySelector(`#${id}${k}`).addEventListener("input", e => {
      pesos = pesos.map((x, j) => j === i ? +e.target.value / 100 : x);
      if (pesos.reduce((a, b) => a + b, 0) <= 0) pesos[i] = 0.01;
      desenha();
    }));
    p.querySelector(`#${id}igual`).addEventListener("click", () => {
      pesos = [1 / 3, 1 / 3, 1 / 3];
      EIXOS.forEach(([k], i) => { p.querySelector(`#${id}${k}`).value = 33; });
      if (sete) { pc = [1 / 6, 1 / 6, 1 / 9, 1 / 9, 1 / 9, 1 / 6, 1 / 6]; D.criterios.forEach((c, j) => { p.querySelector(`#${id}c${j}`).value = Math.round(pc[j] * 100); }); }
      desenha();
    });
    p.querySelector(`#${id}sete`).addEventListener("click", e => {
      sete = !sete;
      const caixa = p.querySelector(`#${id}s7`);
      if (sete && !pc) pc = [1 / 6, 1 / 6, 1 / 9, 1 / 9, 1 / 9, 1 / 6, 1 / 6];
      if (sete) {
        caixa.innerHTML = D.criterios.map((c, j) => ctlFaixa(id + "c" + j, c.rotulo, 101, Math.round(pc[j] * 100))).join("");
        D.criterios.forEach((c, j) => p.querySelector(`#${id}c${j}`).addEventListener("input", ev => {
          pc[j] = +ev.target.value / 100;
          if (pc.reduce((a, b) => a + b, 0) <= 0) pc[j] = 0.01;
          desenha();
        }));
      }
      caixa.hidden = !sete;
      e.target.textContent = sete ? "Voltar aos três eixos" : "Abrir nos sete critérios";
      desenha();
    });
    ajustar();
    desenha();
  }
};

/* ─── a aceitabilidade estocástica (SMAA) ──────────────────────────────── */
FI["fig23_smaa.png"] = {
  curto: "A aceitabilidade estocástica",
  pergunta: "E se ninguém souber dizer os pesos: que volume vence com mais frequência?",
  controles: "método de ranqueamento · estratégia do VIKOR",
  experimente: "Troque o VIKOR pelo TOPSIS e veja se o vencedor resiste à troca de método. Mova a estratégia do VIKOR do consenso (0,5) para o arrependimento mínimo (0) e observe qual volume ganha estabilidade.",
  fonte: "SMAA do próprio programa: 5.000 sorteios de pesos numa distribuição de Dirichlet uniforme sobre os sete critérios, semente 42, com os mesmos sete candidatos da decisão multicritério.",
  montar(p, D, id) {
    let motor = D.padrao[0], v = D.padrao[1], sel = 3;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "m", "Método de ranqueamento", [["vikor", "SMAA-VIKOR"], ["topsis", "SMAA-TOPSIS"]], motor)}
      ${ctlSeg(id + "v", "Estratégia do VIKOR", [[0, "arrependimento (0)"], [0.5, "consenso (0,5)"], [1, "utilidade (1)"]], v)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 250" role="img" aria-label="Aceitabilidade de primeiro lugar de cada volume; clique para escolher um volume"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 250" role="img" aria-label="Distribuição das posições de cada volume nos 5.000 sorteios"></svg>
      ${legenda([[S(4), "1º lugar"], [S(1), "2º lugar; as posições seguintes vêm em tons cada vez mais claros"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const chave = motor === "topsis" ? "topsis|0.5" : `vikor|${v}`;
      const C = D.casos[chave] || D.casos["vikor|0.5"];
      const melhor = C.primeiro.indexOf(Math.max(...C.primeiro));
      const ey = escala(0, Math.max(...C.primeiro) * 1.15, 4);
      const A = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x) + "%", yr: "aceitabilidade de 1º lugar", painel: "(a)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "volume candidato"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.55;
      C.primeiro.forEach((x, i) => {
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(x))}" rx="3" style="fill:${i === melhor ? S(4) : i === sel ? S(1) : "var(--grid)"}"/>`;
        if (x > 0.5) s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(x) - 6}" text-anchor="middle">${fmt(x, 1)}%</text>`;
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, [[S(1), "vence em", fmt(C.primeiro[i], 2) + "% dos sorteios"]]),
        i => { sel = i; desenha(); });

      const B = plano({W, H: 250, l: 58, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, 100], ym: [0, 25, 50, 75, 100],
        yf: x => fmt(x) + "%", yr: "posições nos 5.000 sorteios", painel: "(b)",
        xm: D.volumes.map((_, i) => i), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "volume candidato"});
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
      t += `<text class="g-t" x="${B.X(D.volumes.length - 1) + 4}" y="${B.Y(96)}">1º lugar em verde</text>`;
      p.querySelector(`#${id}h`).innerHTML = t;
      pairar(p.querySelector(`#${id}h`), W, D.volumes.map((_, i) => B.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, C.aceitabilidade[i].map((x, pos) => [pos === 0 ? S(4) : S(1), `${pos + 1}º lugar`, fmt(x, 1) + "%"]).filter((_, pos) => C.aceitabilidade[i][pos] > 0)),
        i => { sel = i; desenha(); });

      const central = C.central[sel], soma = central.reduce((a, b) => a + b, 0);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Mais aceito: ${fmt(D.volumes[melhor])} L, em ${fmt(C.primeiro[melhor], 1)}% dos sorteios</p>
        <div class="fi-n">${cartao("Em destaque", fmt(D.volumes[sel]) + " L", `vence em ${fmt(C.primeiro[sel], 2)}% dos sorteios`)}
        ${cartao("Fator de confiança", C.confianca[sel] >= 1 ? "✓ confirma" : "✕ não confirma", "com o próprio vetor central")}</div>
        ${soma > 0 ? `<p class="fi-sub">Vetor central de pesos que elege ${fmt(D.volumes[sel])} L</p>
        <table class="fi-tabela"><tbody>${DADOS.interativas["fig51_programa_topsis.png"].criterios.map((c, j) =>
          `<tr><td>${c.rotulo}</td><td class="n">${fmt(central[j] * 100, 1)}%</td></tr>`).join("")}</tbody></table>`
        : `<p class="fi-nota">Este volume não venceu nenhum dos ${fmt(D.sorteios)} sorteios, e por isso não tem vetor central de pesos.</p>`}
        <p class="fi-nota">Cada sorteio tira um vetor de pesos ao acaso e ranqueia os volumes. A aceitabilidade de primeiro lugar é a fração dos sorteios em que o volume venceu; o vetor central é a média dos pesos que o elegeram. É a pergunta invertida: em vez de «qual volume estes pesos elegem», «que pesos elegeriam este volume».</p>`;
    };
    ligarSeg(p, id + "m", x => { motor = x; desenha(); });
    ligarSeg(p, id + "v", x => { v = +x; desenha(); });
    desenha();
  }
};

/* ─── os índices pluviométricos ────────────────────────────────────────── */
FI["fig16_indices.png"] = {
  curto: "Os índices pluviométricos, ano a ano",
  pergunta: "O que os nove índices dizem sobre a chuva de cada cidade?",
  controles: "cidade · índice",
  experimente: "Escolha «Maior estiagem» e compare Brasília com Florianópolis: a maior sequência seca de Brasília passa de 100 dias em vários anos, e é ela, não a chuva total, que obriga a cisterna maior. Depois veja o índice de sazonalidade das quatro cidades.",
  fonte: "Índices calculados pelo próprio programa (netuno/core/calculator.py) sobre 30 anos da série de cada capital, com o mesmo período-base de percentil que o programa usa.",
  montar(p, D, id) {
    let cidade = D.padrao[0], indice = D.padrao[1];
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "Cidade", D.cidades.map(c => [c.chave, c.nome]), cidade)}
      <div class="fi-ctl largo"><label class="fi-rot" for="${id}i">Índice</label>
      <select id="${id}i">${D.indices.map(x => `<option value="${x.chave}"${x.chave === indice ? " selected" : ""}>${x.nome} (${x.chave.replace("Seasonality_Index", "SI")})</option>`).join("")}</select></div>
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 260" role="img" aria-label="Valor do índice em cada ano da série"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 190" role="img" aria-label="Média do índice nas quatro capitais"></svg>
      ${legenda([[S(1), "valor do ano"], ["var(--ink3)", "média dos 30 anos", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const c = D.cidades.find(x => x.chave === cidade), meta = D.indices.find(x => x.chave === indice);
      const vals = c.valores[indice], media = vals.reduce((a, b) => a + b, 0) / vals.length;
      const ey = escala(0, Math.max(...vals) * 1.1, 4);
      const A = plano({W, H: 260, l: 62, r: 14, t: 34, b: 44, x: [-0.6, vals.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x, meta.casas > 1 ? 2 : 0), yr: `${meta.nome} (${meta.unidade})`, painel: "(a)",
        xm: c.anos.map((_, i) => i).filter(i => i % 5 === 0), xf: i => c.anos[i], xr: "ano"});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.7;
      const maior = vals.indexOf(Math.max(...vals)), menor = vals.indexOf(Math.min(...vals));
      vals.forEach((x, i) => {
        s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(x)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(x))}" rx="2" style="fill:${S(1)};opacity:${i === maior || i === menor ? 1 : 0.72}"/>`;
      });
      s += `<line class="g-ref" x1="${A.X(-0.6)}" x2="${A.X(vals.length - 0.4)}" y1="${A.Y(media)}" y2="${A.Y(media)}"/>`;
      s += `<text class="g-t" x="${A.X(-0.5)}" y="${A.Y(media) - 6}">média dos 30 anos: ${fmt(media, meta.casas)} ${meta.unidade === "—" ? "" : meta.unidade}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, vals.map((_, i) => A.X(i)),
        i => dicaHTML(`${c.nome}, ${c.anos[i]}`, [[S(1), meta.nome, fmt(vals[i], meta.casas) + " " + (meta.unidade === "—" ? "" : meta.unidade)]]));

      const medias = D.cidades.map(x => x.valores[indice].reduce((a, b) => a + b, 0) / x.valores[indice].length);
      const ry = escala(0, Math.max(...medias) * 1.15, 3);
      const B = plano({W, H: 190, l: 62, r: 14, t: 34, b: 40, x: [-0.6, D.cidades.length - 0.4], y: [0, ry.max], ym: ry.marcas,
        yf: x => fmt(x, meta.casas > 1 ? 2 : 0), yr: `média de 30 anos (${meta.unidade})`, painel: "(b)",
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
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${meta.nome} em ${c.nome}</p>
        <div class="fi-n">${cartao("Média dos 30 anos", fmt(media, meta.casas), meta.unidade === "—" ? "" : meta.unidade)}
        ${cartao("Mediana", fmt(mediana, meta.casas), meta.unidade === "—" ? "" : meta.unidade)}
        ${cartao("Maior valor", fmt(vals[maior], meta.casas), "em " + c.anos[maior])}
        ${cartao("Menor valor", fmt(vals[menor], meta.casas), "em " + c.anos[menor])}</div>
        <p class="fi-nota"><b>${meta.chave.replace("Seasonality_Index", "SI")}.</b> ${meta.texto}</p>`;
    };
    ligarSeg(p, id + "c", x => { cidade = x; desenha(); });
    p.querySelector(`#${id}i`).addEventListener("change", e => { indice = e.target.value; desenha(); });
    desenha();
  }
};

/* ─── o investimento aberto por rubrica ────────────────────────────────── */
FI["fig21_investimento.png"] = {
  curto: "De que é feito o investimento",
  pergunta: "De que é feito o investimento inicial, e o que muda com o volume?",
  controles: "volume · material",
  experimente: "Dobre o volume de 4 para 8 m³: o investimento total sobe bem menos que o dobro, porque só o reservatório inferior cresce. Trocar o material mexe só nessa parcela, e é por isso que o concreto, mais caro por litro, pesa mais nas cisternas grandes.",
  fonte: "As sete parcelas que o programa soma no investimento inicial, com os preços de referência dele e os custos declarados no tutorial. A soma reproduz, para cada volume e material, o mesmo investimento que a análise econômica usa no fluxo de caixa.",
  montar(p, D, id) {
    let vi = D.volumes.indexOf(D.padrao[0]), mat = D.padrao[1];
    const W = 640, cores = [1, 2, 3, 4, 5, 6, 7].map(R);
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "v", "Volume da cisterna", D.volumes.length, vi)}
      ${ctlSeg(id + "m", "Material da cisterna", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Investimento inicial aberto por rubrica, em cada volume"></svg>
      ${legenda(D.rubricas.map((r, i) => [cores[i], r]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const v = D.volumes[vi];
      const totais = D.volumes.map(x => D.casos[`${x}|${mat}`].reduce((a, b) => a + b, 0));
      const ey = escala(0, Math.max(...totais) * 1.08, 5);
      const A = plano({W, H: 300, l: 70, r: 14, t: 34, b: 44, x: [-0.6, D.volumes.length - 0.4], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x), yr: "investimento inicial (R$)",
        xm: D.volumes.map((_, i) => i).filter(i => i % 2 === 0), xf: i => fmt(D.volumes[i] / 1000) + " m³", xr: "volume da cisterna"});
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
        if (i === vi) s += `<text class="g-rot" x="${A.X(i)}" y="${A.Y(base) - 8}" text-anchor="middle" style="fill:var(--ink)">${reais(base)}</text>`;
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map((_, i) => A.X(i)),
        i => dicaHTML(`${fmt(D.volumes[i])} L`, D.casos[`${D.volumes[i]}|${mat}`].map((x, j) => [cores[j], D.rubricas[j].split(" (")[0], reais(x)])
          .concat([["", "total", reais(totais[i])]])),
        i => { vi = i; p.querySelector(`#${id}v`).value = i; desenha(); });
      p.querySelector(`#${id}v-o`).textContent = fmt(v) + " L";
      const partes = D.casos[`${v}|${mat}`], total = partes.reduce((a, b) => a + b, 0);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${fmt(v)} L em ${D.materiais.find(m => m[0] === mat)[1].toLowerCase()}</p>
        <table class="fi-tabela"><tbody>${D.rubricas.map((r, j) => `<tr><td><i style="--c:${cores[j]}"></i>${r}</td><td class="n">${reais(partes[j])}</td><td class="n">${fmt(100 * partes[j] / total, 0)}%</td></tr>`).join("")}
        <tr class="tot"><td>Total</td><td class="n">${reais(total)}</td><td class="n">100%</td></tr></tbody></table>
        <div class="fi-n">${cartao("Custo por litro de cisterna", reais(partes[0] / v, 2), "só o reservatório")}
        ${cartao("Parcela que não depende do volume", fmt(100 * (total - partes[0]) / total, 0) + "%")}</div>
        <p class="fi-nota">A soma das sete rubricas é o investimento inicial que a análise econômica usa${D.fecha_com_o_capex ? ", conferido a cada montagem do site" : ""}. A linha de tratamento entra pelo que acrescenta além da verba de filtração já embutida nos acessórios, para o filtro não ser contado duas vezes.</p>`;
    };
    p.querySelector(`#${id}v`).addEventListener("input", e => { vi = +e.target.value; desenha(); });
    ligarSeg(p, id + "m", x => { mat = x; desenha(); });
    desenha();
  }
};

/* ─── a fatura aberta em parcelas ──────────────────────────────────────── */
FI["fig07_fatura.png"] = {
  curto: "A fatura aberta em parcelas",
  pergunta: "De que é feita a conta de água, e que parte o sistema pluvial consegue mexer?",
  controles: "consumo sem e com o sistema · esgoto",
  experimente: "Baixe o consumo com o sistema: a tarifa de disponibilidade não se move, e só a faixa mais cara encolhe. Zere o percentual de esgoto e veja a economia mensal cair pela metade — em Florianópolis o esgoto iguala a água, e é ele que torna o sistema viável.",
  fonte: "Tarifa da CASAN vigente no tutorial, aberta nas parcelas que o programa calcula: disponibilidade, faixas de consumo e esgoto como percentual da parcela de água. O ponto de partida é o consumo médio do projeto do tutorial.",
  montar(p, D, id) {
    const n = D.consumos.length, idx = v => Math.round(v / 0.25);
    let iSem = idx(D.padrao[0]), iCom = idx(D.padrao[1]), esgoto = 100;
    const W = 560, cores = [S(2), R(3), R(5), R(6), R(7), S(4)];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "s", "Consumo sem o sistema", n, iSem)}
      ${ctlFaixa(id + "c", "Consumo com o sistema", n, iCom)}
      ${ctlSeg(id + "e", "Esgoto", [[0, "sem esgoto"], [40, "40%"], [80, "80%"], [100, "100%"]], esgoto)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" class="estreito" viewBox="0 0 ${W} 330" role="img" aria-label="A fatura mensal aberta em parcelas, sem e com o sistema pluvial"></svg>
      <div class="fi-leg" id="${id}leg"></div>
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      if (iCom > iSem) { iCom = iSem; p.querySelector(`#${id}c`).value = iCom; }
      const monta = i => {
        const linha = D.parcelas[i].slice();
        linha[linha.length - 1] = linha[linha.length - 1] * esgoto / 100;   // esgoto sobre a água
        return linha;
      };
      const casos = [["sem o sistema", monta(iSem), D.consumos[iSem]], ["com o sistema", monta(iCom), D.consumos[iCom]]];
      const totais = casos.map(([, l]) => l.reduce((a, b) => a + b, 0));
      const ey = escala(0, Math.max(...totais) * 1.12, 5);
      const A = plano({W, H: 330, l: 70, r: 14, t: 34, b: 52, x: [-0.6, 1.6], y: [0, ey.max], ym: ey.marcas,
        yf: x => fmt(x), yr: "fatura mensal (R$)", xm: [0, 1], xf: i => casos[i][0]});
      let s = A.s;
      const bw = (A.X(1) - A.X(0)) * 0.46;
      casos.forEach(([rot, linha, consumo], i) => {
        let base = 0;
        linha.forEach((valor, j) => {
          if (valor <= 0) return;
          const alto = A.Y(base) - A.Y(base + valor);
          s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(base + valor)}" width="${bw}" height="${Math.max(0, alto - 1.5)}" style="fill:${cores[j]}"/>`;
          if (alto > 18) s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(base + valor / 2) + 4}" text-anchor="middle" style="fill:${j === 0 || j === 5 || j <= 2 ? "#fff" : "var(--sobre-r7)"}">${reais(valor)}</text>`;
          base += valor;
        });
        s += `<text class="g-rot" x="${A.X(i)}" y="${A.Y(base) - 8}" text-anchor="middle" style="fill:var(--ink)">${reais(base)}</text>`;
        s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(0) + 32}" text-anchor="middle">${fmt(consumo, 2)} m³/mês</text>`;
      });
      const xs = A.X(1) + bw / 2 + 12, y1 = A.Y(totais[0]), y2 = A.Y(totais[1]);
      s += `<line x1="${xs}" x2="${xs}" y1="${y1}" y2="${y2}" style="stroke:${S(4)};stroke-width:1.5"/>`;
      s += `<text class="g-rot" x="${xs - 4}" y="${(y1 + y2) / 2 + 4}" text-anchor="end" style="fill:${S(4)}">−${reais(totais[0] - totais[1])}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      p.querySelector(`#${id}leg`).innerHTML = D.rubricas.map((r, j) => casos[0][1][j] > 0 || casos[1][1][j] > 0
        ? `<span><i style="--c:${cores[j]}"></i>${r}</span>` : "").join("");
      p.querySelector(`#${id}s-o`).textContent = fmt(D.consumos[iSem], 2) + " m³/mês";
      p.querySelector(`#${id}c-o`).textContent = fmt(D.consumos[iCom], 2) + " m³/mês";
      const agua = D.consumos[iSem] - D.consumos[iCom], economia = totais[0] - totais[1];
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Água potável economizada: ${fmt(agua, 2)} m³/mês</p>
        <table class="fi-tabela"><thead><tr><th>Parcela</th><th class="n">Sem</th><th class="n">Com</th><th class="n">Diferença</th></tr></thead><tbody>
        ${D.rubricas.map((r, j) => {
          const a = casos[0][1][j], b = casos[1][1][j];
          if (a <= 0 && b <= 0) return "";
          return `<tr><td><i style="--c:${cores[j]}"></i>${r}</td><td class="n">${reais(a)}</td><td class="n">${reais(b)}</td><td class="n">${a - b > 0.005 ? "−" + reais(a - b) : "—"}</td></tr>`;
        }).join("")}
        <tr class="tot"><td>Total</td><td class="n">${reais(totais[0])}</td><td class="n">${reais(totais[1])}</td><td class="n">−${reais(economia)}</td></tr></tbody></table>
        <div class="fi-n">${cartao("Redução da fatura", fmt(100 * economia / totais[0], 1) + "%", `de ${fmt(100 * agua / (D.consumos[iSem] || 1), 1)}% do consumo`)}
        ${cartao("Economia por m³ poupado", agua > 0 ? reais(economia / agua, 2) : "—", "R$/m³")}</div>
        <p class="fi-nota">A tarifa de disponibilidade é a mesma nos dois casos: é o que se paga por estar ligado à rede. Por isso a fatura cai menos, em proporção, do que o consumo.</p>`;
    };
    p.querySelector(`#${id}s`).addEventListener("input", e => { iSem = +e.target.value; if (iCom > iSem) iCom = iSem; desenha(); });
    p.querySelector(`#${id}c`).addEventListener("input", e => { iCom = Math.min(+e.target.value, iSem); desenha(); });
    ligarSeg(p, id + "e", x => { esgoto = +x; desenha(); });
    desenha();
  }
};

/* ─── a sensibilidade: que premissa move o resultado ───────────────────── */
FI["fig24_tornado.png"] = {
  curto: "O tornado de sensibilidade",
  pergunta: "Que premissa move mais o resultado do projeto?",
  controles: "amplitude da variação",
  experimente: "Com ±30%, nenhuma premissa sozinha derruba o projeto. Suba para ±50% e duas passam a zerar o valor presente líquido: o volume de água captada e o período de análise. São as duas que precisam de dado local — série de chuva medida e vida útil declarada — antes de o estudo ser publicado.",
  fonte: "Análise de sensibilidade do próprio programa (run_sensitivity_analysis) sobre o caso-base do tutorial — cisterna de 4.000 L em concreto, 20 anos, tarifa da CASAN —, a mesma definição de caso-base que a figura do manual usa.",
  montar(p, D, id) {
    let amp = D.padrao, sel = null;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "a", "Amplitude da variação de cada premissa", D.amplitudes.map(a => [a, "±" + a + "%"]), amp)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 380" role="img" aria-label="Variação do valor presente líquido quando cada premissa sobe e desce"></svg>
      ${legenda([[S(4), "premissa para cima"], [S(2), "premissa para baixo"], ["var(--ink3)", "VPL do caso-base", "trac"]])}
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
        xm: ex.marcas, xf: v => menos(v), xr: "valor presente líquido em 20 anos (R$)"});
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
      s += `<text class="g-t" x="${x0}" y="${A.Y(-0.6) - 6}" text-anchor="middle">caso-base: ${reais(D.vpl_base)}</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      const svg = p.querySelector(`#${id}g`);
      svg.onpointermove = e => {
        const r = svg.getBoundingClientRect();
        const y = (e.clientY - r.top) / r.height * 380;
        let k = 0, d = Infinity;
        itens.forEach((x, i) => { const q = Math.abs(A.Y(i) - y); if (q < d) { d = q; k = i; } });
        const x = itens[k], dica = $("#dica");
        dica.innerHTML = dicaHTML(x.nome, [
          [S(4), `+${amp}%`, reais(x.alto) + ` (${menos(x.alto - D.vpl_base)})`],
          [S(2), `−${amp}%`, reais(x.baixo) + ` (${menos(x.baixo - D.vpl_base)})`]]);
        dica.hidden = false;
        const lim = document.documentElement.clientWidth - dica.offsetWidth - 8;
        dica.style.left = Math.max(8, Math.min(e.pageX + 14, lim)) + "px";
        dica.style.top = Math.max(window.scrollY + 64, e.pageY - dica.offsetHeight - 12) + "px";
      };
      svg.onpointerleave = () => { $("#dica").hidden = true; };
      svg.onclick = e => {
        const r = svg.getBoundingClientRect();
        const y = (e.clientY - r.top) / r.height * 380;
        let k = 0, d = Infinity;
        itens.forEach((x, i) => { const q = Math.abs(A.Y(i) - y); if (q < d) { d = q; k = i; } });
        sel = itens[k].nome; desenha();
      };
      const viram = itens.filter(x => Math.min(x.alto, x.baixo) < 0);
      const s1 = itens.find(x => x.nome === sel);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">Caso-base: cisterna de ${fmt(D.volume)} L, VPL de ${reais(D.vpl_base)}</p>
        <div class="fi-n">${cartao("Premissa que mais move o VPL", itens[0].nome.replace(/ \(.*/, ""), `faixa de ${reais(itens[0].amplitude)}`)}
        ${cartao("Premissas que chegam a zerar o VPL", viram.length ? viram.length + " de " + itens.length : "nenhuma", viram.length ? viram.map(x => x.nome.replace(/ \(.*/, "")).join(", ") : `com ±${amp}%`)}</div>
        <p class="fi-sub">Premissa em destaque: ${s1.nome}</p>
        <table class="fi-tabela"><tbody>
        <tr><td><i style="--c:${S(4)}"></i>Premissa ${amp}% maior</td><td class="n">${reais(s1.alto)}</td><td class="n">${reais(s1.alto - D.vpl_base)}</td></tr>
        <tr><td>Caso-base</td><td class="n">${reais(D.vpl_base)}</td><td class="n">—</td></tr>
        <tr><td><i style="--c:${S(2)}"></i>Premissa ${amp}% menor</td><td class="n">${reais(s1.baixo)}</td><td class="n">${reais(s1.baixo - D.vpl_base)}</td></tr>
        </tbody></table>
        <p class="fi-nota">O caso-base sai do modelo econômico simplificado do programa, que desconta um fluxo anual com tarifa marginal única; por isso o valor presente aqui não é o mesmo do fluxo de caixa mensal da figura 28. O que o tornado mede é a sensibilidade relativa. Cada barra move uma premissa de cada vez, mantendo as outras no caso-base. A ordem é a da amplitude: quem está no alto decide o resultado, e é onde vale gastar esforço para conseguir dado local. Uma premissa cuja barra cruza o zero pode, sozinha, tornar o projeto inviável.</p>`;
    };
    ligarSeg(p, id + "a", x => { amp = +x; desenha(); });
    desenha();
  }
};

/* ─── quanto a cobertura capta ─────────────────────────────────────────── */
FI["fig35_escoamento.png"] = {
  curto: "A captação da cobertura",
  pergunta: "Quanta água a sua cobertura capta por mês?",
  controles: "cidade · material · área · descarte",
  experimente: "Troque a telha cerâmica pelo telhado verde: o coeficiente cai de 0,75 para 0,24 e a captação despenca a um terço. Suba o descarte de 0 para 3 mm e veja quanto some — em Florianópolis, um quarto da chuva do ano.",
  fonte: "Chuva diária de 30 anos da série de cada capital, com o descarte aplicado a cada evento como no programa, e o coeficiente de escoamento do material da cobertura. A captação é V = P × A × C, a mesma conta da NBR 15527:2019 e do motor de simulação.",
  montar(p, D, id) {
    let cidade = D.padrao[0], desc = D.padrao[1], area = D.padrao[2], material = D.padrao[3];
    const W = 640;
    const coefDe = () => (D.materiais.find(m => m[0] === material) || D.materiais[0])[1];
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "Cidade", D.cidades.map(c => [c.chave, c.nome]), cidade)}
      <div class="fi-ctl largo"><label class="fi-rot" for="${id}m">Material da cobertura <output id="${id}m-o"></output></label>
      <select id="${id}m">${D.materiais.map(([n, c]) => `<option value="${esc(n)}"${n === material ? " selected" : ""}>${esc(n)} — coeficiente ${fmt(c, 2)}</option>`).join("")}</select></div>
      ${ctlFaixa(id + "a", "Área de cobertura (projeção horizontal)", D.areas.length, D.areas.indexOf(area))}
      ${ctlSeg(id + "d", "Descarte de primeiras águas", D.descartes.map(d => [d, fmt(d) + " mm"]), desc)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Volume captado em cada mês do ano, em média"></svg>
      ${legenda([[S(1), "captação do mês"], [S(2), "parte retida pelo descarte"], ["var(--ink3)", "demanda pluvial do tutorial", "trac"]])}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const c = D.cidades.find(x => x.chave === cidade), coef = coefDe();
      const litros = mm => mm * area * coef;                     // 1 mm em 1 m² = 1 L
      const mensal = c.mensal[String(desc)].map(litros);
      const bruto = c.mensal["0"].map(litros);
      const demandaMes = D.demanda_pluvial_tutorial * 30.4375;
      const ey = escala(0, Math.max(...bruto, demandaMes) * 1.1, 4);
      const A = plano({W, H: 300, l: 66, r: 14, t: 34, b: 44, x: [0.4, 12.6], y: [0, ey.max], ym: ey.marcas,
        yf: v => fmt(v / 1000, 1), yr: "volume captado no mês (m³)",
        xm: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xf: m => MESES[m - 1]});
      let s = A.s;
      const bw = (A.X(2) - A.X(1)) * 0.62;
      mensal.forEach((v, m) => {
        const x = A.X(m + 1) - bw / 2;
        if (bruto[m] > v) s += `<rect x="${x}" y="${A.Y(bruto[m])}" width="${bw}" height="${Math.max(0, A.Y(v) - A.Y(bruto[m]) - 1)}" rx="2" style="fill:${S(2)};opacity:0.55"/>`;
        s += `<rect x="${x}" y="${A.Y(v)}" width="${bw}" height="${Math.max(0, A.Y(0) - A.Y(v))}" rx="2" style="fill:${S(1)}"/>`;
      });
      s += `<line class="g-ref" x1="${A.X(0.4)}" x2="${A.X(12.6)}" y1="${A.Y(demandaMes)}" y2="${A.Y(demandaMes)}"/>`;
      s += `<text class="g-t" x="${A.X(12.6)}" y="${A.Y(demandaMes) - 6}" text-anchor="end">demanda pluvial do tutorial: ${fmt(demandaMes / 1000, 1)} m³/mês</text>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, mensal.map((_, m) => A.X(m + 1)),
        m => dicaHTML(`${MESES[m]} · média de 30 anos`, [
          [S(1), "captado", fmt(mensal[m] / 1000, 2) + " m³"],
          [S(2), "retido no descarte", fmt((bruto[m] - mensal[m]) / 1000, 2) + " m³"],
          ["", "lâmina aproveitável", fmt(c.mensal[String(desc)][m], 1) + " mm"]]));
      p.querySelector(`#${id}a-o`).textContent = fmt(area) + " m²";
      p.querySelector(`#${id}m-o`).textContent = "C = " + fmt(coef, 2);
      const anual = c.anual[String(desc)] * area * coef, anualBruto = c.anual["0"] * area * coef;
      const cobertos = mensal.filter(v => v >= demandaMes).length;
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(c.nome)}, ${fmt(area)} m² de ${esc(material).toLowerCase()}</p>
        <div class="fi-n">${cartao("Captação média anual", fmt(anual / 1000, 1) + " m³")}
        ${cartao("Média diária", fmt(anual / 365.25) + " L/dia")}
        ${cartao("Lâmina aproveitável", fmt(c.anual[String(desc)]) + " mm/ano", `chuva de ${fmt(c.anual["0"])} mm`)}
        ${cartao("Retido pelo descarte", fmt(100 * (1 - anual / anualBruto), 1) + "%", `com ${fmt(desc)} mm por evento`)}
        ${cartao("Meses que cobrem a demanda", cobertos, "de 12, no tutorial")}
        ${cartao("Coeficiente de escoamento", fmt(coefDe(), 2), esc(material))}</div>
        <p class="fi-nota">Esta é a oferta bruta da cobertura, antes da cisterna: o que o reservatório consegue guardar depende do volume e do consumo, e é o que as figuras do balanço diário mostram. Coeficientes de ${esc(D.fonte_coeficientes)}</p>`;
    };
    ligarSeg(p, id + "c", x => { cidade = x; desenha(); });
    ligarSeg(p, id + "d", x => { desc = +x; desenha(); });
    p.querySelector(`#${id}m`).addEventListener("change", e => { material = e.target.value; desenha(); });
    p.querySelector(`#${id}a`).addEventListener("input", e => { area = D.areas[+e.target.value]; desenha(); });
    desenha();
  }
};

/* ─── qual pressurizador gasta menos ───────────────────────────────────── */
FI["fig00k_energia.png"] = {
  curto: "A escolha do pressurizador",
  pergunta: "Qual motobomba gasta menos para pressurizar a água de chuva?",
  controles: "pressão · volume recalcado · partidas",
  experimente: "Suba a pressão de trabalho: acima de 20 m.c.a. os modelos de menor potência deixam de entregar a vazão do ponto e saem da disputa. Repare que o modelo mais potente não é o que gasta mais por metro cúbico — o que decide é o tempo ligado.",
  fonte: "Catálogo de seis pressurizadores do programa, com curva de vazão × pressão de cada fabricante. A energia é a potência elétrica multiplicada pelo tempo ligado, e a vazão efetiva é a menor entre a curva da bomba e a vazão do ponto de uso de 9 L/min.",
  montar(p, D, id) {
    let pi = D.pressoes.indexOf(D.padrao[0]), vol = D.padrao[1], part = D.padrao[2], sel = 0;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlFaixa(id + "p", "Pressão de trabalho", D.pressoes.length, pi)}
      ${ctlSeg(id + "v", "Volume recalcado por ano", D.volumes.map(v => [v, fmt(v) + " m³"]), vol)}
      ${ctlSeg(id + "n", "Partidas por ano", D.partidas.map(n => [n, fmt(n)]), part)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 260" role="img" aria-label="Energia anual de cada modelo do catálogo"></svg>
      <svg id="${id}h" viewBox="0 0 ${W} 260" role="img" aria-label="Curva de vazão contra pressão de cada modelo"></svg>
      ${legenda([[S(4), "modelo que menos gasta"], [S(1), "modelo em destaque"], [S(2), "não entrega a vazão do ponto"], ["var(--ink3)", "vazão do ponto de uso", "trac"]])}
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
        xm: ey.marcas, xf: v => fmt(v), xr: "energia elétrica por ano (kWh)"});
      let s = A.s;
      const h = 20;
      lista.forEach((x, i) => {
        const y = A.Y(i), cor = !x.atende ? S(2) : x.chave === melhor ? S(4) : S(1);
        s += `<rect x="${A.X(0)}" y="${y - h / 2}" width="${Math.max(1, A.X(x.kwh) - A.X(0))}" height="${h}" rx="2" style="fill:${cor};opacity:${i === sel ? 1 : 0.6}"/>`;
        s += `<text class="g-t" x="${A.X(0) - 8}" y="${y + 4}" text-anchor="end" style="${i === sel ? "font-weight:600" : ""}">${esc(meta(x.chave).rotulo)}</text>`;
        s += `<text class="g-t" x="${A.X(x.kwh) + 8}" y="${y + 4}">${x.atende ? fmt(x.kwh) + " kWh" : "não atende"}</text>`;
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
        yf: v => fmt(v), yr: "pressão (m.c.a.)", xm: ex.marcas, xf: v => fmt(v), xr: "vazão (L/min)"});
      let t = B.s;
      const rot = [];
      lista.forEach((x, i) => {
        const m = meta(x.chave), pontos = m.curva.slice().sort((a, b) => a[0] - b[0]);
        const cor = i === sel ? S(1) : "var(--ink3)";
        t += `<polyline points="${pontos.map(([q, hh]) => `${B.X(q)},${B.Y(hh)}`).join(" ")}" style="fill:none;stroke:${cor};stroke-width:${i === sel ? 2.6 : 1.2};opacity:${i === sel ? 1 : 0.5}"/>`;
        if (i === sel) rot.push({y: B.Y(pontos[pontos.length - 1][1]), t: m.rotulo.split(",")[0], c: S(1)});
      });
      t += `<line class="g-ref" x1="${B.X(D.vazao_do_ponto)}" x2="${B.X(D.vazao_do_ponto)}" y1="${B.Y(eh.max)}" y2="${B.Y(0)}"/>`;
      t += `<text class="g-t" x="${B.X(D.vazao_do_ponto) + 6}" y="${B.Y(eh.max) + 12}">vazão do ponto: ${fmt(D.vazao_do_ponto)} L/min</text>`;
      t += `<line x1="${B.X(0)}" x2="${B.X(ex.max)}" y1="${B.Y(pressao)}" y2="${B.Y(pressao)}" style="stroke:${S(4)};stroke-dasharray:4 4"/>`;
      t += `<text class="g-t" x="${B.X(ex.max)}" y="${B.Y(pressao) - 6}" text-anchor="end" style="fill:${S(4)}">pressão de trabalho: ${fmt(pressao, 1)} m.c.a.</text>`;
      t += rotulosNaPonta(rot, B.X(ex.max) + 8, B.Y(eh.max), B.Y(0));
      p.querySelector(`#${id}h`).innerHTML = t;

      p.querySelector(`#${id}p-o`).textContent = fmt(pressao, 1) + " m.c.a.";
      const x = lista[sel], m = meta(x.chave);
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${melhor ? "Menor consumo: " + esc(meta(melhor).rotulo) : "Nenhum modelo entrega a vazão do ponto nesta pressão"}</p>
        <div class="fi-n">${cartao("Energia do modelo em destaque", x.atende ? fmt(x.kwh) + " kWh/ano" : "—", esc(m.rotulo))}
        ${cartao("Consumo específico", x.atende ? fmt(x.kwh_m3, 3) + " kWh/m³" : "—")}
        ${cartao("Custo anual de energia", x.atende ? reais(x.kwh * D.tarifa) : "—", `tarifa de ${reais(D.tarifa, 5)}/kWh`)}
        ${cartao("Tempo ligado", x.atende ? fmt(x.horas) + " h/ano" : "—", `${fmt(part)} partidas`)}</div>
        <p class="fi-sub">Todos os modelos nesta condição</p>
        <table class="fi-tabela"><thead><tr><th>Modelo</th><th class="n">Vazão</th><th class="n">kWh/ano</th><th class="n">kWh/m³</th></tr></thead><tbody>
        ${lista.map((y, i) => {
          const mm = meta(y.chave);
          return `<tr${i === sel ? ' class="atual"' : ""}><td>${esc(mm.rotulo)}<small>${esc({eletronico: "eletrônico"}[mm.controle] || mm.controle)} · ${fmt(mm.kw_eletrico, 3)} kW elétricos</small></td>
            <td class="n">${y.atende ? fmt(y.vazao, 1) + " L/min" : "não atende"}</td><td class="n">${y.atende ? fmt(y.kwh) : "—"}</td><td class="n">${y.atende ? fmt(y.kwh_m3, 3) : "—"}</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">A vazão efetiva é a menor entre a curva da bomba e a vazão do ponto de uso: uma bomba que entrega 40 L/min não enche mais depressa uma bacia que pede 9 L/min, apenas fica ligada o mesmo tempo com mais potência. Fonte da curva: ${esc(m.fonte)}.</p>`;
    };
    p.querySelector(`#${id}p`).addEventListener("input", e => { pi = +e.target.value; desenha(); });
    ligarSeg(p, id + "v", x => { vol = +x; desenha(); });
    ligarSeg(p, id + "n", x => { part = +x; desenha(); });
    desenha();
  }
};

/* ─── as classes de qualidade da água ──────────────────────────────────── */
FI["fig36_classes.png"] = {
  curto: "As classes de qualidade",
  pergunta: "Que qualidade cada uso exige, e o que é norma e o que é adaptação?",
  controles: "classe de qualidade",
  experimente: "Compare a classe 1, que é a da norma, com a classe 4: a turbidez cai de 5 para 2 uT e a cor de 15 para 5 uH. Repare no selo de cada uma — só a primeira pode ser apresentada como requisito normativo.",
  fonte: "As quatro classes como o programa as define (netuno/core/water_quality.py). A classe 1 reproduz a Tabela 1 e o item 4.6.5 da ABNT NBR 15527:2019; as classes 2 a 4 são adaptação do programa, coerente com a edição de 2007 da norma, e assim são declaradas na tela e no relatório.",
  montar(p, D, id) {
    let sel = D.padrao;
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "c", "Classe de qualidade", D.classes.map(c => [c.chave, c.nome.split(":")[0].replace(" (adaptada, não normativa)", "")]), sel)}
    </div>
    <div class="fi-corpo emp"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 300" role="img" aria-label="Limite de cada parâmetro nas quatro classes"></svg>
      ${legenda([[S(1), "classe em destaque"], ["var(--grid)", "demais classes"], [S(4), "classe normativa (NBR 15527:2019)"]])}
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
          xm: D.classes.map((_, i) => i), xf: i => "classe " + (i + 1)});
        s += A.s;
        const bw = (A.X(1) - A.X(0)) * 0.5;
        valores.forEach((v, i) => {
          const cor = D.classes[i].chave === sel ? S(1) : D.classes[i].normativa ? S(4) : "var(--grid)";
          s += `<rect x="${A.X(i) - bw / 2}" y="${A.Y(v)}" width="${bw}" height="${Math.max(1, A.Y(0) - A.Y(v))}" rx="2" style="fill:${cor}"/>`;
          s += `<text class="g-t" x="${A.X(i)}" y="${A.Y(v) - 5}" text-anchor="middle">${fmt(v, param.casas)}</text>`;
        });
      });
      p.querySelector(`#${id}g`).innerHTML = s;
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(c.nome.split(":")[0])}
        <span class="pill ${c.normativa ? "pleno" : "parcial"}">${c.normativa ? "✓ parâmetros da norma" : "◐ adaptação do programa"}</span></p>
        <table class="fi-tabela"><tbody>
        <tr><td>Turbidez</td><td class="n">até ${fmt(c.turbidez, 1)} uT</td></tr>
        <tr><td>Cor aparente</td><td class="n">até ${fmt(c.cor, 1)} uH</td></tr>
        <tr><td>pH</td><td class="n">${fmt(c.ph[0], 1)} a ${fmt(c.ph[1], 1)}</td></tr>
        <tr><td>Cloro residual livre</td><td class="n">${fmt(c.cloro[0], 2)} a ${fmt(c.cloro[1], 2)} mg/L</td></tr>
        <tr><td>Coliformes termotolerantes</td><td class="n">${c.coliformes > 0 ? "até " + fmt(c.coliformes) + " UFC/100 mL" : "ausentes"}</td></tr>
        <tr><td>Desinfecção</td><td class="n">${c.desinfeccao ? "exigida" : "dispensada"}</td></tr>
        <tr><td>Filtração fina</td><td class="n">${c.filtracao ? "exigida" : "dispensada"}</td></tr>
        </tbody></table>
        <p class="fi-nota">${esc(c.descricao)}</p>
        ${D.parametros.map(x => `<p class="fi-nota"><b>${x.nome}.</b> ${x.texto}</p>`).join("")}`;
    };
    ligarSeg(p, id + "c", x => { sel = x; desenha(); });
    desenha();
  }
};

/* ─── o valor presente líquido contra o volume ─────────────────────────── */
FI["fig49_programa_vpl.png"] = {
  curto: "O VPL contra o volume",
  pergunta: "Que volume dá o melhor retorno financeiro?",
  controles: "material da cisterna",
  experimente: "O máximo do valor presente líquido não cai no mesmo volume do critério hidráulico: em concreto ele fica em 2 m³, contra os 4 m³ do ganho marginal. Troque o material e veja o máximo se deslocar — é o preço por litro que o move.",
  fonte: "Uma rodada da análise econômica por volume e material, com o projeto do tutorial, a tarifa da CASAN e horizonte de 20 anos. O volume de VPL máximo é lido da própria curva.",
  montar(p, D, id) {
    let mat = D.padrao, sel = D.volumes.indexOf(4000);
    const W = 640;
    p.innerHTML = `<div class="fi-ctls">
      ${ctlSeg(id + "m", "Material da cisterna", D.materiais, mat)}
    </div>
    <div class="fi-corpo"><div>
      <svg id="${id}g" viewBox="0 0 ${W} 320" role="img" aria-label="Valor presente líquido em função do volume da cisterna, por material"></svg>
      ${legenda(D.materiais.map(([k, t], i) => [S(i + 1), t, "linha"]).concat([["var(--ink2)", "volume em destaque", "trac"]]))}
    </div><div class="fi-leit" id="${id}l"></div></div>`;
    const desenha = () => {
      const todos = D.materiais.flatMap(([k]) => D.casos[k].map(x => x[0]));
      const ey = escala(Math.min(...todos, 0), Math.max(...todos) * 1.08, 5);
      const A = plano({W, H: 320, l: 74, r: 120, t: 34, b: 46, x: [0, 20000], y: [ey.min, ey.max], ym: ey.marcas,
        yf: v => menos(v), yr: "valor presente líquido em 20 anos (R$)",
        xm: [0, 5000, 10000, 15000, 20000], xf: v => fmt(v / 1000) + " m³", xr: "volume da cisterna"});
      let s = A.s;
      const rot = [];
      D.materiais.forEach(([k, t], i) => {
        const linha = D.casos[k], cor = S(i + 1), atual = k === mat;
        s += `<polyline points="${linha.map((x, j) => `${A.X(D.volumes[j])},${A.Y(x[0])}`).join(" ")}" style="fill:none;stroke:${cor};stroke-width:${atual ? 2.6 : 1.4};opacity:${atual ? 1 : 0.45}"/>`;
        const melhor = linha.reduce((a, x, j) => x[0] > linha[a][0] ? j : a, 0);
        if (atual) {
          s += `<circle cx="${A.X(D.volumes[melhor])}" cy="${A.Y(linha[melhor][0])}" r="6" style="fill:${cor};stroke:var(--surface);stroke-width:2"/>`;
          s += `<text class="g-rot" x="${A.X(D.volumes[melhor])}" y="${A.Y(linha[melhor][0]) - 12}" text-anchor="middle" style="fill:${cor}">máximo: ${fmt(D.volumes[melhor])} L</text>`;
        }
        rot.push({y: A.Y(linha[linha.length - 1][0]), t: t.split(" (")[0], c: cor});
      });
      s += rotulosNaPonta(rot, A.X(20000) + 8, A.Y(ey.max), A.Y(ey.min));
      s += `<line class="g-ref" x1="${A.X(D.volumes[sel])}" x2="${A.X(D.volumes[sel])}" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="stroke:var(--ink2)"/>`;
      s += `<line class="g-guia" x1="0" x2="0" y1="${A.Y(ey.max)}" y2="${A.Y(ey.min)}" style="display:none"/>`;
      p.querySelector(`#${id}g`).innerHTML = s;
      pairar(p.querySelector(`#${id}g`), W, D.volumes.map(v => A.X(v)),
        j => dicaHTML(`${fmt(D.volumes[j])} L`, D.materiais.map(([k, t], i) => [S(i + 1), t.split(" (")[0], reais(D.casos[k][j][0])])),
        j => { sel = j; desenha(); });
      const linha = D.casos[mat], melhor = linha.reduce((a, x, j) => x[0] > linha[a][0] ? j : a, 0);
      const x = linha[sel];
      p.querySelector(`#${id}l`).innerHTML = `<p class="fi-sub">${esc(D.materiais.find(m => m[0] === mat)[1])}</p>
        <div class="fi-n">${cartao("Volume de VPL máximo", fmt(D.volumes[melhor]) + " L", reais(linha[melhor][0]))}
        ${cartao("Volume em destaque", fmt(D.volumes[sel]) + " L", "clique no gráfico para trocar")}
        ${cartao("VPL", reais(x[0]), x[0] >= 0 ? "✓ positivo" : "✕ negativo")}
        ${cartao("Tempo de retorno", x[1] ? fmt(x[1], 1) + " anos" : "mais de 20 anos")}
        ${cartao("Potencial de economia", fmt(x[2], 2) + "%")}
        ${cartao("Diferença para o máximo", reais(x[0] - linha[melhor][0]))}</div>
        <p class="fi-sub">O melhor volume de cada material</p>
        <table class="fi-tabela"><tbody>${D.materiais.map(([k, t], i) => {
          const l = D.casos[k], m = l.reduce((a, y, j) => y[0] > l[a][0] ? j : a, 0);
          return `<tr${k === mat ? ' class="atual"' : ""}><td><i style="--c:${S(i + 1)}"></i>${t}</td><td class="n">${fmt(D.volumes[m])} L</td><td class="n">${reais(l[m][0])}</td></tr>`;
        }).join("")}</tbody></table>
        <p class="fi-nota">A curva tem máximo interior porque o investimento cresce com o volume enquanto a economia de água satura. Um volume à direita do máximo continua economizando mais água, e rendendo menos dinheiro.</p>`;
    };
    ligarSeg(p, id + "m", x => { mat = x; desenha(); });
    desenha();
  }
};

/* ─── montagem nas páginas ─────────────────────────────────────────────── */
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
    caixa.innerHTML = `<div class="fi-topo"><span class="fi-selo"><i></i>Figura ${num} · interativa</span>
      <div class="fi-modo" role="group" aria-label="Versão da figura"><button type="button" data-m="i" aria-pressed="true">Interativa</button><button type="button" data-m="e" aria-pressed="false">Figura do manual</button></div></div>
      <p class="fi-pergunta">${def.pergunta}</p><div class="fi-palco"></div>
      <p class="fi-exp"><b>Experimente.</b> ${def.experimente}</p><p class="fi-fonte"><b>De onde vêm os números.</b> ${def.fonte}</p>`;
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

/* Onde cada figura interativa está, por seção, na ordem do manual. */
const INTERATIVAS_DA_SECAO = {};
Object.keys(FI_ONDE).forEach(arquivo => {
  if (!FI_D[arquivo]) return;
  const o = FI_ONDE[arquivo];
  (INTERATIVAS_DA_SECAO[o.secao] = INTERATIVAS_DA_SECAO[o.secao] || []).push({arquivo, numero: o.numero});
});
Object.values(INTERATIVAS_DA_SECAO).forEach(lista => lista.sort((a, b) => a.numero - b.numero));

/* A página inicial não abre figura nenhuma: aponta para onde cada uma está. */
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
    <h2>Perguntas que você responde mexendo</h2>
    <p class="sub">Estas figuras do manual têm versão interativa. Elas não abrem aqui: cada uma vive na seção onde o assunto entra, para o texto e o gráfico serem lidos juntos.</p>
    <ul class="perguntas">${destaque.map(a => {
      const o = FI_ONDE[a];
      return `<li><a href="#/${o.secao}/fig-${o.numero}"><b>${esc(FI[a].pergunta)}</b><small>seção ${esc(o.secao)} · figura ${o.numero}</small></a></li>`;
    }).join("")}</ul>
    <p class="depois">São ${fmt(todas.length)} ao todo, distribuídas pelo manual. No sumário de cada página elas vêm marcadas como <b class="marca-i">interativa</b>, e a busca as encontra pelo nome.</p>
  </section>`;
}

/* A busca encontra a pergunta que cada figura interativa responde, e não só a
   legenda da figura estática: é assim que o leitor chega pelo que quer saber. */
Object.keys(FI_ONDE).forEach(arquivo => {
  const o = FI_ONDE[arquivo], def = FI[arquivo];
  if (!def || !FI_D[arquivo] || typeof INDICE === "undefined") return;
  const item = INDICE.find(i => i.t === "interativa" && i.id === o.secao && i.a === "fig-" + o.numero);
  if (!item) return;
  item.x = item.n + " " + def.curto + " · controles: " + def.controles;
  item.n = def.pergunta;
  item.nn = semAcento((item.r + " " + item.n + " " + item.x).toLowerCase());
  item.xn = semAcento(item.x.toLowerCase());
});
