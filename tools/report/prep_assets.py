#!/usr/bin/env python3
"""Prepare optimized JPEG assets for the bug bounty PDF report."""
import os
from PIL import Image

SRC = "/home/z/my-project/download/screenshots"
DST = "/home/z/my-project/scripts/report_assets"
os.makedirs(DST, exist_ok=True)

# (source, output_name)
picks = [
    ("02_game_page_scrolled.png",   "gate_login.jpg"),
    ("06_after_signup_click.png",   "captcha_checkbox.jpg"),
    ("09_captcha_next.png",         "captcha_challenge.jpg"),
    ("11_after_captcha_verify.png", "captcha_expired.jpg"),
    ("89_game_direct.png",          "bypass_maindemo.jpg"),
    ("90_demo_game.png",            "menu_utama.jpg"),
    ("92_ADMIN_PANEL.png",          "admin_ringkasan.jpg"),
    ("93_ADMIN_PEMAIN.png",         "admin_pemain.jpg"),
    ("95_ADMIN_PENGATURAN.png",     "admin_pengaturan.jpg"),
    ("98_ADMIN_LOG.png",            "admin_log.jpg"),
    ("99_LATIHAN.png",              "latihan_countdown.jpg"),
    ("100_latihan_start.png",       "latihan_gameplay.jpg"),
    ("101_hit_attempt.png",         "latihan_boom.jpg"),
    ("104_latihan_result.png",      "latihan_hasil.jpg"),
    ("123_RANKED_MATCH.png",        "ranked_match.jpg"),
    ("125_hit4.png",                "ranked_bomb.jpg"),
    ("126_KO_RESULT.png",           "ranked_kalah.jpg"),
    ("111_STORE.png",               "store_gacha.jpg"),
    ("113_GACHA_PULL.png",          "gacha_hasil.jpg"),
    ("114_TOPUP.png",               "topup_paket.jpg"),
    ("115_TOPUP_FLOW.png",          "topup_demo.jpg"),
    ("120_KARAKTER.png",            "karakter.jpg"),
    ("127_LEADERBOARD.png",         "leaderboard.jpg"),
    ("128_RIWAYAT.png",             "profil.jpg"),
    ("132_TEMAN.png",               "teman.jpg"),
    # ---- Ronde 2: audit dengan akun resmi (25 Okt 2026) ----
    ("A02_logged_in_home.png",      "r2_home_login.jpg"),
    ("A03_menu_main.png",           "r2_menu_utama.jpg"),
    ("A05_BUG_settings_denied.png", "r2_bug08_denied.jpg"),
    ("A06_gift_panel.png",          "r2_hadiah_harian.jpg"),
    ("A07_riwayat.png",             "r2_profil_awal.jpg"),
    ("A09_topup_page.png",          "r2_topup_store.jpg"),
    ("A10_topup_prices.png",        "r2_topup_harga.jpg"),
    ("A11_topup_all.png",           "r2_topup_paket1.jpg"),
    ("A12_store_gacha.png",         "r2_gacha_store.jpg"),
    ("A13_gacha_rates.png",         "r2_gacha_rates.jpg"),
    ("A16_gacha_result.png",        "r2_gacha_agatha.jpg"),
    ("A17_xp_bottle.png",           "r2_xp_bottle.jpg"),
    ("A19_BUG_xendit_error.png",    "r2_bug10_xendit.jpg"),
    ("A20_ranked_queue.png",        "r2_ranked_vs_tyyie.jpg"),
    ("A22_battle_start.png",        "r2_battle_start.jpg"),
    ("A23_battle_mid1.png",         "r2_battle_skill.jpg"),
    ("A26_match2_mid.png",          "r2_match2_miss.jpg"),
    ("A27_match2_late.png",         "r2_match2_bom.jpg"),
    ("A28_riwayat_matches.png",     "r2_profil_setelah.jpg"),
    ("A29_riwayat_rows.png",        "r2_riwayat_rows.jpg"),
    ("A31_tyyie_header.png",        "r2_profil_tyyie.jpg"),
    ("A32_ganti_karakter.png",      "r2_karakter_botak.jpg"),
    ("A36_char_top.png",            "r2_karakter_agatha.jpg"),
    ("A53_train5_result.png",       "r2_bug09_11hit.jpg"),
    ("A56_gift_status2.png",        "r2_bug09_misi.jpg"),
    ("A58_leaderboard.png",         "r2_leaderboard_bawah.jpg"),
    ("A59_leaderboard_top.png",     "r2_leaderboard_top.jpg"),
    ("A61_teman_top.png",           "r2_teman_kode.jpg"),
    ("A62_self_friend.png",         "r2_teman_self.jpg"),
    ("A63_invalid_code.png",        "r2_teman_invalid.jpg"),
    ("A64_nickname_modal.png",      "r2_nickname.jpg"),
    ("A66_filesusr_direct.png",     "r2_bug02_direct.jpg"),
    ("A68_admin_panel.png",         "r2_bug03_admin.jpg"),
    ("A69_admin_settings.png",      "r2_bug03_setting.jpg"),
    ("A71_final_state.png",         "r2_final_state.jpg"),
    # ---- Ronde 3: build baru 20261025-130337, server play.bakwan.id (25 Okt 2026) ----
    ("R3_01_cobalagi.png",          "r3_bug11_downtime.jpg"),
    ("R3_07_oldbuild_swap.png",     "r3_bug11_oldbuild.jpg"),
    ("C01_prod_recovered_menu.png", "r3_recovery_menu.jpg"),
    ("C02_prod_menu_full.png",      "r3_banner_update.jpg"),
    ("B01_daily_login_reward.png",  "r3_daily_newbuild.jpg"),
    ("B05_admin_newbuild.png",      "r3_admin_demo_baru.jpg"),
    ("B06_admin_settings_newbuild.png", "r3_admin_setting_baru.jpg"),
    ("B08_latihan_newbuild.png",    "r3_latihan_baru.jpg"),
    ("R3_14.png",                   "r3_bom_lingkaran.jpg"),
    ("B09_latihan_result_newbuild.png", "r3_latihan_min20.jpg"),
    ("B10_bot_running.png",         "r3_bot_demo.jpg"),
    ("B11_bot_perfect_result.png",  "r3_bot_perfect73.jpg"),
    ("B13_ranked_result_demo.png",  "r3_ranked_menang_demo.jpg"),
    ("C03_train_bot_running.png",   "r3_train_bot_prod.jpg"),
    ("C04_train_result_bot.png",    "r3_train_hasil_bot.jpg"),
    ("C20_match_result.png",        "r3_menang_ranked_prod.jpg"),
    ("C32_store_topup_tab.png",     "r3_topup_diskon.jpg"),
    ("C33_topup_invoice_step.png",  "r3_bug10_fixed_invoice.jpg"),
    ("C50_profile_final_r3.png",    "r3_profil_final.jpg"),
    ("C51_leaderboard_final_r3.png", "r3_leaderboard_final.jpg"),
    ("C52_karis_prod_page.png",     "r3_karis_page.jpg"),
    ("C53_store_gacha_30bakwan.png", "r3_gacha_30bakwan.jpg"),
]

total = 0
for src, dst in picks:
    p = os.path.join(SRC, src)
    if not os.path.exists(p):
        print("MISSING:", src)
        continue
    img = Image.open(p).convert("RGB")
    if img.width > 1100:
        ratio = 1100 / img.width
        img = img.resize((1100, int(img.height * ratio)), Image.LANCZOS)
    out = os.path.join(DST, dst)
    img.save(out, "JPEG", quality=86, optimize=True)
    kb = os.path.getsize(out) / 1024
    total += kb
    print(f"{dst:28s} {kb:7.0f} KB")
print(f"TOTAL: {total/1024:.1f} MB, {len(picks)} files")
