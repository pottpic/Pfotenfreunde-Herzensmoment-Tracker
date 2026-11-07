"""Baut die Silvester-Checkliste (1080x1350, Dunkelgrün/Creme, Logo). Aufruf: python3 team/grafik/silvester_checkliste.py"""
from PIL import Image, ImageDraw, ImageFont
G, C = (0x2F, 0x5D, 0x50), (0xFA, 0xF1, 0xE0)
W, H = 1080, 1350
F = "/usr/share/fonts/truetype/dejavu/"
title = ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 84)
sub = ImageFont.truetype(F + "DejaVuSans.ttf", 38)
item = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 40)
foot = ImageFont.truetype(F + "DejaVuSans.ttf", 30)
img = Image.new("RGB", (W, H), G)
d = ImageDraw.Draw(img)
d.rounded_rectangle((50, 50, W - 50, H - 50), radius=40, outline=C, width=4)
d.text((W // 2, 170), "Gut durch Silvester", font=title, fill=C, anchor="mm")
d.text((W // 2, 255), "Deine Checkliste zum Speichern", font=sub, fill=C, anchor="mm")
items = ["Geschirr sitzt sicher", "Schleppleine dran", "Schon Tage vorher an der Leine",
         "Ruhiger Rückzugsort drinnen", "Letzte Runde noch im Hellen",
         "Marke mit Telefonnummer", "Starke Angst? Früh zur Tierärztin"]
y = 360
for t in items:
    d.rounded_rectangle((130, y - 26, 182, y + 26), radius=10, outline=C, width=5)
    d.line((142, y, 154, y + 13, 172, y - 15), fill=C, width=7, joint="curve")
    d.text((215, y), t, font=item, fill=C, anchor="lm")
    y += 98
logo = Image.open("logo/derner-schnauzenbande-logo.png").convert("RGBA")
logo.thumbnail((130, 130))
badge = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
ImageDraw.Draw(badge).ellipse((0, 0, 199, 199), fill=C)
badge.paste(logo, ((200 - logo.width) // 2, (200 - logo.height) // 2), logo)
img.paste(badge, (W // 2 - 100, 1030), badge)
d.text((W // 2, 1268), "Derner Schnauzenbande · www.dernerschnauzenbande.de", font=foot, fill=C, anchor="mm")
img.save("ergebnisse/social/2026-10-31-silvester-checkliste.png")
