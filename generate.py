#!/usr/bin/env python3
"""Generate meme.png for the gta6-meme-x-01 entry.

A WANTED poster for "the biggest heist in Leonida": GTA VI's launch-day
sales, with make.fun's official ghost mascot (assets/mark-1024.png, from
the make.fun press kit) worked into a Vice City sunset scene.

Deterministic: fixed layout, fixed fonts, no randomness, no wall clock.
Re-running produces byte-identical output. Output: 1600x900 PNG (landscape,
so it stays legible when the judge shrinks it to fit 768x480).

Usage: python3 generate.py   (writes meme.png next to this script)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900

CREAM = (243, 230, 192, 255)
INK = (25, 20, 25, 255)          # near-black, matches the make.fun wordmark
GOLD = (255, 193, 7, 255)
MAGENTA = (194, 24, 123, 255)    # make.fun brand magenta
DARK_STRIP = (25, 20, 25, 255)
WHITE = (255, 255, 255, 255)
SILHOUETTE = (30, 16, 40, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_outer, r_inner, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def vgrad(draw, box, stops):
    """Vertical gradient across box, stops = [(pos0to1, (r,g,b)), ...]."""
    x0, y0, x1, y1 = box
    height = y1 - y0
    for y in range(height):
        t = y / max(height - 1, 1)
        # find surrounding stops
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
                break
        else:
            col = stops[-1][1]
        draw.line([(x0, y0 + y), (x1, y0 + y)], fill=col + (255,))


def centered(draw, cx, y, text, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1]


def palm(draw, x, base_y, height, lean, color):
    """A palm silhouette: curved trunk + 7 drooping fronds."""
    top_x = x + lean
    top_y = base_y - height
    # trunk: polyline along a quadratic curve
    pts = []
    for i in range(13):
        t = i / 12
        px = x + (top_x - x) * t * t + lean * 0.15 * math.sin(t * math.pi)
        py = base_y - height * t
        pts.append((px, py))
    draw.line(pts, fill=color, width=14, joint="curve")
    # fronds: droop downward from the crown, like a real palm
    for k in range(6):
        ang = math.radians(-155 + k * 30)  # fan from up-left to up-right
        length = height * (0.55 if k in (0, 5) else 0.68)
        fx = top_x + length * math.cos(ang)
        fy = top_y + length * math.sin(ang) * 0.55 + 62
        mid_x = top_x + (fx - top_x) * 0.55
        mid_y = top_y + (fy - top_y) * 0.45 - 8
        draw.line([(top_x, top_y), (mid_x, mid_y), (fx, fy)],
                  fill=color, width=12, joint="curve")
    # coconuts
    draw.ellipse([top_x - 12, top_y + 2, top_x + 2, top_y + 16], fill=color)
    draw.ellipse([top_x + 2, top_y + 4, top_x + 16, top_y + 18], fill=color)


def money_bag(draw, cx, cy, s):
    """A green money sack with a $ on it, centred at (cx, cy), size s."""
    green = (46, 125, 50, 255)
    dark_green = (27, 94, 32, 255)
    # sack body
    draw.ellipse([cx - s * 0.52, cy - s * 0.28, cx + s * 0.52, cy + s * 0.52],
                 fill=green, outline=dark_green, width=6)
    # tied neck: a knot with two short ribbon ends
    draw.polygon([(cx - s * 0.16, cy - s * 0.26), (cx + s * 0.16, cy - s * 0.26),
                  (cx + s * 0.10, cy - s * 0.46), (cx - s * 0.10, cy - s * 0.46)],
                 fill=green, outline=dark_green)
    draw.ellipse([cx - s * 0.10, cy - s * 0.34, cx + s * 0.10, cy - s * 0.18],
                 fill=dark_green)
    draw.line([(cx - s * 0.22, cy - s * 0.30), (cx + s * 0.22, cy - s * 0.30)],
              fill=dark_green, width=8)
    # dollar sign
    f = font(SANS_BOLD, int(s * 0.55))
    centered(draw, cx, cy - s * 0.08, "$", f, WHITE)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- poster frame -------------------------------------------------
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=7)
    d.rectangle([30, 30, W - 31, H - 31], outline=INK, width=2)

    # --- wanted stars + WANTED ---------------------------------------
    for i, sx in enumerate([560, 680, 800, 920, 1040]):
        d.polygon(star_points(sx, 78, 34, 14), fill=GOLD, outline=INK)
    centered(d, W // 2, 118, "WANTED", font(SERIF_BOLD, 128), INK)

    # --- headline ------------------------------------------------------
    centered(d, W // 2, 262, "THE BIGGEST HEIST IN LEONIDA",
             font(SANS_BOLD, 48), INK)

    # --- sunset scene band --------------------------------------------
    bx0, by0, bx1, by1 = 60, 322, W - 60, 548
    vgrad(d, (bx0, by0, bx1, by1), [
        (0.0, (255, 140, 66)),
        (0.45, (232, 84, 120)),
        (1.0, (96, 32, 120)),
    ])
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=4)
    # sun (smaller, so the skyline reads)
    d.ellipse([725, 360, 875, 510], fill=(255, 214, 130, 255))
    # skyline silhouettes (fixed, deterministic)
    skyline = [(60, 500, 150, 548), (150, 470, 230, 548), (230, 505, 330, 548),
               (330, 455, 430, 548), (430, 495, 520, 548), (520, 470, 610, 548),
               (990, 480, 1080, 548), (1080, 450, 1180, 548), (1180, 500, 1280, 548),
               (1280, 465, 1380, 548), (1380, 505, 1540, 548)]
    for (x0, y0, x1, y1) in skyline:
        d.rectangle([x0, y0, x1, y1], fill=SILHOUETTE)
        for wy in (y0 + 14, y0 + 34):
            for wx in range(x0 + 12, x1 - 8, 26):
                d.rectangle([wx, wy, wx + 8, wy + 10], fill=(255, 214, 130, 255))
    # palms
    palm(d, 130, 548, 150, 26, SILHOUETTE)
    palm(d, 1470, 548, 165, -30, SILHOUETTE)
    # money bag on the left of the scene
    money_bag(d, 225, 480, 130)
    # make.fun ghost (official press-kit mark) on the right, in the scene:
    # inside the band, clear of the headline above it
    ghost = Image.open(os.path.join(HERE, "assets", "mark-1024.png")).convert("RGBA")
    ghost = ghost.resize((240, 240), Image.LANCZOS)
    img.paste(ghost, (1200, 308), ghost)
    d = ImageDraw.Draw(img)  # redraw handle after paste

    # --- fact line ------------------------------------------------------
    centered(d, W // 2, 568, "24.6M PLAYERS PAID $2.36 BILLION IN ONE DAY",
             font(SANS_BOLD, 44), INK)
    centered(d, W // 2, 618, "(Sensor Tower estimate)",
             font(SANS_ITALIC, 26), (90, 80, 70, 255))

    # --- punchline ------------------------------------------------------
    centered(d, W // 2, 652, "MY CUT? MY AI AGENT DID THE WORK.",
             font(SANS_BOLD, 52), MAGENTA)

    # --- bottom strip: make.fun + play code -----------------------------
    d.rectangle([60, 742, W - 60, 872], fill=DARK_STRIP)
    centered(d, W // 2, 758, "make.fun", font(SANS_BOLD, 62), WHITE)
    centered(d, W // 2, 828, "Play code: makefun-latch-condor-planet",
             font(SANS, 34), (255, 214, 130, 255))

    return img


def main():
    img = build()
    out = os.path.join(HERE, "meme.png")
    img.save(out, format="PNG")
    print(f"wrote {out} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
