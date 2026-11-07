# -*- coding: utf-8 -*-
"""Mede o espaço que uma base por células da Península ocuparia, com a E-OBS (1950-2025) em três codificações."""
import random, zlib, os
import numpy as np
import xarray as xr

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402
ds = xr.open_dataset(C.EOBS_NC)
anos = []
for a in range(1950, 2026):
    anos.append(ds.rr.sel(time=str(a), latitude=slice(36, 43.9), longitude=slice(-9.6, 4.4)).values)
x = np.concatenate(anos, axis=0)                       # (dias, lat, lon)
terra = np.isfinite(x[:365 * 3]).all(axis=0)
n = int(terra.sum()); print("células com dado:", n, "forma:", x.shape, flush=True)
ii = np.argwhere(terra); rng = random.Random(1)
f32, u16, planos = [], [], []
for k in rng.sample(range(len(ii)), 40):
    s = x[:, ii[k][0], ii[k][1]]
    f32.append(len(zlib.compress(s.astype(np.float32).tobytes(), 9)))
    q = np.where(np.isfinite(s), np.round(s * 10), 65535).astype(np.uint16)
    u16.append(len(zlib.compress(q.tobytes(), 9)))
    planos.append(len(zlib.compress(q.view(np.uint8).reshape(-1, 2).T.tobytes(), 9)))
for nome, v in (("float32+zlib", f32), ("uint16 0,1 mm+zlib", u16), ("uint16 em planos de byte+zlib", planos)):
    print("%-32s %.1f KB por célula | Península (%d células): %.0f MB" % (nome, np.mean(v) / 1024, n, n * np.mean(v) / 1e6))
