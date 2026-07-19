"""Renders assets/profile-cube.png: my GitHub avatar as a spinning cube (APNG).

Usage: python assets/cube.py
Deps:  pillow, numpy
"""
import io
import os
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

AVATAR_URL = "https://github.com/jianrontan.png?size=460"
OUT = os.path.join(os.path.dirname(__file__), "profile-cube.png")

W = H = 300
N_FRAMES = 72
DIST = 5.0
FOCAL = W * 0.92
TILT = -0.35  # radians about x-axis; tips the top face toward the viewer
TEX = 256

avatar = Image.open(io.BytesIO(urllib.request.urlopen(AVATAR_URL).read()))
avatar = avatar.convert("RGBA").resize((TEX, TEX), Image.LANCZOS)

# texture corners in TL, TR, BR, BL order
SRC = [(0, 0), (TEX, 0), (TEX, TEX), (0, TEX)]

# side faces: (corners TL,TR,BR,BL in local coords, outward normal)
FACES = [
    ([(-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)], (0, 0, -1)),   # front
    ([(1, 1, -1), (1, 1, 1), (1, -1, 1), (1, -1, -1)], (1, 0, 0)),        # right
    ([(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)], (0, 0, 1)),        # back
    ([(-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1)], (-1, 0, 0)),   # left
]
TOP = ([(-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1)], (0, 1, 0))
TOP_COLOR = (30, 34, 42)

LIGHT = np.array([0.35, 0.55, -0.76])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def rot_matrix(theta):
    ry = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)],
    ])
    rx = np.array([
        [1, 0, 0],
        [0, np.cos(TILT), -np.sin(TILT)],
        [0, np.sin(TILT), np.cos(TILT)],
    ])
    return rx @ ry


def project(pts):
    out = []
    zs = []
    for p in pts:
        z = p[2] + DIST
        out.append((W / 2 + p[0] * FOCAL / z, H / 2 - p[1] * FOCAL / z))
        zs.append(z)
    return out, sum(zs) / len(zs)


def find_coeffs(pa, pb):
    """Homography coeffs for Image.transform PERSPECTIVE: output quad pa -> source corners pb."""
    m = []
    for (x, y), (u, v) in zip(pa, pb):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(m, dtype=np.float64)
    B = np.array(pb, dtype=np.float64).reshape(8)
    return np.linalg.solve(A, B)


def shade(tex, brightness):
    arr = np.asarray(tex, dtype=np.float64).copy()
    arr[..., :3] *= brightness
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


frames = []
for i in range(N_FRAMES):
    theta = 2 * np.pi * i / N_FRAMES
    R = rot_matrix(theta)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    drawlist = []
    for corners, normal in FACES + [TOP]:
        n = R @ np.array(normal, dtype=np.float64)
        if n[2] >= 0:  # backface: camera is at z=0 looking toward +z
            continue
        pts = [R @ np.array(c, dtype=np.float64) for c in corners]
        quad, depth = project(pts)
        brightness = 0.45 + 0.55 * max(0.0, float(n @ LIGHT))
        drawlist.append((depth, quad, brightness, normal == (0, 1, 0)))

    drawlist.sort(key=lambda d: -d[0])  # farthest first
    for depth, quad, brightness, is_top in drawlist:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if is_top:
            c = tuple(int(min(255, v * (brightness + 0.25))) for v in TOP_COLOR)
            ImageDraw.Draw(layer).polygon(quad, fill=c + (255,))
        else:
            coeffs = find_coeffs(quad, SRC)
            layer = shade(avatar, brightness).transform(
                (W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        canvas = Image.alpha_composite(canvas, layer)

    frames.append(canvas)

# crop away the transparent padding: union bbox of the cube across all frames
l = t = 10**9
r = b = -1
for f in frames:
    bbox = f.getchannel("A").getbbox()
    l, t = min(l, bbox[0]), min(t, bbox[1])
    r, b = max(r, bbox[2]), max(b, bbox[3])
PAD = 2
box = (max(0, l - PAD), max(0, t - PAD), min(W, r + PAD), min(H, b + PAD))
frames = [f.crop(box) for f in frames]

frames[0].save(
    OUT, save_all=True, append_images=frames[1:],
    duration=73, loop=0, disposal=0, blend=0,
)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
