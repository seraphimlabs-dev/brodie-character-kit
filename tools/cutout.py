#!/usr/bin/env python3
"""Make the plain white background around a Brodie sticker transparent.
Flood-fills near-white from the image border only, so white teeth, chef hats and
pillows inside the black outline stay opaque.
Usage: cutout.py in.png out.png"""
import sys
from collections import deque
import numpy as np
from PIL import Image

def cutout(src, dst, tol=28):
    im = np.asarray(Image.open(src).convert("RGBA")).copy()
    h, w = im.shape[:2]
    light = (im[..., :3].min(axis=-1) > 255 - tol) | (im[..., 3] == 0)
    seen = np.zeros((h, w), bool)
    q = deque((y, x) for y in range(h) for x in (0, w - 1)) 
    q.extend((y, x) for x in range(w) for y in (0, h - 1))
    while q:
        y, x = q.popleft()
        if seen[y, x] or not light[y, x]: continue
        seen[y, x] = True
        if y > 0: q.append((y - 1, x))
        if y < h - 1: q.append((y + 1, x))
        if x > 0: q.append((y, x - 1))
        if x < w - 1: q.append((y, x + 1))
    im[seen, 3] = 0
    Image.fromarray(im).save(dst)

if __name__ == "__main__":
    cutout(sys.argv[1], sys.argv[2])
