#!/usr/bin/env python3
"""Merge cover + body into final PDF, normalize A4."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

def normalize(page):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    if abs(w - A4_W) > 0.1 or abs(h - A4_H) > 0.1:
        page.scale_to(A4_W, A4_H)
    return page

writer = PdfWriter()
writer.add_page(normalize(PdfReader("/home/z/my-project/scripts/cover.pdf").pages[0]))
for p in PdfReader("/home/z/my-project/scripts/body.pdf").pages:
    writer.add_page(normalize(p))
writer.add_metadata({
    "/Title": "Laporan Bug Bounty - Bakwan Fight Back (bakwan.id/game)",
    "/Author": "Z.ai", "/Creator": "Z.ai",
    "/Subject": "Laporan QA dan bug bounty game beta Bakwan Fight Back (bakwan.id)",
})
out = "/home/z/my-project/download/Laporan_Bug_Bounty_Bakwan_Fight_Back.pdf"
with open(out, "wb") as f:
    writer.write(f)
print("FINAL:", out, "pages:", len(writer.pages))
