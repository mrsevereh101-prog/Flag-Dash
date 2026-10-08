#!/usr/bin/env python3
"""Cut game icons out of a chroma-key sheet (green or magenta background).

usage: cut.py SHEET green|magenta OUTDIR id1 id2 ... [--size 256] [--hi 0.2 --lo 0]
Ids are given in reading order: left to right, then top row before bottom row.
Writes OUTDIR/<id>.webp (square, transparent) and prints one line per icon.
--hi/--lo set the key strength (0..1) where a pixel starts to count as object and where it is solid.
Lower them for an object with a coloured glow around it, so the glow is dropped.
"""
import sys
from collections import deque
import numpy as np
from PIL import Image

VALUED = ('--size', '--hi', '--lo')
def opt(name, default):
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and sys.argv[i - 1] not in VALUED]
SIZE = int(opt('--size', 256))
sheet, bg, outdir, ids = args[0], args[1], args[2], args[3:]
assert bg in ('green', 'magenta') and ids

a = np.asarray(Image.open(sheet).convert('RGB')).astype(np.float32) / 255
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
K = g - np.maximum(r, b) if bg == 'green' else np.minimum(r, b) - g   # how "screen-coloured" a pixel is

edge = np.zeros((H, W), bool); edge[:10] = edge[-10:] = True; edge[:, :10] = edge[:, -10:] = True
Kb = float(np.percentile(K[edge], 10))          # key strength of the background
B = np.median(a[edge], axis=0)                  # background colour
hi = opt('--hi', Kb - 0.06)                      # anything below this starts to be object
lo = opt('--lo', 0.15)                           # anything below this is solid object
alpha = np.clip((hi - K) / (hi - lo), 0, 1)

# take the background colour back out of soft edges, then remove any leftover tint
al = alpha[..., None]
F = np.where(al > 0.02, (a - (1 - al) * B) / np.maximum(al, 0.02), a)
F = np.clip(F, 0, 1)
if bg == 'green':
    F[..., 1] = np.minimum(F[..., 1], np.maximum(F[..., 0], F[..., 2]))
else:
    m = np.clip(np.minimum(F[..., 0], F[..., 2]) - F[..., 1], 0, None)
    F[..., 0] -= m; F[..., 2] -= m

# find the objects on a 4x smaller mask, merging nearby bits (a flame next to a shoe)
S = 4
small = alpha[:H - H % S, :W - W % S].reshape(H // S, S, W // S, S).max(axis=(1, 3)) > 0.35
R = 4
dil = small.copy()
for dy in range(-R, R + 1):
    for dx in range(-R, R + 1):
        dil |= np.roll(np.roll(small, dy, 0), dx, 1)
h, w = dil.shape
lab = np.zeros((h, w), int); comps = []
for y0 in range(h):
    for x0 in range(w):
        if dil[y0, x0] and not lab[y0, x0]:
            n = len(comps) + 1; q = deque([(y0, x0)]); lab[y0, x0] = n; pts = []
            while q:
                y, x = q.popleft(); pts.append((y, x))
                for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if 0 <= yy < h and 0 <= xx < w and dil[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n; q.append((yy, xx))
            ys, xs = zip(*pts)
            comps.append({'n': n, 'area': len(pts), 'cy': np.mean(ys), 'cx': np.mean(xs)})
comps.sort(key=lambda c: -c['area'])
big, rest = comps[:len(ids)], comps[len(ids):]
if len(big) < len(ids):
    sys.exit(f'found only {len(big)} objects, expected {len(ids)}')
# fold leftover specks into the nearest object
for c in rest:
    near = min(big, key=lambda o: (o['cy'] - c['cy']) ** 2 + (o['cx'] - c['cx']) ** 2)
    lab[lab == c['n']] = near['n']
# reading order: rows by height, then left to right
big.sort(key=lambda c: c['cy'])
rows = 2 if len(ids) == 6 else 1
per = len(ids) // rows
order = []
for i in range(rows):
    order += sorted(big[i * per:(i + 1) * per], key=lambda c: c['cx'])

full = np.kron(lab, np.ones((S, S), int))
full = np.pad(full, ((0, H - full.shape[0]), (0, W - full.shape[1])), mode='edge')
for c, name in zip(order, ids):
    m = (full == c['n'])
    A = np.where(m, alpha, 0)
    ys, xs = np.nonzero(A > 0.02)
    y1, y2, x1, x2 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([F[y1:y2, x1:x2], A[y1:y2, x1:x2]])
    img = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), 'RGBA')
    side = int(max(img.size) * 1.08)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(img, ((side - img.size[0]) // 2, (side - img.size[1]) // 2))
    sq = sq.convert('RGBa').resize((SIZE, SIZE), Image.LANCZOS).convert('RGBA')
    sq.save(f'{outdir}/{name}.webp', 'WEBP', quality=90, method=6)
    print(f'{name}: {x2 - x1}x{y2 - y1} at {x1},{y1}')
