#!/usr/bin/env python3
"""Shared Playwright session module for bakwan production game control."""
import json, time, sys
from playwright.sync_api import sync_playwright

STATE = "/home/z/my-project/scripts/auth_state.json"
SHOT_DIR = "/home/z/my-project/download/screenshots"

class Game:
    def __init__(self, headless=True, shot_prefix="PW"):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=headless)
        self.ctx = self.browser.new_context(
            storage_state=STATE, viewport={"width": 1280, "height": 760},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        self.page = self.ctx.new_page()
        self.console = []
        self.page.on("console", lambda m: self.console.append(f"[{m.type}] {m.text[:200]}"))
        self.page.on("pageerror", lambda e: self.console.append(f"[pageerror] {str(e)[:200]}"))
        self.frame = None
        self.attach()

    def attach(self):
        self.page.goto("https://www.bakwan.id/game", wait_until="domcontentloaded")
        deadline = time.time() + 240
        while time.time() < deadline:
            for f in self.page.frames:
                if "play.bakwan.id" in f.url or ("filesusr.com" in f.url and "c1ed9b_" in f.url):
                    self.frame = f
                    break
            if self.frame:
                break
            self.page.wait_for_timeout(2000)
        if not self.frame:
            raise RuntimeError("game frame not found")
        for _ in range(60):
            if self.frame.evaluate("typeof window.BFB_DEBUG") == "object":
                break
            self.page.wait_for_timeout(2000)
        # wait until menu screen
        for _ in range(60):
            try:
                if self.ev("window.BFB_DEBUG && window.BFB_DEBUG.G.screen") in ("menu", "boot"):
                    if self.ev("window.BFB_DEBUG.G.screen") == "menu":
                        break
            except Exception:
                pass
            self.page.wait_for_timeout(1500)
        return self

    def ev(self, js):
        return self.frame.evaluate(js)

    def shot(self, name, full=False):
        path = f"{SHOT_DIR}/{name}.png" if not name.startswith("/") else name
        self.page.screenshot(path=path, full_page=full)
        return path

    # ---------- state helpers ----------
    def player(self):
        return self.ev("JSON.parse(JSON.stringify(window.BFB_DEBUG.G.player))")

    def owned(self):
        return self.ev("JSON.parse(JSON.stringify(window.BFB_DEBUG.G.owned))")

    def config(self):
        return self.ev("JSON.parse(JSON.stringify(window.BFB_DEBUG.BFB ? window.BFB_DEBUG.BFB.cfg || {} : (window.__CFG||{})))")

    def net_state(self):
        return self.ev("""(() => { const N = window.BFB_DEBUG.Net; return JSON.stringify({url: N.url, ready: N.ready, down: N.down, seq: N.seq}); })()""")

    def call(self, fn, *args):
        """Direct API call through the game's Net relay."""
        args_js = json.dumps(list(args))
        js = f"""(async () => {{
          const N = window.BFB_DEBUG.Net;
          const r = await N.call('{fn}', ...{args_js});
          return JSON.parse(JSON.stringify(r));
        }})()"""
        return self.ev(js)

    def screen(self):
        return self.ev("window.BFB_DEBUG.G.screen")

    def close(self):
        try:
            self.ctx.storage_state(path=STATE)  # refresh session state
        except Exception:
            pass
        self.browser.close()
        self.pw.stop()

if __name__ == "__main__":
    g = Game()
    try:
        print("PLAYER:", json.dumps(g.player(), ensure_ascii=False)[:600])
        print("NET:", g.net_state())
    finally:
        g.close()
