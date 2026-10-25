#!/usr/bin/env python3
"""Production UI sweep: store tabs, topup flow (invoice creation only), characters, leaderboard."""
import json, time
from bakwan_session import Game

def click_button(g, pattern):
    return g.frame.evaluate(f"""(() => {{
      const b = Array.from(document.querySelectorAll('button')).find(b => /{pattern}/i.test(b.textContent));
      if (b) {{ b.click(); return true; }} return false; }})()""")

def main():
    g = Game()
    try:
        print("screen:", g.screen())
        # Store
        click_button(g, "Store")
        g.page.wait_for_timeout(2000)
        g.shot("C30_store_gacha_tab")
        print("gacha buttons:", g.ev("""(() => JSON.stringify(Array.from(document.querySelectorAll('button')).map(b=>b.textContent.trim()).filter(t=>/bakwan|XP|Rp/i.test(t))))()"""))
        # XP bottle tab
        click_button(g, "XP Bottle")
        g.page.wait_for_timeout(1500)
        g.shot("C31_store_xp_tab")
        # Topup tab
        click_button(g, "Top-up")
        g.page.wait_for_timeout(1500)
        g.shot("C32_store_topup_tab")
        # click the Rp5000 pack -> invoice creation (NO payment)
        r = click_button(g, "Rp.?5\\.000|5\\.000")
        print("clicked 5000 pack:", r)
        g.page.wait_for_timeout(4000)
        g.shot("C33_topup_invoice_step")
        # capture any new tab / modal state
        print("pages:", [pg.url[:90] for pg in g.ctx.pages])
        # go back to menu, open characters
        click_button(g, "Menu")
        g.page.wait_for_timeout(1500)
        click_button(g, "Ganti Karakter")
        g.page.wait_for_timeout(2000)
        g.shot("C34_chars_screen")
        click_button(g, "Menu")
        g.page.wait_for_timeout(1200)
        # leaderboard
        click_button(g, "Leaderboard")
        g.page.wait_for_timeout(2000)
        g.shot("C35_leaderboard_prod")
        click_button(g, "Menu")
        g.page.wait_for_timeout(1200)
        # profile/history
        click_button(g, "Riwayat")
        g.page.wait_for_timeout(1800)
        g.shot("C36_profile_prod")
        p = g.player()
        print("player:", json.dumps({k: p[k] for k in ("name", "elo", "bakwan", "wins", "losses", "draws", "selectedChar")}))
    finally:
        g.close()

if __name__ == "__main__":
    main()
