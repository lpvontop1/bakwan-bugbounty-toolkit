#!/usr/bin/env python3
"""Bakwan latihan bot v3 — rolling multi-frame ring tracking.
Fire only when ring is close (rr-rn<TRIG px); extrapolate with slope from
last K samples; subtract measured click latency."""
import subprocess, time, math, sys
from PIL import Image

SHOT = "/home/z/my-project/scripts/_tb3.png"
AB = ["agent-browser"]
X0, Y0, X1, Y1 = 0, 155, 800, 510
CLICK_LAT = 0.33
TRIG = 34          # px remaining to trigger
K = 5              # samples for slope
MAX_SEC = float(sys.argv[1]) if len(sys.argv) > 1 else 95

def sh(args):
    return subprocess.run(AB + args, capture_output=True, text=True)

def grab():
    sh(["screenshot", SHOT])
    return Image.open(SHOT).convert("RGB").crop((X0, Y0, X1, Y1))

def analyze(im):
    w, h = im.size
    px = im.load()
    orange = []; white = []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if r > 215 and 110 < g < 195 and b < 90:
                orange.append((x, y))
            elif r > 225 and g > 225 and b > 215:
                white.append((x, y))
    if len(orange) < 15:
        return []
    clusters = []
    for p in orange:
        placed = False
        for c in clusters:
            if abs(p[0]-c[0][0]) < 60 and abs(p[1]-c[0][1]) < 60:
                c.append(p); placed = True; break
        if not placed:
            clusters.append([p])
    notes = []
    for c in clusters:
        if len(c) < 15: continue
        xs = [p[0] for p in c]; ys = [p[1] for p in c]
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        rn = math.sqrt(len(c)*4/math.pi)
        rr = 0
        for (x, y) in white:
            d = math.hypot(x-cx, y-cy)
            if d > rr and d < rn*3.4:
                rr = d
        notes.append([cx+X0, cy+Y0, rn, rr])
    return notes

def click(x, y):
    sh(["mouse", "move", str(int(x)), str(int(y))])
    sh(["mouse", "down", "left"]); sh(["mouse", "up", "left"])

def main():
    t0 = time.time()
    tracks = {}   # idx -> list of (t, rr, rn, cx, cy)
    nclick = 0
    while time.time()-t0 < MAX_SEC:
        im = grab(); now = time.time()
        notes = analyze(im)
        live = set()
        for n in notes:
            cx, cy, rn, rr = n
            if rr <= rn or rr > 190: continue
            # track by position bucket
            key = (int(cx)//50, int(cy)//50)
            live.add(key)
            tracks.setdefault(key, []).append((now, rr, rn, cx, cy))
            tr = tracks[key][-K:]
            if len(tr) >= 3:
                # slope of rr over time
                (t1, r1, *_), (t2, r2, *_) = tr[0], tr[-1]
                if t2 - t1 < 0.05: continue
                rate = (r1 - r2) / (t2 - t1)
                if rate < 8: continue
                gap = r2 - rn
                ttt = gap / rate - CLICK_LAT
                if gap < TRIG and 0.0 < ttt < 0.9:
                    time.sleep(max(0, ttt))
                    click(cx, cy); nclick += 1
                    print(f"click ({cx:.0f},{cy:.0f}) gap={gap:.0f} rate={rate:.0f} wait={ttt:.2f} n={len(tr)}", flush=True)
                    tracks[key] = []          # reset this track
                    time.sleep(0.4)
                    break
        # prune stale tracks
        for k in list(tracks):
            if k not in live and tracks[k] and now - tracks[k][-1][0] > 1.0:
                del tracks[k]
            elif len(tracks[k]) > 12:
                tracks[k] = tracks[k][-8:]
    print("done clicks=", nclick)

if __name__ == "__main__":
    main()
