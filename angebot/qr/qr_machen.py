"""QR-Codes für Aushang und Karten bauen (0 €, offline).

Aufruf:  python3 angebot/qr/qr_machen.py aushang karte hundeschule-xy

Steht in angebot/konfig.js eine WhatsApp-Nummer, führt der Code direkt
zu WhatsApp, mit fertiger Nachricht an Moni, inkl. Herkunft.
Sonst führt er auf die Angebotsseite (<seitenUrl>?von=<name>).
Macht pro Name angebot/qr/<name>.svg und <name>.png.
Braucht: pip install qrcode pillow
"""
import pathlib, re, sys, urllib.parse
import qrcode, qrcode.image.svg

hier = pathlib.Path(__file__).resolve().parent
konfig = (hier.parent / "konfig.js").read_text(encoding="utf-8")
url = re.search(r'seitenUrl:\s*"([^"]*)"', konfig).group(1)
wa = re.search(r'whatsapp:\s*"([^"]*)"', konfig).group(1)

HERKUNFT = {"aushang": "ich habe deinen Aushang gesehen", "karte": "ich habe deine Karte mitgenommen"}

def ziel(name):
    if wa:
        wo = HERKUNFT.get(name, f"ich habe deinen Aushang bei {name.replace('-', ' ').title()} gesehen")
        text = f"Hey Moni, {wo} und möchte mehr wissen!"
        return f"https://wa.me/{wa}?text=" + urllib.parse.quote(text)
    return f"{url}?von={name}"

for name in sys.argv[1:] or ["aushang", "karte"]:
    if not re.fullmatch(r"[a-z0-9-]{1,40}", name):
        sys.exit(f"Name nur aus a-z, 0-9 und Bindestrich: {name}")
    z = ziel(name)
    for fabrik, endung, extra in [(qrcode.image.svg.SvgPathImage, "svg", {}), (None, "png", {})]:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2 if endung == "svg" else 3, box_size=10 if endung == "svg" else 20)
        qr.add_data(z)
        qr.make(fit=True)
        if fabrik:
            qr.make_image(image_factory=fabrik).save(hier / f"{name}.{endung}")
        else:
            qr.make_image(fill_color="#1a120b", back_color="white").convert("RGB").save(hier / f"{name}.{endung}")
    print(f"{name}  ->  {urllib.parse.unquote(z)}  (Version {qr.version})")
