#!/usr/bin/env python3
"""Real train session with perfect bot; claims daily firstTrain (+10 bakwan)."""
import json, time
from bakwan_session import Game

BOT_JS = open("/home/z/my-project/scripts/perfect_bot.js").read()

def main():
    g = Game()
    try:
        p0 = g.player()
        print(f"before: bakwan={p0['bakwan']} daily={p0['daily']}")
        g.ev(BOT_JS)
        # open train via DOM
        g.frame.evaluate("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /Train|Latihan/i.test(b.textContent)); if (b) b.click(); })()""")
        # wait for board
        started = False
        for i in range(40):
            st = g.ev("""(() => { const B = window.BFB_DEBUG.B; return B && B.m ? JSON.stringify({started: !!B.m.startAt, ended: !!B.ended, mode: B.m.mode}) : null; })()""")
            if st and json.loads(st)["started"] and not json.loads(st)["ended"]:
                started = True
                break
            g.page.wait_for_timeout(1500)
        print("train started:", started)
        if started:
            g.shot("C03_train_bot_running")
            g.ev("window.__KB.start(70000)")
            for i in range(50):
                st = g.ev("""(() => { const B = window.BFB_DEBUG.B; return JSON.stringify({ended: !!B.ended}); })()""")
                if json.loads(st)["ended"]:
                    break
                g.page.wait_for_timeout(3000)
            time.sleep(4)
            print("bot:", g.ev("window.__KB.status()"))
            g.shot("C04_train_result_bot")
            g.page.wait_for_timeout(4000)
            p1 = g.player()
            print(f"after: bakwan={p1['bakwan']} daily={p1['daily']}")
            # capture result modal if present
            g.shot("C05_train_result_modal")
    finally:
        g.close()

if __name__ == "__main__":
    main()
