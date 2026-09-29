"""Exportação da volumetria: glTF binário (.glb) e página HTML interativa.

* ``.glb`` (glTF 2.0) abre no Visualizador 3D do Windows, no Blender, no
  SketchUp (com extensão) e em qualquer visualizador web. Cada sólido é um nó
  nomeado com a sua ficha em ``extras``.
* ``.html`` é autocontido: um visualizador WebGL escrito aqui, sem bibliotecas
  nem internet, para girar, aproximar, clicar nas peças e compartilhar.
"""

from __future__ import annotations

import json
import math
import struct
from html import escape
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from .pipe_network import PIPE_SYSTEMS
from .volumetry import Point, Scene, Solid, build_volumetry, face_normal

_ANGLE_FEATURE_DEG = 25.0
# Cascas abertas ou translúcidas de propósito: as duas faces são visíveis.
_DOUBLE_SIDED = {"building", "slab", "ground"}


def _key(p: Point) -> Tuple[float, float, float]:
    return (round(p[0], 3), round(p[1], 3), round(p[2], 3))


def feature_edges(solid: Solid) -> List[List[Tuple[Point, Point]]]:
    """Arestas que marcam a forma, por face: bordas livres e dobras acentuadas.

    Omite as arestas entre faces quase coplanares, como as geratrizes de um
    cilindro facetado, que só poluiriam o desenho.
    """
    normals = [face_normal(face) for face in solid.faces]
    owners: Dict[Tuple, List[int]] = {}
    for index, face in enumerate(solid.faces):
        for a, b in zip(face, list(face[1:]) + [face[0]]):
            owners.setdefault(tuple(sorted((_key(a), _key(b)))), []).append(index)
    limit = math.cos(math.radians(_ANGLE_FEATURE_DEG))
    result: List[List[Tuple[Point, Point]]] = [[] for _ in solid.faces]
    for index, face in enumerate(solid.faces):
        for a, b in zip(face, list(face[1:]) + [face[0]]):
            faces = owners[tuple(sorted((_key(a), _key(b))))]
            others = [f for f in faces if f != index]
            if not others or any(sum(x * y for x, y in zip(normals[index], normals[o])) < limit for o in others):
                result[index].append((a, b))
    return result


def _triangles(face: Sequence[Point]) -> List[Tuple[Point, Point, Point]]:
    return [(face[0], face[i], face[i + 1]) for i in range(1, len(face) - 1)]


# ── glTF binário ─────────────────────────────────────────────────────────────

def _to_gltf(p: Point) -> Tuple[float, float, float]:
    # Netuno: mm, z para cima. glTF: metros, y para cima (rotação própria, preserva a orientação das faces).
    return (p[0] / 1000.0, p[2] / 1000.0, -p[1] / 1000.0)


def write_glb(scene: Scene, output_path: str) -> str:
    binary = bytearray()
    buffer_views, accessors, meshes, nodes, materials = [], [], [], [], []
    material_index: Dict[Tuple, int] = {}

    def add_view(data: bytes, target: int) -> int:
        while len(binary) % 4:
            binary.append(0)
        buffer_views.append({"buffer": 0, "byteOffset": len(binary), "byteLength": len(data), "target": target})
        binary.extend(data)
        return len(buffer_views) - 1

    for solid in scene.solids:
        positions: List[float] = []
        normals: List[float] = []
        for face in solid.faces:
            n = _to_gltf(tuple(c * 1000.0 for c in face_normal(face)))  # type: ignore[arg-type]
            for tri in _triangles(face):
                for p in tri:
                    positions.extend(_to_gltf(p))
                    normals.extend(n)
        if not positions:
            continue
        count = len(positions) // 3
        xs, ys, zs = positions[0::3], positions[1::3], positions[2::3]
        pos_view = add_view(struct.pack(f"<{len(positions)}f", *positions), 34962)
        nor_view = add_view(struct.pack(f"<{len(normals)}f", *normals), 34962)
        accessors.append({"bufferView": pos_view, "componentType": 5126, "count": count, "type": "VEC3",
                          "min": [min(xs), min(ys), min(zs)], "max": [max(xs), max(ys), max(zs)]})
        accessors.append({"bufferView": nor_view, "componentType": 5126, "count": count, "type": "VEC3"})
        mat_key = (solid.color, round(solid.opacity, 3), solid.kind in _DOUBLE_SIDED)
        if mat_key not in material_index:
            r, g, b = (c / 255.0 for c in solid.color)
            material = {"name": f"netuno_{len(materials)}", "doubleSided": solid.kind in _DOUBLE_SIDED,
                        "pbrMetallicRoughness": {"baseColorFactor": [r, g, b, solid.opacity], "metallicFactor": 0.0, "roughnessFactor": 0.8}}
            if solid.opacity < 1.0:
                material["alphaMode"] = "BLEND"
            materials.append(material)
            material_index[mat_key] = len(materials) - 1
        meshes.append({"name": solid.key, "primitives": [{"attributes": {"POSITION": len(accessors) - 2, "NORMAL": len(accessors) - 1},
                                                           "material": material_index[mat_key]}]})
        nodes.append({"name": solid.key, "mesh": len(meshes) - 1,
                      "extras": {"titulo": solid.title, "ficha": solid.info, "tipo": solid.kind}})

    while len(binary) % 4:
        binary.append(0)
    document = {
        "asset": {"version": "2.0", "generator": "Netuno 5 — volumetria"},
        "scene": 0,
        "scenes": [{"name": scene.title, "nodes": list(range(len(nodes))), "extras": {"notas": scene.notes, "unidades": "m, y para cima"}}],
        "nodes": nodes, "meshes": meshes, "materials": materials, "accessors": accessors,
        "bufferViews": buffer_views, "buffers": [{"byteLength": len(binary)}],
    }
    json_chunk = json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    json_chunk += b" " * ((4 - len(json_chunk) % 4) % 4)
    total = 12 + 8 + len(json_chunk) + 8 + len(binary)
    data = b"".join([
        struct.pack("<4sII", b"glTF", 2, total),
        struct.pack("<I4s", len(json_chunk), b"JSON"), json_chunk,
        struct.pack("<I4s", len(binary), b"BIN\x00"), bytes(binary),
    ])
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


def write_volumetry_package(project_data: Dict, stem: str) -> Tuple[str, str]:
    """Grava ``<stem>_volumetria.glb`` e ``<stem>_volumetria.html`` da mesma cena."""
    scene = build_volumetry(project_data)
    return write_glb(scene, f"{stem}_volumetria.glb"), write_html_viewer(scene, f"{stem}_volumetria.html")


# ── HTML interativo ──────────────────────────────────────────────────────────

def scene_payload(scene: Scene) -> Dict:
    """Cena em metros, pronta para o visualizador: triângulos, arestas e fichas."""
    solids = []
    for solid in scene.solids:
        tris: List[float] = []
        norms: List[float] = []
        for face in solid.faces:
            n = face_normal(face)
            for tri in _triangles(face):
                for p in tri:
                    tris.extend(round(c / 1000.0, 4) for c in p)
                    norms.extend(round(c, 4) for c in n)
        edges: List[float] = []
        if solid.outline:
            seen = set()
            for face_edges in feature_edges(solid):
                for a, b in face_edges:
                    k = tuple(sorted((_key(a), _key(b))))
                    if k not in seen:
                        seen.add(k)
                        edges.extend(round(c / 1000.0, 4) for c in (*a, *b))
        solids.append({
            "key": solid.key, "kind": solid.kind, "title": solid.title, "info": solid.info,
            "color": list(solid.color), "opacity": solid.opacity, "pickable": solid.pickable, "group": solid.group,
            "label": [round(c / 1000.0, 4) for c in solid.label_at] if solid.label_at else None,
            "tris": tris, "norms": norms, "edges": edges,
        })
    low, high = scene.bounds
    return {"title": scene.title, "notes": scene.notes, "solids": solids,
            "bounds": [[c / 1000.0 for c in low], [c / 1000.0 for c in high]],
            "systems": [{"label": s["label"], "color": s["svg"]} for s in PIPE_SYSTEMS]}


def write_html_viewer(scene: Scene, output_path: str) -> str:
    payload = json.dumps(scene_payload(scene), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = _HTML_TEMPLATE.replace("__TITLE__", escape(scene.title)).replace("__SCENE__", payload)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return str(path)


_HTML_TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Volumetria 3D — __TITLE__</title>
<style>
  :root { --bg:#f8fafc; --panel:#ffffff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0; --accent:#1d4ed8; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0b1220; --panel:#111a2e; --ink:#e2e8f0; --muted:#94a3b8; --line:#1e293b; --accent:#60a5fa; } }
  * { box-sizing: border-box; }
  html, body { margin:0; height:100%; background:var(--bg); color:var(--ink); font:14px/1.4 "Segoe UI", system-ui, sans-serif; }
  #app { display:grid; grid-template-columns: 1fr 300px; height:100%; }
  #stage { position:relative; overflow:hidden; }
  canvas { position:absolute; inset:0; width:100%; height:100%; display:block; touch-action:none; }
  #gl { cursor:grab; } #gl.dragging { cursor:grabbing; }
  #overlay { pointer-events:none; }
  header { position:absolute; left:16px; top:12px; right:16px; pointer-events:none; }
  header h1 { margin:0; font-size:17px; } header p { margin:2px 0 0; color:var(--muted); font-size:12px; }
  .toolbar { position:absolute; left:16px; bottom:16px; display:flex; flex-wrap:wrap; gap:6px; }
  button, label.toggle { font:inherit; font-size:12.5px; border:1px solid var(--line); background:var(--panel); color:var(--ink);
    padding:6px 10px; border-radius:8px; cursor:pointer; display:inline-flex; align-items:center; gap:6px; }
  button:hover { border-color:var(--accent); }
  aside { border-left:1px solid var(--line); background:var(--panel); padding:16px; overflow:auto; }
  aside h2 { font-size:13px; margin:0 0 8px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
  .legend div { display:flex; align-items:center; gap:8px; margin:4px 0; font-size:13px; }
  .sw { width:22px; height:6px; border-radius:3px; }
  #info { margin-top:18px; } #info h3 { margin:0 0 6px; font-size:15px; } #info li { margin:3px 0; }
  #info ul { padding-left:18px; margin:0; } .hint { color:var(--muted); font-size:12.5px; }
  .notes { margin-top:18px; font-size:12px; color:var(--muted); }
  @media (max-width: 760px) { #app { grid-template-columns: 1fr; grid-template-rows: 1fr auto; } aside { max-height:40vh; border-left:0; border-top:1px solid var(--line); } header p { display:none; } }
</style>
</head>
<body>
<div id="app">
  <div id="stage">
    <canvas id="gl"></canvas><canvas id="overlay"></canvas>
    <header><h1>Volumetria 3D — __TITLE__</h1><p>Arraste para girar · botão direito ou Shift para deslocar · roda para aproximar · clique numa peça</p></header>
    <div class="toolbar">
      <button data-view="persp">Perspectiva</button><button data-view="top">Planta</button>
      <button data-view="front">Frente</button><button data-view="side">Lateral</button>
      <label class="toggle"><input type="checkbox" id="tBuilding" checked> Edificação</label>
      <label class="toggle"><input type="checkbox" id="tGround" checked> Terreno</label>
      <label class="toggle"><input type="checkbox" id="tLabels" checked> Rótulos</label>
      <button id="btnFs" title="Alternar tela cheia (F11)">⛶ Tela cheia</button>
    </div>
  </div>
  <aside>
    <h2>Sistemas</h2><div class="legend" id="legend"></div>
    <div id="info"><p class="hint">Clique num reservatório, motor ou trecho para ver a ficha.</p></div>
    <div class="notes" id="notes"></div>
  </aside>
</div>
<script>
"use strict";
const SCENE = __SCENE__;
const gl = document.getElementById("gl").getContext("webgl", {antialias:true, alpha:false});
const overlay = document.getElementById("overlay"), ctx = overlay.getContext("2d");
if (!gl) { document.getElementById("info").innerHTML = "<p>Este navegador não oferece WebGL.</p>"; throw new Error("WebGL"); }

// ── Shaders: iluminação difusa de duas luzes + ambiente, cor por sólido.
const vs = `attribute vec3 p; attribute vec3 n; uniform mat4 mvp; varying vec3 vn;
  void main(){ vn = n; gl_Position = mvp * vec4(p, 1.0); }`;
const fs = `precision mediump float; varying vec3 vn; uniform vec4 color; uniform float lit;
  void main(){ vec3 N = normalize(vn); float d = 0.42 + 0.45*max(dot(N, normalize(vec3(0.4,0.3,0.85))),0.0)
    + 0.18*max(dot(N, normalize(vec3(-0.6,-0.5,0.2))),0.0); gl_FragColor = vec4(mix(color.rgb, color.rgb*d, lit), color.a); }`;
function shader(type, src){ const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }
const prog = gl.createProgram(); gl.attachShader(prog, shader(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, fs));
gl.linkProgram(prog); gl.useProgram(prog);
const aP = gl.getAttribLocation(prog, "p"), aN = gl.getAttribLocation(prog, "n");
const uMVP = gl.getUniformLocation(prog, "mvp"), uColor = gl.getUniformLocation(prog, "color"), uLit = gl.getUniformLocation(prog, "lit");
function buffer(data){ const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW); return b; }

const solids = SCENE.solids.map(s => ({...s, vb: buffer(s.tris), nb: buffer(s.norms), eb: s.edges.length ? buffer(s.edges) : null,
  center: centroid(s.tris), count: s.tris.length/3, ecount: s.edges.length/3 }));
function centroid(t){ let x=0,y=0,z=0,n=t.length/3; for(let i=0;i<t.length;i+=3){x+=t[i];y+=t[i+1];z+=t[i+2];} return [x/n,y/n,z/n]; }

// ── Câmera orbital (z para cima).
const [lo, hi] = SCENE.bounds, target0 = [(lo[0]+hi[0])/2, (lo[1]+hi[1])/2, (lo[2]+hi[2])/2];
const radius0 = Math.hypot(hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]) || 1;
const cam = { yaw:-0.75, pitch:0.55, dist:radius0*1.35, target:[...target0], ortho:false };
const VIEWS = { persp:[-0.75,0.55,false], top:[-Math.PI/2,1.5707,true], front:[-Math.PI/2,0.0,true], side:[0,0.0,true] };
let selected = null, show = {building:true, ground:true, labels:true}, autoFit = true;

function sub(a,b){return [a[0]-b[0],a[1]-b[1],a[2]-b[2]];} function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function norm(a){const l=Math.hypot(...a)||1;return [a[0]/l,a[1]/l,a[2]/l];}
function eye(){ const c=Math.cos(cam.pitch); return [cam.target[0]+cam.dist*c*Math.cos(cam.yaw), cam.target[1]+cam.dist*c*Math.sin(cam.yaw), cam.target[2]+cam.dist*Math.sin(cam.pitch)]; }
function basis(){ const e=eye(), f=norm(sub(cam.target,e)); let up=[0,0,1]; if (Math.abs(dot(f,up))>0.999) up=[-Math.cos(cam.yaw),-Math.sin(cam.yaw),0]; // vista de cima: o "à frente" vira o alto da tela
  const r=norm(cross(f,up)), u=cross(r,f); return {e,f,r,u}; }
function matrices(){
  const W=gl.canvas.width, H=gl.canvas.height, asp=W/H, {e,f,r,u}=basis();
  const view=[r[0],u[0],-f[0],0, r[1],u[1],-f[1],0, r[2],u[2],-f[2],0, -dot(r,e),-dot(u,e),dot(f,e),1];
  const near=cam.dist/200, far=cam.dist*20; let proj;
  if (cam.ortho){ const h=cam.dist*0.45, w=h*asp; proj=[1/w,0,0,0, 0,1/h,0,0, 0,0,-2/(far-near),0, 0,0,-(far+near)/(far-near),1]; }
  else { const t=1/Math.tan(0.35); proj=[t/asp,0,0,0, 0,t,0,0, 0,0,(far+near)/(near-far),-1, 0,0,2*far*near/(near-far),0]; }
  return mul(proj, view);
}
function mul(a,b){ const o=new Array(16).fill(0); for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k]; return o; }
function project(m,p){ const x=m[0]*p[0]+m[4]*p[1]+m[8]*p[2]+m[12], y=m[1]*p[0]+m[5]*p[1]+m[9]*p[2]+m[13], w=m[3]*p[0]+m[7]*p[1]+m[11]*p[2]+m[15];
  return w<=0?null:[(x/w*0.5+0.5)*overlay.clientWidth, (1-(y/w*0.5+0.5))*overlay.clientHeight]; }

// Enquadra pelas extensões projetadas (não pela esfera envolvente, que sobra).
function fit(fill=0.82){ const W=overlay.clientWidth, H=overlay.clientHeight; if(W<50||H<50) return;
  const pts=[]; solids.filter(s=>visible(s)&&s.kind!=="ground").forEach(s=>{ for(let i=0;i<s.tris.length;i+=9) pts.push([s.tris[i],s.tris[i+1],s.tris[i+2]]); });
  for(let it=0; it<4; it++){ let m=matrices(), xs=[], ys=[]; pts.forEach(p=>{ const q=project(m,p); if(q){xs.push(q[0]); ys.push(q[1]);} });
    if(!xs.length) return; const ratio=Math.max((Math.max(...xs)-Math.min(...xs))/W,(Math.max(...ys)-Math.min(...ys))/H); if(ratio<=0) return;
    cam.dist=Math.max(radius0*0.05,Math.min(radius0*8,cam.dist*ratio/fill)); m=matrices(); xs=[]; ys=[];
    pts.forEach(p=>{ const q=project(m,p); if(q){xs.push(q[0]); ys.push(q[1]);} });
    const {r,u}=basis(), k=cam.dist/H*(cam.ortho?0.9:0.7), dx=(Math.max(...xs)+Math.min(...xs))/2-W/2, dy=(Math.max(...ys)+Math.min(...ys))/2-H/2;
    for(let i=0;i<3;i++) cam.target[i]+=(dx*r[i]-dy*u[i])*k; } }
function visible(s){ return !((s.kind==="building"||s.kind==="slab") && !show.building) && !(s.kind==="ground" && !show.ground); }
function sizeCanvases(){ const dpr=window.devicePixelRatio||1, W=gl.canvas.clientWidth, H=gl.canvas.clientHeight;
  for (const c of [gl.canvas, overlay]) if (c.width!==Math.round(W*dpr)||c.height!==Math.round(H*dpr)){ c.width=Math.round(W*dpr); c.height=Math.round(H*dpr); } }
function draw(){
  sizeCanvases();
  gl.viewport(0,0,gl.canvas.width,gl.canvas.height);
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  gl.clearColor(dark?0.043:0.973, dark?0.07:0.98, dark?0.125:0.988, 1); gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  const m=matrices(), e=eye(); gl.uniformMatrix4fv(uMVP,false,new Float32Array(m));
  gl.enable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  const vis=solids.filter(visible), opaque=vis.filter(s=>s.opacity>=1), clear=vis.filter(s=>s.opacity<1)
    .sort((a,b)=>Math.hypot(...sub(b.center,e))-Math.hypot(...sub(a.center,e)));
  gl.depthMask(true); opaque.forEach(s=>mesh(s)); gl.depthMask(false); clear.forEach(s=>mesh(s)); gl.depthMask(true);
  vis.forEach(s=>{ if(!s.eb) return; edges(s); });
  labels(m);
}
function mesh(s){ if(s.kind==="building"||s.kind==="slab"||s.kind==="ground") gl.disable(gl.CULL_FACE); else gl.enable(gl.CULL_FACE);
  const hi=selected && (selected.group ? selected.group===s.group : selected.key===s.key);
  const col=hi?[0.96,0.62,0.04]:s.color.map(v=>v/255);
  gl.uniform4f(uColor,col[0],col[1],col[2],hi?(s.kind==="building"?0.3:Math.max(s.opacity,0.85)):s.opacity); gl.uniform1f(uLit,1);
  gl.bindBuffer(gl.ARRAY_BUFFER,s.vb); gl.vertexAttribPointer(aP,3,gl.FLOAT,false,0,0); gl.enableVertexAttribArray(aP);
  gl.bindBuffer(gl.ARRAY_BUFFER,s.nb); gl.vertexAttribPointer(aN,3,gl.FLOAT,false,0,0); gl.enableVertexAttribArray(aN);
  gl.drawArrays(gl.TRIANGLES,0,s.count); }
function edges(s){ gl.disable(gl.CULL_FACE); const k=s.kind==="building"||s.kind==="slab"||s.kind==="ground"?0.45:0.35;
  gl.uniform4f(uColor,s.color[0]/255*k,s.color[1]/255*k,s.color[2]/255*k,s.kind==="slab"?0.35:0.8); gl.uniform1f(uLit,0);
  gl.bindBuffer(gl.ARRAY_BUFFER,s.eb); gl.vertexAttribPointer(aP,3,gl.FLOAT,false,0,0); gl.enableVertexAttribArray(aP);
  gl.disableVertexAttribArray(aN); gl.vertexAttrib3f(aN,0,0,1); gl.drawArrays(gl.LINES,0,s.ecount); }
function labels(m){ const dpr=window.devicePixelRatio||1; ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,overlay.width,overlay.height);
  if(!show.labels) return; ctx.font="600 12px Segoe UI, system-ui, sans-serif"; ctx.textBaseline="bottom";
  const ink=getComputedStyle(document.body).getPropertyValue("--ink"), bg=getComputedStyle(document.body).getPropertyValue("--bg");
  solids.filter(s=>s.label && visible(s)).forEach(s=>{ const q=project(m,s.label); if(!q) return; const t=s.key;
    ctx.lineWidth=4; ctx.strokeStyle=bg; ctx.strokeText(t,q[0]+6,q[1]-6); ctx.fillStyle=ink; ctx.fillText(t,q[0]+6,q[1]-6);
    ctx.beginPath(); ctx.arc(q[0],q[1],2.5,0,7); ctx.fill(); }); }

// ── Seleção: raio contra os triângulos das peças clicáveis (Möller–Trumbore).
function pick(px,py){ const {e,f,r,u}=basis(), W=overlay.clientWidth, H=overlay.clientHeight, asp=W/H;
  const nx=(px/W)*2-1, ny=1-(py/H)*2; let o,d;
  if(cam.ortho){ const h=cam.dist*0.45; o=[e[0]+r[0]*nx*h*asp+u[0]*ny*h, e[1]+r[1]*nx*h*asp+u[1]*ny*h, e[2]+r[2]*nx*h*asp+u[2]*ny*h]; d=f; }
  else { const t=Math.tan(0.35); o=e; d=norm([f[0]+r[0]*nx*t*asp+u[0]*ny*t, f[1]+r[1]*nx*t*asp+u[1]*ny*t, f[2]+r[2]*nx*t*asp+u[2]*ny*t]); }
  let best=null, bestT=Infinity;
  for(const s of solids){ if(!s.pickable||!visible(s)) continue; const T=s.tris;
    for(let i=0;i<T.length;i+=9){ const a=[T[i],T[i+1],T[i+2]], e1=sub([T[i+3],T[i+4],T[i+5]],a), e2=sub([T[i+6],T[i+7],T[i+8]],a);
      const pv=cross(d,e2), det=dot(e1,pv); if(Math.abs(det)<1e-12) continue; const inv=1/det, tv=sub(o,a), uu=dot(tv,pv)*inv; if(uu<0||uu>1) continue;
      const qv=cross(tv,e1), vv=dot(d,qv)*inv; if(vv<0||uu+vv>1) continue; const t=dot(e2,qv)*inv;
      // Edificação translúcida só é escolhida se nada estiver dentro dela na linha do clique.
      const bias = s.kind==="building" ? radius0*10 : 0; if(t>0 && t+bias<bestT){ bestT=t+bias; best=s; } } }
  return best; }
function showInfo(s){ const el=document.getElementById("info");
  if(!s){ el.innerHTML='<p class="hint">Clique num reservatório, motor ou trecho para ver a ficha.</p>'; return; }
  el.innerHTML="<h3></h3><ul></ul>"; el.querySelector("h3").textContent=s.title;
  const ul=el.querySelector("ul"); s.info.forEach(t=>{ const li=document.createElement("li"); li.textContent=t; ul.appendChild(li); }); }

// ── Interação.
const canvas=gl.canvas; let drag=null;
canvas.addEventListener("contextmenu",e=>e.preventDefault());
canvas.addEventListener("pointerdown",e=>{ canvas.setPointerCapture(e.pointerId); drag={x:e.clientX,y:e.clientY,pan:e.button!==0||e.shiftKey,moved:false}; canvas.classList.add("dragging"); });
canvas.addEventListener("pointermove",e=>{ if(!drag) return; const dx=e.clientX-drag.x, dy=e.clientY-drag.y; if(Math.abs(dx)+Math.abs(dy)>2){ drag.moved=true; autoFit=false; }
  drag.x=e.clientX; drag.y=e.clientY;
  if(drag.pan){ const {r,u}=basis(), k=cam.dist/overlay.clientHeight; for(let i=0;i<3;i++) cam.target[i]+=(-dx*r[i]+dy*u[i])*k; }
  else { cam.yaw-=dx*0.008; cam.pitch=Math.max(-1.55,Math.min(1.5707,cam.pitch+dy*0.008)); cam.ortho=false; }
  draw(); });
canvas.addEventListener("pointerup",e=>{ canvas.classList.remove("dragging"); const r=canvas.getBoundingClientRect();
  if(drag && !drag.moved){ selected=pick(e.clientX-r.left,e.clientY-r.top); showInfo(selected); draw(); } drag=null; });
canvas.addEventListener("wheel",e=>{ e.preventDefault(); autoFit=false; cam.dist=Math.max(radius0*0.05,Math.min(radius0*8,cam.dist*Math.exp(e.deltaY*0.0012))); draw(); },{passive:false});
document.querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>{ const [y,p,o]=VIEWS[b.dataset.view];
  cam.yaw=y; cam.pitch=p; cam.ortho=o; cam.dist=radius0*1.35; cam.target=[...target0]; sizeCanvases(); fit(); draw(); }));
[["tBuilding","building"],["tGround","ground"],["tLabels","labels"]].forEach(([id,k])=>document.getElementById(id).addEventListener("change",e=>{ show[k]=e.target.checked; draw(); }));
window.addEventListener("resize",()=>{ sizeCanvases(); if(autoFit) fit(); draw(); }); matchMedia("(prefers-color-scheme: dark)").addEventListener("change",draw);

const used=new Set(solids.filter(s=>s.kind==="pipe").map(s=>s.title.split(" · ")[1]));
document.getElementById("legend").innerHTML=SCENE.systems.filter(s=>used.has(s.label)).map(s=>`<div><span class="sw" style="background:${s.color}"></span>${s.label}</div>`).join("")||'<p class="hint">Sem trechos.</p>';
document.getElementById("notes").textContent=SCENE.notes.join(" ");

const btnFs=document.getElementById("btnFs");
function updateFsBtn(){
  const isFs=!!(document.fullscreenElement||document.webkitFullscreenElement);
  if(btnFs){
    btnFs.textContent=isFs?"🗗 Minimizar":"⛶ Tela cheia";
    btnFs.title=isFs?"Sair da tela cheia / Minimizar (Esc ou F11)":"Alternar modo tela cheia (F11)";
  }
}
if(btnFs){
  btnFs.addEventListener("click",()=>{
    if(!document.fullscreenElement&&!document.webkitFullscreenElement){
      const el=document.documentElement;
      if(el.requestFullscreen) el.requestFullscreen().catch(()=>{});
      else if(el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    } else {
      if(document.exitFullscreen) document.exitFullscreen().catch(()=>{});
      else if(document.webkitExitFullscreen) document.webkitExitFullscreen();
    }
  });
}
document.addEventListener("fullscreenchange",updateFsBtn);
document.addEventListener("webkitfullscreenchange",updateFsBtn);
window.addEventListener("keydown",e=>{ if(e.key==="F11"){ e.preventDefault(); if(btnFs) btnFs.click(); } });

sizeCanvases(); fit(); draw();
</script>
</body>
</html>
"""
