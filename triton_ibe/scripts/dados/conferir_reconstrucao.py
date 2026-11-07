# -*- coding: utf-8 -*-
"""Confere, concelho a concelho, a série reconstruída do ibe_prototipo.db contra o portugal_eobs.db atual e lista os que divergem."""
import os, re, sqlite3, zlib
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import construir_banco_ibe as cb

AQUI = cb.AQUI
novo = sqlite3.connect(os.path.join(AQUI, "ibe_prototipo.db"))
velho = sqlite3.connect(f"file:{cb.BASE_ATUAL}?mode=ro", uri=True)
linhas = []
for uid, nome, in novo.execute("select id, nome from unidade"):
    w = novo.execute("select ponto_id, peso, metodo from unidade_ponto where unidade_id=?", (uid,)).fetchall()
    s = np.zeros(27759)
    for pid, peso, m in w:
        parts = [cb.decodificar(b, d) for d, b in novo.execute("select dias, dados from serie_bloco where ponto_id=? order by ano_ini", (pid,))]
        s += peso * np.concatenate(parts)
    r = velho.execute("select dados, metodo from series where dtmn=?", (uid[3:],)).fetchone()
    ref = np.frombuffer(zlib.decompress(r[0]), dtype=np.float32).astype(float)
    n_velho = int(re.search(r"(\d+) c", r[1]).group(1)) if re.search(r"(\d+) c", r[1]) else 1
    d = np.abs(s - ref)
    linhas.append((float(np.nanmax(d)), nome, len(w), n_velho, w[0][2], r[1], int(np.isnan(s).sum()), int(np.isnan(ref).sum())))
linhas.sort(reverse=True)
print("concelhos com diferença máxima > 0,1 mm:", sum(1 for l in linhas if l[0] > 0.1), "de", len(linhas))
for l in linhas[:12]:
    print("%7.2f mm  %-24s células novo=%d velho=%d (%s) | %s | NaN novo=%d velho=%d" % l)
