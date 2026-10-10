#!/usr/bin/env python3
"""Snap a generated Brodie's body fill back to canon cream #EFE7DA.

Shifts every cream-family pixel by (canon - measured fill) in CIELAB, so shading,
anti-aliasing and soft shadows keep their relative values. Ink, the black tank,
white teeth and white props (chef hat, towel) sit outside the mask and are untouched.

Usage: fix_cream.py in.png out.png
"""
import sys
import numpy as np
from PIL import Image
from cream import rgb_to_lab, lab_to_rgb, hue_chroma
from check_cream import CANON, measure


def fix(src, dst):
    fill, _ = measure(src)
    if fill is None:
        raise SystemExit(f"no cream body found in {src}")
    im = np.asarray(Image.open(src).convert("RGBA")).copy()
    lab = rgb_to_lab(im[..., :3])
    hue, chroma = hue_chroma(lab)
    # wider than the measuring mask: include shaded cream and outline anti-aliasing
    d = np.linalg.norm(lab - fill, axis=-1)
    m = (im[..., 3] > 0) & (chroma > 2.5) & (chroma < 18) & ((hue < 120) | (hue > 330)) & (lab[..., 0] > 55)
    w = np.clip(1.2 - d / 30.0, 0, 1)[..., None] * m[..., None]
    shift = CANON - fill
    shift[0] *= 0.5                     # keep the artist's lightness mostly
    lab2 = lab + w * shift
    im[..., :3] = np.where(m[..., None], lab_to_rgb(lab2), im[..., :3])
    Image.fromarray(im).save(dst)
    print(f"fixed {src} -> {dst}  (shift a{shift[1]:+.1f} b{shift[2]:+.1f})")


if __name__ == "__main__":
    fix(sys.argv[1], sys.argv[2])
