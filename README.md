# Bakwan Fight Back — Bug Bounty Toolkit & Evidence

Repositori ini berisi **seluruh alat (tools), bot, skrip probe, log, dan bukti** yang digunakan selama pengujian bug bounty pada fitur game beta **Bakwan Fight Back** (`bakwan.id/game`) milik Bakwan, dalam **3 ronde pengujian** (24–25 Okt 2026) yang menghasilkan **12 temuan** (BUG-01 s.d. BUG-12).

> Laporan lengkap (50 halaman, Bahasa Indonesia): [`docs/Laporan_Bug_Bounty_Bakwan_Fight_Back.pdf`](docs/Laporan_Bug_Bounty_Bakwan_Fight_Back.pdf)

---

## Ringkasan Hasil Pengujian

| ID | Judul | Severity | Status (per 25 Okt) |
|----|-------|----------|---------------------|
| BUG-01 | Loop reCAPTCHA "Verification challenge expired" menolak semua pendaftaran | Kritis | Diverifikasi 6 sesi / 15+ ronde captcha |
| BUG-02 | Bypass gerbang login via iframe `filesusr.com` → demo terbuka tanpa akun | Kritis | Masih hidup (re-audit R2, build 20261024-190551) |
| BUG-03 | Panel Admin demo penuh tanpa autentikasi (`isAdmin:true` hardcoded) | Kritis | Masih hidup (re-audit R2) |
| BUG-04 | Seed 8 NPC + `demoPay` terekspos di klien demo | Sedang | Masih hidup (R2) |
| BUG-05 | State admin demo dapat diubah tanpa auth | Sedang | — |
| BUG-06 | ATK XP bottle menampilkan desimal (39.1) | Rendah | — |
| BUG-07 | Inkonsistensi UI minor | Rendah | — |
| BUG-08 | Menu "Pengaturan Akun" → paywall `restrictedPageId` untuk member login | Sedang | **Dikonfirmasi dev — dalam pengerjaan** |
| BUG-09 | XP latihan tidak masuk (desinkronisasi `trainMinHits` server vs UI) | Mayor | **Dinyatakan by-design oleh dev** (server menghitung hit via `sendHits`) |
| BUG-10 | Checkout top-up Xendit gagal permanen ("Sorry, this wasn't supposed to happen") | Kritis | **Dikonfirmasi dev — diperbaiki; diverifikasi fixed di R3** (invoice `bfb-mvngxvaj65cdx8` terbit mulus, tidak dibayar) |
| BUG-11 | Produksi DOWN total ±1 jam (`WD_SCHEMA_DOES_NOT_EXIST`) di kedua build | Kritis | Pulih sendiri saat build 20261025-130337 digulirkan |
| BUG-12 | Hook debug publik `window.BFB_DEBUG` → bot 80/80 perfect di produksi | Kritis | Masih hidup |

**Aktivitas pengujian pada akun resmi `vameb61409`** (milik penyelenggara): 16 match ranked (10W/8L, Elo 100→165 puncak), 6+ sesi latihan, gacha 2 tarikan, 1 invoice Xendit **tidak dibayar** (tanpa otorisasi uang nyata), tidak ada data pemain lain yang tersentuh.

---

## Struktur Repositori

```
├── tools/
│   ├── session/          # Manajemen sesi browser & email
│   ├── bots/             # Bot gameplay (latihan, ranked, perfect-tap)
│   ├── probes/           # Probe API & pengambil bukti
│   └── report/           # Generator laporan PDF & aset
├── evidence/
│   ├── logs/             # Log run bot, state produksi, monitor
│   ├── run_screenshots/  # Screenshot hasil eksekusi tool
│   ├── report_assets/    # Aset JPEG final yang dipakai di laporan
│   └── source_dumps/     # Dump HTML build game (demo/produksi)
└── docs/
    └── Laporan_Bug_Bounty_Bakwan_Fight_Back.pdf   # Laporan final 50 hal
```

---

## Inventaris Tools

### 1. `tools/session/` — Sesi & Akses

| File | Fungsi |
|------|--------|
| `tempmail.py` | Klien API mail.tm — pembuatan email sementara + polling inbox (Ronde 1, pendaftaran akun) |
| `bakwan_session.py` | Login Wix IAM (`_api/iam/authentication/v2/login`) → `createSessionCookie` → simpan `auth_state.json` (storage state Playwright, **tidak di-commit**) |
| `pw_attach.py` | Launcher Playwright Chromium persisten (CDP 9222) + helper attach ke sesi login yang ada |

### 2. `tools/bots/` — Bot Gameplay

| File | Fungsi |
|------|--------|
| `train_bot.py` | Bot latihan ronde 2 — tap pixel note via koordinat (iterasi 1) |
| `train_bot2.py` | Bot latihan v2 — toleransi timing lebih baik |
| `train_bot3.py` | Bot latihan v3 — final, dipakai untuk 5 sesi bukti BUG-09 (sesi 11/65 hit) |
| `perfect_bot.js` | **Bot in-page sempurna** via hook `window.BFB_DEBUG` (sched+tap) — bukti BUG-12: 73/73 perfect demo, 80/80 perfect produksi (3.594 dmg) |
| `prod_monitor.sh` | Poll ketersediaan build produksi tiap 30s selama insiden DOWN (BUG-11) |

### 3. `tools/probes/` — Probe API & Bukti

| File | Fungsi |
|------|--------|
| `pw_probe.py` | Probe awal endpoint game (guard, state, storefront) |
| `pw_probe2.py` | Probe lanjutan — 37 panggilan API dalam 9 kelompok (gacha 7 varian, `buyItem`/`useItem` negatif, `trainDone` palsu, `selectChar` legendary, `creditPurchase`, 6 fungsi admin) → **semua ditolak server (hardened)** |
| `pw_admin_probe.py` | Verifikasi panel admin demo + fungsi admin (hasil: `NOT_ADMIN`, `NO_FN`) |
| `pw_dump.py` | Dump state game & snapshot DOM untuk analisis |
| `pw_ranked.py` / `pw_ranked2.py` | Otomasi match ranked (matchmaking, battle, hasil, log Elo per match) |
| `pw_train.py` | Driver sesi latihan terkontrol (bukti BUG-09) |
| `pw_sweep.py` | Sweep seluruh menu game (store, gacha, karakter, teman, profil, leaderboard) |
| `pw_select_isolate.py` | Isolasi perilaku pemilihan karakter & validasi input |
| `pw_verify.py` | Verifikasi ulang bug spesifik (reproduksi bersih) |
| `pw_demopay.py` | Uji `demoPay` di demo vs produksi |
| `pw_evidence.py` | Pengambil screenshot bukti otomatis (seri B/C/R3) |

### 4. `tools/report/` — Generator Laporan

| File | Fungsi |
|------|--------|
| `prep_assets.py` | Optimasi 60+ screenshot PNG → JPEG terkompresi + crop panel (v1 tersimpan `.bak`) |
| `gen_report.py` | Generator laporan utama — ReportLab, 15 bab, matriks 12 temuan, kronologi, tabel probe, auto-number gambar |
| `merge_final.py` | Gabung `cover.pdf` + `body.pdf` → laporan final |
| `cover.html` | Sampul laporan (html2poster, "Edisi Ronde 3") |

---

## Cara Menjalankan

```bash
pip install playwright reportlab pymupdf pillow
playwright install chromium

# 1. Login & simpan sesi (isi EMAIL/PASSWORD sendiri)
python tools/session/bakwan_session.py

# 2. Buka game dalam sesi persisten
python tools/session/pw_attach.py

# 3. Contoh probe / bot
python tools/probes/pw_sweep.py
node tools/bots/perfect_bot.js   # dijalankan di dalam konsol halaman game
```

> `auth_state.json` (cookie sesi) **sengaja tidak di-commit** — mengandung kredensial hidup.

---

## Catatan Keamanan & Integritas

- **Tidak di-commit**: `auth_state.json` (cookie sesi Wix akun audit) dan `mail_session.json` (token mail.tm) karena berisi kredensial aktif. Semua file lain diunggah apa adanya tanpa modifikasi.
- Tidak ada kredensial/password yang di-hardcode di skrip manapun; email akun audit hanya muncul dalam prosa laporan.
- Token akses GitHub yang dipakai untuk membuat repo ini **disimpan di mana pun** — disarankan **revoke PAT** setelah verifikasi.
- Invoice Xendit pada pengujian BUG-10/R3 sengaja **tidak dibayar**; tidak ada pembelian uang nyata yang dilakukan.
- Repositori dibuat **private** sesuai permintaan pemilik akun.

---

## Kronologi Singkat

- **Ronde 1 (24 Okt)** — Rekonsais + pendaftaran temp-mail (BUG-01), bypass demo (BUG-02), audit panel admin (BUG-03/04/05), dokumentasi mekanik inti, laporan v1 (21 hal).
- **Ronde 2 (25 Okt pagi)** — Re-audit akun resmi: ranked vs pemain nyata, gacha, top-up (BUG-10), latihan bot (BUG-09), pengaturan akun (BUG-08), verifikasi ulang BUG-02/03/04, laporan v2 (40 hal).
- **Ronde 3 (25 Okt siang)** — Insiden DOWN produksi (BUG-11), migrasi infra `play.bakwan.id` + WS dedicated, `BFB_DEBUG` perfect bot (BUG-12), 37 probe API (semua ditolak — server hardened), verifikasi fix BUG-10, analisis ekonomi gacha Karis (legendary ~1,43%/tarikan, tanpa pity → E≈70 tarikan ≈ 6.300–7.000 bakwan), laporan v3 (50 hal).
