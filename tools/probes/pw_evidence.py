#!/usr/bin/env python3
"""Final evidence screenshots: profile, leaderboard, gacha affordability, Karis page."""
import json
from bakwan_session import Game

def click_button(g, pattern):
    return g.frame.evaluate(f"""(() => {{
      const b = Array.from(document.querySelectorAll('button')).find(b => /{pattern}/i.test(b.textContent));
      if (b) {{ b.click(); return true; }} return false; }})()""")

def main():
    g = Game()
    try:
        print("screen:", g.screen())
        p = g.player()
        print("player:", json.dumps({k: p.get(k) for k in ("name", "elo", "peakElo", "bakwan", "wins", "losses", "draws", "selectedChar")}))
        # profile + history
        click_button(g, "Riwayat")
        g.page.wait_for_timeout(2000)
        g.shot("C50_profile_final_r3")
        click_button(g, "Kembali|Menu")
        g.page.wait_for_timeout(1500)
        # leaderboard
        click_button(g, "Leaderboard")
        g.page.wait_for_timeout(2200)
        g.shot("C51_leaderboard_final_r3")
        click_button(g, "Kembali|Menu")
        g.page.wait_for_timeout(1500)
        # characters -> Karis (unowned showcase)
        click_button(g, "Ganti Karakter")
        g.page.wait_for_timeout(2000)
        g.frame.evaluate("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /Karis/i.test(b.textContent)); if (b) b.click(); })()""")
        g.page.wait_for_timeout(1800)
        g.shot("C52_karis_prod_page")
        click_button(g, "Kembali|Menu")
        g.page.wait_for_timeout(1500)
        # store gacha with 30 bakwan (affordability evidence)
        click_button(g, "Store")
        g.page.wait_for_timeout(2000)
        g.shot("C53_store_gacha_30bakwan")
        print("store text:", g.ev("""(() => JSON.stringify(Array.from(document.querySelectorAll('button')).map(b=>b.textContent.trim()).filter(t=>/bakwan|1x|10x/i.test(t)).slice(0,8)))()"""))
    finally:
        g.close()

if __name__ == "__main__":
    main()
