"""Renders the spinning-cube APNGs used in the profile README:

  - profile-cube.png : my GitHub avatar on all four sides
  - chess-cube.png   : the chess.svg pawn on all four sides

Usage: python assets/cube.py
Deps:  pillow, numpy, cairosvg
"""
import io
import os
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
AVATAR_URL = "https://github.com/jianrontan.png?size=460"

W = H = 300
N_FRAMES = 72
DURATION = 73  # ms per frame
DIST = 5.0
FOCAL = W * 0.92
TILT = -0.35  # radians about x-axis; tips the top face toward the viewer
TEX = 256

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
# single flat face through the rotation axis: spins in place like a coin
FACE = ([(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)], (0, 0, -1))

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
    return list(np.linalg.solve(A, B))


def shade(tex, brightness):
    arr = np.asarray(tex, dtype=np.float64).copy()
    arr[..., :3] *= brightness
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def render_cube(texture, out_path, top_color=(30, 34, 42), transparent=False,
                textured_faces=(0, 1, 2, 3), coin=False):
    """transparent=True renders a glass cube: no top face, and back faces stay
    visible (shaded by their inward-facing side) since you can see through.
    textured_faces picks which of the 4 side faces get the texture; the rest
    are empty (only meaningful together with transparent=True).
    coin=True ignores the cube entirely and spins FACE about its own y-axis,
    so the texture rotates in place with no side-to-side sweep."""
    if coin:
        faces = [FACE]
        transparent = True  # the mirrored back side stays visible
    else:
        faces = [FACES[i] for i in textured_faces]
        if not transparent:
            faces = faces + [TOP]
    frames = []
    for i in range(N_FRAMES):
        theta = 2 * np.pi * i / N_FRAMES
        R = rot_matrix(theta)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        drawlist = []
        for corners, normal in faces:
            n = R @ np.array(normal, dtype=np.float64)
            if n[2] >= 0:  # backface: camera is at z=0 looking toward +z
                if not transparent:
                    continue
                n = -n
            pts = [R @ np.array(c, dtype=np.float64) for c in corners]
            quad, depth = project(pts)
            # skip near-edge-on frames where the homography is singular
            area = abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1)
                           in zip(quad, quad[1:] + quad[:1]))) / 2
            if area < 4:
                continue
            brightness = 0.45 + 0.55 * max(0.0, float(n @ LIGHT))
            drawlist.append((depth, quad, brightness, normal == (0, 1, 0)))

        drawlist.sort(key=lambda d: -d[0])  # farthest first
        for depth, quad, brightness, is_top in drawlist:
            if is_top:
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                c = tuple(int(min(255, v * (brightness + 0.25))) for v in top_color)
                ImageDraw.Draw(layer).polygon(quad, fill=c + (255,))
            else:
                coeffs = find_coeffs(quad, SRC)
                layer = shade(texture, brightness).transform(
                    (W, H), Image.Transform.PERSPECTIVE, coeffs,
                    Image.Resampling.BICUBIC)
            canvas = Image.alpha_composite(canvas, layer)

        frames.append(canvas)

    # crop away the transparent padding: union bbox of the cube across all frames
    l = t = 10**9
    r = b = -1
    for f in frames:
        bbox = f.getchannel("A").getbbox()
        if bbox is None:  # blank frame (coin seen exactly edge-on)
            continue
        l, t = min(l, bbox[0]), min(t, bbox[1])
        r, b = max(r, bbox[2]), max(b, bbox[3])
    pad = 2
    box = (max(0, l - pad), max(0, t - pad), min(W, r + pad), min(H, b + pad))
    frames = [f.crop(box) for f in frames]

    frames[0].save(
        out_path, save_all=True, append_images=frames[1:],
        duration=DURATION, loop=0, disposal=0, blend=0,
    )
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


def avatar_texture():
    img = Image.open(io.BytesIO(urllib.request.urlopen(AVATAR_URL).read()))
    return img.convert("RGBA").resize((TEX, TEX), Image.Resampling.LANCZOS)


def chess_texture():
    """chess.svg pawn centred on a transparent face."""
    import cairosvg
    png = cairosvg.svg2png(url=os.path.join(HERE, "chess.svg"), output_height=TEX * 2)
    assert isinstance(png, bytes)  # svg2png only returns None when write_to is set
    pawn = Image.open(io.BytesIO(png)).convert("RGBA")
    pawn.thumbnail((int(TEX * 0.72), int(TEX * 0.88)), Image.Resampling.LANCZOS)
    face = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0))
    face.alpha_composite(
        pawn, ((TEX - pawn.width) // 2, (TEX - pawn.height) // 2))
    return face


if __name__ == "__main__":
    render_cube(avatar_texture(), os.path.join(HERE, "profile-cube.png"))
    render_cube(chess_texture(), os.path.join(HERE, "chess-spin.png"), coin=True)
