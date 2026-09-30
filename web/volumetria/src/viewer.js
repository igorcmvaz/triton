/*
 * Visualizador 3D da volumetria do Netuno.
 *
 * Recebe a cena que o Python monta (netuno/core/volumetry_export.py,
 * scene_payload): metros, z para cima, uma entrada por sólido com o tipo do
 * catálogo, a caixa envolvente, o eixo dos tubos e a ficha técnica. A geometria
 * de posição e tamanho é a do Python — a que os testes validam —; aqui ela ganha
 * forma de peça (tanque com tampa e nervuras, motobomba com motor aletado,
 * registro com volante), materiais físicos, iluminação por HDRI e sombras.
 *
 * O mesmo arquivo serve o HTML exportado e a aba do programa (QtWebEngine).
 * Tudo é local: three.js vai empacotado e o céu (Poly Haven, CC0) vai embutido.
 */

import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { HDRLoader } from "three/addons/loaders/HDRLoader.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { OutlinePass } from "three/addons/postprocessing/OutlinePass.js";
import { GTAOPass } from "three/addons/postprocessing/GTAOPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const UP = new THREE.Vector3(0, 0, 1);
THREE.Object3D.DEFAULT_UP.copy(UP);

// ── Textos da interface (o Python injeta a tradução em opts.texts) ───────────
const TEXTOS_PADRAO = {
  titulo: "Volumetria 3D",
  dica: "Arraste para girar · botão direito para deslocar · roda para aproximar · duplo clique para focar",
  iso: "Perspectiva", planta: "Planta", frente: "Frente", lateral: "Lateral", enquadrar: "Enquadrar",
  edificacao: "Edificação", terreno: "Terreno", rotulos: "Rótulos", fluxo: "Fluxo", raiox: "Raio-X",
  ceu: "Céu", sombras: "Sombras", corte: "Corte por cota", medir: "Medir", foto: "Imagem PNG",
  telaCheia: "Tela cheia", tema: "Tema", painel: "Painel", sistemas: "Sistemas", componentes: "Componentes",
  ficha: "Ficha técnica", notas: "Notas", semSelecao: "Clique numa peça para ver a ficha técnica.",
  medirDica: "Clique em dois pontos para medir. Esc encerra.", distancia: "Distância",
  semWebGL: "Este computador não oferece WebGL: a volumetria 3D não pode ser desenhada aqui.",
  creditos: "three.js (MIT) · céu «Quarry» do Poly Haven (CC0)", cota: "cota",
};

// ── Materiais ─────────────────────────────────────────────────────────────────
function rgb(c) { return new THREE.Color(c[0] / 255, c[1] / 255, c[2] / 255); }
const MAT = {
  polietileno: (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.42, metalness: 0, clearcoat: 0.35, clearcoatRoughness: 0.4, sheen: 0.2 }),
  concreto: () => new THREE.MeshStandardMaterial({ color: 0xc9cdd2, roughness: 0.92, metalness: 0 }),
  aco: () => new THREE.MeshStandardMaterial({ color: 0x9aa3ad, roughness: 0.35, metalness: 0.85 }),
  acoEscuro: () => new THREE.MeshStandardMaterial({ color: 0x3b4450, roughness: 0.45, metalness: 0.7 }),
  pintura: (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.32, metalness: 0.25, clearcoat: 0.6, clearcoatRoughness: 0.2 }),
  pvc: (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.3, metalness: 0, clearcoat: 0.25 }),
  borracha: () => new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.9 }),
  vidro: () => new THREE.MeshPhysicalMaterial({ color: 0xdbeafe, roughness: 0.08, metalness: 0, transparent: true, opacity: 0.14, depthWrite: false, side: THREE.DoubleSide }),
  laje: () => new THREE.MeshStandardMaterial({ color: 0xe8ebef, roughness: 0.95, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide }),
  agua: () => new THREE.MeshPhysicalMaterial({ color: 0x3b82f6, roughness: 0.05, transmission: 0, transparent: true, opacity: 0.55, depthWrite: false }),
};

// ── Geometria de apoio ────────────────────────────────────────────────────────
function cylinderBetween(a, b, radius, segments = 20, open = false) {
  const dir = new THREE.Vector3().subVectors(b, a);
  const len = dir.length();
  const g = new THREE.CylinderGeometry(radius, radius, Math.max(len, 1e-4), segments, 1, open);
  g.translate(0, len / 2, 0);
  const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
  g.applyQuaternion(q);
  g.translate(a.x, a.y, a.z);
  return g;
}
function zCylinder(r, h, z0 = 0, seg = 40, rTop = r) {
  const g = new THREE.CylinderGeometry(rTop, r, h, seg);
  g.rotateX(Math.PI / 2);
  g.translate(0, 0, z0 + h / 2);
  return g;
}
function mesh(geometry, material, shadows = true) {
  const m = new THREE.Mesh(geometry, material);
  m.castShadow = shadows; m.receiveShadow = true;
  return m;
}

// ── Peças detalhadas: cada uma ocupa a caixa (w × d × h) que o Python calculou ─
function tanque(w, d, h, cor, enterrado) {
  const g = new THREE.Group();
  const r = Math.min(w, d) / 2;
  const corpo = MAT.polietileno(cor);
  // Perfil de revolução: fundo arredondado, costado levemente cônico, ombro e tampa.
  const p = [];
  const rb = r * 0.94, cant = Math.min(r, h) * 0.08;
  p.push(new THREE.Vector2(0, 0));
  p.push(new THREE.Vector2(rb - cant, 0));
  p.push(new THREE.Vector2(rb, cant));
  p.push(new THREE.Vector2(r, h * 0.84));
  p.push(new THREE.Vector2(r * 0.96, h * 0.9));
  p.push(new THREE.Vector2(r * 0.55, h * 0.97));
  p.push(new THREE.Vector2(r * 0.42, h * 0.97));
  p.push(new THREE.Vector2(0, h * 0.97));
  const lathe = new THREE.LatheGeometry(p, 56);
  lathe.rotateX(Math.PI / 2);
  g.add(mesh(lathe, corpo));
  // Nervuras horizontais do costado
  const ribs = [];
  for (let i = 1; i <= 4; i++) {
    const z = h * 0.84 * i / 5;
    const rr = rb + (r - rb) * (z / (h * 0.84));
    const t = new THREE.TorusGeometry(rr, Math.max(r * 0.018, 0.008), 8, 56);
    t.translate(0, 0, z);
    ribs.push(t);
  }
  g.add(mesh(mergeGeometries(ribs), corpo));
  // Tampa de inspeção rosqueada com pega
  g.add(mesh(zCylinder(r * 0.4, h * 0.035, h * 0.965, 40), MAT.pintura(new THREE.Color(cor).multiplyScalar(0.7))));
  g.add(mesh(new RoundedBoxGeometry(r * 0.35, r * 0.06, h * 0.03, 2, r * 0.01).translate(0, 0, h + h * 0.005), MAT.borracha()));
  // Nível d'água indicativo (70%), visível no raio-X
  const agua = mesh(zCylinder(rb * 0.97, h * 0.62, cant * 0.5, 48), MAT.agua(), false);
  agua.userData.xrayOnly = true; agua.visible = false;
  g.add(agua);
  if (enterrado) {
    // Laje de fundo e poço de escavação: a cisterna fica enterrada no recuo.
    g.add(mesh(new THREE.BoxGeometry(r * 2.5, r * 2.5, h * 0.06).translate(0, 0, -h * 0.03), MAT.concreto()));
  }
  return g;
}

function descarte(w, d, h, cor) {
  // Tubo vertical de descarte (first flush) com tampas, tê de entrada e registro de purga.
  const g = new THREE.Group();
  const r = Math.min(w, d) / 2;
  const pvc = MAT.pvc(cor);
  g.add(mesh(zCylinder(r * 0.8, h * 0.9, h * 0.04, 32), pvc));
  g.add(mesh(zCylinder(r * 0.92, h * 0.06, 0, 32), MAT.pintura(new THREE.Color(cor).multiplyScalar(0.6))));
  g.add(mesh(zCylinder(r * 0.92, h * 0.06, h * 0.94, 32), MAT.pintura(new THREE.Color(cor).multiplyScalar(0.6))));
  g.add(mesh(cylinderBetween(new THREE.Vector3(0, 0, h * 0.8), new THREE.Vector3(r * 1.6, 0, h * 0.8), r * 0.45, 20), pvc));
  const purga = new THREE.TorusGeometry(r * 0.35, r * 0.06, 8, 24); purga.rotateY(Math.PI / 2); purga.translate(-r * 1.1, 0, h * 0.12);
  g.add(mesh(purga, MAT.pintura(0xdc2626)));
  g.add(mesh(cylinderBetween(new THREE.Vector3(0, 0, h * 0.12), new THREE.Vector3(-r * 1.1, 0, h * 0.12), r * 0.12, 12), MAT.aco()));
  return g;
}

function filtro(w, d, h, cor) {
  // Filtro vórtex: corpo cilíndrico, fundo cônico, tampa e bocais de entrada e saída.
  const g = new THREE.Group();
  const r = Math.min(w, d) / 2;
  const corpo = MAT.polietileno(cor);
  g.add(mesh(zCylinder(r, h * 0.55, h * 0.3, 40), corpo));
  g.add(mesh(zCylinder(r * 0.25, h * 0.3, 0, 40, r), corpo));
  g.add(mesh(zCylinder(r * 1.04, h * 0.08, h * 0.85, 40), MAT.pintura(0x334155)));
  g.add(mesh(zCylinder(r * 0.5, h * 0.07, h * 0.93, 32), MAT.aco()));
  const bocal = r * 0.28;
  g.add(mesh(cylinderBetween(new THREE.Vector3(-r * 1.5, 0, h * 0.7), new THREE.Vector3(0, 0, h * 0.7), bocal), MAT.pvc(0x94a3b8)));
  g.add(mesh(cylinderBetween(new THREE.Vector3(0, 0, h * 0.45), new THREE.Vector3(r * 1.5, 0, h * 0.45), bocal), MAT.pvc(0x94a3b8)));
  return g;
}

function motobomba(w, d, h, cor) {
  // Conjunto centrífugo: base, motor aletado com tampa do ventilador, voluta e bocais.
  const g = new THREE.Group();
  const L = Math.max(w, d), W = Math.min(w, d);
  const alongX = w >= d;
  const base = new RoundedBoxGeometry(L, W * 0.9, h * 0.08, 2, h * 0.015).translate(0, 0, h * 0.04);
  g.add(mesh(base, MAT.acoEscuro()));
  const rm = Math.min(W * 0.38, h * 0.36);
  const zc = h * 0.08 + rm * 1.05;
  const x0 = -L * 0.48, x1 = L * 0.12;
  const motor = cylinderBetween(new THREE.Vector3(x0 + L * 0.08, 0, zc), new THREE.Vector3(x1, 0, zc), rm, 40);
  const pintura = MAT.pintura(cor);
  g.add(mesh(motor, pintura));
  const aletas = [];
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    const f = new THREE.BoxGeometry((x1 - x0) * 0.8, rm * 0.05, rm * 0.2);
    f.translate(0, 0, rm * 1.03);
    f.rotateX(a);
    f.translate((x0 + L * 0.08 + x1) / 2, 0, zc);
    aletas.push(f);
  }
  g.add(mesh(mergeGeometries(aletas), pintura));
  g.add(mesh(cylinderBetween(new THREE.Vector3(x0, 0, zc), new THREE.Vector3(x0 + L * 0.08, 0, zc), rm * 0.92, 32), MAT.acoEscuro()));
  // Pés do motor
  for (const x of [x0 + L * 0.15, x1 - L * 0.08]) {
    g.add(mesh(new THREE.BoxGeometry(L * 0.06, W * 0.7, zc - h * 0.08).translate(x, 0, (zc + h * 0.08) / 2), pintura));
  }
  // Caixa de ligação
  g.add(mesh(new RoundedBoxGeometry(L * 0.14, rm * 0.7, rm * 0.35, 2, rm * 0.05).translate((x0 + x1) / 2, 0, zc + rm * 1.1), pintura));
  // Voluta (caracol) e bocais
  const rv = rm * 1.15;
  const voluta = cylinderBetween(new THREE.Vector3(x1, 0, zc), new THREE.Vector3(x1 + L * 0.18, 0, zc), rv, 40);
  g.add(mesh(voluta, MAT.aco()));
  g.add(mesh(cylinderBetween(new THREE.Vector3(x1 + L * 0.18, 0, zc), new THREE.Vector3(L * 0.5, 0, zc), rv * 0.38, 24), MAT.aco()));
  g.add(mesh(cylinderBetween(new THREE.Vector3(x1 + L * 0.09, 0, zc + rv * 0.6), new THREE.Vector3(x1 + L * 0.09, 0, h), rv * 0.3, 24), MAT.aco()));
  if (!alongX) g.rotation.z = Math.PI / 2;
  return g;
}

function registro(w, d, h, tipo) {
  const g = new THREE.Group();
  const s = Math.min(w, d, h);
  const corpo = MAT.aco();
  g.add(mesh(new THREE.SphereGeometry(s * 0.32, 24, 16).translate(0, 0, s * 0.4), corpo));
  g.add(mesh(cylinderBetween(new THREE.Vector3(-w / 2, 0, s * 0.4), new THREE.Vector3(w / 2, 0, s * 0.4), s * 0.2, 20), corpo));
  if (tipo === "registro_esfera") {
    g.add(mesh(new RoundedBoxGeometry(s * 0.9, s * 0.12, s * 0.06, 2, s * 0.02).translate(s * 0.3, 0, s * 0.8), MAT.pintura(0xdc2626)));
  } else if (tipo === "valvula_retencao") {
    g.add(mesh(zCylinder(s * 0.18, s * 0.3, s * 0.6, 20), corpo));
  } else {
    g.add(mesh(zCylinder(s * 0.06, s * 0.4, s * 0.6, 12), corpo));
    const volante = new THREE.TorusGeometry(s * 0.3, s * 0.05, 10, 32); volante.translate(0, 0, s * 1.0);
    g.add(mesh(volante, MAT.pintura(0xdc2626)));
  }
  return g;
}

function acessorio(w, d, h, cor, tipo) {
  if (tipo && (tipo.startsWith("registro") || tipo === "valvula_retencao")) return registro(w, d, h, tipo);
  const g = new THREE.Group();
  if (tipo === "air_gap") {
    g.add(mesh(zCylinder(Math.min(w, d) * 0.15, h * 0.5, 0, 24, Math.min(w, d) * 0.5), MAT.pvc(cor)));
    g.add(mesh(zCylinder(Math.min(w, d) * 0.08, h * 0.35, h * 0.62, 16), MAT.aco()));
    return g;
  }
  g.add(mesh(new RoundedBoxGeometry(w, d, h, 3, Math.min(w, d, h) * 0.15).translate(0, 0, h / 2), MAT.pintura(cor)));
  return g;
}

// ── Textura de fluxo (setas), compartilhada e animada ─────────────────────────
function texturaDeFluxo() {
  const c = document.createElement("canvas");
  c.width = 64; c.height = 128;
  const x = c.getContext("2d");
  x.clearRect(0, 0, 64, 128);
  x.fillStyle = "#ffffff";
  x.beginPath(); x.moveTo(8, 40); x.lineTo(32, 88); x.lineTo(56, 40); x.lineTo(44, 40); x.lineTo(32, 64); x.lineTo(20, 40); x.closePath(); x.fill();
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function texturaDoTerreno(escuro) {
  const c = document.createElement("canvas");
  c.width = c.height = 512;
  const x = c.getContext("2d");
  x.fillStyle = escuro ? "#1f2a1f" : "#9fb58b";
  x.fillRect(0, 0, 512, 512);
  // Grama: ruído fino, determinístico (mesma imagem sempre).
  let seed = 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 9000; i++) {
    const v = rnd();
    x.fillStyle = escuro ? `rgba(90,120,80,${0.08 + v * 0.12})` : `rgba(70,100,55,${0.06 + v * 0.1})`;
    x.fillRect(rnd() * 512, rnd() * 512, 1 + rnd() * 2, 1 + rnd() * 3);
  }
  // Malha de 1 m (a textura cobre 1 m e se repete)
  x.strokeStyle = escuro ? "rgba(255,255,255,0.10)" : "rgba(255,255,255,0.35)";
  x.lineWidth = 3; x.strokeRect(0, 0, 512, 512);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

function decodeBase64(b64) {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out.buffer;
}

// ── Interface ────────────────────────────────────────────────────────────────
const CSS = `
.nv-root{--bg:#f5f7fa;--panel:#ffffff;--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--accent:#1d4ed8;--chip:#eef2ff;
 position:relative;display:grid;grid-template-columns:1fr 340px;height:100%;width:100%;background:var(--bg);color:var(--ink);
 font:13px/1.45 "Segoe UI",system-ui,-apple-system,sans-serif;overflow:hidden}
.nv-root.nv-dark{--bg:#0b1220;--panel:#111a2e;--ink:#e2e8f0;--muted:#94a3b8;--line:#1e293b;--accent:#60a5fa;--chip:#1e293b}
.nv-stage{position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 35%,#ffffff 0%,#e8edf3 60%,#d9e0e8 100%)}
.nv-dark .nv-stage{background:radial-gradient(ellipse at 50% 35%,#1a2540 0%,#0d1526 60%,#070c17 100%)}
.nv-stage canvas{display:block;width:100%!important;height:100%!important;outline:none}
.nv-css2d{position:absolute;inset:0;pointer-events:none}
.nv-head{position:absolute;left:16px;top:12px;right:360px;pointer-events:none}
.nv-head h1{margin:0;font-size:16px;font-weight:650;letter-spacing:.01em;text-shadow:0 0 6px var(--bg),0 0 2px var(--bg);
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nv-head p{margin:2px 0 0;color:var(--muted);font-size:11.5px;text-shadow:0 0 6px var(--bg),0 0 2px var(--bg);
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nv-root.nv-nopanel{grid-template-columns:1fr} .nv-nopanel .nv-side{display:none}
@media (max-width:1100px){.nv-head p{display:none}}
.nv-bar{position:absolute;left:12px;bottom:12px;right:12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;pointer-events:none}
.nv-bar>*{pointer-events:auto}
.nv-grp{display:flex;gap:2px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:3px;box-shadow:0 1px 3px rgba(15,23,42,.08)}
.nv-btn{font:inherit;font-size:12px;border:0;background:transparent;color:var(--ink);padding:5px 9px;border-radius:7px;cursor:pointer;white-space:nowrap}
.nv-btn:hover{background:var(--chip)} .nv-btn.on{background:var(--accent);color:#fff}
.nv-tools{position:absolute;right:12px;top:10px}
.nv-cut{display:flex;align-items:center;gap:6px;padding:0 8px;font-size:12px;color:var(--muted)}
.nv-cut input{width:120px}
.nv-side{border-left:1px solid var(--line);background:var(--panel);padding:14px 16px;overflow:auto}
.nv-side h2{font-size:11px;margin:16px 0 8px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:650}
.nv-side h2:first-child{margin-top:0}
.nv-leg label{display:flex;align-items:center;gap:8px;margin:3px 0;cursor:pointer;font-size:12.5px}
.nv-sw{width:22px;height:6px;border-radius:3px;flex:none}
.nv-list{display:flex;flex-direction:column;gap:2px}
.nv-item{display:flex;align-items:center;gap:8px;padding:5px 8px;border-radius:7px;cursor:pointer;font-size:12.5px}
.nv-item:hover{background:var(--chip)} .nv-item.sel{background:var(--accent);color:#fff}
.nv-dot{width:10px;height:10px;border-radius:50%;flex:none}
.nv-card{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px}
.nv-card h3{margin:0 0 8px;font-size:13.5px;line-height:1.3}
.nv-row{display:flex;justify-content:space-between;gap:10px;margin:4px 0;font-size:12px}
.nv-row .k{color:var(--muted);font-weight:600} .nv-row .v{text-align:right}
.nv-sub{margin:2px 0 2px 8px;font-size:11.5px} .nv-hint{color:var(--muted);font-size:12px}
.nv-notes{font-size:11.5px;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px;margin-top:14px}
.nv-label{font:600 11px/1.2 "Segoe UI",system-ui,sans-serif;color:#0f172a;background:rgba(255,255,255,.92);border:1px solid rgba(15,23,42,.12);
 padding:3px 7px;border-radius:999px;white-space:nowrap;box-shadow:0 1px 4px rgba(15,23,42,.15);transform:translateY(-10px)}
.nv-dark .nv-label{color:#e2e8f0;background:rgba(17,26,46,.92);border-color:rgba(226,232,240,.15)}
.nv-measure{font:700 12px/1 "Segoe UI",system-ui,sans-serif;color:#fff;background:#0f172a;padding:4px 8px;border-radius:6px}
.nv-scale{position:absolute;right:14px;bottom:60px;font-size:11px;color:var(--muted);text-align:right;pointer-events:none}
.nv-scale div{height:6px;border:2px solid var(--muted);border-top:0;margin-top:2px}
.nv-toast{position:absolute;left:50%;top:56px;transform:translateX(-50%);background:var(--panel);border:1px solid var(--line);padding:6px 12px;
 border-radius:8px;font-size:12px;box-shadow:0 2px 8px rgba(15,23,42,.12);display:none}
.nv-foot{margin-top:14px;font-size:10.5px;color:var(--muted)}
@media (max-width:760px){.nv-root{grid-template-columns:1fr;grid-template-rows:1fr auto}.nv-side{max-height:40vh;border-left:0;border-top:1px solid var(--line)}.nv-head p{display:none}.nv-tools{top:auto;bottom:56px}}
`;

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  for (const c of children) if (c != null) e.append(c);
  return e;
}

// ── Visualizador ─────────────────────────────────────────────────────────────
class Visualizador {
  constructor(container, opts) {
    this.opts = opts || {};
    this.t = { ...TEXTOS_PADRAO, ...(this.opts.texts || {}) };
    this.container = container;
    this.show = { building: true, ground: true, labels: true, flow: true, xray: false, sky: false, shadows: true };
    this.hiddenSystems = new Set();
    this.selected = null;
    this.measuring = false;
    this.measurePts = [];
    this.timer = new THREE.Timer();
    this._buildDom();
    if (!this._initRenderer()) { this.renderer = null; return; }
    this._initScene();
    if (this.opts.scene) this.setScene(this.opts.scene);
    this._loop();
  }

  _buildDom() {
    if (!document.getElementById("nv-style")) document.head.append(el("style", { id: "nv-style" }, CSS));
    const t = this.t;
    const dark = this.opts.theme ? this.opts.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    this.root = el("div", { class: "nv-root" + (dark ? " nv-dark" : "") });
    this.stage = el("div", { class: "nv-stage" });
    this.title = el("h1", {}, t.titulo);
    this.stage.append(el("div", { class: "nv-head" }, this.title, el("p", {}, t.dica)));
    this.toast = el("div", { class: "nv-toast" });
    this.scaleBar = el("div", { class: "nv-scale" });
    this.stage.append(this.toast, this.scaleBar);

    const views = el("div", { class: "nv-grp" });
    for (const [k, label] of [["iso", t.iso], ["top", t.planta], ["front", t.frente], ["side", t.lateral]]) {
      views.append(el("button", { class: "nv-btn", "data-view": k, onclick: () => this.setView(k) }, label));
    }
    views.append(el("button", { class: "nv-btn", onclick: () => this.frame() }, t.enquadrar));
    const toggles = el("div", { class: "nv-grp" });
    this.toggleBtns = {};
    for (const [k, label] of [["building", t.edificacao], ["ground", t.terreno], ["labels", t.rotulos], ["flow", t.fluxo],
      ["xray", t.raiox], ["sky", t.ceu], ["shadows", t.sombras]]) {
      const b = el("button", { class: "nv-btn" + (this.show[k] ? " on" : ""), "data-toggle": k, onclick: () => this.toggle(k) }, label);
      this.toggleBtns[k] = b; toggles.append(b);
    }
    this.cutInput = el("input", { type: "range", min: "0", max: "1000", value: "1000", "aria-label": t.corte });
    this.cutInput.addEventListener("input", () => this._applyCut());
    this.cutLabel = el("span", {}, "");
    const cut = el("div", { class: "nv-grp" }, el("div", { class: "nv-cut" }, t.corte, this.cutInput, this.cutLabel));
    const tools = el("div", { class: "nv-grp" },
      this.measureBtn = el("button", { class: "nv-btn", onclick: () => this.toggleMeasure() }, t.medir),
      el("button", { class: "nv-btn", onclick: () => this.screenshot() }, t.foto),
      this.panelBtn = el("button", { class: "nv-btn on", onclick: () => this.togglePanel() }, t.painel),
      el("button", { class: "nv-btn", onclick: () => this.toggleTheme() }, t.tema),
      el("button", { class: "nv-btn", onclick: () => this.fullscreen() }, t.telaCheia));
    this.stage.append(el("div", { class: "nv-bar" }, views, toggles, cut), el("div", { class: "nv-tools" }, tools));

    this.side = el("aside", { class: "nv-side" });
    this.legend = el("div", { class: "nv-leg" });
    this.list = el("div", { class: "nv-list" });
    this.info = el("div", {}, el("p", { class: "nv-hint" }, t.semSelecao));
    this.notes = el("div", { class: "nv-notes" });
    this.side.append(el("h2", {}, t.ficha), this.info, el("h2", {}, t.sistemas), this.legend,
      el("h2", {}, t.componentes), this.list, this.notes, el("div", { class: "nv-foot" }, t.creditos));
    this.root.append(this.stage, this.side);
    this.container.replaceChildren(this.root);
  }

  _initRenderer() {
    try {
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    } catch (e) {
      this.stage.append(el("div", { class: "nv-toast", style: "display:block" }, this.t.semWebGL));
      window.__netunoVolumetria = { erro: "webgl" };
      return false;
    }
    const r = this.renderer;
    r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.AgXToneMapping;
    r.toneMappingExposure = 1.05;
    r.shadowMap.enabled = true;
    r.shadowMap.type = THREE.PCFShadowMap;
    r.localClippingEnabled = true;
    r.setClearColor(0x000000, 0);
    this.stage.prepend(r.domElement);
    this.labelRenderer = new CSS2DRenderer();
    this.labelRenderer.domElement.className = "nv-css2d";
    this.stage.append(this.labelRenderer.domElement);
    new ResizeObserver(() => this._resize()).observe(this.stage);
    return true;
  }

  _initScene() {
    this.scene = new THREE.Scene();
    this.scene.environmentRotation.x = Math.PI / 2;  // HDRI é y-para-cima; a cena é z-para-cima
    this.scene.backgroundRotation.x = Math.PI / 2;
    this.camera = new THREE.PerspectiveCamera(38, 1, 0.05, 5000);
    this.camera.up.copy(UP);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.screenSpacePanning = true;
    this.controls.addEventListener("change", () => this._updateScale());

    this.hemi = new THREE.HemisphereLight(0xffffff, 0x8d9a7c, 0.35);
    this.hemi.position.set(0, 0, 1);
    this.sun = new THREE.DirectionalLight(0xfff4e5, 2.2);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(2048, 2048);
    this.sun.shadow.bias = -0.0004;
    this.sun.shadow.normalBias = 0.02;
    this.sun.shadow.radius = 4;
    this.scene.add(this.hemi, this.sun, this.sun.target);

    if (this.opts.hdr) {
      const buffer = typeof this.opts.hdr === "string" ? decodeBase64(this.opts.hdr) : this.opts.hdr;
      try {
        const data = new HDRLoader().parse(buffer);
        const tex = new THREE.DataTexture(data.data, data.width, data.height, THREE.RGBAFormat, data.type);
        tex.colorSpace = THREE.LinearSRGBColorSpace;
        tex.mapping = THREE.EquirectangularReflectionMapping;
        tex.minFilter = THREE.LinearFilter; tex.magFilter = THREE.LinearFilter; tex.generateMipmaps = false;
        tex.needsUpdate = true;
        const pmrem = new THREE.PMREMGenerator(this.renderer);
        this.envMap = pmrem.fromEquirectangular(tex).texture;
        this.skyTexture = tex;
        this.scene.environment = this.envMap;
        this.scene.environmentIntensity = 0.9;
        pmrem.dispose();
      } catch (e) {
        console.warn("Netuno: HDRI não carregado", e);
      }
    }
    if (!this.scene.environment) this.hemi.intensity = 1.1;

    this.flowTexture = texturaDeFluxo();
    this.model = new THREE.Group();
    this.scene.add(this.model);
    this.measureGroup = new THREE.Group();
    this.scene.add(this.measureGroup);

    const cutPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 1e6);
    this.cutPlane = cutPlane;

    this.composer = new EffectComposer(this.renderer, new THREE.WebGLRenderTarget(1, 1, { samples: 4, type: THREE.HalfFloatType }));
    this.renderPass = new RenderPass(this.scene, this.camera);
    this.composer.addPass(this.renderPass);
    this.gtao = new GTAOPass(this.scene, this.camera, 1, 1);
    this.gtao.blendIntensity = 0.85;
    this.composer.addPass(this.gtao);
    this.outline = new OutlinePass(new THREE.Vector2(1, 1), this.scene, this.camera);
    this.outline.edgeStrength = 4; this.outline.edgeThickness = 1.2; this.outline.edgeGlow = 0.2;
    this.outline.visibleEdgeColor.set(0xf59e0b); this.outline.hiddenEdgeColor.set(0xb45309);
    this.composer.addPass(this.outline);
    this.composer.addPass(new OutputPass());

    this.raycaster = new THREE.Raycaster();
    const dom = this.renderer.domElement;
    let down = null;
    dom.addEventListener("pointerdown", (e) => { down = [e.clientX, e.clientY]; });
    dom.addEventListener("pointerup", (e) => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return;
      this._click(e);
    });
    dom.addEventListener("dblclick", (e) => {
      const hit = this._pick(e);
      if (hit) this.focus(hit.object.userData.solid);
    });
    window.addEventListener("keydown", (e) => {
      if (e.target && /input|textarea/i.test(e.target.tagName)) return;
      if (e.key === "Escape") { this.select(null); if (this.measuring) this.toggleMeasure(); }
      else if (e.key === "f" || e.key === "F") this.frame();
      else if (["1", "2", "3", "4"].includes(e.key)) this.setView(["iso", "top", "front", "side"][+e.key - 1]);
    });
  }

  // ── Cena ──
  setScene(payload, { keepCamera = false } = {}) {
    this.payload = payload;
    this.title.textContent = `${this.t.titulo} — ${payload.title || ""}`;
    this.select(null);
    this.model.traverse((o) => { if (o.geometry) o.geometry.dispose(); });
    this.model.clear();
    this.labels = [];
    this.flowMeshes = [];
    this.pickables = [];
    this.byKey = new Map();
    this.systems = new Map((payload.systems || []).map((s) => [s.id, s]));
    const [lo, hi] = payload.bounds;
    this.bounds = new THREE.Box3(new THREE.Vector3(...lo), new THREE.Vector3(...hi));
    // Enquadra o que interessa: tudo menos o terreno, que tem margem de sobra.
    this.frameBox = new THREE.Box3();
    for (const s of payload.solids) {
      if (s.kind === "ground" || !s.box) continue;
      this.frameBox.expandByPoint(new THREE.Vector3(...s.box[0])).expandByPoint(new THREE.Vector3(...s.box[1]));
    }
    if (this.frameBox.isEmpty()) this.frameBox.copy(this.bounds);
    this.diag = Math.max(this.bounds.getSize(new THREE.Vector3()).length(), 1);

    for (const s of payload.solids) {
      const obj = this._solidObject(s);
      if (!obj) continue;
      obj.userData.solid = s;
      obj.traverse((o) => { o.userData.solid = s; });
      if (s.pickable) this.pickables.push(obj);
      if (!this.byKey.has(s.key)) this.byKey.set(s.key, obj);
      this.model.add(obj);
      if (s.label && ["tank", "pump", "filter", "accessory"].includes(s.kind)) {
        const tag = el("div", {}, el("div", { class: "nv-label" }, s.key));
        const lbl = new CSS2DObject(tag);
        lbl.position.set(...s.label);
        lbl.center.set(0.5, 1);
        this.model.add(lbl);
        this.labels.push(lbl);
      }
    }
    this._fitSun();
    this._legend();
    this._componentList();
    this.notes.replaceChildren(...(payload.notes || []).map((n) => el("div", {}, "• " + n)));
    this.cutInput.value = "1000";
    this._applyVisibility();
    this._applyCut();
    if (!keepCamera || !this._framedOnce) { this.setView("iso", false); this._framedOnce = true; }
    window.__netunoVolumetria = { pronto: true, solidos: payload.solids.length, pecas: this.pickables.length, visualizador: this };
  }

  _solidObject(s) {
    const cor = rgb(s.color);
    if (s.kind === "pipe") return this._pipe(s, cor);
    if (s.kind === "ground") return this._ground(s);
    if (s.kind === "building" || s.kind === "slab") return this._fromTris(s, s.kind === "building" ? MAT.vidro() : MAT.laje(), true);
    if (!s.box) return this._fromTris(s, MAT.pintura(cor), false);
    const [lo, hi] = s.box;
    const w = hi[0] - lo[0], d = hi[1] - lo[1], h = hi[2] - lo[2];
    let g;
    switch (s.type) {
      case "cisterna_inferior": g = tanque(w, d, h, cor, true); break;
      case "reservatorio_superior": g = tanque(w, d, h, cor, false); break;
      case "first_flush": g = descarte(w, d, h, cor); break;
      case "filtro_pluvial": g = filtro(w, d, h, cor); break;
      case "motobomba": {
        // A caixa do Python já vem girada; a peça é modelada no próprio eixo.
        const rot = THREE.MathUtils.degToRad(s.rotation || 0);
        const c = Math.abs(Math.cos(rot)), sn = Math.abs(Math.sin(rot));
        const det = c * c - sn * sn;
        let lw = w, ld = d;
        if (Math.abs(det) > 0.2) { lw = (w * c - d * sn) / det; ld = (d * c - w * sn) / det; }
        g = motobomba(Math.max(lw, 0.05), Math.max(ld, 0.05), h, cor);
        g.rotation.z += rot;
        break;
      }
      default: g = acessorio(w, d, h, cor, s.type);
    }
    g.position.set((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]);
    return g;
  }

  _fromTris(s, material, edges) {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(s.tris, 3));
    g.setAttribute("normal", new THREE.Float32BufferAttribute(s.norms, 3));
    const grp = new THREE.Group();
    // Casca e lajes translúcidas não projetam sombra: escureceriam o interior todo.
    const m = mesh(g, material, !(s.kind === "building" || s.kind === "slab"));
    grp.add(m);
    if (edges && s.edges && s.edges.length) {
      const eg = new THREE.BufferGeometry();
      eg.setAttribute("position", new THREE.Float32BufferAttribute(s.edges, 3));
      grp.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.55 })));
    }
    return grp;
  }

  _pipe(s, cor) {
    if (!s.axis) return this._fromTris(s, MAT.pvc(cor), false);
    const a = new THREE.Vector3(s.axis[0], s.axis[1], s.axis[2]);
    const b = new THREE.Vector3(s.axis[3], s.axis[4], s.axis[5]);
    // DN real, com um mínimo para o tubo não sumir na vista de conjunto.
    const r = Math.max((s.dn || s.axis[6] * 2000) / 2000, this.diag * 0.0011);
    const grp = new THREE.Group();
    grp.userData.system = s.system;
    const mat = MAT.pvc(cor);
    if (a.distanceTo(b) < 1e-6) {
      // Nó de mudança de direção: curva representada por uma esfera do mesmo DN.
      grp.add(mesh(new THREE.SphereGeometry(r * 1.12, 20, 14).translate(a.x, a.y, a.z), mat));
      return grp;
    }
    grp.add(mesh(cylinderBetween(a, b, r, 20), mat));
    // Luvas nas pontas: dão leitura de tubo, e não de bastão.
    const dir = new THREE.Vector3().subVectors(b, a).normalize();
    const len = a.distanceTo(b);
    const luva = Math.min(r * 1.6, len * 0.2);
    grp.add(mesh(cylinderBetween(a, a.clone().addScaledVector(dir, luva), r * 1.18, 20), mat));
    grp.add(mesh(cylinderBetween(b.clone().addScaledVector(dir, -luva), b, r * 1.18, 20), mat));
    // Setas de fluxo: casca levemente maior, textura animada no sentido a→b.
    const tex = this.flowTexture.clone();
    tex.needsUpdate = true;
    const spacing = Math.max(r * 8, 0.25);
    tex.repeat.set(1, Math.max(1, len / spacing));
    const flowMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.9, color: 0xffffff });
    const flow = new THREE.Mesh(cylinderBetween(a, b, r * 1.04, 16, true), flowMat);
    flow.userData.flowSpeed = 0.6 / Math.max(1, len / spacing) * (len / spacing);
    flow.renderOrder = 2;
    this.flowMeshes.push(flow);
    grp.add(flow);
    return grp;
  }

  _ground(s) {
    const [lo, hi] = [s.box[0], s.box[1]];
    const w = (hi[0] - lo[0]) * 1.6, d = (hi[1] - lo[1]) * 1.6;
    const tex = texturaDoTerreno(this.root.classList.contains("nv-dark"));
    tex.repeat.set(w, d);
    const mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 1, transparent: true, opacity: 0.82, depthWrite: false, side: THREE.DoubleSide });
    const g = new THREE.PlaneGeometry(w, d);
    g.translate((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0);
    const m = new THREE.Mesh(g, mat);
    m.receiveShadow = true;
    m.renderOrder = -1;
    const grp = new THREE.Group();
    grp.add(m);
    // Camada de solo em corte: mostra o que está enterrado.
    const depth = Math.max(0.5, -this.bounds.min.z + 0.3);
    const solo = new THREE.Mesh(new THREE.BoxGeometry(w, d, depth).translate((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, -depth / 2),
      new THREE.MeshStandardMaterial({ color: 0x8b6b4a, roughness: 1, transparent: true, opacity: 0.12, depthWrite: false }));
    solo.userData.soil = true;
    grp.add(solo);
    return grp;
  }

  _grid() {
    if (this.gridHelper) this.scene.remove(this.gridHelper);
    const size = Math.ceil(this.diag * 2);
    const grid = new THREE.GridHelper(size, size, 0x94a3b8, 0xcbd5e1);
    grid.rotation.x = Math.PI / 2;
    grid.position.set(this.bounds.getCenter(new THREE.Vector3()).x, this.bounds.getCenter(new THREE.Vector3()).y, 0.002);
    grid.material.transparent = true; grid.material.opacity = 0.35; grid.material.depthWrite = false;
    this.gridHelper = grid;
    this.scene.add(grid);
  }

  _fitSun() {
    const c = this.bounds.getCenter(new THREE.Vector3());
    const r = this.diag * 0.75;
    this.sun.position.set(c.x - r * 0.6, c.y - r * 0.9, c.z + r * 1.3);
    this.sun.target.position.copy(c);
    const cam = this.sun.shadow.camera;
    cam.left = cam.bottom = -r; cam.right = cam.top = r;
    cam.near = 0.1; cam.far = r * 5;
    cam.updateProjectionMatrix();
  }

  // ── Painel lateral ──
  _legend() {
    const presentes = new Set(this.payload.solids.filter((s) => s.kind === "pipe").map((s) => s.system));
    this.legend.replaceChildren();
    for (const sys of this.payload.systems || []) {
      if (!presentes.has(sys.id)) continue;
      const cb = el("input", { type: "checkbox" });
      cb.checked = !this.hiddenSystems.has(sys.id);
      cb.addEventListener("change", () => {
        if (cb.checked) this.hiddenSystems.delete(sys.id); else this.hiddenSystems.add(sys.id);
        this._applyVisibility();
      });
      this.legend.append(el("label", {}, cb, el("span", { class: "nv-sw", style: `background:${sys.color}` }), sys.label));
    }
  }

  _componentList() {
    this.list.replaceChildren();
    this.listItems = new Map();
    for (const s of this.payload.solids) {
      if (!s.pickable || s.kind === "pipe" || s.kind === "building" || s.kind === "slab") continue;
      const item = el("div", { class: "nv-item", onclick: () => { this.select(s); this.focus(s); } },
        el("span", { class: "nv-dot", style: `background:rgb(${s.color.join(",")})` }), s.title);
      this.listItems.set(s.key, item);
      this.list.append(item);
    }
  }

  _card(s) {
    const card = el("div", { class: "nv-card" }, el("h3", {}, s.title));
    for (const line of s.info || []) {
      const i = line.indexOf(":");
      if (line.startsWith(" •")) card.append(el("div", { class: "nv-sub" }, line.trim()));
      else if (i > 0 && i < 48 && line.slice(i + 1).trim()) {
        card.append(el("div", { class: "nv-row" }, el("span", { class: "k" }, line.slice(0, i)), el("span", { class: "v" }, line.slice(i + 1).trim())));
      } else card.append(el("div", { class: "nv-row" }, el("span", { class: "k" }, line)));
    }
    return card;
  }

  // ── Interação ──
  _pick(e) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const p = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(p, this.camera);
    const vis = this.pickables.filter((o) => o.visible && this._visibleSolid(o.userData.solid));
    const hits = this.raycaster.intersectObjects(vis, true).filter((h) => h.object.visible && !h.object.userData.xrayOnly
      && (h.object.material && h.object.material.opacity > 0.2 || h.object.userData.solid.kind === "pipe")
      && (!this.cutActive || h.point.z <= this.cutZ + 1e-6));
    return hits[0] || null;
  }

  _click(e) {
    const hit = this._pick(e);
    if (this.measuring) {
      if (hit) this._measurePoint(hit.point.clone());
      return;
    }
    this.select(hit ? hit.object.userData.solid : null);
  }

  select(s) {
    this.selected = s;
    if (this.listItems) for (const [k, item] of this.listItems) item.classList.toggle("sel", !!s && k === s.key);
    if (!s) {
      this.outline.selectedObjects = [];
      this.info.replaceChildren(el("p", { class: "nv-hint" }, this.t.semSelecao));
      return;
    }
    const objs = s.kind === "pipe" && s.group
      ? this.pickables.filter((o) => o.userData.solid.group === s.group)
      : [this.byKey.get(s.key)].filter(Boolean);
    this.outline.selectedObjects = objs;
    this.info.replaceChildren(this._card(s));
  }

  focus(s) {
    const obj = this.byKey.get(s.key);
    if (!obj) return;
    const box = new THREE.Box3().setFromObject(obj);
    const c = box.getCenter(new THREE.Vector3());
    const r = Math.max(box.getSize(new THREE.Vector3()).length(), 0.5);
    const dir = new THREE.Vector3().subVectors(this.camera.position, this.controls.target).normalize();
    this._animateTo(c, c.clone().addScaledVector(dir, r * 2.4));
  }

  _animateTo(target, position, ms = 550) {
    const t0 = performance.now(), fromT = this.controls.target.clone(), fromP = this.camera.position.clone();
    this._anim = (now) => {
      const k = Math.min(1, (now - t0) / ms), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      this.controls.target.lerpVectors(fromT, target, e);
      this.camera.position.lerpVectors(fromP, position, e);
      if (k >= 1) this._anim = null;
    };
  }

  setView(view, animate = true) {
    const c = this.frameBox.getCenter(new THREE.Vector3());
    const dirs = { iso: new THREE.Vector3(-0.9, -1.25, 0.95), top: new THREE.Vector3(0, -0.0001, 1), front: new THREE.Vector3(0, -1, 0.02), side: new THREE.Vector3(1, 0, 0.02) };
    const dir = (dirs[view] || dirs.iso).normalize();
    const dist = this._fitDistance(dir);
    const pos = c.clone().addScaledVector(dir, dist);
    this.root.querySelectorAll("[data-view]").forEach((b) => b.classList.toggle("on", b.dataset.view === view));
    if (animate) this._animateTo(c, pos); else { this.controls.target.copy(c); this.camera.position.copy(pos); this.controls.update(); }
  }

  _fitDistance(dir) {
    // Distância que enquadra a caixa da cena (sem o terreno) no campo de visão.
    const size = this.frameBox.getSize(new THREE.Vector3());
    const fov = THREE.MathUtils.degToRad(this.camera.fov);
    const aspect = this.camera.aspect || 1;
    const right = new THREE.Vector3().crossVectors(dir, UP);
    if (right.lengthSq() < 1e-6) right.set(1, 0, 0);
    right.normalize();
    const up = new THREE.Vector3().crossVectors(right, dir).normalize();
    const half = (v) => Math.abs(v.x) * size.x / 2 + Math.abs(v.y) * size.y / 2 + Math.abs(v.z) * size.z / 2;
    const hw = half(right), hh = half(up), hd = half(dir);
    const dh = hh / Math.tan(fov / 2), dw = hw / (Math.tan(fov / 2) * aspect);
    return Math.max(dh, dw) * 1.06 + hd;
  }

  frame() { const v = this.root.querySelector("[data-view].on"); this.setView(v ? v.dataset.view : "iso"); }

  toggle(k) {
    this.show[k] = !this.show[k];
    this.toggleBtns[k].classList.toggle("on", this.show[k]);
    this._applyVisibility();
  }

  _visibleSolid(s) {
    if (!s) return true;
    if ((s.kind === "building" || s.kind === "slab") && !this.show.building) return false;
    if (s.kind === "ground" && !this.show.ground) return false;
    if (s.kind === "pipe" && this.hiddenSystems.has(s.system)) return false;
    return true;
  }

  _applyVisibility() {
    if (!this.model) return;
    for (const obj of this.model.children) {
      const s = obj.userData.solid;
      if (obj.isCSS2DObject) { obj.visible = this.show.labels; continue; }
      obj.visible = this._visibleSolid(s);
      obj.traverse((o) => {
        if (!o.isMesh) return;
        if (o.userData.xrayOnly) o.visible = this.show.xray;
        if (o.userData.soil) o.visible = this.show.xray;
        const tank = s && (s.kind === "tank" || s.kind === "filter");
        if (tank && !o.userData.xrayOnly && o.material) {
          o.material.transparent = this.show.xray;
          o.material.opacity = this.show.xray ? 0.35 : 1;
          o.material.depthWrite = !this.show.xray;
        }
        if (s && s.kind === "ground" && !o.userData.soil) o.material.opacity = this.show.xray ? 0.35 : 0.82;
      });
    }
    for (const f of this.flowMeshes) f.visible = this.show.flow;
    for (const l of this.labels) l.visible = this.show.labels && (!this.cutActive || l.position.z <= this.cutZ + 0.05);
    this.renderer.shadowMap.enabled = this.show.shadows;
    this.sun.castShadow = this.show.shadows;
    this.scene.background = this.show.sky && this.skyTexture ? this.skyTexture : null;
    this.scene.backgroundBlurriness = 0.25;
    this.scene.traverse((o) => { if (o.material) o.material.needsUpdate = true; });
  }

  _applyCut() {
    const f = Number(this.cutInput.value) / 1000;
    const z0 = this.bounds.min.z, z1 = this.bounds.max.z + 0.01;
    this.cutZ = z0 + (z1 - z0) * f;
    this.cutActive = f < 0.999;
    this.cutPlane.constant = this.cutActive ? this.cutZ : 1e6;
    this.cutLabel.textContent = this.cutActive ? `${this.t.cota} ${this.cutZ.toFixed(2).replace(".", ",")} m` : "";
    const planes = this.cutActive ? [this.cutPlane] : [];
    this.model.traverse((o) => { if (o.material) o.material.clippingPlanes = planes; });
    if (this.labels) for (const l of this.labels) l.visible = this.show.labels && (!this.cutActive || l.position.z <= this.cutZ + 0.05);
  }

  // ── Medição ──
  toggleMeasure() {
    this.measuring = !this.measuring;
    this.measureBtn.classList.toggle("on", this.measuring);
    this.measurePts = [];
    this.measureGroup.clear();
    this._toast(this.measuring ? this.t.medirDica : "");
  }

  _measurePoint(p) {
    this.measurePts.push(p);
    const s = Math.max(this.diag * 0.004, 0.02);
    this.measureGroup.add(new THREE.Mesh(new THREE.SphereGeometry(s, 16, 12).translate(p.x, p.y, p.z), new THREE.MeshBasicMaterial({ color: 0x0f172a, depthTest: false })));
    if (this.measurePts.length === 2) {
      const [a, b] = this.measurePts;
      const g = new THREE.BufferGeometry().setFromPoints([a, b]);
      const line = new THREE.Line(g, new THREE.LineBasicMaterial({ color: 0x0f172a, depthTest: false }));
      line.renderOrder = 10;
      this.measureGroup.add(line);
      const d = a.distanceTo(b);
      const tag = new CSS2DObject(el("div", { class: "nv-measure" }, `${d.toFixed(2).replace(".", ",")} m`));
      tag.position.copy(a.clone().add(b).multiplyScalar(0.5));
      this.measureGroup.add(tag);
      this._toast(`${this.t.distancia}: ${d.toFixed(3).replace(".", ",")} m · Δz ${(b.z - a.z).toFixed(2).replace(".", ",")} m`);
      this.measurePts = [];
    }
  }

  _declutter() {
    // Rótulos que se sobrepõem na tela sobem em degraus, em vez de se cobrirem.
    if (!this.labels || !this.show.labels) return;
    const w = this.stage.clientWidth, h = this.stage.clientHeight;
    const placed = [];
    const items = this.labels.map((l) => {
      const p = l.getWorldPosition(new THREE.Vector3()).project(this.camera);
      return { l, x: (p.x + 1) / 2 * w, y: (1 - p.y) / 2 * h };
    }).sort((a, b) => b.y - a.y);
    for (const it of items) {
      const inner = it.l.element.firstChild;
      const bw = inner.offsetWidth || 40, bh = (inner.offsetHeight || 18) + 2;
      let dy = 0;
      for (let guard = 0; guard < 8; guard++) {
        const hit = placed.find((p) => Math.abs(p.x - it.x) < (p.w + bw) / 2 && Math.abs(p.y - (it.y - dy)) < bh);
        if (!hit) break;
        dy += bh;
      }
      inner.style.transform = `translateY(${-10 - dy}px)`;
      placed.push({ x: it.x, y: it.y - dy, w: bw });
    }
  }

  _toast(msg) { this.toast.textContent = msg; this.toast.style.display = msg ? "block" : "none"; }

  // ── Utilidades ──
  screenshot() {
    this._render();
    const url = this.renderer.domElement.toDataURL("image/png");
    const a = el("a", { href: url, download: `${(this.payload && this.payload.title) || "volumetria"}_3d.png` });
    document.body.append(a); a.click(); a.remove();
  }

  togglePanel() {
    // Recolhe a ficha lateral: o modelo ganha a largura inteira.
    const oculto = this.root.classList.toggle("nv-nopanel");
    this.panelBtn.classList.toggle("on", !oculto);
  }

  toggleTheme() {
    this.root.classList.toggle("nv-dark");
    if (this.payload) this.setScene(this.payload, { keepCamera: true });
  }

  fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (this.root.requestFullscreen) this.root.requestFullscreen();
  }

  _updateScale() {
    if (!this.camera) return;
    const dist = this.camera.position.distanceTo(this.controls.target);
    const pxPerM = this.stage.clientHeight / (2 * dist * Math.tan(THREE.MathUtils.degToRad(this.camera.fov) / 2));
    const nice = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100];
    const m = nice.find((n) => n * pxPerM >= 70) || 100;
    this.scaleBar.replaceChildren(document.createTextNode(`${String(m).replace(".", ",")} m`), el("div", { style: `width:${(m * pxPerM).toFixed(0)}px` }));
  }

  _resize() {
    const w = Math.max(this.stage.clientWidth, 1), h = Math.max(this.stage.clientHeight, 1);
    this.renderer.setSize(w, h, false);
    this.labelRenderer.setSize(w, h);
    this.composer.setSize(w, h);
    this.gtao.setSize(w, h);
    this.outline.resolution.set(w, h);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this._updateScale();
  }

  _render() {
    this.gtao.enabled = this.show.shadows;
    this.composer.render();
    this.labelRenderer.render(this.scene, this.camera);
  }

  _loop() {
    const tick = (now) => {
      requestAnimationFrame(tick);
      this.timer.update(now); const dt = this.timer.getDelta();
      if (this._anim) this._anim(now);
      this.controls.update();
      if (this.show.flow) for (const f of this.flowMeshes) f.material.map.offset.y -= dt * 0.9;
      this.camera.near = Math.max(this.diag / 2000, 0.01);
      this.camera.far = this.diag * 50;
      this.camera.updateProjectionMatrix();
      if ((this._frame = (this._frame || 0) + 1) % 6 === 0) this._declutter();
      this._render();
    };
    this._resize();
    requestAnimationFrame(tick);
  }
}

export function mount(container, opts) {
  const v = new Visualizador(container, opts);
  mount.current = v;
  return v;
}

export function setScene(payload, opts) {
  // Sem WebGL não há o que redesenhar; a aba do programa já trocou de visualizador.
  if (mount.current && mount.current.renderer) mount.current.setScene(payload, opts);
}
