"""QR-Codes für Aushang und Karten bauen (0 €, offline).

Aufruf:  python3 angebot/qr/qr_machen.py aushang karte hundeschule-xy
Macht pro Name eine Datei angebot/qr/<name>.svg, die auf
<seitenUrl>?von=<name> zeigt. Die Adresse steht in angebot/konfig.js.
Braucht: pip install qrcode
"""
import pathlib, re, sys
import qrcode, qrcode.image.svg

hier = pathlib.Path(__file__).resolve().parent
konfig = (hier.parent / "konfig.js").read_text(encoding="utf-8")
url = re.search(r'seitenUrl:\s*"([^"]+)"', konfig).group(1)

for name in sys.argv[1:] or ["aushang", "karte"]:
    if not re.fullmatch(r"[a-z0-9-]{1,40}", name):
        sys.exit(f"Name nur aus a-z, 0-9 und Bindestrich: {name}")
    ziel = f"{url}?von={name}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
    qr.add_data(ziel)
    qr.make(fit=True)
    qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(hier / f"{name}.svg")
    print(f"{name}.svg  ->  {ziel}")
