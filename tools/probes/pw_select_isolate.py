#!/usr/bin/env python3
"""Isolate the selectChar crash pattern: legendary vs rare vs common unowned chars."""
import time
from bakwan_session import Game

def call(g, name, fn, *args):
    try:
        r = g.call(fn, *args)
        print(f"[{name}] OK -> {str(r)[:120]}")
        return r
    except Exception as e:
        print(f"[{name}] ERR -> {str(e).split(chr(10))[0][:100]}")
        return None

def wait_ready(g, tries=30):
    for _ in range(tries):
        try:
            if g.ev("window.BFB_DEBUG.Net.ready"):
                return True
        except Exception:
            pass
        g.page.wait_for_timeout(1000)
    return False

def main():
    g = Game()
    try:
        # unowned: legendaries kazera/beaconcream/yoo0, rare jelllykukis, common peywish
        targets = [("kazera", "LEGENDARY Langit"), ("beaconcream", "LEGENDARY Karis"),
                   ("yoo0", "LEGENDARY PakYoo"), ("jelllykukis", "RARE Niko"),
                   ("peywish", "COMMON Kai"), ("mefelz", "LEGENDARY Bhima")]
        for cid, label in targets:
            print(f"--- selectChar {cid} ({label})")
            call(g, cid, "selectChar", cid)
            time.sleep(2)
            if not wait_ready(g):
                print("  net still down; waiting more...")
                wait_ready(g, 60)
            # restore own char each time (if server alive)
            r = call(g, "restore", "selectChar", "arethakirana")
            if not r:
                wait_ready(g, 60)
                call(g, "restore2", "selectChar", "arethakirana")
            time.sleep(1)
        p = g.player()
        print("END selectedChar:", p.get("selectedChar"))
    finally:
        g.close()

if __name__ == "__main__":
    main()
