#!/usr/bin/env python3
"""Ranked grinder with in-page perfect bot. Usage: python3 pw_ranked.py [n_matches]"""
import json, sys, time
from bakwan_session import Game

BOT_JS = open("/home/z/my-project/scripts/perfect_bot.js").read()

def match_state(g):
    return g.ev("""(() => { const B = window.BFB_DEBUG.B; if (!B || !B.m) return null;
        return JSON.stringify({mode: B.m.mode, started: !!B.m.startAt, ended: !!B.ended, start: B.m.startAt, dur: B.m.durationMs,
          L: B.L ? {dealt: B.L.dealt, hits: B.L.hits, perfects: B.L.perfects, combo: B.L.combo, bombed: B.L.bombed} : null}); })()""")

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    g = Game()
    log = []
    last_start = 0
    try:
        print("attached. screen:", g.screen())
        # install bot
        g.ev(BOT_JS)
        for m in range(n):
            p0 = g.player()
            print(f"--- match {m+1}/{n}: elo={p0['elo']} bakwan={p0['bakwan']} W/L={p0['wins']}/{p0['losses']}")
            # click Ranked via DOM
            try:
                g.frame.click("text=Ranked", timeout=8000)
            except Exception:
                # fallback: canvas menu via first DOM button containing Ranked
                g.frame.evaluate("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /Ranked/i.test(b.textContent)); if (b) b.click(); })()""")
            # wait for a FRESH match (different startAt, not ended)
            started = False
            for i in range(90):  # up to 180s (queue + bot fallback)
                st = match_state(g)
                if st:
                    s = json.loads(st)
                    if s.get("started") and not s.get("ended") and s.get("start", 0) > last_start + 1000:
                        started = True
                        break
                g.page.wait_for_timeout(2000)
            if not started:
                print("  no match started; state:", match_state(g))
                g.frame.evaluate("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /Batal|Keluar/i.test(b.textContent)); if (b) b.click(); })()""")
                continue
            st0 = json.loads(match_state(g))
            last_start = st0.get("start", 0)
            print("  match:", st0["mode"], "dur", st0["dur"])
            g.ev("window.__KB.start()")
            # wait for end
            for i in range(120):
                st = match_state(g)
                if st and '"ended":true' in st:
                    break
                g.page.wait_for_timeout(3000)
            # grab last match id to detect freshness next round
            time.sleep(3)
            g.ev("window.__KB.stop()")
            print("  bot:", g.ev("window.__KB.status()"))
            print("  sched:", g.ev("""(() => { const B = window.BFB_DEBUG.B; if(!B||!B.sched) return 'none';
              const c = B.sched.objs.filter(o=>o.k==='c').length, bo = B.sched.objs.filter(o=>o.k==='bomb').length;
              return JSON.stringify({objs: B.sched.objs.length, circles: c, bombs: bo}); })()"""))
            p1 = g.player()
            st1 = json.loads(match_state(g) or "{}")
            rec = {"mode": st0["mode"], "dealt": (st1.get("L") or {}).get("dealt"),
                   "perfects": (st1.get("L") or {}).get("perfects"), "hits": (st1.get("L") or {}).get("hits"),
                   "bombed": (st1.get("L") or {}).get("bombed"),
                   "elo": [p0["elo"], p1["elo"]], "bakwan": [p0["bakwan"], p1["bakwan"]],
                   "wl": [p0["wins"], p0["losses"], p1["wins"], p1["losses"]]}
            log.append(rec)
            print("  RESULT:", json.dumps(rec))
            # back to menu
            g.page.wait_for_timeout(2500)
            g.frame.evaluate("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /Menu|Main Lagi|MAIN LAGI|MENU/i.test(b.textContent)); if (b) b.click(); })()""")
            g.page.wait_for_timeout(3000)
        p = g.player()
        print("FINAL:", json.dumps({"elo": p["elo"], "bakwan": p["bakwan"], "wins": p["wins"], "losses": p["losses"]}))
        with open("/home/z/my-project/scripts/ranked_log.json", "w") as f:
            json.dump(log, f, indent=1)
    finally:
        g.shot("C99_pw_ranked_end")
        g.close()

if __name__ == "__main__":
    main()
