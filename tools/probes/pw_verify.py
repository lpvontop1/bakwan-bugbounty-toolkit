#!/usr/bin/env python3
"""Verify account state after the selectChar anomaly."""
import json
from bakwan_session import Game

def main():
    g = Game()
    try:
        p = g.player()
        print("PLAYER:", json.dumps({k: p.get(k) for k in ("name", "elo", "bakwan", "selectedChar", "wins", "losses", "draws", "items")}, ensure_ascii=False))
        print("OWNED:", g.ev("""(() => { const G = window.BFB_DEBUG.G; return JSON.stringify(G.owned); })()"""))
        print("NET:", g.net_state())
        # also try bootstrap fresh
        try:
            bs = g.call('bootstrap')
            pl = bs.get('player') or {}
            print("BOOTSTRAP player:", json.dumps({k: pl.get(k) for k in ("name", "selectedChar", "bakwan")}, ensure_ascii=False))
            print("BOOTSTRAP owned:", json.dumps(bs.get('owned')))
        except Exception as e:
            print("bootstrap err:", str(e).split(chr(10))[0][:200])
    finally:
        g.close()

if __name__ == "__main__":
    main()
