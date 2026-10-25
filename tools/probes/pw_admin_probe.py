#!/usr/bin/env python3
"""Admin ACL probes — safe: no valid payloads, only arg-less/invalid calls.
If server checks admin BEFORE args -> PERMISSION/NO_AUTH error (ACL ok).
If it errors on missing args first -> ACL hole (CRITICAL, no broadcast made)."""
import json
from bakwan_session import Game

def call(g, name, fn, *args):
    try:
        r = g.call(fn, *args)
        s = json.dumps(r, ensure_ascii=False, default=str)
        print(f"[{name}] {fn}{list(args)} OK -> {s[:200]}")
        return r
    except Exception as e:
        print(f"[{name}] {fn}{list(args)} ERR -> {str(e).split(chr(10))[0][:150]}")
        return None

def main():
    g = Game()
    try:
        p0 = g.player()
        print(f"START bakwan={p0['bakwan']}")
        # arg-less admin probes (should be DENIED for non-admin)
        call(g, "ov", "adminOverview")
        call(g, "log", "adminLog")
        call(g, "getset", "adminGetSettings")
        call(g, "search", "adminSearch", "")
        # announcement with EMPTY text (worst case: no-op broadcast of empty string)
        call(g, "ann_empty", "adminAnnounce", "")
        # action with garbage (should never match a real action)
        call(g, "act_junk", "adminAction", "__nonexistent__", "noop")
        p1 = g.player()
        print(f"END bakwan={p1['bakwan']}")
    finally:
        g.close()

if __name__ == "__main__":
    main()
