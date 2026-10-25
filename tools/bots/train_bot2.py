#!/usr/bin/env python3
"""Bakwan latihan bot v2 — predict perfect moment from ring shrink rate.
Frames: detect orange note (pos+radius) + white ring radius -> extrapolate
time when ring radius == note radius -> sleep -> click."""
import subprocess, time, math, sys
from PIL import Image

SHOT = "/home/z/my-project/scripts/_tb2.png"
AB = ["agent-browser"]
X0, Y0, X1, Y1 = 0, 155, 800, 510
CLICK_LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.30   # sec, click roundtrip comp
MAX_NOTES = int(sys.argv[2]) if len(sys.argv) > 2 else 14
MAX_SEC = 95

def sh(args):
    return subprocess.run(AB + args, capture_output=True, text=True)

def grab():
    sh(["screenshot", SHOT])
    return Image.open(SHOT).convert("RGB").crop((X0, Y0, X1, Y1))

def analyze(im):
    """Return list of notes: (cx, cy, r_note, r_ring) in page coords."""
    w, h = im.size
    px = im.load()
    orange = []; white = []
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            if r > 215 and 110 < g < 195 and b < 90:
                orange.append((x, y))
            elif r > 225 and g > 225 and b > 215:
                white.append((x, y))
    if len(orange) < 15:
        return []
    # cluster orange points
    clusters = []
    for p in orange:
        placed = False
        for c in clusters:
            if abs(p[0]-c[0][0]) < 70 and abs(p[1]-c[0][1]) < 70:
                c.append(p); placed = True; break
        if not placed:
            clusters.append([p])
    notes = []
    for c in clusters:
        if len(c) < 12: continue
        xs = [p[0] for p in c]; ys = [p[1] for p in c]
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        r_note = math.sqrt(len(c)*9/math.pi)
        # ring radius: max dist of white px near this cluster (within 3x note radius)
        rr = 0
        for (x, y) in white:
            d = math.hypot(x-cx, y-cy)
            if d > rr and d < r_note*3.2:
                rr = d
        notes.append((cx+X0, cy+Y0, r_note, rr))
    return notes

def click(x, y):
    sh(["mouse", "move", str(int(x)), str(int(y))])
    sh(["mouse", "down", "left"]); sh(["mouse", "up", "left"])

def main():
    t0 = time.time(); hits_attempt = 0
    prev = None  # (cx,cy,r_note,r_ring,t)
    while time.time()-t0 < MAX_SEC and hits_attempt < MAX_NOTES:
        im = grab(); now = time.time()
        notes = analyze(im)
        if not notes:
            prev = None; time.sleep(0.15); continue
        # match with previous frame's note (nearest centroid)
        target = None
        if prev:
            best, bd = None, 1e9
            for n in notes:
                d = math.hypot(n[0]-prev[0], n[1]-prev[1])
                if d < 60 and d < bd: best, bd = n, d
            target = best
        if target is None:
            # pick the note with the smallest ring radius (closest to perfect)
            target = min(notes, key=lambda n: n[3]) if notes else None
            prev = (*target, now) if target else None
            time.sleep(0.12); continue
        cx, cy, rn, rr = target
        pt = now
        if prev and rr > rn and prev[3] > rn:
            dt = pt - prev[4]
            rate = (prev[3] - rr) / dt if dt > 0.03 else None  # px/sec shrink
            if rate and rate > 5:
                ttt = (rr - rn) / rate - CLICK_LAT  # time to perfect
                if 0.02 < ttt < 1.4:
                    time.sleep(ttt)
                    click(cx, cy); hits_attempt += 1
                    print(f"hit@({cx:.0f},{cy:.0f}) rn={rn:.0f} rr={rr:.0f} rate={rate:.0f} wait={ttt:.2f}", flush=True)
                    prev = None; time.sleep(0.35); continue
        prev = (*target, pt)
        time.sleep(0.12)
    print("done attempts=", hits_attempt)

if __name__ == "__main__":
    main()
