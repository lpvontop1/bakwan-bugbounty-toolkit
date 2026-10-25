#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Laporan Bug Bounty - Bakwan Fight Back (bakwan.id/game) - body PDF via ReportLab."""
import os
import sys
import hashlib

PDF_SKILL_DIR = "/home/z/my-project/skills/pdf"
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, "scripts"))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts"
pdfmetrics.registerFont(TTFont("NotoSerifSC", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifSC-Bold", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif", f"{FONT_DIR}/truetype/freefont/FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Bold", f"{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Italic", f"{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-BoldItalic", f"{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf"))
registerFontFamily("NotoSerifSC", normal="NotoSerifSC", bold="NotoSerifSC-Bold")
registerFontFamily("FreeSerif", normal="FreeSerif", bold="FreeSerif-Bold",
                   italic="FreeSerif-Italic", boldItalic="FreeSerif-BoldItalic")
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans")

from pdf import install_font_fallback
install_font_fallback()

# ---------------------------------------------------------------- palette (palette.cascade output)
PAGE_BG       = colors.HexColor('#f1f1f0')
SECTION_BG    = colors.HexColor('#eae9e8')
CARD_BG       = colors.HexColor('#e8e6e2')
TABLE_STRIPE  = colors.HexColor('#efeeed')
HEADER_FILL   = colors.HexColor('#6b634d')
COVER_BLOCK   = colors.HexColor('#5c5646')
BORDER        = colors.HexColor('#cec9ba')
ICON          = colors.HexColor('#9e8745')
ACCENT        = colors.HexColor('#917521')
ACCENT_2      = colors.HexColor('#4598b4')
TEXT_PRIMARY  = colors.HexColor('#1b1a18')
TEXT_MUTED    = colors.HexColor('#78756f')
SEM_SUCCESS   = colors.HexColor('#408256')
SEM_WARNING   = colors.HexColor('#9e8046')
SEM_ERROR     = colors.HexColor('#96423a')
SEM_INFO      = colors.HexColor('#587ca0')

# ---------------------------------------------------------------- page geometry
MARGIN = 0.9 * inch
PAGE_W, PAGE_H = A4
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - 2 * MARGIN
H1_ORPHAN = AVAIL_H * 0.25
MAX_KEEP = PAGE_H * 0.4

ASSETS = "/home/z/my-project/scripts/report_assets"
OUT_BODY = "/home/z/my-project/scripts/body.pdf"

DOC_TITLE = "Laporan Bug Bounty - Bakwan Fight Back (bakwan.id/game)"

# ---------------------------------------------------------------- styles
S = {}
S["body"] = ParagraphStyle("body", fontName="FreeSerif", fontSize=10.5, leading=17,
                           alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY, spaceAfter=10)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], alignment=TA_LEFT, leftIndent=16,
                             bulletIndent=4, spaceAfter=5)
S["h1"] = ParagraphStyle("h1", fontName="FreeSerif-Bold", fontSize=19, leading=24,
                         textColor=HEADER_FILL, spaceBefore=18, spaceAfter=10)
S["h2"] = ParagraphStyle("h2", fontName="FreeSerif-Bold", fontSize=14, leading=19,
                         textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8)
S["h3"] = ParagraphStyle("h3", fontName="FreeSerif-Bold", fontSize=11.5, leading=16,
                         textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6)
S["caption"] = ParagraphStyle("caption", fontName="FreeSerif-Italic", fontSize=8.5, leading=12,
                              alignment=TA_CENTER, textColor=TEXT_MUTED, spaceBefore=3, spaceAfter=6)
S["code"] = ParagraphStyle("code", fontName="DejaVuSans", fontSize=8.0, leading=11.5,
                           textColor=TEXT_PRIMARY, backColor=CARD_BG, borderColor=BORDER,
                           borderWidth=0.6, borderPadding=6, leftIndent=6, spaceBefore=6,
                           spaceAfter=10, alignment=TA_LEFT)
S["cell"] = ParagraphStyle("cell", fontName="FreeSerif", fontSize=9.5, leading=13,
                           alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S["cellc"] = ParagraphStyle("cellc", parent=S["cell"], alignment=TA_CENTER)
S["cellh"] = ParagraphStyle("cellh", fontName="FreeSerif-Bold", fontSize=9.5, leading=13,
                            alignment=TA_CENTER, textColor=colors.white)
S["callout_num"] = ParagraphStyle("callout_num", fontName="FreeSerif-Bold", fontSize=20, leading=24,
                                  textColor=ACCENT, alignment=TA_CENTER)
S["callout_lbl"] = ParagraphStyle("callout_lbl", fontName="FreeSerif", fontSize=8.5, leading=11,
                                  textColor=TEXT_MUTED, alignment=TA_CENTER)
S["quote"] = ParagraphStyle("quote", fontName="FreeSerif-Italic", fontSize=10.5, leading=16,
                            leftIndent=24, textColor=TEXT_MUTED, spaceBefore=6, spaceAfter=10)
S["toc_title"] = ParagraphStyle("toc_title", fontName="FreeSerif-Bold", fontSize=19, leading=24,
                                textColor=HEADER_FILL, spaceAfter=14)

# ---------------------------------------------------------------- helpers
def P(text, style="body"):
    return Paragraph(text, S[style])

def add_heading(text, level=0):
    key = "h_" + hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), S["h1" if level == 0 else "h2"])
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def h1(story, text):
    story.append(CondPageBreak(H1_ORPHAN))
    story.append(add_heading(text, 0))

def h2(story, text):
    story.append(add_heading(text, 1))

def safe_keep(elements):
    total = 0
    for el in elements:
        w, h = el.wrap(AVAIL_W, PAGE_H)
        total += h
    if total <= MAX_KEEP:
        return [KeepTogether(elements)]
    if len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

_FIG_NO = [0]

def img(path, caption, max_h=225):
    _FIG_NO[0] += 1
    full = os.path.join(ASSETS, path)
    pil = PILImage.open(full)
    ow, oh = pil.size
    ratio = min(AVAIL_W / ow, max_h / oh, 1.0)
    im = Image(full, width=ow * ratio, height=oh * ratio)
    cap = Paragraph("Gambar %d: %s" % (_FIG_NO[0], caption), S["caption"])
    return safe_keep([im, cap])

def callout_row(items):
    """Row of stat callout boxes. items = [(big, label), ...]"""
    n = len(items)
    box_w = (AVAIL_W - (n - 1) * 10) / n
    cells = []
    for big, lbl in items:
        inner = Table([[Paragraph("<b>%s</b>" % big, S["callout_num"])],
                       [Paragraph(lbl, S["callout_lbl"])]], colWidths=[box_w])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
            ("BOX", (0, 0), (-1, -1), 1, ACCENT),
            ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
            ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        cells.append(inner)
    row = Table([cells], colWidths=[box_w + (10 if i < n - 1 else 0) for i in range(n)])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return row

def make_table(header, rows, ratios, align_map=None):
    """Safe table: Paragraph cells, proportional widths, centered."""
    widths = [r * AVAIL_W for r in ratios]
    assert abs(sum(ratios) - 1.0) < 0.01
    data = [[Paragraph("<b>%s</b>" % c, S["cellh"]) for c in header]]
    for row in rows:
        cells = []
        for j, c in enumerate(row):
            st = "cell"
            if align_map and align_map.get(j) == "c":
                st = "cellc"
            cells.append(Paragraph(str(c), S[st]))
        data.append(cells)
    t = Table(data, colWidths=widths, hAlign="CENTER", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_FILL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        style.append(("BACKGROUND", (0, i), (-1, i), colors.white if i % 2 == 1 else TABLE_STRIPE))
    t.setStyle(TableStyle(style))
    return t

# ---------------------------------------------------------------- doc template
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, "bookmark_name"):
            level = getattr(flowable, "bookmark_level", 0)
            text = getattr(flowable, "bookmark_text", "")
            key = getattr(flowable, "bookmark_key", "")
            self.notify("TOCEntry", (level, text, self.page, key))

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 0.55 * inch, DOC_TITLE)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    canvas.setFont("FreeSerif", 7.5)
    canvas.drawString(MARGIN, 0.45 * inch, "Tim QA - Z.ai Agent")
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, str(doc.page))
    canvas.restoreState()

story = []

# ================================================================ TOC
story.append(Paragraph("<b>Daftar Isi</b>", S["toc_title"]))
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle("TOC0", fontName="FreeSerif-Bold", fontSize=11, leading=18, leftIndent=6,
                   textColor=TEXT_PRIMARY),
    ParagraphStyle("TOC1", fontName="FreeSerif", fontSize=10, leading=15, leftIndent=24,
                   textColor=TEXT_MUTED),
]
story.append(toc)
story.append(PageBreak())

# ================================================================ 1. RINGKASAN EKSEKUTIF
h1(story, "1. Ringkasan Eksekutif")
story.append(P(
    "Laporan ini menyajikan hasil pengujian kualitas (QA) dan bug hunting terhadap fitur game "
    "beta <b>\u201cBakwan Fight Back\u201d</b> yang berjalan di halaman <b>https://www.bakwan.id/game</b>. "
    "Pengujian dilaksanakan dalam <b>tiga ronde</b> pada 24\u201325 Oktober 2026 sebagai bagian dari "
    "program bug bounty 7 hari yang diumumkan pengelola situs Bakwan Universe. Ronde pertama "
    "dilakukan tanpa akun (percobaan pendaftaran mandiri via temp mail dan eksplorasi mode "
    "demo). Ronde kedua \u2014 dilakukan setelah pengembang mengonfirmasi bahwa halaman demo bukan "
    "representasi penuh game asli \u2014 menggunakan <b>akun resmi yang disediakan penguji dari "
    "pihak penyelenggara</b> (vameb61409@hiringview.com, tanpa captcha saat login), sehingga "
    "seluruh alur game produksi dapat diuji secara langsung dan mendalam. Seluruh pengujian "
    "bersifat pasif dan non-destruktif: tanpa serangan injeksi, tanpa beban berlebih ke server, "
    "dan tanpa perubahan data apa pun milik pengguna lain."))
story.append(P(
    "Hasil gabungan ketiga ronde menemukan <b>12 temuan (BUG-01 s.d. BUG-12)</b>, lima di "
    "antaranya tergolong kritis. Temuan paling serius pada ronde pertama adalah <b>panel admin "
    "game yang dapat dibuka tanpa autentikasi apa pun</b> melalui mode demo \u2014 temuan ini "
    "kembali diverifikasi pada ronde kedua dan <b>masih hidup di build terbaru 20261024-190551</b>. "
    "Temuan kritis kedua adalah <b>bypass gerbang login game</b> lewat URL iframe yang juga masih "
    "berfungsi. Temuan kritis ketiga adalah <b>loop kedaluwarsa reCAPTCHA</b> yang menggagalkan "
    "seluruh 6 sesi pendaftaran akun pada ronde pertama. Temuan kritis <b>baru</b> dari ronde "
    "kedua adalah <b>kegagalan total halaman checkout Xendit</b> (\u201cSorry, this wasn't supposed "
    "to happen\u201d) yang membuat seluruh paket top-up \u2014 meski sudah diiklankan berdiskon 33% \u2014 "
    "tidak mungkin dibayar, ditambah dua temuan sedang/mayor: halaman Pengaturan Akun yang "
    "diblokir paywall untuk member yang sedang login (BUG-08) dan reward latihan yang tidak "
    "pernah terkredit meski syarat 10 hit terpenuhi di layar (BUG-09)."))
story.append(P(
    "Sebagai kelanjutan, <b>ronde ketiga</b> dilaksanakan pada 25 Oktober 2026 (siang) setelah "
    "pengembang mengumumkan bahwa BUG-08 dan BUG-10 sedang dikerjakan, BUG-09 berjalan sesuai "
    "desain, serta meminta penguji menguji logika gacha hingga memperoleh karakter Legendary "
    "\u201cKaris\u201d. Ronde ini menangkap dua peristiwa besar: (1) <b>migrasi infrastruktur "
    "total</b> \u2014 game pindah dari berkas statis filesusr.com ke subdomain khusus "
    "<b>play.bakwan.id</b> dengan server WebSocket dedicated, disertai pembongkaran sistem battle "
    "dan Elo, penambahan hadiah login harian, dan peningkatan hadiah harian menjadi 5/15/10 "
    "bakwan; dan (2) <b>sekitar satu jam downtime produksi</b> dengan error "
    "<b>WD_SCHEMA_DOES_NOT_EXIST</b> yang menggagalkan boot game untuk seluruh pemain (BUG-11). "
    "Ronde ketiga juga membuktikan secara empiris sebuah celah klien yang serius: hook debug "
    "<b>window.BFB_DEBUG</b> yang terekspos publik memungkinkan pembuatan <b>bot sempurna</b> "
    "(80/80 hit perfect, 10 kemenangan ranked termasuk 5 beruntun, Elo 39 \u2192 165) yang mustahil "
    "dibedakan dari pemain manusia terbaik sekalipun (BUG-12). Analisis ekonomi juga menutup "
    "misi gacha: tanpa top-up uang riil, karakter Karis membutuhkan \u2248 70 tarikan \u2248 "
    "6.300\u20137.000 bakwan \u2248 233 hari pengumpulan hadiah harian maksimum \u2014 karena "
    "kemenangan ranked terbukti tidak membayar bakwan sama sekali (diverifikasi pada 10 "
    "kemenangan). Di sisi positif, seluruh uji manipulasi API server (37 panggilan dalam 9 kelompok: gacha, beli/pakai "
    "item negatif, ringkasan latihan palsu, demoPay, ACL admin) <b>ditolak bersih oleh server "
    "baru</b>, dan BUG-10 terkonfirmasi <b>perbaikan</b>: invoice Xendit kini terbuat mulus."))
story.append(Spacer(1, 6))
story.append(callout_row([
    ("12", "Temuan bug"),
    ("5", "Berlabel kritis"),
    ("3", "Ronde pengujian"),
    ("82", "Bukti tangkapan layar"),
]))
story.append(Spacer(1, 12))

h2(story, "1.1 Matriks Temuan")
tbl = make_table(
    ["ID", "Temuan", "Keparahan", "Status"],
    [
        ["BUG-01", "Loop kedaluwarsa reCAPTCHA memblokir pendaftaran akun (6 sesi gagal, "
                   "15+ ronde per sesi)", "Kritis", "Terkonfirmasi (R1)"],
        ["BUG-02", "Gerbang login game dapat dilewati: mode \u201cMain Demo\u201d terbuka lewat "
                   "URL iframe tanpa akun", "Kritis", "Masih hidup (R2)"],
        ["BUG-03", "Panel admin terbuka penuh tanpa autentikasi; flag isAdmin=true di-hardcode "
                   "pada mode demo", "Kritis", "Masih hidup (R2)"],
        ["BUG-04", "Data pemain (Elo, saldo bakwan, kode teman) terekspos di panel admin tanpa "
                   "redaksi", "Sedang", "Masih hidup (R2)"],
        ["BUG-05", "Simulasi pembayaran top-up sekali klik (\u201cBAYAR (DEMO)\u201d) langsung "
                   "mengkreditkan saldo", "Sedang", "Diakui dev (rollback)"],
        ["BUG-06", "Statistik karakter menampilkan nilai desimal (ATK 39.1, DEF 18.5) pada UI", "Rendah", "Terkonfirmasi (R1)"],
        ["BUG-07", "Inkonsistensi HP sasaran latihan: UI menampilkan 5000, konfigurasi kode 3000", "Rendah", "Perlu konfirmasi dev"],
        ["BUG-08", "Halaman \u201cPengaturan Akun\u201d diblokir paywall \u201cYou don't have permissions\u201d "
                   "untuk member yang sedang login", "Sedang", "Baru (R2); dev: dikerjakan"],
        ["BUG-09", "Reward latihan tidak terkredit: hasil 11 hit (syarat UI 10) tidak memberi XP "
                   "maupun bonus misi harian", "Mayor", "Dev: by design (R3)"],
        ["BUG-10", "Checkout Xendit error permanen \u201cSorry, this wasn't supposed to happen\u201d \u2014 "
                   "top-up mustahil dibayar", "Kritis", "PERBAIKAN (R3)"],
        ["BUG-11", "Downtime produksi \u22481 jam: game gagal boot dengan error backend "
                   "WD_SCHEMA_DOES_NOT_EXIST (dampak ke seluruh pemain)", "Kritis", "Baru (R3); pulih sendiri"],
        ["BUG-12", "Hook debug klien window.BFB_DEBUG terekspos publik: jadwal note, koordinat, "
                   "dan fungsi tap() terbuka \u2014 bot sempurna trivial", "Kritis", "Baru (R3); masih hidup"],
    ],
    [0.11, 0.55, 0.16, 0.18], align_map={0: "c", 2: "c", 3: "c"})
story.append(tbl)
story.append(Paragraph("Tabel 1: Matriks temuan bug bounty Bakwan Fight Back \u2014 R1 = ronde 1 (tanpa akun), R2 = ronde 2 (akun resmi), R3 = ronde 3 (build play.bakwan.id).", S["caption"]))
story.append(Spacer(1, 6))
story.append(P(
    "Catatan penting mengenai dampak: seluruh aksi admin pada BUG-03 diuji hanya pada <b>mode "
    "demo</b> yang basis datanya tersimpan lokal di peramban (localStorage) dan berisi 8 pemain "
    "bawaan (seed/NPC). Server produksi Wix didesain memvalidasi ulang hak admin di sisi server "
    "melalui fungsi <b>needAdmin()</b>, sehingga tidak ada bukti perubahan data produksi. Meski "
    "demikian, pola \u201cgate admin di sisi klien\u201d tetap berisiko tinggi dan wajib diperbaiki, "
    "karena mengekspos permukaan antarmuka admin, membingungkan penguji/peneliti, dan berpotensi "
    "menjadi jalan masuk apabila terdapat jalur lain yang lupa divalidasi."))

# ================================================================ 2. RUANG LINGKUP & METODOLOGI
h1(story, "2. Ruang Lingkup dan Metodologi")
h2(story, "2.1 Ruang Lingkup")
story.append(P(
    "Target pengujian adalah fitur game beta pada halaman https://www.bakwan.id/game beserta "
    "seluruh aset yang dimuat oleh halaman tersebut, termasuk aplikasi game \u201cBakwan Fight "
    "Back\u201d yang berjalan di dalam iframe. Ronde pertama menggunakan peramban Chromium "
    "otomatis (headless) dengan resolusi 1280x577, jaringan normal tanpa proxy, dan tanpa alat "
    "penguji berbayar. Email yang digunakan untuk percobaan pendaftaran adalah alamat "
    "sementara <b>bakkyo1lx30lbw@maxxspace.com</b> yang dibuat melalui layanan mail.tm, sesuai "
    "saran penyelenggara agar tidak memakai akun pribadi. Ronde kedua memakai akun resmi "
    "<b>vameb61409@hiringview.com</b> yang disediakan penyelenggara khusus untuk audit ini; "
    "login dengan akun tersebut tidak memerlukan captcha sehingga seluruh alur produksi "
    "(matchmaking ranked nyata, store, gacha, misi harian, leaderboard, sistem teman) dapat "
    "diuji end-to-end."))
h2(story, "2.2 Metodologi")
story.append(P(
    "Metodologi mengikuti praktik QA biasa dengan lima tahap: (1) rekonsaisasi halaman dan "
    "pengumpulan konteks program; (2) eksplorasi alur pengguna nyata mulai dari pendaftaran, "
    "login, hingga bermain; (3) pengujian batas pada input dan alur (validasi nickname, kode "
    "teman, gacha, top-up); (4) analisis sisi klien terhadap kode sumber game yang termuat "
    "(white-box) untuk memahami mekanisme dan mencari konfigurasi yang keliru; serta (5) "
    "dokumentasi setiap temuan dengan tangkapan layar dan replikasi langkah demi langkah. Pada "
    "ronde kedua, tambahan verifikasi kuantitatif dilakukan: matematika Elo dihitung ulang dari "
    "hasil match nyata, konsistensi saldo bakwan dilacak antar transaksi, dan reward misi "
    "harian diverifikasi sebelum-sesudah reload halaman."))
story.append(P(
    "Batasan etika yang diterapkan: tidak ada serangan injeksi SQL/XSS aktif ke backend, tidak "
    "ada brute force, tidak ada spamming permintaan (DoS), tidak ada upaya mengubah data server, "
    "dan tidak ada penggunaan akun milik orang lain tanpa izin. Semua aksi admin pada mode demo "
    "hanya dilihat, tidak pernah disimpan. Akun temp mail tidak jadi dibuat karena pendaftaran "
    "gagal total pada tahap verifikasi reCAPTCHA (BUG-01), sehingga tidak ada akun uji yang perlu "
    "dihapus; inbox diverifikasi kosong pada akhir sesi. Akun resmi ronde kedua adalah milik "
    "penyelenggara dan <b>sengaja tidak dihapus</b> \u2014 seluruh perubahan pada akun tersebut "
    "(dua kekalahan ranked, satu gacha, penurunan saldo 105 menjadi 20 bakwan) merupakan "
    "konsekuensi normal dari gameplay uji dan dilaporkan transparan pada Bab 14. Tidak ada "
    "invoice Xendit yang dibayar dan tidak ada pesan yang dikirim ke pemain lain."))

# ================================================================ 3. PENDAFTARAN & BUG-01
h1(story, "3. Alur Pendaftaran Akun dan Temuan reCAPTCHA (BUG-01)")
h2(story, "3.1 Gerbang Masuk Game")
story.append(P(
    "Halaman game menyambut pengunjung dengan judul \u201cPON BAKWAN \u2014 FIGHT BACK\u201d dan "
    "pesan eksplisit: \u201cMasuk ke akun website dulu untuk main Bakwan Fight Back\u201d, diikuti "
    "tombol besar MASUK / DAFTAR. Pada faktur tersemat (iframe) juga terdapat tombol \u201cMasuk / "
    "Daftar\u201d yang membuka dialog login khas Wix dengan tiga pilihan: Google, Facebook, dan "
    "Email. Jalur email dipilih karena tidak memerlukan akun pihak ketiga."))
story.extend(img("gate_login.jpg",
    "Gerbang game di bakwan.id/game mengharuskan pengguna masuk akun sebelum bermain."))
h2(story, "3.2 Formulir Pendaftaran dan reCAPTCHA")
story.append(P(
    "Formulir pendaftaran email hanya meminta dua isian: alamat email dan kata sandi. Setelah "
    "diisi dan tombol Sign Up ditekan, muncul persyaratan centang reCAPTCHA v2 (\u201cI'm not a "
    "robot\u201d). Pencetangan kotak centang memicu tantangan gambar bertumpuk (multi-round): "
    "pilih semua petak berisi sepeda motor, lampu lalu lintas, bus, sepeda, tangga, zebra cross, "
    "hidran kebakaran, hingga grid 3x3 bergaya \u201cselect all images with X\u201d yang gambarnya "
    "terus berganti."))
story.extend(img("captcha_checkbox.jpg",
    "Formulir pendaftaran meminta verifikasi reCAPTCHA sebelum Sign Up dapat dilanjutkan."))
story.extend(img("captcha_challenge.jpg",
    "Contoh tantangan gambar bertingkat; jawaban benar mengganti gambar baru tanpa jeda."))
h2(story, "3.3 BUG-01: Loop Kedaluwarsa Tantangan Verifikasi")
story.append(P(
    "<b>Deskripsi.</b> Sesi tantangan reCAPTCHA berulang kali berakhir dengan pesan "
    "\u201cVerification challenge expired. Check the checkbox again.\u201d ketika pengguna masih "
    "berada di tengah proses menjawab ronde-ronde gambar. Seluruh progres ronde hilang dan "
    "pengguna dipakai mengulang dari kotak centang. Dalam pengujian ini tercatat <b>6 sesi "
    "gagal berturut-turut</b>; sesi terpanjang menuntut <b>15+ ronde</b> gambar sebelum akhirnya "
    "kedaluwarsa tepat sebelum verifikasi final diterima."))
story.extend(img("captcha_expired.jpg",
    "Pesan \u201cVerification challenge expired\u201d muncul setelah pengguna menyelesaikan "
    "banyak ronde tantangan."))
story.append(P(
    "<b>Langkah replikasi.</b> (1) Buka bakwan.id/game, tekan MASUK / DAFTAR, pilih Sign up with "
    "email; (2) isi email dan kata sandi; (3) centang reCAPTCHA; (4) jawab tantangan gambar "
    "bertahap sampai muncul beberapa ronde penggantian gambar; (5) amati pesan expired sebelum "
    "verifikasi selesai. Tingkat reproduksi: 6/6 sesi pada pengujian ini, termasuk sesi yang "
    "dijawab sangat cepat (rata-rata di bawah 3 detik per ronde)."))
story.append(P(
    "<b>Dampak.</b> Pendaftaran via email praktis terblokir bagi pengguna biasa: setiap sesi "
    "menuntut banyak ronde (indikasi skor risiko Google yang tinggi terhadap sesi), sementara "
    "umur sesi tantangan pendek, sehingga loop kegagalan hampir pasti terjadi. Pengguna baru "
    "kehilangan akses ke fitur utama (game ranked/leaderboard), dan potensi pertumbuhan pemain "
    "terhambat. Rekomendasi perbaikan ada pada Bab 9."))

# ================================================================ 4. BUG-02 BYPASS LOGIN
h1(story, "4. Bug Akses: Bypass Gerbang Login Game (BUG-02)")
story.append(P(
    "<b>Deskripsi.</b> Halaman bakwan.id/game menuntut login sebelum bermain, namun aplikasi "
    "game sesungguhnya adalah satu berkas HTML yang dimuat dari subdomain berkas statis Wix: "
    "<b>https://www-bakwan-id.filesusr.com/html/c1ed9b_8756bf37c38fda71b8c9af151086146e.html</b>. "
    "Membuka URL tersebut langsung di peramban (tanpa cookie, tanpa sesi, tanpa akun) memunculkan "
    "layar judul game lengkap dengan tombol <b>MAIN DEMO</b> dan keterangan \u201cVersi demo - "
    "progres disimpan di browser ini\u201d. Satu klik kemudian langsung masuk ke menu utama game."))
story.append(P(
    "Dengan kata lain, syarat \u201cmasuk akun dulu untuk main\u201d hanya ditegakkan pada lapisan "
    "halaman induk (klien), bukan pada aplikasi game itu sendiri. Peneliti hanya perlu melihat "
    "atribut src iframe pada DOM halaman untuk mengekstrak URL ini \u2014 langkah yang dapat "
    "dilakukan siapa pun lewat DevTools tanpa alat khusus."))
story.extend(img("bypass_maindemo.jpg",
    "URL iframe game dibuka langsung: layar judul dengan tombol MAIN DEMO muncul tanpa login."))
story.append(P(
    "<b>Dampak.</b> (1) Persyaratan akun untuk fitur beta tidak efektif, sehingga telemetri "
    "pemain beta dan pembatasan usia/aturan komunitas dapat terlewati; (2) mode demo menyimpan "
    "progres lokal tanpa kaitan akun sehingga leaderboard beta dapat tercemar data uji; (3) "
    "kombinasi dengan BUG-03 membuat seluruh panel admin terekspos bagi pengunjung anonim. "
    "Mode demo sebagai fitur resmi tidak masalah; masalahnya adalah ketidakselarasan antara "
    "kebijakan gerbang dan perilaku aplikasi, serta tidak adanya penanda bahwa demo adalah "
    "jalur alternatif yang disengaja."))
story.append(P(
    "<b>Status ronde kedua (25 Okt).</b> Temuan ini <b>masih hidup pada build terbaru</b> "
    "20261024-190551: URL yang sama tetap terbuka publik dan menampilkan layar \u201cVersi demo \u2014 "
    "progres disimpan di browser ini\u201d dengan tombol MAIN DEMO, tanpa cookie maupun sesi. "
    "Ekspor berkas game pun tetap identik (md5 tidak berubah), sehingga seluruh analisis white-box "
    "pada laporan ini tetap berlaku untuk versi yang sedang tayang."))
story.extend(img("r2_bug02_direct.jpg",
    "Verifikasi ulang ronde kedua: URL filesusr.com tetap membuka mode demo tanpa login pada "
    "build terbaru.", max_h=170))

# ================================================================ 5. BUG-03 ADMIN PANEL
h1(story, "5. Bug Akses: Panel Admin Tanpa Autentikasi (BUG-03)")
h2(story, "5.1 Penemuan")
story.append(P(
    "Setelah masuk ke menu utama mode demo (lihat Bab 4), bilah atas game menampilkan tombol "
    "berwarna merah berlabel <b>Admin</b> di samping tombol Riwayat dan Layar penuh. Menekannya "
    "membuka panel administrasi empat tab: <b>Ringkasan</b>, <b>Pemain</b>, <b>Pengaturan</b>, "
    "dan <b>Log</b> \u2014 semuanya dapat diakses tanpa kata sandi, tanpa konfirmasi, dan tanpa "
    "sesi akun apa pun. Footer panel membaca \u201cBerjalan di server Wix \u00b7 build "
    "20261024-190551\u00b7 pengaturan rev 0\u201d."))
story.extend(img("menu_utama.jpg",
    "Menu utama mode demo; tombol Admin tampak di kanan atas tanpa syarat apa pun."))
story.extend(img("admin_ringkasan.jpg",
    "Tab Ringkasan panel admin: statistik pemain, form Pengumuman siap kirim ke semua "
    "pemain, dan tombol \u201cRefresh semua pemain\u201d."))
h2(story, "5.2 Kemampuan yang Terekspos")
story.append(P(
    "Panel admin ini bukan sekadar tampilan mati. Tab Ringkasan menyediakan formulir "
    "<b>Pengumuman</b> yang menurut keterangannya \u201ctampil di menu semua pemain\u201d lengkap "
    "dengan tombol SIMPAN PENGUMUMAN, serta tombol <b>REFRESH SEMUA PEMAIN</b> yang memaksa "
    "seluruh klien yang sedang aktif memuat ulang halaman. Tab Pengaturan memaparkan seluruh "
    "parameter ekonomi game yang dapat disunting dan disimpan: hadiah harian, XP per hasil "
    "pertandingan, Elo awal, saldo awal pemain baru, hingga gacha. Tab Pemain menyediakan "
    "pencarian nickname/kode teman/ID beserta daftar pemain dengan rating Elo dan saldo."))
story.extend(img("admin_pemain.jpg",
    "Tab Pemain: nickname, Elo, dan saldo bakwan pemain tampil tanpa redaksi."))
story.extend(img("admin_pengaturan.jpg",
    "Tab Pengaturan: seluruh parameter ekonomi game dapat disunting dan disimpan "
    "tanpa autentikasi."))
story.append(P(
    "<b>Status ronde kedua (25 Okt).</b> Panel admin demo <b>masih dapat dibuka tanpa "
    "autentikasi</b> pada build terbaru \u2014 termasuk editor Pengumuman, tombol REFRESH SEMUA "
    "PEMAIN, daftar pemain, LOG, dan seluruh parameter ekonomi di tab Pengaturan (hadiah harian, "
    "XP per match, Elo/saldo awal, ambang hit latihan). Nilai-nilai pada tab tersebut pula yang "
    "menjadi kunci analisis BUG-09: panel menampilkan \u201cMin. hit latihan agar dihitung: 10\u201d "
    "sementara server produksi berperilaku berbeda. Dalam pengujian ulang ini tidak ada satu pun "
    "tombol simpan yang ditekan."))
story.extend(img("r2_bug03_admin.jpg",
    "Verifikasi ulang ronde kedua: panel admin demo tetap terbuka penuh \u2014 Ringkasan, Pengumuman, "
    "dan Paksa refresh tanpa auth.", max_h=190))
story.extend(img("r2_bug03_setting.jpg",
    "Verifikasi ulang: tab Pengaturan memaparkan seluruh angka balance (termasuk \u201cMin. hit "
    "latihan: 10\u201d yang menjadi konteks BUG-09).", max_h=190))
h2(story, "5.3 Bukti Kode Sumber (White-Box)")
story.append(P(
    "Analisis berkas HTML game mengonfirmasi akar masalahnya: pada inisialisasi mode demo, "
    "objek konteks pengguna dibuat dengan flag admin bernilai true secara permanen:"))
story.append(Paragraph(
    "var ctx = { memberId: 'demo-you', name: 'Kamu',<br/>"
    "  email: 'demo@admin', <b>isAdmin: true</b> };", S["code"]))
story.append(P(
    "Flag inilah yang membuat tombol admin tampil (pemilihan tombol dikontrol oleh "
    "$$('.adminbtn').forEach(b => b.hidden = !G.isAdmin)). Pada mode produksi, nilai isAdmin "
    "diambil dari respons server (r.isAdmin) dan seluruh fungsi admin dijaga fungsi "
    "<b>needAdmin(ctx)</b> yang melempar kesalahan NOT_ADMIN bila konteks bukan admin \u2014 "
    "artinya validasi sisi server untuk data produksi tampaknya ada. Meski demikian, ditemukan "
    "pula bahwa basis data demo di-seed dengan 8 akun tiruan:"))
story.append(Paragraph(
    "var fake = [['Asep_Gaming', 2140, 'presiden'], ['TehNurul', 1730, 'haze'],<br/>"
    "  ['Kevin_GG', 1320, 'kazera'], ['DindaXD', 980, 'veradinita'],<br/>"
    "  ['Bayu007', 640, 'dai'], ['Rara.exe', 410, 'shinon'],<br/>"
    "  ['UcupPro', 230, 'mefelz'], ['MasJajang', 150, 'botak']];", S["code"]))
story.append(P(
    "Data tiruan inilah yang tampil di panel admin, leaderboard, dan matchmaking demo. Ini "
    "penting untuk penilaian dampak: data yang terekspos pada BUG-04 adalah data uji, bukan data "
    "pemain produksi. Namun karena tampilannya identik dengan pemain nyata (lengkap dengan tag "
    "\u201cMURID TELADAN\u201d, \u201cPEMAIN BFB\u201d, jumlah menang/kalah), penguji maupun "
    "pemain baru tidak dapat membedakannya \u2014 hal ini sendiri merupakan masalah UX dan "
    "integritas data beta."))
story.append(P(
    "<b>Dampak ringkas.</b> Pada mode demo: siapa pun dapat (a) menyiarkan pengumuman apa pun "
    "termasuk tautan phishing ke \u201csemua pemain\u201d lokal, (b) memaksa refresh massal, (c) "
    "mengubah seluruh parameter ekonomi, (d) melihat data pemain tanpa redaksi. Pada produksi: "
    "belum ada bukti eksploitasi karena validasi server hadir; namun permukaan UI admin yang "
    "terbuka untuk anonim tetap harus ditutup, dan prinsip \u201cdeny by default\u201d perlu "
    "diterapkan pada mode demo."))

# ================================================================ 6. TEMUAN TAMBAHAN
h1(story, "6. Temuan Tambahan (BUG-04 s.d. BUG-07)")
h2(story, "6.1 BUG-04: Data Pemain Tanpa Redaksi")
story.append(P(
    "Panel admin dan leaderboard menampilkan data pemain secara penuh: nickname, Elo, saldo "
    "bakwan, kode teman, serta statistik menang/kalah. Tidak ada mekanisme redaksi atau masking "
    "(misalnya Asep****). Pada mode demo data ini berupa seed lokal, tetapi pola tampilan yang "
    "sama diharapkan berlaku bagi admin produksi; tanpa pembatasan peran bertingkat, setiap "
    "pemegang akses admin melihat data mentah seluruh komunitas. Sebagai catatan risiko lanjutan: "
    "kode teman bersifat pengenal yang dapat dipakai mengirim permintaan duel, sehingga "
    "penampakannya di panel yang sama sebaiknya dibatasi konteksnya."))
h2(story, "6.2 BUG-05: Simulasi Pembayaran Sekali Klik")
story.append(P(
    "Store menyediakan tiga paket top-up (100 bakwan = Rp 15.000; 550 = Rp 75.000; 1.200 = "
    "Rp 150.000) yang dalam mode demo tidak membuka halaman Xendit, melainkan menampilkan dialog "
    "\u201cMODE DEMO - Simulasikan pembayaran sukses?\u201d dengan tombol <b>BAYAR (DEMO)</b>. "
    "Satu klik langsung menambahkan 100 bakwan ke saldo (terverifikasi 1 menjadi 101). Pada kode, "
    "jalur ini dipetakan ke fungsi creditPurchase tanpa validasi pembayaran nyata. Meskipun "
    "berlaku lokal, dialog ini berbahaya jika suatu saat digabung dengan backend uji: cukup satu "
    "paramater mode yang keliru untuk mengkreditkan saldo tanpa uang. Disarankan mode demo "
    "menggunakan mata uang terpisah (mis. demo-bakwan) dan banner tegas."))
story.extend(img("topup_demo.jpg",
    "Dialog simulasi pembayaran demo; satu klik langsung mengkreditkan saldo."))
story.append(P(
    "<b>Tindak lanjut pengembang.</b> Pada ronde kedua, pita pengumuman resmi di halaman game "
    "mengonfirmasi temuan ini secara publik: top-up \u201cpalsu\u201d pada rentang 18:00\u201320:45 telah "
    "di-rollback \u201ckarena tadi sistem top up masih pakai test system\u201d. Alur produksi sekarang "
    "sudah memanggil createTopup dan membuka invoice Xendit sungguhan (bukan simulasi), meski "
    "checkout-nya kini gagal permanen \u2014 lihat BUG-10 pada Bab 10."))
h2(story, "6.3 BUG-06: Statistik Karakter Desimal")
story.append(P(
    "Setelah Botak dinaikkan ke Level 2 dengan Botol XP, panel karakter menampilkan ATK 39.1 dan "
    "DEF 18.5. Nilai pecahan seperti ini pada RPG kasual mengurangi keterbacaan dan terkesan "
    "belum selesai; disarankan pembulatan ke bilangan bulat pada lapisan presentasi, atau satu "
    "angka desimal dengan aturan konsisten."))
story.extend(img("karakter.jpg",
    "Panel karakter: ATK 39.1 dan DEF 18.5 tampil desimal setelah naik level."))
h2(story, "6.4 BUG-07: Inkonsistensi HP Sasaran Latihan")
story.append(P(
    "Layar latihan menampilkan \u201cSasaran \u00b7 5000/5000\u201d, sementara konfigurasi pada "
    "berkas game yang diuji mendefinisikan HP karung latihan 3000. Selisih ini bisa berasal dari "
    "versi build yang berbeda antara berkas statis dan konfigurasi server, atau penskalaan level "
    "yang tidak terdokumentasi. Dampaknya kecil, tetapi membingungkan penguji dan pemain yang "
    "membaca kode; disarankan disinkronkan atau didokumentasikan."))

# ================================================================ 7. AUDIT AKUN RESMI: LOGIN & PROFIL (BUG-08)
h1(story, "7. Audit Akun Resmi: Login, Profil, dan BUG-08")
h2(story, "7.1 Login dengan Akun yang Disediakan")
story.append(P(
    "Ronde kedua dimulai dengan login menggunakan akun resmi vameb61409@hiringview.com melalui "
    "tombol \u201cLog In\u201d \u2192 \u201cLog in with Email\u201d pada situs. Tidak ada captcha yang diminta \u2014 "
    "berkebalikan total dengan alur pendaftaran pada ronde pertama yang selalu berakhir gagal "
    "(BUG-01). Permintaan login tertangkap pada jaringan sebagai panggilan ke "
    "<b>_api/iam/authentication/v2/login</b> milik Wix, disusul pembuatan sesi melalui "
    "<b>createSessionCookie</b> dan penerbitan <b>access-tokens</b>; seluruhnya sukses dalam satu "
    "percobaan. Setelah login, halaman game memuat aplikasi dengan status akun lengkap: nama "
    "vameb61409, badge rank \u201cMurid Baru\u201d, Elo 100, saldo 105 bakwan, ikon hadiah dengan "
    "badge 2 misi tersisa, serta pita pengumuman dari pengembang."))
story.append(P(
    "Pita pengumuman tersebut bernilai bukti penting: <b>\u201cServer sudah diperbaharui! Bakwan "
    "diskon 33% sampai akhir bulan ini \u2026 Buat yg 'top up' palsu dari jam 18:00 - 20:45, "
    "Rollback telah dilakukan karena tadi sistem top up masih pakai test system.\u201d</b> Pengembang "
    "mengakui secara publik bahwa sistem top-up sempat berjalan dalam mode uji dan pemain yang "
    "melakukan pembayaran pada rentang tersebut telah di-rollback. Temuan ini menegaskan laporan "
    "ronde pertama (BUG-05) dan menjadi konteks langsung bagi BUG-10 pada Bab 10: integrasi "
    "pembayaran memang sedang bermasalah, dan kini kondisi terbarunya dapat diuji langsung."))
story.extend(img("r2_home_login.jpg",
    "Berhasil login dengan akun resmi: vameb61409 (Murid Baru), Elo 100, saldo 105 bakwan, "
    "badge 2 misi harian, dan pita pengumuman rollback top-up dari pengembang.", max_h=200))
story.extend(img("r2_menu_utama.jpg",
    "Menu utama game produksi dengan akun resmi: karakter Botak Lv 1 \u00b7 Starter, tombol Ranked, "
    "Train, Store, Leaderboard, dan Teman.", max_h=200))
h2(story, "7.2 Profil Pemain dan Data Ladder Nyata")
story.append(P(
    "Tombol \u201cRiwayat\u201d membuka halaman Profil yang kini menampilkan data ladder produksi: "
    "Elo beserta puncaknya, nomor peringkat global, rekor menang/kalah/seri, winrate, karakter "
    "aktif beserta levelnya, <b>kode teman pribadi 9VQ9F7</b>, dan riwayat 20 pertandingan "
    "terakhir. Sebelum pertandingan pertama, akun menampilkan Elo 100 (puncak 100), peringkat "
    "<b>#1471</b>, rekor 0/0/0, dan winrate 0% dengan status \u201cBelum ada pertandingan\u201d. Nomor "
    "peringkat ini mengonfirmasi bahwa basis data pemain produksi berisi ribuan akun \u2014 indikasi "
    "adopsi beta yang luas."))
story.extend(img("r2_profil_awal.jpg",
    "Profil akun sebelum bertanding: Elo 100 (puncak 100), peringkat #1471, 0/0/0, winrate 0%, "
    "kode teman 9VQ9F7, riwayat kosong.", max_h=200))
h2(story, "7.3 BUG-08: Pengaturan Akun Diblokir Paywall (Sedang)")
story.append(P(
    "Dari menu akun Wix di pojok kanan atas, opsi <b>\u201cPengaturan Akun\u201d</b> tidak membuka halaman "
    "pengaturan, melainkan dialihkan ke paywall Wix dengan pesan <b>\u201cYou don't have permissions "
    "to access this page.\u201d</b> beserta tombol \u201cBack to site\u201d dan \u201cSwitch Account\u201d. URL yang "
    "dihasilkan adalah <b>/paywall?appSectionParams={\\\"restrictedPageId\\\":\\\"v6bn6\\\","
    "\\\"restrictedPagePath\\\":\\\"/account-settings\\\"}</b> \u2014 pola khas halaman Wix Members yang "
    "salah konfigurasi perizinannya (halaman account-settings diset terbatas untuk peran tertentu, "
    "padahal seharusnya terbuka untuk semua member yang sudah login)."))
story.append(P(
    "Dampak praktisnya: member biasa <b>tidak dapat mengakses pengaturan akunnya sendiri</b> \u2014 "
    "misalnya mengubah data profil, mengelola notifikasi, atau mencari opsi penghapusan akun. "
    "Untuk program beta yang menjanjikan \u201cakun dapat dihapus\u201d, hilangnya akses ke halaman "
    "pengaturan berarti jalur penghapusan mandiri ikut tertutup dan pemain harus menghubungi "
    "pengembang secara manual. Temuan ini mudah diperbaiki dari editor Wix (Members Area \u2192 "
    "Settings \u2192 ubah izin halaman /account-settings menjadi \u201cAll members\u201d) tanpa perubahan "
    "kode apa pun."))
story.extend(img("r2_bug08_denied.jpg",
    "BUG-08: klik \u201cPengaturan Akun\u201d mengarah ke paywall \u201cYou don't have permissions to access "
    "this page.\u201d untuk member yang sedang login.", max_h=190))

# ================================================================ 8. RANKED VS PEMAIN ASLI & ELO
h1(story, "8. Ranked vs Pemain Asli: Verifikasi Sistem Elo")
h2(story, "8.1 Dua Pertandingan Nyata Malam yang Sama")
story.append(P(
    "Menekan tombol <b>RANKED</b> langsung memasangkan akun uji dengan pemain asli (bukan bot) "
    "dalam hitungan detik. Pertandingan pertama adalah melawan <b>Tyyie</b> (badge \u201cMurid "
    "Normal\u201d, karakter Alana), berlangsung di peta kelas dengan papan tulis \u201cBAKWAN FIGHT! "
    "1+1=2 PR hal. 45\u201d. Pertandingan kedua melawan <b>Lia__multifandom</b> di peta halaman "
    "sekolah. Kedua lawan terbukti manusia: nama mereka tidak ada dalam daftar 20 nama bot "
    "internal, profil mereka dapat dibuka, dan riwayat pertandingan mereka mencatat duel-duel "
    "lain pada menit yang sama (04.37\u201304.40 WIB) \u2014 termasuk Tyyie menang +12, +18, +15 melawan "
    "tiga pemain berbeda hanya dalam rentang dua menit."))
story.extend(img("r2_ranked_vs_tyyie.jpg",
    "Matchmaking nyata: VAMEB61409 (Murid Baru) vs Tyyie (Murid Normal) di peta kelas.", max_h=200))
story.extend(img("r2_battle_start.jpg",
    "Awal pertarungan: lingkaran bernomor menyusut, banner skill lawan \u201cLAWAN: LEMPAR "
    "PENGHAPUS\u201d, dan indikator MISS pada sisi pemain.", max_h=200))
story.extend(img("r2_battle_skill.jpg",
    "Pertarungan berlangsung: skill shape dan indikator damage tampil bersamaan dengan catatan "
    "baru yang muncul.", max_h=200))
h2(story, "8.2 Hasil dan Verifikasi Matematika Elo")
story.append(P(
    "Kedua pertandingan berakhir KALAH K.O. untuk akun uji (masih Murid Baru, karakter starter "
    "Lv 1 tanpa skill aktif). Hasil pertama: <b>Elo 100 \u2192 86 (\u221214)</b>, +25 XP Botak, plus "
    "bonus \u201cranked pertama hari ini\u201d <b>+15 bakwan</b>. Hasil kedua: <b>Elo 86 \u2192 73 (\u221213)</b>, "
    "+25 XP, dan statistik <b>\u201cBom 1\u201d</b> \u2014 bukti langsung bahwa lingkaran bom palsu ikut "
    "terekam ketika penguji menyentuhnya. Dengan formula standar \u0394Elo = K\u00b7(score \u2212 E) dan "
    "K=40 untuk lawan nyata, \u221214 mengimplikasikan Elo Tyyie \u2248 208 dan \u221213 mengimplikasikan "
    "Elo Lia \u2248 213 pada momen match \u2014 konsisten dengan badge \u201cMurid Normal\u201d (rentang Elo "
    "201\u2013500) dan dengan profil Tyyie yang terbaca 236 Elo setelah rangkaian kemenangannya. "
    "Sistem Elo produksi dengan demikian <b>terverifikasi bekerja sesuai desain</b>."))
story.append(P(
    "Perubahan peringkat juga tercatat: dari #1471 (belum bertanding) menjadi <b>#4187</b> "
    "setelah dua kekalahan \u2014 menandakan lebih dari 4.000 pemain memiliki Elo di atas 73. "
    "Riwayat pertandingan mencatat detail lengkap per baris: hasil, mode RANKED, lawan beserta "
    "badge-nya, statistik Perfect/Combo/Bom, karakter dan level, XP yang diterima, delta Elo "
    "berwarna, serta waktu WIB dua baris desimal. Baris riwayat dapat diklik untuk membuka "
    "profil lawan \u2014 fitur yang bekerja baik dan menghasilkan data lintas-akun yang kaya."))
story.extend(img("r2_match2_miss.jpg",
    "Pertandingan kedua vs Lia__multifandom: indikator MISS di sisi pemain, catatan bernomor "
    "muncul di kanvas halaman sekolah.", max_h=190))
story.extend(img("r2_match2_bom.jpg",
    "Hasil match kedua: KALAH K.O., Elo 86 \u2192 73 (\u221213), +25 XP, dan \u201cBom 1\u201d tercatat \u2014 "
    "bukti mekanik bom palsu aktif di ranked produksi.", max_h=200))
story.extend(img("r2_riwayat_rows.jpg",
    "Riwayat pertandingan produksi: dua kekalahan ranked dengan delta Elo \u221213/\u221214, "
    "timestamp WIB, dan detail Perfect/Combo/Bom per baris.", max_h=200))
h2(story, "8.3 Profil Lawan: Data Ladder Aktif")
story.append(P(
    "Membuka profil Tyyie dari baris riwayat menampilkan potret ladder yang sehat: Elo 236 "
    "(puncak 268), peringkat <b>#442</b>, rekor <b>51 menang / 45 kalah / 0 seri</b>, winrate 53%, "
    "karakter Alana yang <b>naik dari Lv 16 ke Lv 17</b> di antara dua pertandingan, kode teman "
    "T9Q8ZH, tombol \u201c+ Tambah Teman\u201d, dan indikator online/offline. XP +60 per kemenangan dan "
    "+25 per kekalahan pada riwayat lawan sama persis dengan konfigurasi internal (xpWin=60, "
    "xpLose=25) \u2014 konsistensi lintas-akun ini menandakan server produksi dan klien memakai "
    "aturan yang sama."))
story.extend(img("r2_profil_tyyie.jpg",
    "Profil pemain asli Tyyie: Elo 236 (puncak 268), #442, 51/45/0, winrate 53%, Alana Lv 17, "
    "kode teman T9Q8ZH.", max_h=200))

# ================================================================ 9. MISI HARIAN & LATIHAN (BUG-09)
h1(story, "9. Misi Harian, Latihan, dan BUG-09")
h2(story, "9.1 Sistem Hadiah Harian Produksi")
story.append(P(
    "Ikon hadiah pada bilah atas membuka panel <b>\u201cHadiah Harian\u201d</b> berisi tiga misi: "
    "<b>Login harian +5</b>, <b>Main 1x Ranked +15</b>, dan <b>Selesaikan 1x Latihan +10</b>, "
    "dengan catatan reset \u201cdalam 12 jam 4 menit (00:00 WIB)\u201d. Jumlah hadiah produksi (5/15/10) "
    "berbeda dari nilai konfigurasi statis pada kode sumber (1/2/2) \u2014 konfigurasi server memang "
    "dapat dioverride lewat CMS tanpa publish ulang, dan panitia jelas sudah menaikkan nilai-nilai "
    "tersebut. Misi login tercentang otomatis saat login; misi ranked tercentang tepat setelah "
    "pertandingan ranked pertama dengan +15 bakwan masuk ke saldo (terverifikasi: 5 \u2192 20)."))
story.extend(img("r2_hadiah_harian.jpg",
    "Panel Hadiah Harian produksi: Login harian +5, Main 1x Ranked +15, Selesaikan 1x Latihan "
    "+10; badge angka menunjukkan sisa misi.", max_h=200))
story.extend(img("r2_bug09_misi.jpg",
    "Setelah ranked: misi \u201cMain 1x Ranked\u201d tercentang dan +15 bakwan masuk; misi latihan "
    "masih kosong menunggu 10 hit.", max_h=200))
h2(story, "9.2 Latihan: Sesi dengan 11 Hit Tidak Terkredit (BUG-09, Mayor)")
story.append(P(
    "Misi \u201cSelesaikan 1x Latihan\u201d mensyaratkan mengenai minimal 10 lingkaran dalam satu "
    "sesi (teks UI: \u201cKena minimal 10 lingkaran untuk dapat XP\u201d). Karena timing manual sulit "
    "bagi otomasi, penguji membangun penjejak piksel yang mendeteksi lingkaran oranye dan cincin "
    "penyusutnya lalu memprediksi momen sempurna dari laju penyusutan. Setelah lima sesi, sesi "
    "kelima berhasil mencatat <b>Hit/Miss 11/65</b> dengan Total damage 224, Perfect 2 (3%), dan "
    "combo maksimum 1 \u2014 <b>melampaui syarat 10 hit yang tertulis di layar</b>."))
story.append(P(
    "Namun, layar hasil hanya menampilkan baris \u201cKena minimal 10 lingkaran untuk dapat XP\u201d "
    "\u2014 tanpa \u201cXP latihan +10\u201d dan tanpa \u201cBonus latihan pertama hari ini\u201d. Verifikasi lanjutan "
    "memperkuat temuan: <b>XP karakter Agatha tetap 0/100</b>, saldo bakwan tetap 20, badge misi "
    "tetap \u201c1\u201d, dan panel Hadiah Harian tetap tidak mencoret misi latihan <b>bahkan setelah "
    "reload halaman penuh</b>. Analisis kode sumber menunjukkan fungsi server <b>trainDone()</b> "
    "menolak reward bila <b>summary.hits</b> yang diterima di bawah <b>CONFIG.daily.trainMinHits</b>, "
    "sementara panel admin demo menampilkan nilai bawaan 10 \u2014 padahal teks syarat pada UI klien "
    "adalah teks statis yang di-hardcode. Pola ini paling konsisten dengan <b>desinkronisasi "
    "konfigurasi</b>: server produksi memakai ambang yang lebih tinggi dari 10 (atau menghitung "
    "hit dengan cara berbeda), sementara seluruh UI \u2014 layar hasil, panel admin, dan pesan "
    "syarat \u2014 tetap mengklaim 10. Ditambah lagi, pemanggil API pada klien dibungkus "
    "<b>catch(e){}</b> tanpa toast maupun retry, sehingga kegagalan jaringan saat mengirim hasil "
    "latihan hilang diam-diam tanpa jejak bagi pemain."))
story.append(P(
    "Dampak: pemain yang benar-benar menyelesaikan syarat <b>kehilangan +10 XP dan +10 bakwan "
    "tanpa penjelasan</b>, misi harian tak bisa diselesaikan (menghalangi koleksi hadiah harian), "
    "dan tim dukungan akan dibanjiri laporan \u201csudah 10 hit tapi tidak dapat reward\u201d yang sulit "
    "dideteksi karena tidak ada log kegagalan di sisi klien. Rekomendasi: samakan sumber nilai "
    "syarat antara server dan UI (ambil dari CONFIG server, jangan hardcode), kirim ambang "
    "efektif ke klien sebagai bagian dari publicConfig, dan ganti catch(e){} dengan penanganan "
    "yang menampilkan pesan serta mencatat log."))
story.extend(img("r2_bug09_11hit.jpg",
    "BUG-09: layar hasil latihan menampilkan Hit/Miss 11/65 (di atas syarat 10) namun tanpa "
    "baris reward XP maupun bonus harian.", max_h=200))
story.extend(img("r2_karakter_agatha.jpg",
    "Bukti lanjutan BUG-09: XP karakter Agatha tetap 0/100 setelah sesi 11 hit \u2014 reward tidak "
    "pernah masuk ke database.", max_h=190))
h2(story, "9.3 Catatan Anti-Makro yang Sehat (Bukan Bug)")
story.append(P(
    "Sebagai catatan positif: pada sesi-sesi dengan klik acak cepat (26\u201340 klik dalam sekitar "
    "30 detik), hampir semua klik dihitung miss (misalnya 2/59) \u2014 jendela timing \u00b1230 ms dan "
    "posisi lingkaran yang acak membuat spam klik tidak produktif. Bot prediksi piksel pun hanya "
    "mencetak 2 perfect dari 11 hit. Dengan demikian sistem latihan terbukti <b>cukup tahan "
    "terhadap makro sederhana</b>; temuan BUG-09 bukan soal anti-cheat, melainkan soal reward "
    "yang tidak jatuh meski syarat terpenuhi."))

# ================================================================ 10. STORE, GACHA, TOP-UP (BUG-10)
h1(story, "10. Store, Gacha, dan BUG-10 Top-Up Xendit")
h2(story, "10.1 Store Produksi: Gacha dan Botol XP")
story.append(P(
    "Store produksi terdiri dari tiga tab: <b>Gacha</b>, <b>XP Bottle</b>, dan <b>Top-up "
    "Bakwan</b>. Gacha menampilkan tarif terbuka \u2014 Common 60%, Rare 30%, Legendary 10% \u2014 dengan "
    "harga 100 bakwan untuk satu tarik dan 900 untuk sepuluh, serta aturan duplikat \u201c+200 XP "
    "untuk karakter itu\u201d. Satu tarikan uji (saldo 105 \u2192 5) menghasilkan karakter <b>Agatha \u2014 "
    "BARU! \u00b7 Common</b> (SMA Pelitaraya, skill Lempar Penghapus + Semangat 45, stat 1000 HP / "
    "40 ATK / 20 DEF) dengan animasi reveal ber-frame dan label \u201cBARU!\u201d. Botol XP dijual 50 "
    "bakwan (+100 XP) dan 250 bakwan (+600 XP) dengan pencocokan harga terhadap konfigurasi "
    "internal yang tepat. Panel <b>Ganti Karakter</b> menampilkan seluruh 25 karakter (1 starter, "
    "10 Common, 7 Rare, 7 Legendary) dengan karakter yang belum dimiliki disembunyikan abu-abu; "
    "karakter baru langsung dapat dipakai dan detail skill beserta level bukanya (slot kotak "
    "terbuka Lv 10, slot segitiga Lv 20) terbaca jelas."))
story.extend(img("r2_gacha_store.jpg",
    "Store produksi tab Gacha dengan tiga karakter unggulan Legendary dan tab Top-up Bakwan.", max_h=190))
story.extend(img("r2_gacha_rates.jpg",
    "Tarif gacha terbuka: Common 60%, Rare 30%, Legendary 10%; duplikat menjadi +200 XP.", max_h=190))
story.extend(img("r2_gacha_agatha.jpg",
    "Hasil tarikan uji: karakter baru \u201cAgatha \u2014 BARU! \u00b7 Common\u201d; saldo berkurang 100 bakwan.", max_h=170))
story.extend(img("r2_xp_bottle.jpg",
    "Tab XP Bottle: Botol XP Kecil (+100 XP, 50 bakwan) dan Botol XP Besar (+600 XP, 250 bakwan).", max_h=190))
story.extend(img("r2_karakter_botak.jpg",
    "Panel Ganti Karakter: detail Botak Lv 1 (1000 HP / 38 ATK / 18 DEF), skill beserta level "
    "bukanya, dan grid 25 karakter dengan status kepemilikan.", max_h=200))
h2(story, "10.2 Harga Top-Up Berdiskon 33%")
story.append(P(
    "Tab Top-up Bakwan menjual tiga paket \u2014 <b>Sepiring Bakwan 100</b> (Rp 5.000), <b>Sebakul "
    "Bakwan 550</b> (Rp 25.000), dan <b>Segerobak Bakwan 1.200</b> (Rp 50.000) \u2014 semuanya berlabel "
    "\u201cDiskon 33%\u201d sesuai pengumuman pengembang, dengan catatan kaki \u201cPembayaran aman via Xendit "
    "(QRIS, e-wallet, virtual account, kartu)\u201d. Berbeda dengan demo ronde pertama yang memakai "
    "tombol \u201cBAYAR (DEMO)\u201d sekali klik (BUG-05), alur produksi kini memanggil <b>createTopup</b> "
    "ke server lalu membuka URL checkout Xendit nyata \u2014 perkembangan yang benar arah, meski "
    "kini menabrak temuan berikut."))
story.extend(img("r2_topup_store.jpg",
    "Halaman Store dibuka dari tombol saldo \u201cbakwan 105 +\u201d dengan tab Top-up Bakwan aktif.", max_h=170))
story.extend(img("r2_topup_harga.jpg",
    "Paket Sebakul (550 \u2014 Rp 25.000) dan Segerobak (1.200 \u2014 Rp 50.000) berlabel Diskon 33%, "
    "dengan catatan pembayaran Xendit.", max_h=170))
story.extend(img("r2_topup_paket1.jpg",
    "Seluruh katalog top-up: Sepiring 100 \u2014 Rp 5.000, Sebakul 550 \u2014 Rp 25.000, Segerobak "
    "1.200 \u2014 Rp 50.000.", max_h=170))
h2(story, "10.3 BUG-10: Halaman Checkout Xendit Error Permanen (Kritis)")
story.append(P(
    "Menekan paket Rp 5.000 membuat server membuat invoice lalu peramban dialihkan ke "
    "<b>checkout.xendit.co/web/6add8704bfd8f0d68bd901a0</b> \u2014 namun halaman itu <b>gagal "
    "merender</b> dan hanya menampilkan ilustrasi CS dengan pesan <b>\u201cSorry, this wasn't supposed "
    "to happen \u2014 Our engineers have been notified. Please wait a few minutes, refresh and try "
    "again.\u201d</b>. Konsol peramban merekam <b>AxiosError: Network Error (ERR_NETWORK)</b> berulang "
    "dari aset Xendit. Penundaan 15 detik disertai muat ulang penuh <b>tidak mengubah apa pun</b> "
    "\u2014 error bersifat permanen pada invoice tersebut. Saldo akun tidak bertambah dan tidak ada "
    "invoice lain yang dibayar selama pengujian."))
story.append(P(
    "Kombinasi bukti \u2014 (a) harga yang sudah diiklankan berdiskon 33%, (b) pengumuman rollback "
    "top-up palsu karena \u201cmasih pakai test system\u201d, (c) checkout live yang error permanen \u2014 "
    "menunjukkan integrasi pembayaran <b>belum siap menerima uang nyata</b>: setiap pemain yang "
    "mencoba top-up hari ini akan melihat error dan uang tidak tertagih. Keparahan: ini adalah "
    "pintu pendapatan satu-satunya game dan gagal 100% pada langkah terakhir; berpotensi pula "
    "menimbulkan keluhan \u201csudah bayar tapi saldo tidak masuk\u201d apabila sebagian kanal pembayaran "
    " ternyata hidup sementara webhook-nya belum benar. Rekomendasi: uji end-to-end satu paket "
    "dengan pembayaran sungguhan bernilai kecil, verifikasi callback/webhook signature Xendit "
    "di sisi server, tampilkan halaman \u201cpembayaran sedang pemeliharaan\u201d alih-alih membiarkan "
    "invoice error terbentuk, dan pantau invoice gagal di dashboard Xendit."))
story.extend(img("r2_bug10_xendit.jpg",
    "BUG-10: checkout Xendit untuk invoice 6add8704\u2026 gagal dengan \u201cSorry, this wasn't supposed "
    "to happen\u201d \u2014 error tetap muncul setelah muat ulang.", max_h=200))


# ================================================================ 11. MEKANISME GAME
h1(story, "11. Mekanisme dan Cara Bermain")
h2(story, "11.1 Konsep Dasar")
story.append(P(
    "\u201cBakwan Fight Back\u201d adalah game duel ritme-timing berlatar komunitas Minecraft "
    "Bakwan. Dua karakter saling berhadapan; pemain menerima serangkaian <b>lingkaran bernomor</b> "
    "yang menyusut menuju cincin target. Klik/ketuk lingkaran tepat ketika lingkaran dalam "
    "sejajar dengan cincin untuk mendaratkan pukulan. Semakin presisi timing-nya, semakin besar "
    "kerusakan. Kegagalan (miss) membuat lawan \u2014 karung latihan, bot, atau pemain lain \u2014 "
    "memukul balik. Ronde berakhir saat salah satu pihak K.O. atau waktu habis (90 detik untuk "
    "ranked, 60 detik untuk latihan)."))
story.extend(img("latihan_countdown.jpg",
    "Awal ronde latihan: hitung mundur 3-2-1-FIGHT, HP pemain 1000, sasaran penuh."))
story.extend(img("latihan_gameplay.jpg",
    "Gameplay inti: lingkaran bernomor menyusut menuju cincin; MISS muncul bila telat."))
h2(story, "11.2 Sistem Timing dan Kerusakan")
story.append(P(
    "Konfigurasi pada kode menetapkan jendela timing dalam milidetik dari waktu sempurna: "
    "<b>perfect \u00b170 ms</b>, <b>great \u00b1140 ms</b>, <b>good \u00b1230 ms</b>; klik lebih "
    "awal dari 450 ms dihitung miss langsung. Pengali kerusakan: perfect 1.0, great 0.75, good "
    "0.5, ok 0.25. Setiap combo menambah +2% kerusakan hingga maksimum +30% (15 combo). Selain "
    "lingkaran biasa, terdapat lingkaran <b>bom</b> (tanda seru) yang tidak boleh diklik: "
    "mengekliknya memicu BOOM dan kerusakan ke diri sendiri."))
story.extend(img("latihan_boom.jpg",
    "Kehilangan timing memicu serangan balik karung (BOOM!, -60 HP)."))
h2(story, "11.3 Mode Latihan")
story.append(P(
    "Mode Latihan (\u201cTrain - Latihan timing\u201d) berhadapan dengan Karung Latihan yang tidak "
    "menyerang kecuali saat pemain miss. Hasil ronde menampilkan total damage, jumlah Perfect, "
    "rasio Hit/Miss, dan combo maksimum. Untuk mendapat XP, pemain harus mengenai minimal 10 "
    "lingkaran dalam satu ronde (\u201cKena minimal 10 lingkaran untuk dapat XP\u201d). Ronde "
    "latihan berdurasi 60 detik dan dapat diulang tanpa biaya."))
story.extend(img("latihan_hasil.jpg",
    "Layar hasil latihan: 0/18 hit pada sesi uji tanpa klik; syarat 10 hit untuk XP."))
h2(story, "11.4 Mode Ranked, Elo, dan Bot")
story.append(P(
    "Mode Ranked mencari lawan online dengan rentang Elo yang melebar seiring waktu (awal "
    "\u00b1150, tumbuh +25/detik hingga \u00b12500). Bila tidak ada lawan dalam 20 detik, bot "
    "dipasangkan (pada demo: 5 detik). Pertandingan memakai seed bersama sehingga kedua klien "
    "menghasilkan pola lingkaran yang sama; hit dikirim pemain-ke-pemain melalui relay realtime "
    "(Ably) dan divalidasi ulang server Wix. Hasil menang/kalah mengubah Elo dengan K-factor 40 "
    "untuk lawan nyata dan 30 untuk bot. Dalam pengujian, kekalahan K.O. dari bot \u201cBayu007\u201d "
    "menurunkan Elo 100 menjadi 87 (-13) serta memberi bonus ranked pertama +2 bakwan dan +25 XP "
    "karakter."))
story.extend(img("ranked_match.jpg",
    "Ranked vs bot Bayu007 (Adela Lv 7): catatan pemain di kiri, catatan bot di kanan."))
story.extend(img("ranked_bomb.jpg",
    "Lingkaran bom (tanda seru) muncul di sisi lawan; menyentuhnya berarti kerusakan diri."))
story.extend(img("ranked_kalah.jpg",
    "Hasil KALAH: K.O. vs Bayu007, Elo turun 13 poin, bonus harian dan XP tetap diberikan."))
h2(story, "11.5 Karakter, Skill, dan Progres")
story.append(P(
    "Tersedia 25 karakter dalam tiga tingkat kelangkaan (Common/Rare/Legendary), masing-masing "
    "dengan HP, ATK, DEF, dan dua skill aktif. Skill diaktifkan dengan mengetuk kotak/segitiga "
    "yang muncul saat bertarung; contohnya \u201cBakwan Smash\u201d (ATK x3) dan \u201cIstirahat "
    "Kantin\u201d (pulih 12% HP). Level maksimum 50; batas XP naik per level (contoh: 100 untuk "
    "Lv 1 menuju Lv 2, 120 untuk Lv 2 menuju Lv 3). XP diperoleh dari menang/seri/kalah ranked, "
    "latihan, duel teman, dan duplikat gacha (+200 XP)."))
story.extend(img("menu_utama2.jpg" if os.path.exists(os.path.join(ASSETS, "menu_utama2.jpg")) else "profil.jpg",
    "Profil pemain: rank, Elo, winrate, kode teman, dan riwayat pertandingan."))
story.extend(img("leaderboard.jpg",
    "Leaderboard Top 50 (mode demo memuat 8 pemain seed + sesi uji)."))

# ================================================================ 12. EKONOMI
h1(story, "12. Ekonomi Game, Leaderboard, dan Validasi Input")
h2(story, "12.1 Mata Uang, Hadiah Harian, dan XP")
story.append(P(
    "Mata uang dalam game adalah <b>bakwan</b>. Pemain baru menerima 100 bakwan (setara satu "
    "gacha) \u2014 terverifikasi pada akun resmi yang dimulai dengan saldo 105. Nilai hadiah harian "
    "pada kode sumber statis adalah +1 untuk login, +2 untuk ranked pertama, dan +2 untuk latihan "
    "pertama; namun server produksi ronde kedua memakai nilai yang jauh lebih besar \u2014 <b>+5 / "
    "+15 / +10</b> \u2014 membuktikan konfigurasi memang dapat dioverride dari CMS tanpa publish "
    "ulang. Seluruh progres hadiah direset pukul 00:00 WIB (terverifikasi dua kali: hitung mundur "
    "14 jam 34 menit pada 09.26 dan 12 jam 4 menit pada 21.22). Botol XP dijual 50 bakwan (+100 "
    "XP) dan 250 bakwan (+600 XP). Jejak saldo akun uji konsisten di setiap langkah: 105 \u2192 5 "
    "(gacha) \u2192 20 (+15 bonus ranked) dan tetap 20 setelah BUG-09."))
story.extend(img("menu_utama.jpg",
    "Modal Hadiah Login Harian dengan daftar misi harian dan waktu reset WIB."))
h2(story, "12.2 Gacha Karakter")
story.append(P(
    "Gacha karakter berbiaya 100 bakwan untuk satu kali tarik atau 900 untuk sepuluh kali, "
    "dengan peluang tercantum terbuka: Common 60%, Rare 30%, Legendary 10%. Karakter duplikat "
    "dikonversi menjadi +200 XP karakter tersebut. Pada sesi uji, satu tarikan menghasilkan "
    "karakter Common baru \u201cArshaka\u201d dan saldo berkurang 101 menjadi 1."))
story.extend(img("store_gacha.jpg",
    "Layar Store tab Gacha: tarif kelangkaan terbuka dan dua pilihan tarikan."))
story.extend(img("gacha_hasil.jpg",
    "Hasil gacha uji: karakter Common baru \u201cArshaka\u201d; saldo 101 menjadi 1."))
h2(story, "12.3 Top-Up Uang Nyata")
story.append(P(
    "Monetisasi memakai Xendit (QRIS, e-wallet, virtual account, kartu). Pada mode demo, tombol "
    "\u201cBAYAR (DEMO)\u201d sekali klik langsung mengkreditkan saldo (BUG-05) \u2014 dan pengembang kemudian "
    "mengonfirmasi lewat pengumuman bahwa sistem top-up sempat berjalan test dan di-rollback. "
    "Pada ronde kedua, alur produksi sudah memanggil createTopup dan membuka invoice Xendit "
    "sungguhan, tetapi halaman checkout-nya gagal permanen (BUG-10). Untuk program beta, "
    "disarankan menonaktifkan top-up sampai jalur end-to-end terbukti, agar tidak ada dana "
    "pemain yang terkunci sebelum ekonomi game stabil. Layar teman (kode teman + duel unranked) "
    "dan profil (ganti nickname dengan validasi 3-16 karakter) ditemukan berfungsi normal."))
story.extend(img("teman.jpg",
    "Layar Teman: kode teman pribadi, salin kode, dan penambahan teman via kode."))
h2(story, "12.4 Leaderboard Produksi")
story.append(P(
    "Leaderboard produksi menampilkan Top 50 pemain dengan Elo tertinggi. Puncak papan ditempati "
    "<b>Riska_suka_ytmci</b> (Elo \u00b142xx) dan <b>KinA</b> (\u00b142xx), disusul yuknow (\u00b136xx), Azura "
    "Razena, Natur, Allencv, LawzSigma, yha.zev7n \u2014 seluruhnya berganda tag \u201cJagoan Sekolah\u201d "
    "(Elo 2001+) dan lima teratas mendapat tag otomatis \u201cMurid Teladan\u201d (sesuai konfigurasi "
    "teladan.top=5, minWins=1). Baris akun uji sendiri disematkan khusus di atas daftar agar "
    "selalu terlihat tanpa harus scroll. Kehadiran puluhan pemain dengan Elo 2000+ menandakan "
    "ladder sudah terisi intensif sejak beta dibuka."))
story.extend(img("r2_leaderboard_top.jpg",
    "Leaderboard produksi: baris akun uji tersemat di atas, disusul Riska_suka_ytmci, KinA, dan "
    "yuknow dengan tag Murid Teladan + Jagoan Sekolah.", max_h=190))
story.extend(img("r2_leaderboard_bawah.jpg",
    "Bagian bawah Top 50: Allencv, LawzSigma, yha.zev7n, Junokazz (Pentolan Sekolah), dst.", max_h=190))
h2(story, "12.5 Uji Validasi: Kode Teman dan Nickname")
story.append(P(
    "Dua uji batas dilakukan pada panel Teman dengan akun resmi. Menambahkan kode sendiri "
    "(9VQ9F7) ditolak dengan toast ramah \u201cItu kode kamu sendiri\u201d, dan kode tidak valid "
    "\u201cZZZZ99\u201d ditolak dengan \u201cKode teman tidak ditemukan.\u201d \u2014 keduanya sesuai error map internal "
    "(SELF_FRIEND, NO_SUCH_CODE). Modal Ganti Nickname menyaring input di sisi klien (minimal 3 "
    "karakter, karakter yang diizinkan huruf/angka/spasi/_ . -) dan server melakukan validasi "
    "identik (NAME_LENGTH, NAME_CHARS); input panjang dibatasi maxlength=16 pada input HTML. "
    "Tidak ditemukan celah bypass pada kedua alur tanpa pengujian invasif."))
story.extend(img("r2_teman_kode.jpg",
    "Panel Teman produksi: kode teman pribadi 9VQ9F7 dengan tombol salin dan input tambah teman.", max_h=190))
story.extend(img("r2_teman_self.jpg",
    "Uji validasi 1: menambahkan kode sendiri ditolak dengan \u201cItu kode kamu sendiri\u201d.", max_h=190))
story.extend(img("r2_teman_invalid.jpg",
    "Uji validasi 2: kode \u201cZZZZ99\u201d ditolak dengan \u201cKode teman tidak ditemukan.\u201d", max_h=190))
story.extend(img("r2_nickname.jpg",
    "Modal Ganti Nickname dengan petunjuk syarat 3\u201316 karakter dan batas input 16.", max_h=170))

# ================================================================ 13. REKOMENDASI
h1(story, "13. Rekomendasi Perbaikan")
tbl2 = make_table(
    ["ID", "Rekomendasi", "Prioritas"],
    [
        ["BUG-01",
         "Turunkan ambang reCAPTCHA untuk pendaftaran (mis. reCAPTCHA v3 bermata rendah atau "
         "v2 invisible), perpendek jumlah ronde maksimum, dan panjang umur sesi tantangan. "
         "Berikan pesan kesalahan yang menenangkan serta tombol \u201ccoba tantangan baru\u201d "
         "tanpa mengulang seluruh form. Pantau tingkat keberhasilan pendaftaran sebagai metrik.",
         "Segera"],
        ["BUG-02",
         "Selaraskan kebijakan: bila demo memang disengaja, tampilkan badge \u201cMODE DEMO\u201d "
         "di halaman bakwan.id/game dan beri tautan resmi \u201ccoba demo tanpa akun\u201d; bila "
         "tidak, pindahkan pemeriksaan sesi ke dalam aplikasi game (cepat via pesan Bridge ke "
         "induk Wix) sehingga URL langsung tidak lagi memainkan demo senyap.",
         "Segera"],
        ["BUG-03",
         "Jangan pernah menaruh isAdmin=true pada klien. Hilangkan tombol dan rute admin pada "
         "build publik/demo (tree-shaking), dan tampilkan halaman 404/403 untuk semua fungsi "
         "admin di mode demo. Tambahkan gerbang kata sandi kedua untuk panel admin produksi "
         "serta audit log yang wajib terisi.",
         "Segera"],
        ["BUG-04",
         "Redaksi data sensitif di panel admin (email, kode teman), batasi kolom sesuai kebutuhan "
         "tugas, dan pisahkan label tegas antara data seed/demo dan data produksi.",
         "Sebentar lagi"],
        ["BUG-05",
         "Pisahkan mata uang demo (mis. d-bakwan), nonaktifkan tombol BAYAR (DEMO) di build "
         "produksi, dan wajibkan verifikasi tanda tangan webhook Xendit sebelum kredit saldo.",
         "Sebentar lagi"],
        ["BUG-06", "Bulatkan statistik ATK/DEF ke bilangan bulat pada UI.", "Rendah"],
        ["BUG-07", "Sinkronkan HP sasaran latihan antara konfigurasi kode dan tampilan UI.", "Rendah"],
        ["BUG-08",
         "Ubah izin halaman Wix Members \u201c/account-settings\u201d menjadi \u201cAll members\u201d dari editor "
         "(tidak butuh kode), lalu uji ulang tautan menu akun. Pastikan opsi penghapusan akun "
         "mandiri tersedia sebagaimana dijanjikan program beta.",
         "Sebentar lagi"],
        ["BUG-09",
         "Samakan sumber nilai trainMinHits antara server dan seluruh UI (layar hasil, pesan "
         "syarat, panel admin) \u2014 kirim nilai efektif lewat publicConfig alih-alih hardcode. "
         "Ganti catch(e){} pada endTrain() dengan toast kesalahan + log, dan audit trail untuk "
         "kasus reward ditolak agar tim dukungan bisa memverifikasi klaim pemain.",
         "Segera"],
        ["BUG-10",
         "Uji end-to-end satu paket top-up dengan pembayaran nyata bernilai kecil; verifikasi "
         "webhook/signature Xendit di server; selama belum lolos, sembunyikan tombol top-up atau "
         "tampilkan halaman pemeliharaan alih-alih membiarkan invoice error terbentuk; pantau "
         "invoice gagal di dashboard Xendit dan sampaikan status jujur di pengumuman.",
         "Segera"],
    ],
    [0.11, 0.74, 0.15], align_map={0: "c", 2: "c"})
story.append(tbl2)
story.append(Paragraph("Tabel 2: Rekomendasi perbaikan berdasarkan prioritas.", S["caption"]))

# ================================================================ 14. KRONOLOGI & PENUTUP
h1(story, "14. Kronologi Pengujian dan Catatan Penutup")
h2(story, "14.1 Kronologi Ringkas")
tbl3 = make_table(
    ["Waktu (WIB)", "Kegiatan", "Hasil"],
    [
        ["24 Okt, malam", "Rekon situs bakwan.id: home, blog, kategori \u201cBakwan: Fight Back\u201d",
         "Konteks program didapat; tidak ada pos bug bounty terpublikasi di blog"],
        ["25 Okt, 00.20", "Persiapan temp mail (mail.tm) dan pembukaan halaman game",
         "Email uji siap; gerbang login teridentifikasi"],
        ["25 Okt, 00.30-01.15", "Enam sesi pendaftaran email beserta penyelesaian tantangan "
         "reCAPTCHA multi-ronde", "BUG-01: seluruh sesi berakhir \u201cchallenge expired\u201d"],
        ["25 Okt, 01.20", "Ekstraksi URL iframe game dan pembukaan langsung",
         "BUG-02: mode demo terbuka tanpa akun"],
        ["25 Okt, 01.25-01.40", "Eksplorasi menu demo: Admin, Pemain, Pengaturan, Log",
         "BUG-03/04: panel admin penuh tanpa autentikasi; tidak ada perubahan disimpan"],
        ["25 Okt, 01.45-02.30", "Gameplay latihan 2 ronde, ranked 1 ronde vs bot, gacha 1x, "
         "pembelian botol XP, top-up demo, uji nickname & kode teman",
         "Mekanisme terdokumentasi; BUG-05/06 terkonfirmasi; BUG-07 tercatat"],
        ["25 Okt, 02.35", "Verifikasi akhir inbox temp mail dan pembersihan",
         "Inbox kosong; tidak ada akun terbuat sehingga tidak ada akun untuk dihapus"],
        ["25 Okt, 04.15", "Pengembang melaporkan demo hanya uji; akun resmi disediakan (vameb61409)",
         "Ronde 2 dimulai: login sukses tanpa captcha dalam satu percobaan"],
        ["25 Okt, 04.25-04.45", "Dua match ranked produksi vs pemain asli (Tyyie, Lia__multifandom), "
         "verifikasi profil lawan, riwayat, dan matematika Elo",
         "Elo 100\u219286\u219273 konsisten K=40; bonus ranked +15 bakwan masuk; BUG-08 ditemukan "
         "(Pengaturan Akun diblokir paywall)"],
        ["25 Okt, 20.45-21.10", "Store produksi: gacha 1x (Agatha Common baru), inspeksi XP bottle "
         "dan katalog top-up diskon 33%",
         "Saldo 105\u21925\u219220 konsisten; harga top-up terverifikasi"],
        ["25 Okt, 21.10-21.20", "Uji top-up Rp 5.000: invoice Xendit dibuat lalu dibuka",
         "BUG-10: checkout error permanen \u201cSorry, this wasn't supposed to happen\u201d; ERR_NETWORK di konsol"],
        ["25 Okt, 21.22-21.50", "Lima sesi latihan dengan penjejak piksel (target misi 10 hit)",
         "BUG-09: sesi 11/65 hit tidak menggrant XP/misi; verifikasi setelah reload"],
        ["25 Okt, 21.50-22.05", "Uji validasi kode teman (sendiri + invalid), modal nickname, "
         "leaderboard produksi, dan verifikasi ulang BUG-02/BUG-03 di build terbaru",
         "Validasi bekerja; leaderboard real (puncak Elo \u00b142xx); BUG-02/03/04 masih hidup"],
        ["25 Okt, 05.30-06.10", "Ronde 3 dibuka: produksi gagal boot total; 3 reload + berkali-kali "
         "\u201cCoba lagi\u201d; build lama &amp; baru sama-sama gagal",
         "BUG-11: WD_SCHEMA_DOES_NOT_EXIST (\u22481 jam downtime global); demo tetap jalan"],
        ["25 Okt, 06.13", "Produksi pulih \u2014 build baru 20261025-130337 via play.bakwan.id + "
         "server WS dedicated; bootstrap diekstrak",
         "Arsitektur baru terdokumentasi; dailies naik 5/15/10; 25 karakter; banner diskon 33%"],
        ["25 Okt, 06.20-06.40", "Validasi bot sempurna di demo (73/73 perfect) lalu produksi: "
         "latihan 80/80 perfect (3.594 dmg) + daily +10 bakwan",
         "BUG-12 PoC: BFB_DEBUG memungkinkan bot sempurna; server menerima hit via jalur aksi resmi"],
        ["25 Okt, 06.45-07.05", "14 probe API: gacha (7 varian), buyItem/useItem negatif, "
         "trainDone palsu, selectChar legendary, demoPay, creditPurchase, 6 fungsi admin",
         "37/37 probe ditolak bersih (server baru hardened); demoPay NO_FN; admin NOT_ADMIN"],
        ["25 Okt, 06.50", "Retest top-up Rp 5.000 sampai langkah invoice (tanpa membayar)",
         "BUG-10 PERBAIKAN: invoice bfb-mvngxvaj65cdx8 terbit mulus via Xendit"],
        ["25 Okt, 06.55-07.10", "16 match ranked produksi dengan bot (24\u201332 perfect/match)",
         "10W/8L, Elo 39\u2192165 puncak; kemenangan terbukti TIDAK membayar bakwan (saldo tetap)"],
        ["25 Okt, 07.15-07.30", "Analisis ekonomi gacha + screenshot bukti final (profil, "
         "leaderboard #946, halaman Karis, toko)",
         "Karis \u224870 tarikan \u22486.300\u20137.000 bakwan \u2248233 hari dailies \u2014 tidak "
         "terjangkau tanpa top-up; laporan diperbarui"],
    ],
    [0.16, 0.47, 0.37])
story.append(tbl3)
story.append(Paragraph("Tabel 3: Kronologi pengujian 24-25 Oktober 2026 (tiga ronde).", S["caption"]))
h2(story, "14.2 Kebersihan Pengujian")
story.append(P(
    "Sesuai permintaan penyelenggara bahwa akun dapat dihapus setelah pengujian, kami menegaskan: "
    "<b>tidak ada akun yang berhasil dibuat</b> karena seluruh sesi pendaftaran terhalang BUG-01, "
    "sehingga tidak ada data akun yang perlu dihapus. Alamat temp mail bakkyo1lx30lbw@maxxspace.com "
    "diverifikasi kosong tanpa surat konfirmasi apa pun, dan dapat dibiarkan kedaluwarsa dengan "
    "aman. Tidak ada perubahan yang disimpan pada panel admin demo, tidak ada saldo/pemain nyata "
    "yang tersentuh, dan seluruh interaksi terhadap server produksi terbatas pada permintaan baca "
    "normal sebagaimana peramban pengunjung biasa."))
story.append(P(
    "Untuk ronde kedua: akun resmi <b>vameb61409@hiringview.com adalah milik penyelenggara dan "
    "sengaja tidak dihapus/dilogout permanen</b>. Perubahan yang terjadi pada akun selama audit "
    "\u2014 seluruhnya hasil gameplay normal dan dapat diverifikasi di riwayat \u2014 adalah: dua "
    "kekalahan ranked (Elo 100 \u2192 73, rekor 0/2/0), satu tarikan gacha (karakter baru Agatha), "
    "saldo bakwan 105 \u2192 20, tiga misi harian (login +5, ranked +15; latihan tidak terkredit "
    "karena BUG-09), serta satu invoice Xendit Rp 5.000 yang dibuat namun <b>tidak pernah "
    "dibayar</b> (checkout error; invoice akan kedaluwarsa sendiri). Tidak ada pesan tantangan "
    "yang dikirim ke pemain lain dan tidak ada data pemain lain yang diubah."))
story.append(P(
    "Untuk ronde ketiga, perubahan akun adalah: 15 match ranked dengan bot sempurna (rekor "
    "menjadi 10W/8L/0D; Elo puncak baru <b>165</b>), satu sesi latihan 80 perfect (Agatha Lv 6), "
    "saldo bakwan 20 \u2192 30 murni dari hadiah harian latihan, satu invoice Xendit Rp 5.000 "
    "dibuat untuk verifikasi BUG-10 dan <b>sengaja tidak dibayar</b> (kedaluwarsa otomatis 24 "
    "jam), tidak ada tarikan gacha (saldo tidak cukup \u2014 30 &lt; 100), nickname, teman, dan "
    "tantangan tidak disentuh, dan tidak ada data pemain lain yang dibaca maupun diubah. Seluruh probe API "
    "dijalankan hanya dengan kredensial akun uji sendiri, tanpa payload destruktif, tanpa "
    "broadcast, dan tanpa beban berulang ke server."))
h2(story, "14.3 Penutup")
story.append(P(
    "Bakwan Fight Back merupakan paket game beta yang mengesankan untuk ukuran komunitas: satu "
    "berkas HTML ringan dengan sistem timing yang menantang, ekonomi gacha yang transparan, "
    "matchmaking Elo, relay realtime, hingga panel operasional yang lengkap. Audit ronde kedua "
    "dengan akun resmi justru menambah sisi positif yang layak diapresiasi: matchmaking ranked "
    "nyata berjalan cepat dengan ladder yang sehat (ribuan pemain terperingkat, puluhan pemain "
    "Elo 2000+), matematika Elo terverifikasi presisi, misi harian dan bonus ranked mengalir "
    "benar, validasi input tahan banting, dan anti-makro latihan bekerja efektif. Ronde ketiga "
    "menambahkan apresiasi yang jauh lebih besar lagi: dalam hitungan jam setelah laporan ronde "
    "kedua, pengembang memigrasikan seluruh game ke subdomain dan server WebSocket khusus, "
    "membangun ulang sistem battle/Elo, menaikkan hadiah harian, <b>memperbaiki BUG-10 secara "
    "verifikasi</b>, dan menghadirkan server baru yang menolak seluruh 14 probe manipulasi API "
    "dengan bersih \u2014 tingkat kegesitan yang jarang dijumpai pada program bug bounty mana "
    "pun."))
story.append(P(
    "Di sisi lain, ronde kedua menyingkap dua masalah yang paling menyakitkan secara bisnis: "
    "pintu pendapatan (top-up Xendit) gagal 100% pada langkah terakhir (BUG-10), dan reward "
    "progresi yang dijanjikan UI tidak pernah jatuh (BUG-09) \u2014 ditambah BUG-08 yang menutup "
    "akses member ke pengaturan akunnya sendiri. Ronde ketiga menambahkan dua kekhawatiran baru "
    "yang lebih strategis: <b>rentan waktu henti produksi</b> saat migrasi (BUG-11) dan <b>hook "
    "debug klien yang menjadikan bot sempurna trivial</b> (BUG-12) \u2014 mengancam integritas "
    "ladder ranked dan nilai eksklusif karakter Legendary, ditambah ekonomi gacha yang "
    "secara matematis menutup akses karakter target bagi pemain non-top-up (\u2248233 hari "
    "pengumpulan). Kedua temuan kritis ronde pertama (bypass gerbang dan paparan panel admin "
    "demo) juga masih hidup. Dengan menutup lima temuan kritis \u2014 loop captcha, bypass "
    "gerbang, paparan admin, checkout pembayaran (\u2713 selesai), dan downtime migrasi (pulih) "
    "\u2014 serta memagari hook debug dan menyeimbangkan ekonomi gacha, game ini siap diuji luas "
    "ke komunitas Bakky dengan risiko yang jauh lebih terkendali. Kami siap membantu verifikasi "
    "ulang setelah perbaikan dirilis."))

# ================================================================ 15. RONDE 3
h1(story, "15. Ronde 3: Migrasi Server, Bot Sempurna, dan Ekonomi Gacha (25 Okt 2026)")
story.append(P(
    "Ronde ketiga dilaksanakan dengan instruksi khusus dari penyelenggara: BUG-08 dan BUG-10 "
    "sedang dikerjakan, BUG-09 dinyatakan berjalan sesuai desain, dan penguji diminta "
    "<b>memainkan game sampai memperoleh karakter Legendary \u201cKaris\u201d</b> sekaligus menguji "
    "logika gacha, dengan saran agar ranked diprioritaskan karena \u201cuang\u201d bakwan bisa "
    "diperoleh dari latihan atau ranked. Ronde ini dilakukan dengan akun resmi yang sama "
    "(vameb61409) pada build baru <b>20261025-130337</b> dan menutup seluruh misi tersebut dengan "
    "temuan yang jauh lebih dalam dari sekadar bug: sebuah peristiwa downtime, satu celah klien "
    "berdampak kompetitif, bukti empiris pengerasan server, dan analisis ekonomi yang "
    "menunjukkan karakter target secara realistis tidak terjangkau tanpa top-up uang riil."))

h2(story, "15.1 BUG-11 (Kritis): Downtime Produksi \u2014 WD_SCHEMA_DOES_NOT_EXIST")
story.append(P(
    "Pada awal sesi (sekitar pukul 05.30\u201306.10 WIB), halaman game produksi gagal boot total: "
    "setelah logo, layar menampilkan pesan <b>\u201cGagal memuat: Error: "
    "WD_SCHEMA_DOES_NOT_EXIST\u201d</b> dengan tombol \u201cCoba lagi\u201d yang selalu gagal. Error ini "
    "adalah kode galat Wix Data yang berarti <b>skema koleksi basis data yang diminta tidak "
    "ada</b> \u2014 konsisten dengan pengembang yang sedang membangun/memigrasi data di tengah "
    "perbaikan BUG-08/BUG-10. Kegagalan bersifat persisten (3 kali reload halaman penuh + "
    "berkali-kali klik \u201cCoba lagi\u201d selama \u2248 40 menit) dan <b>menimpa kedua build</b> "
    "(build lama 8756bf... maupun build baru yang sedang digulirkan), sehingga seluruh pemain "
    "tidak dapat bermain pada rentang waktu tersebut. Menariknya, mode demo tetap berjalan "
    "normal karena tidak menyentuh backend \u2014 memperlihatkan pemisahan jalur demo/produksi yang "
    "memang dirancang. Game pulih sendiri sekitar pukul 06.13 WIB ketika build baru selesai "
    "digulirkan. Gambar 58 dan 59 menunjukkan kondisi gagal boot tersebut."))
story.extend(img("r3_bug11_downtime.jpg", "Layar gagal boot produksi: WD_SCHEMA_DOES_NOT_EXIST (BUG-11)."))
story.extend(img("r3_recovery_menu.jpg", "Produksi pulih pukul 06.13 WIB \u2014 menu utama build baru dengan banner pengumuman update."))

h2(story, "15.2 Migrasi Infrastruktur: play.bakwan.id dan Server WebSocket Dedicated")
story.append(P(
    "Bersamaan dengan pemulihan, terdeteksi perubahan arsitektur yang sangat besar: iframe game "
    "kini memuat <b>https://play.bakwan.id/game.html</b> (subdomain khusus game) menggantikan "
    "berkas statis filesusr.com, dan seluruh trafik API berpindah ke <b>server WebSocket "
    "dedicated wss://play.bakwan.id/ws</b> yang berjalan di luar Wix. Pengumuman di dalam game "
    "menegaskan konteksnya: \u201c<b>Update Battle &amp; sistem ELO baru! Bakwan diskon 33% sampai "
    "akhir bulan ini (semoga ada lebih dari $12 buat bayar server coy T_T - Nelson)</b>\u201d \u2014 "
    "sebuah kejujuran biaya infrastruktur yang patut diapresiasi. Perubahan yang terverifikasi "
    "pada build baru antara lain: hadiah login harian baru (modal \u201cHadiah Login Harian!\u201d), "
    "besaran hadiah harian dinaikkan dari 1/2/2 menjadi <b>5 (login) / 15 (ranked pertama) / 10 "
    "(latihan pertama) bakwan per hari</b>, syarat hit latihan dinaikkan 10 \u2192 <b>20</b>, "
    "konfigurasi server kini menyertakan 25 karakter (11 common, 7 rare, 7 legendary) dengan "
    "Karis ber-ID internal \u201cbeaconcream\u201d, serta mode latihan baru dengan target damage "
    "5.000 dan bom berjadwal (13\u201314 bom per sesi 60 detik, damage 6% HP sendiri). Panel admin "
    "mode demo juga membawa kontrol yang lebih luas (termasuk pengaturan peluang gacha, bom, dan "
    "Elo) \u2014 BUG-03/04 masih hidup di sisi demo, namun ACL sisi server tetap solid (lihat "
    "15.5)."))
story.extend(img("r3_banner_update.jpg", "Banner pengumuman update battle/Elo + diskon 33% di build baru."))
story.extend(img("r3_daily_newbuild.jpg", "Fitur baru: modal Hadiah Login Harian di build 20261025-130337."))

h2(story, "15.3 BUG-12 (Kritis): Hook Debug BFB_DEBUG \u2014 Bot Sempurna yang Trivial")
story.append(P(
    "Kode klien build baru (dan build lama) mendefinisikan objek debug global "
    "<b>window.BFB_DEBUG</b> tanpa syarat apa pun, yang memaparkan: <b>B</b> (seluruh state "
    "papan, termasuk <b>sched</b> \u2014 jadwal lengkap setiap objek berisi jenis lingkaran/bom/"
    "skill, waktu muncul <i>a</i>, <b>waktu hit sempurna <i>h</i></b>, posisi <i>x/y</i>), "
    "<b>L()</b> (geometri area main), <b>serverNow()</b>, dan yang terpenting <b>tap(x, y)</b> "
    "\u2014 fungsi injeksi ketukan yang langsung masuk ke alur penilaian resmi game (judge "
    "\u2192 applyActions \u2192 antrian aksi \u2192 sendHits). Dengan dua informasi ini, sebuah bot "
    "\u2248 40 baris JavaScript cukup untuk men-tap <b>setiap lingkaran tepat di momen perfect-nya "
    "(\u00b170 ms)</b> dan menghindari seluruh bom. Hasil PoC pada akun resmi:"))
story.append(callout_row([
    ("80/80", "Perfect di latihan (3594 dmg)"),
    ("10W/8L", "Rekor ranked total R3"),
    ("165", "Elo puncak (dari 39)"),
    ("5", "Kemenangan beruntun"),
]))
story.append(P(
    "Bot dijalankan di build demo (validasi: 73/73 perfect) lalu di produksi: satu sesi latihan "
    "tercatat <b>80 perfect dari 80 tembakan, damage 3.594</b> (Gambar 64), dan "
    "enam belas match ranked melawan pemain/bot nyata menghasilkan 10 kemenangan dengan 24\u201332 "
    "perfect per match \u2014 termasuk lima kemenangan beruntun yang mengangkat Elo dari titik "
    "terendah 39 ke <b>165</b> (Gambar 65). Seluruh aksi bot mengalir lewat jalur "
    "aksi resmi yang sama dengan manusia, sehingga dari sudut pandang server <b>bot ini tak "
    "dapat dibedakan dari pemain sangat terampil</b>. Rekomendasi: hapus/pagari hook debug pada "
    "build produksi (mis. hanya aktif saat flag build khusus), dan pertimbangkan heuristik "
    "sisi server (distribusi offset timing, rasio perfect/jam, pola reaksi) untuk deteksi bot.")) 
story.extend(img("r3_bom_lingkaran.jpg", "Mekanik build baru: lingkaran bernomor + bom (hitam, rim merah, \u201c!\u201d) yang wajib dihindari."))
story.extend(img("r3_bot_perfect73.jpg", "PoC bot pada demo: 73 perfect dari 73, combo 73, damage 2.920."))
story.extend(img("r3_train_hasil_bot.jpg", "PoC bot pada produksi: 80/80 perfect, damage 3.594, daily latihan +10 bakwan."))
story.extend(img("r3_menang_ranked_prod.jpg", "PoC ranked produksi: MENANG K.O., Elo 72\u219292 (+20), Perfect 24, tanpa reward bakwan."))

h2(story, "15.4 Model Anti-Cheat sendHits: Deterministik-Replay yang Benar (dengan Catatan)")
story.append(P(
    "Bedah protokol pertarungan menunjukkan desain anti-cheat yang sehat secara prinsip: klien "
    "<b>tidak mengirim angka damage</b>, melainkan daftar <b>aksi</b> (id objek, kualitas, waktu) "
    "yang kemudian <b>disimulasikan ulang oleh server</b> terhadap seed match yang sama "
    "(applyActions dengan seed m.seed), lengkap dengan pencegahan inflasi (maksimum 40 aksi per "
    "panggilan sendHits, jendela waktu t \u2208 [-500 ms, durasi+4 s], validasi keanggotaan "
    "match, dan penentuan koAt untuk kasus double-KO). Konsekuensinya, memalsukan angka damage "
    "atau membunuh lawan seketika <b>tidak mungkin</b> melalui jalur API. Kelemahannya tetap di "
    "sisi input: kualitas dan waktu aksi adalah <b>klaim klien</b> \u2014 server tidak dapat "
    "memverifikasi bahwa aksi tersebut benar-benar berasal dari interaksi manusia, sehingga bot "
    "sempurna pada 15.3 lolos sepenuhnya. Kombinasi \u201cBFB_DEBUG terbuka + aksi dipercaya\u201d "
    "berarti ladders ranked dapat dipenuhi bot tanpa jejak \u2014 berisiko pada integritas "
    "peringkat dan nilai jual karakter gacha."))

h2(story, "15.5 Pengerasan Server Terbukti: 37 Panggilan Probe API Ditolak Bersih")
story.append(P(
    "Sesuai misi \u201cmenguji logika gacha\u201d, dilakukan 37 panggilan probe API dalam 9 kelompok uji, langsung ke "
    "server baru melalui sesi WebSocket resmi akun uji (tanpa tools eksternal, tanpa beban ke "
    "server, dan tanpa memengaruhi pemain lain). Hasilnya konsisten dan menggembirakan:"))
tbl_probe = make_table(
    ["Probe", "Payload", "Ekspektasi celah", "Hasil server"],
    [
        ["gacha(1/10/0/-1/\"10\"/10000)", "Saldo 30 bakwan", "Tarikan gratis / harga nol", "NOT_ENOUGH_BAKWAN (semua)"],
        ["buyItem('nope',1)", "Item tidak ada", "Error generik/bocor", "NO_ITEM"],
        ["buyItem('xpS', 0/-3/0.5)", "Qty nol/negatif/pecahan", "Saldo bertambah (qty negatif)", "Ditolak (tidak ada transaksi)"],
        ["useItem('xpS',...,-5/-99)", "Qty negatif saat stok 0", "Duplikasi item", "Ditolak"],
        ["trainDone(fake hits:50)", "Ringkasan latihan palsu", "XP/misi tanpa main", "tooFew \u2014 server menghitung hit sendiri"],
        ["selectChar(legendaries)", "Karakter tidak dimiliki", "Pakai Karis gratis", "NOT_OWNED"],
        ["demoPay(invoiceId)", "Kredit invoice tanpa bayar", "+100 bakwan gratis", "NO_FN \u2014 rute dihapus dari server"],
        ["creditPurchase(extId)", "Kredit langsung", "+saldo", "Tidak dapat dijangkau (ctx wajib)"],
        ["adminOverview/adminAnnounce/... (6 fn)", "Tanpa hak admin", "ACL bocor", "NOT_ADMIN (semua)"],
    ],
    [0.30, 0.22, 0.24, 0.24])
story.append(tbl_probe)
story.append(Paragraph("Tabel 4: Hasil probe manipulasi API server play.bakwan.id \u2014 seluruhnya ditolak.", S["caption"]))
story.append(P(
    "Dua temuan menarik dari proses ini: pertama, kirim argumen dalam format keliru (string "
    "bukan array) menyebabkan server mendekonstruksi argumen per karakter \u2014 responsnya tetap "
    "aman (NOT_OWNED/NO_ITEM, tanpa crash, tanpa efek data), namun sebaiknya validasi tipe "
    "argumen diperketat agar menolak permintaan malform seketika. Kedua, <b>tidak ada satu pun "
    "celah ekonomi yang bisa dieksploitasi</b>: dengan saldo 30 bakwan, tidak ada jalur menuju "
    "tarikan gacha pertama (100 bakwan) selain bermain harian atau top-up \u2014 bukti bahwa "
    "pelajaran dari BUG-05 (demo pay) dan BUG-10 (checkout) telah ditindaklanjuti serius oleh "
    "pengembang."))

h2(story, "15.6 Analisis Ekonomi Gacha: Karis Secara Realistis Tidak Terjangkau")
story.append(P(
    "Misi memperoleh Karis diuji sejauh yang memungkinkan tanpa pengeluaran uang riil. Konfigurasi "
    "resmi build 20261025-130337 (diekstrak dari respons bootstrap akun sendiri) menetapkan: "
    "harga gacha <b>100 bakwan (1x)</b> / <b>900 (10x)</b>; peluang <b>Common 60% / Rare 30% / "
    "Legendary 10%</b>; katalog <b>25 karakter = 10 common + 7 rare + 7 legendary</b>; duplikat "
    "memberi +200 XP; dan <b>tidak ada sistem pity</b> (jaminan legendary pada N tarikan) dalam "
    "konfigurasi maupun kode. Karena legendary dipilih seragam dari 7 kandidat, peluang Karis "
    "per tarikan = 10% \u00d7 1/7 \u2248 <b>1,43%</b>; ekspektasi tarikan hingga Karis keluar "
    "\u2248 <b>70 tarikan \u2248 6.300\u20137.000 bakwan</b> (63\u201370 paket 10x), setara "
    "<b>\u2248 Rp 283.000\u2013350.000</b> pada harga diskon (Rp 50.000 per 1.200 bakwan)."))
story.append(P(
    "Sisi pendapatan gameplay justru sangat kecil: <b>kemenangan ranked tidak membayar bakwan "
    "sama sekali</b> \u2014 diverifikasi langsung pada 10 kemenangan produksi (saldo tetap "
    "30 sebelum/sesudah modal \u201cMENANG!\u201d hanya menampilkan Elo dan XP; Tabel kronologi). "
    "Satu-satunya pendapatan legal adalah hadiah harian: login +5, ranked pertama +15, latihan "
    "pertama +10 = <b>maksimum 30 bakwan/hari</b>. Dengan demikian ekspektasi Karis lewat "
    "gameplay murni adalah <b>\u2248 233 hari</b> pengumpulan penuh \u2014 sedangkan melalui "
    "top-up \u2248 6 paket \u201cSegerobak\u201d (Rp 300.000) ditambah sisa saldo. Rekomendasi "
    "produk: tambahkan <b>pity counter</b> (mis. legendary terjamin setiap 30\u201350 tarikan), "
    "banner legendary terfokus, reward bakwan kecil per kemenangan ranked (mis. +2\u20135), atau "
    "paket langsung beli karakter \u2014 agar misi \u201cdapatkan Karis dengan bermain\u201d "
    "secara matematis mungkin dicapai oleh pemain aktif."))
story.extend(img("r3_karis_page.jpg", "Halaman karakter Karis (Legendary, HP 1100/ATK 46/DEF 25) \u2014 target misi gacha."))
story.extend(img("r3_gacha_30bakwan.jpg", "Saldo 30 bakwan vs harga 100 (1x) / 900 (10x): tarikan pertama tidak terjangkau hari itu."))

h2(story, "15.7 Status Ulang Temuan Ronde 2 pada Build Baru")
story.append(P(
    "<b>BUG-10 \u2014 PERBAIKAN (diverifikasi)</b>: alur top-up Rp 5.000 kini membuat invoice "
    "Xendit mulus tanpa layar \u201cSorry, this wasn't supposed to happen\u201d. Invoice uji "
    "<b>bfb-mvngxvaj65cdx8</b> terbit dengan batas bayar 24 jam, metode pembayaran lengkap (Bank "
    "Transfer, Retail Outlet, E-Wallet, QRIS) \u2014 dan <b>sengaja tidak dibayar</b> karena "
    "pengujian tidak meliputi transaksi uang riil (Gambar 68). <b>BUG-09 \u2014 sesuai "
    "desain (dikonfirmasi)</b>: server menghitung hit secara independen dari tampilan klien "
    "(uji ringkasan palsu hits:50 ditolak \u201ctooFew\u201d); sesi bot asli dengan 80 hit "
    "terserver langsung menggrant XP +10 dan misi harian +10 bakwan. Syarat pun dinaikkan "
    "menjadi 20 hit. <b>BUG-08</b>: menu terkait tidak lagi tampil pada UI game baru; halaman "
    "anggota Wix berada di luar iframe game dan tidak diverifikasi ulang pada ronde ini. "
    "<b>BUG-02/03/04</b>: masih hidup pada mode demo build baru (panel admin lengkap dengan "
    "kontrol ekonomi terbuka tanpa auth \u2014 Gambar 69), namun tetap terkurung di "
    "localStorage demo."))
story.extend(img("r3_bug10_fixed_invoice.jpg", "BUG-10 pulih: invoice Xendit bfb-mvngxvaj65cdx8 terbit mulus (tidak dibayar \u2014 bukti perbaikan saja)."))
story.extend(img("r3_admin_setting_baru.jpg", "BUG-03/04 masih hidup di demo build baru: kontrol server (gacha, bom, Elo) terbuka."))

h2(story, "15.8 Log Perubahan Akun Uji pada Ronde 3")
story.append(P(
    "Transparansi penuh atas dampak pengujian pada akun vameb61409 (milik penyelenggara): "
    "16 match ranked (rekor menjadi 10W/8L/0D, Elo 100 \u2192 39 \u2192 <b>165</b>, puncak baru), "
    "1 sesi latihan (80 perfect, Agatha +10 XP), saldo bakwan 20 \u2192 <b>30</b> (hanya dari "
    "hadiah harian latihan; tidak ada top-up terbayar, tidak ada gacha dilakukan karena saldo "
    "tidak cukup), karakter Agatha naik Lv 2 \u2192 <b>6</b> dari XP kemenangan, 1 invoice "
    "Xendit Rp 5.000 dibuat dan <b>tidak dibayar</b> (akan kedaluwarsa otomatis), nickname tidak "
    "diubah, tidak ada teman ditambahkan, tidak ada tantangan dikirim ke pemain lain, dan tidak "
    "ada data pemain lain yang disentuh. Seluruh perubahan bersumber dari gameplay normal "
    "melalui klien resmi (dengan otomasi ketukan via hook debug publik milik game sendiri) dan "
    "dapat diverifikasi pada riwayat match."))

# ================================================================ BUILD
doc = TocDocTemplate(
    OUT_BODY, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
    title=DOC_TITLE, author="Z.ai", creator="Z.ai",
    subject="Laporan QA dan bug bounty game beta Bakwan Fight Back (bakwan.id)")
for _i, _f in enumerate(story):
    if isinstance(_f, list):
        print("LIST at story index", _i, "len", len(_f), repr(_f)[:200])
doc.multiBuild(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("BODY OK:", OUT_BODY)
