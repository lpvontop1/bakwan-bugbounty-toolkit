#!/usr/bin/env python3
"""Ranked grind v2 — screenshots at key moments, win-modal capture, Elo tracking."""
import json, sys, time
from bakwan_session import Game

BOT_JS = open("/home/z/my-project/scripts/perfect_bot.js").read()

def board(g):
    return g.ev("""(() => { const B = window.BFB_DEBUG.B; if (!B || !B.m) return null;
        return JSON.stringify({mode: B.m.mode, started: !!B.m.startAt, ended: !!B.ended, start: B.m.startAt, dur: B.m.durationMs,
          L: B.L ? {dealt: B.L.dealt, hits: B.L.hits, perfects: B.L.perfects} : null}); })()""")

def click_button(g, pattern):
    return g.frame.evaluate(f"""(() => {{
      const b = Array.from(document.querySelectorAll('button')).find(b => /{pattern}/i.test(b.textContent));
      if (b) {{ b.click(); return true; }} return false; }})()""")

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    g = Game()
    log = []
    try:
        print("attached. screen:", g.screen())
        g.ev(BOT_JS)
        g.shot("C06_ranked_queue_screen")
        last_start = 0
        for m in range(n):
            p0 = g.player()
            print(f"--- match {m+1}/{n}: elo={p0['elo']} bakwan={p0['bakwan']} W/L/D={p0['wins']}/{p0['losses']}/{p0['draws']}")
            click_button(g, "Ranked")
            started = False
            for i in range(90):
                st = board(g)
                if st:
                    s = json.loads(st)
                    if s.get("started") and not s.get("ended") and s.get("start", 0) > last_start + 1000:
                        started = True
                        break
                g.page.wait_for_timeout(2000)
            if not started:
                print("  no match; bail")
                click_button(g, "Batal|Keluar")
                continue
            st0 = json.loads(board(g))
            last_start = st0["start"]
            g.shot(f"C1{m}_match_start")
            print("  match:", st0["mode"], "dur", st0["dur"])
            g.ev("window.__KB.start()")
            for i in range(120):
                st = board(g)
                if st and json.loads(st)["ended"]:
                    break
                g.page.wait_for_timeout(2500)
                if i == 8:
                    g.shot(f"C1{m}_match_mid")
            time.sleep(3)
            g.ev("window.__KB.stop()")
            g.shot(f"C2{m}_match_result")   # win/lose modal!
            p1 = g.player()
            st1 = json.loads(board(g) or "{}")
            rec = {"mode": st0["mode"], "dealt": (st1.get("L") or {}).get("dealt"),
                   "perfects": (st1.get("L") or {}).get("perfects"), "hits": (st1.get("L") or {}).get("hits"),
                   "elo": [p0["elo"], p1["elo"]], "bakwan": [p0["bakwan"], p1["bakwan"]],
                   "wl": [p0["wins"], p0["losses"], p1["wins"], p1["losses"], p1["draws"]]}
            log.append(rec)
            print("  RESULT:", json.dumps(rec))
            g.page.wait_for_timeout(2500)
            click_button(g, "Menu|Main Lagi")
            g.page.wait_for_timeout(2500)
        p = g.player()
        print("FINAL:", json.dumps({"elo": p["elo"], "peak": p["peakElo"], "bakwan": p["bakwan"],
              "W/L/D": [p["wins"], p["losses"], p["draws"]]}))
        with open("/home/z/my-project/scripts/ranked_log2.json", "w") as f:
            json.dump(log, f, indent=1)
    finally:
        g.close()

if __name__ == "__main__":
    main()
