#!/usr/bin/env python3
"""API edge-case probes against the live play.bakwan.id WS backend.
Non-destructive order: validation probes first, then state-changing PoC tests."""
import json
from bakwan_session import Game

def call(g, name, fn, *args):
    try:
        r = g.call(fn, *args)
        s = json.dumps(r, ensure_ascii=False, default=str)
        print(f"[{name}] {fn}{list(args)} OK -> {s[:260]}")
        return r
    except Exception as e:
        msg = str(e)[:220]
        print(f"[{name}] {fn}{list(args)} ERR -> {msg}")
        return {"__err": msg}

def main():
    g = Game()
    try:
        p0 = g.player()
        print(f"START bakwan={p0['bakwan']} elo={p0['elo']} items={p0.get('items')}")
        print("NET:", g.net_state())

        # --- group 1: read-only / harmless
        call(g, "lb", "leaderboard")
        call(g, "hist", "history")

        # --- group 2: gacha validation (should all fail NOT_ENOUGH with 20 bakwan)
        call(g, "g1", "gacha", 1)
        call(g, "g10", "gacha", 10)
        call(g, "g0", "gacha", 0)
        call(g, "gneg", "gacha", -1)
        call(g, "gstr", "gacha", "10")
        call(g, "gnoarg", "gacha")
        call(g, "gbig", "gacha", 10000)

        # --- group 3: buyItem validation
        call(g, "bnope", "buyItem", "nope", 1)
        call(g, "bzero", "buyItem", "xpS", 0)
        call(g, "bneg", "buyItem", "xpS", -3)
        call(g, "bfloat", "buyItem", "xpS", 0.5)

        # --- group 4: trainDone trust test (client-supplied summary)
        call(g, "train", "trainDone", "arethakirana", {"hits": 50, "perfects": 40, "combo": 20})

        p1 = g.player()
        print(f"END bakwan={p1['bakwan']} items={p1.get('items')}")
    finally:
        g.close()

if __name__ == "__main__":
    main()
