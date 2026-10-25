#!/usr/bin/env python3
"""Bakwan Fight Back - latihan auto-tapper.
Loop: screenshot -> find orange note circle (HSV filter) -> click centroid.
Run inside the game viewport only (iframe area)."""
import subprocess, time, sys, os
from PIL import Image

SHOT = "/home/z/my-project/scripts/_tb.png"
AB = ["agent-browser"]
# Playfield inside viewport (iframe content area, below Wix header)
X0, Y0, X1, Y1 = 0, 155, 800, 510
CLICK_BUDGET = 26          # max clicks per run
MAX_SEC = 75
COOLDOWN_HIT = 0.55        # pause after a click

def sh(args, **kw):
    return subprocess.run(AB + args, capture_output=True, text=True, **kw)

def find_circle(path):
    im = Image.open(path).convert("RGB").crop((X0, Y0, X1, Y1))
    w, h = im.size
    px = im.load()
    # orange note: high R (220-255), mid G (120-190), low B (<80)
    pts = []
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            if r > 215 and 110 < g < 195 and b < 90:
                pts.append((x, y))
    if len(pts) < 12:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    cx = sum(xs) / len(xs) + X0
    cy = sum(ys) / len(ys) + Y0
    return cx, cy, len(pts)

def click(x, y):
    sh(["mouse", "move", str(int(x)), str(int(y))])
    sh(["mouse", "down", "left"]); sh(["mouse", "up", "left"])

def main():
    t0 = time.time(); clicks = 0
    while time.time() - t0 < MAX_SEC and clicks < CLICK_BUDGET:
        sh(["screenshot", SHOT])
        r = find_circle(SHOT)
        if r:
            cx, cy, n = r
            click(cx, cy); clicks += 1
            print(f"[{time.time()-t0:5.1f}s] click ({cx:.0f},{cy:.0f}) px={n}", flush=True)
            time.sleep(COOLDOWN_HIT)
        else:
            time.sleep(0.25)
    print("done clicks=", clicks)

if __name__ == "__main__":
    main()
