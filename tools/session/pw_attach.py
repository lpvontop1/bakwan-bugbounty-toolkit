#!/usr/bin/env python3
"""Attach to bakwan game iframe with real session via Playwright.
Verifies BFB_DEBUG access inside the production iframe."""
import json, time, sys
from playwright.sync_api import sync_playwright

STATE = "/home/z/my-project/scripts/auth_state.json"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            storage_state=STATE, viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        page = ctx.new_page()
        page.goto("https://www.bakwan.id/game", wait_until="domcontentloaded")
        print("page opened, waiting for game iframe...")
        deadline = time.time() + 300
        game = None
        seen = 0
        while time.time() < deadline and game is None:
            seen += 1
            if seen % 10 == 0:
                print('  t+%ds frames:' % (seen*2), [f.url[:60] for f in page.frames])
            for f in page.frames:
                if "play.bakwan.id" in f.url or ("filesusr.com" in f.url and "c1ed9b_" in f.url):
                    game = f
                    break
            page.wait_for_timeout(2000)
        if game is None:
            page.screenshot(path="/home/z/my-project/scripts/PW_fail.png", full_page=False)
            print("frames seen:")
            for f in page.frames:
                print("  -", f.url[:100])
            print("FAIL: no game frame found"); browser.close(); sys.exit(1)
        print("game frame:", game.url[:90])
        # wait for boot
        for i in range(30):
            has = game.evaluate("typeof window.BFB_DEBUG")
            if has == "object":
                break
            page.wait_for_timeout(2000)
        print("BFB_DEBUG:", has)
        if has == "object":
            st = game.evaluate("""(() => { const d = window.BFB_DEBUG; const G = d.G;
                return JSON.stringify({mode: G.mode, name: G.player && G.player.name, bakwan: G.player && G.player.bakwan,
                  elo: G.player && G.player.elo, isAdmin: G.isAdmin, relay: G.relay, cfgRev: G.cfgRev,
                  wsReady: d.Net.ready, screen: G.screen}); })()""")
            print("STATE:", st)
        page.screenshot(path="/home/z/my-project/scripts/PW_first.png")
        browser.close()

if __name__ == "__main__":
    main()
