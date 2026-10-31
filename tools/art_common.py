"""
art_common.py - supersampled toon renderer shared by every generated sprite.

Shapes are rasterised into high-resolution masks (S x), each part gets a dark
outline, a soft core shadow away from the light and a rim highlight toward it,
then the frame is downsampled with Lanczos. The look follows the template's
smooth cartoon art: dark outlines, soft cel shading, light from the top-left.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

S = 4  # supersampling factor
OUTLINE = (36, 26, 34)
LIGHT_AWAY = (0.55, 0.83)  # direction pointing away from the light (down-right)

_disk_cache = {}


def _disk(r):
    r = max(1, int(round(r)))
    if r not in _disk_cache:
        y, x = np.ogrid[-r:r + 1, -r:r + 1]
        _disk_cache[r] = (x * x + y * y) <= r * r + 0.5
    return _disk_cache[r]


def mix(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def shade_col(c, amt, tint=(70, 60, 110)):
    """darker and slightly cooler"""
    return mix(c, mix(tint, (0, 0, 0), 0.35), amt)


def light_col(c, amt):
    return mix(c, (255, 250, 235), amt)


class Frame:
    def __init__(self, w, h, s=S):
        self.w, self.h, self.s = w, h, s
        self.W, self.H = w * s, h * s
        self.rgb = np.zeros((self.H, self.W, 3), dtype=np.float32)
        self.a = np.zeros((self.H, self.W), dtype=np.float32)

    # ----- mask creation (coordinates in 1x pixels)
    def blank(self):
        im = Image.new("L", (self.W, self.H), 0)
        return im, ImageDraw.Draw(im)

    def _m(self, im):
        return np.asarray(im, dtype=np.float32) / 255.0

    def ellipse(self, cx, cy, rx, ry, rot=0.0):
        s = self.s
        if abs(rot) < 1e-3:
            im, d = self.blank()
            d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], fill=255)
            return self._m(im)
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            px, py = rx * math.cos(t), ry * math.sin(t)
            pts.append((cx + px * math.cos(rot) - py * math.sin(rot), cy + px * math.sin(rot) + py * math.cos(rot)))
        return self.poly(pts)

    def poly(self, pts):
        im, d = self.blank()
        if len(pts) >= 3:
            d.polygon([(x * self.s, y * self.s) for x, y in pts], fill=255)
        return self._m(im)

    def capsule(self, p1, p2, r1, r2=None):
        r2 = r1 if r2 is None else r2
        im, d = self.blank()
        s = self.s
        (x1, y1), (x2, y2) = p1, p2
        d.ellipse([(x1 - r1) * s, (y1 - r1) * s, (x1 + r1) * s, (y1 + r1) * s], fill=255)
        d.ellipse([(x2 - r2) * s, (y2 - r2) * s, (x2 + r2) * s, (y2 + r2) * s], fill=255)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1e-6
        nx, ny = -dy / L, dx / L
        d.polygon([((x1 + nx * r1) * s, (y1 + ny * r1) * s), ((x2 + nx * r2) * s, (y2 + ny * r2) * s),
                   ((x2 - nx * r2) * s, (y2 - ny * r2) * s), ((x1 - nx * r1) * s, (y1 - ny * r1) * s)],
                  fill=255)
        return self._m(im)

    def ribbon(self, pts, widths):
        """polyline with per-point half widths -> filled strip (hair strands, capes, tails)"""
        left, right = [], []
        n = len(pts)
        for i in range(n):
            x, y = pts[i]
            if i == 0:
                dx, dy = pts[1][0] - x, pts[1][1] - y
            elif i == n - 1:
                dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
            else:
                dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
            L = math.hypot(dx, dy) or 1e-6
            nx, ny = -dy / L, dx / L
            w = widths[i] if isinstance(widths, (list, tuple)) else widths
            left.append((x + nx * w, y + ny * w))
            right.append((x - nx * w, y - ny * w))
        return self.poly(left + right[::-1])

    def line_mask(self, pts, width):
        im, d = self.blank()
        d.line([(x * self.s, y * self.s) for x, y in pts], fill=255, width=max(1, int(width * self.s)),
               joint="curve")
        return self._m(im)

    # ----- painting
    def paint(self, m, color, alpha=1.0):
        m = np.clip(m, 0, 1) * alpha
        col = np.array(color[:3], dtype=np.float32)
        self.rgb = self.rgb * (1 - m[..., None]) + col * m[..., None]
        self.a = self.a + m * (1 - self.a)

    def paint_under(self, m, color, alpha=1.0):
        """paint only where nothing has been drawn yet (behind existing pixels)"""
        m = np.clip(m, 0, 1) * alpha * (1 - self.a)
        col = np.array(color[:3], dtype=np.float32)
        self.rgb = self.rgb + col * m[..., None]
        self.a = self.a + m

    def shift(self, m, dx, dy):
        """m sampled at p + (dx, dy) (1x units)"""
        sx, sy = int(round(dx * self.s)), int(round(dy * self.s))
        out = np.zeros_like(m)
        H, W = m.shape
        ys0, ys1 = max(0, -sy), min(H, H - sy)
        xs0, xs1 = max(0, -sx), min(W, W - sx)
        if ys1 > ys0 and xs1 > xs0:
            out[ys0:ys1, xs0:xs1] = m[ys0 + sy:ys1 + sy, xs0 + sx:xs1 + sx]
        return out

    def dilate(self, m, r):
        b = m > 0.5
        return ndimage.binary_dilation(b, structure=_disk(r * self.s)).astype(np.float32)

    def blur(self, m, sigma):
        return ndimage.gaussian_filter(m, sigma * self.s)

    def part(self, m, color, outline=OUTLINE, ow=1.25, shade=0.38, hl=0.30, band=None, hl_band=None,
             soft=1.0, clip=None):
        """Draw one toon-shaded part. band = shadow offset (1x px); hl_band = rim offset."""
        if clip is not None:
            m = m * clip
        if m.max() <= 0.01:
            return m
        ys, xs = np.nonzero(m > 0.5)
        if len(xs) == 0:
            return m
        size = min(xs.max() - xs.min(), ys.max() - ys.min()) / self.s
        if band is None:
            band = max(1.2, min(9.0, size * 0.32))
        if hl_band is None:
            hl_band = max(0.8, min(4.0, size * 0.14))
        if outline is not None and ow > 0:
            om = self.dilate(m, ow)
            if clip is not None:
                om = om * np.maximum(clip, self.dilate(clip, ow) * 0)
            self.paint(om, outline)
        self.paint(m, color)
        if shade > 0:
            away = self.shift(m, LIGHT_AWAY[0] * band, LIGHT_AWAY[1] * band)
            sh = np.clip(m - away, 0, 1)
            sh = self.blur(sh, soft) * m
            self.paint(sh, shade_col(color, shade))
        if hl > 0:
            tow = self.shift(m, -LIGHT_AWAY[0] * hl_band, -LIGHT_AWAY[1] * hl_band)
            h = np.clip(m - tow, 0, 1)
            h = self.blur(h, soft * 0.6) * m
            self.paint(h, light_col(color, hl))
        return m

    def glow(self, m, color, sigma=3.0, strength=1.0):
        g = self.blur(m, sigma) * strength
        self.paint(np.clip(g, 0, 1), color, 1.0)

    def result(self):
        rgba = np.zeros((self.H, self.W, 4), dtype=np.float32)
        a = np.clip(self.a, 0, 1)
        safe = np.where(a > 1e-4, a, 1)
        # rgb is premultiplied-ish (painted with coverage); un-premultiply for export
        rgba[..., :3] = np.clip(self.rgb / safe[..., None] * (a[..., None] > 1e-4), 0, 255)
        rgba[..., 3] = a * 255
        # downsample in premultiplied space to avoid dark fringes
        pm = rgba.copy()
        pm[..., :3] *= a[..., None]
        im = Image.fromarray(pm.astype(np.uint8), "RGBA")
        small_pm = np.asarray(im.resize((self.w, self.h), Image.LANCZOS), dtype=np.float32)
        al = small_pm[..., 3:4] / 255.0
        out = small_pm.copy()
        out[..., :3] = np.where(al > 1e-3, small_pm[..., :3] / np.maximum(al, 1e-3), 0)
        out = np.clip(out, 0, 255)
        return Image.fromarray(out.astype(np.uint8), "RGBA")


def premul_resize(im, size):
    a = np.asarray(im.convert("RGBA"), dtype=np.float32)
    al = a[..., 3:4] / 255.0
    a[..., :3] *= al
    r = np.asarray(Image.fromarray(a.astype(np.uint8), "RGBA").resize(size, Image.LANCZOS), dtype=np.float32)
    al2 = r[..., 3:4] / 255.0
    r[..., :3] = np.where(al2 > 1e-3, r[..., :3] / np.maximum(al2, 1e-3), 0)
    return Image.fromarray(np.clip(r, 0, 255).astype(np.uint8), "RGBA")


def tint_image(im, rgb, amount):
    a = np.asarray(im, dtype=np.float32)
    a[..., :3] = a[..., :3] * (1 - amount) + np.array(rgb, dtype=np.float32) * amount
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def rotate_about(im, angle_deg, pivot):
    """rotate RGBA image around pivot (x, y) keeping canvas size"""
    return im.rotate(angle_deg, resample=Image.BICUBIC, center=pivot)


def soft_shadow(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    a = np.zeros((h, w), dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    d = ((xx - (w - 1) / 2) / (w / 2)) ** 2 + ((yy - (h - 1) / 2) / (h / 2)) ** 2
    a = np.clip(1 - d, 0, 1) ** 0.8
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def periodic_noise(size, scale, seed, octaves=3):
    """tileable value noise in [0,1] (period = size)"""
    rng = np.random.default_rng(seed)
    out = np.zeros((size, size), dtype=np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        n = max(2, int(size / scale * (2 ** o)))
        g = rng.random((n, n)).astype(np.float32)
        # wrap-around bicubic-ish upscale via FFT-free method: repeat + zoom with wrap
        big = np.tile(g, (3, 3))
        z = ndimage.zoom(big, size / n, order=3)
        c = z[size:2 * size, size:2 * size]
        out += c[:size, :size] * amp
        total += amp
        amp *= 0.5
    out /= total
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    return out


def star_points(cx, cy, r_out, r_in, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        t = rot + i * math.pi / n
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts
