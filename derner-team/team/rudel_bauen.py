#!/usr/bin/env python3
"""Baut derner-team/team/rudel.html (Das Derner-Rudel) – Aufruf: python3 rudel_bauen.py
Neue Figur? Eintrag in TEAM ergänzen, Skript laufen lassen, fertig."""
import html, pathlib

def hair(style, c):
    if style == "bun":
        return f'<circle cx="89" cy="40" r="15" fill="{c}"/>', f'<path d="M56 80 C58 58 72 48 90 48 C108 48 122 58 122 80 C106 64 74 64 56 80 Z" fill="{c}"/>'
    if style == "long":
        return f'<path d="M50 86 C44 120 50 150 62 160 L118 160 C130 150 134 120 128 86 Z" fill="{c}"/>', f'<path d="M54 84 C54 58 70 46 90 46 C112 46 126 60 124 84 C112 70 98 66 86 64 C76 70 64 76 54 84 Z" fill="{c}"/>'
    if style == "curly":
        return f'<g fill="{c}"><circle cx="58" cy="76" r="14"/><circle cx="68" cy="58" r="14"/><circle cx="90" cy="50" r="15"/><circle cx="112" cy="58" r="14"/><circle cx="122" cy="76" r="14"/></g>', ''
    return '', f'<path d="M56 78 C60 56 76 48 90 48 C108 48 120 58 122 78 C104 70 92 62 84 58 C78 66 66 74 56 78 Z" fill="{c}"/>'  # short

def dog(d):
    fur, ear, muz = d["fur"], d["ear"], d["muz"]
    if d["type"] == "pointed":
        ears = f'<path d="M124 138 L120 108 L140 128 Z" fill="{ear}"/><path d="M168 138 L172 108 L152 128 Z" fill="{ear}"/>'
    else:
        ears = f'<ellipse cx="122" cy="152" rx="10" ry="18" fill="{ear}" transform="rotate(18 122 152)"/><ellipse cx="170" cy="152" rx="10" ry="18" fill="{ear}" transform="rotate(-18 170 152)"/>'
    extra = d.get("extra", "")
    return (f'<g transform="translate(150 158) scale(1.32) translate(-146 -150)">{ears}<ellipse cx="146" cy="150" rx="24" ry="26" fill="{fur}"/>{extra}'
            f'<ellipse cx="146" cy="160" rx="15" ry="11" fill="{muz}"/><ellipse cx="146" cy="154" rx="6" ry="4.4" fill="#1A1210"/>'
            '<path d="M146 158 V162 M140 164 Q146 168 152 164" stroke="#1A1210" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            '<circle cx="135" cy="144" r="3.6" fill="#1A1210"/><circle cx="157" cy="144" r="3.6" fill="#1A1210"/>'
            '<circle cx="136" cy="142.8" r="1.1" fill="#fff"/><circle cx="158" cy="142.8" r="1.1" fill="#fff"/>'
            '<path d="M142 166 Q146 176 150 166 Z" fill="#E86A7A"/></g>')

S = 'stroke="#2B3A2F" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
 "kompass": f'<circle cx="18" cy="18" r="9" {S}/><path d="M22 14 L19 19 L14 22 L17 17 Z" {S}/>',
 "brief": f'<rect x="8" y="11" width="20" height="14" rx="2" {S}/><path d="M8 12 L18 20 L28 12" {S}/>',
 "flagge": f'<path d="M12 28 V9 M12 10 H26 L23 15 L26 20 H12" {S}/>',
 "ordner": f'<path d="M8 12 H15 L17 15 H28 V26 H8 Z" {S}/>',
 "kette": f'<path d="M15 21 L21 15 M13 17 a4 4 0 0 1 0 -6 a4 4 0 0 1 6 0 M23 19 a4 4 0 0 1 0 6 a4 4 0 0 1 -6 0" {S}/>',
 "stern": f'<path d="M18 8 L20.5 15 L28 15.5 L22 20 L24 27.5 L18 23.5 L12 27.5 L14 20 L8 15.5 L15.5 15 Z" {S}/>',
 "pinsel": f'<path d="M26 9 L15 20 M15 20 a4 4 0 0 0 -4 4 a3 3 0 0 1 -2 3 a6 6 0 0 0 8 -2 a4 4 0 0 0 -2 -5" {S}/>',
 "schild": f'<path d="M18 8 L27 11 V18 C27 23 23 27 18 29 C13 27 9 23 9 18 V11 Z" {S}/><path d="M14 18 l3 3 l5-6" {S}/>',
 "pfote": f'<circle cx="12" cy="14" r="2.6" {S}/><circle cx="18" cy="11" r="2.6" {S}/><circle cx="24" cy="14" r="2.6" {S}/><path d="M13 24 C13 19 23 19 23 24 C23 27 13 27 13 24 Z" {S}/>',
}

def avatar(f):
    back, front = hair(f["hair_style"], f["hair"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="{f["name"]}"><defs><clipPath id="c-{f["id"]}-{{u}}"><circle cx="100" cy="100" r="100"/></clipPath></defs>'
            f'<g clip-path="url(#c-{f["id"]}-{{u}})"><rect width="200" height="200" fill="{f["bg"]}"/><circle cx="160" cy="40" r="46" fill="#fff" opacity=".25"/>{back}'
            f'<path d="M30 200 C30 160 56 142 90 142 C124 142 150 160 150 200 Z" fill="{f["cloth"]}"/>'
            f'<rect x="80" y="112" width="20" height="26" rx="8" fill="{f["skin"]}"/><path d="M78 138 Q90 150 102 138" stroke="{f["skin"]}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="90" cy="86" rx="34" ry="38" fill="{f["skin"]}"/><ellipse cx="56" cy="90" rx="5" ry="7" fill="{f["skin"]}"/><ellipse cx="124" cy="90" rx="5" ry="7" fill="{f["skin"]}"/>{front}'
            '<ellipse cx="77" cy="90" rx="3.2" ry="4" fill="#2B1D16"/><ellipse cx="103" cy="90" rx="3.2" ry="4" fill="#2B1D16"/>'
            '<path d="M70 80 Q77 76 84 80" stroke="#2B1D16" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/><path d="M96 80 Q103 76 110 80" stroke="#2B1D16" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>'
            '<circle cx="70" cy="102" r="6" fill="#E8735A" opacity=".25"/><circle cx="110" cy="102" r="6" fill="#E8735A" opacity=".25"/><path d="M80 106 Q90 115 100 106" stroke="#7A2E22" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
            f'{dog(f["dog"])}</g><g transform="translate(18 18)"><circle cx="18" cy="18" r="18" fill="#FFFCF3" stroke="#2B3A2F" stroke-width="2"/>{ICONS[f["icon"]]}</g></svg>')

TEAM = [
 dict(id="bandenchefin", name="Bandenchefin", rolle="Leitung", agent="Claude-Sitzung", gruppe="chef", icon="kompass",
      merk="Nimmt deine Wünsche für den Verein an und holt die Richtigen dazu.", ruf="„Derner los: Weihnachtsfeier.“", hund="Schnauzer",
      bg="#DCE8D4", cloth="#1F4D3A", skin="#EBC9A6", hair="#6B4A2E", hair_style="short",
      dog=dict(type="floppy", fur="#9AA0A4", ear="#7D8387", muz="#D9DCDE", extra='<path d="M132 168 Q146 186 160 168 Q146 174 132 168 Z" fill="#D9DCDE"/><path d="M130 134 Q136 128 142 134 M150 134 Q156 128 162 134" stroke="#D9DCDE" stroke-width="5" fill="none" stroke-linecap="round"/>')),
 dict(id="platzhirschin", name="Platzhirschin", rolle="Social Media", agent="derner-social", gruppe="planen", icon="stern",
      merk="Macht, dass der Verein auf Instagram und Facebook nach Verein klingt.", ruf="„Platzhirschin, schreib 'n Post zum Freilauf am Mittwoch.“", hund="Golden Retriever",
      bg="#F3E3B8", cloth="#2F6B4F", skin="#F0CBA5", hair="#B4552E", hair_style="long",
      dog=dict(type="floppy", fur="#E3A653", ear="#C4853A", muz="#F5C98A")),
 dict(id="schnupperschnauze", name="Schnupperschnauze", rolle="Mitglieder &amp; Anfragen", agent="derner-mitglieder", gruppe="input", icon="pfote",
      merk="Sorgt dafür, dass Neue gut ankommen – von der ersten Frage bis zum Probetraining.", ruf="„Schnupperschnauze, wie antworten wir auf 'ne Probetraining-Anfrage?“", hund="Beagle",
      bg="#E6D9F0", cloth="#8A4F7D", skin="#D9A07A", hair="#2A1A12", hair_style="curly",
      dog=dict(type="floppy", fur="#F2E6D0", ear="#8E4F22", muz="#FFFFFF", extra='<ellipse cx="146" cy="134" rx="14" ry="9" fill="#B9783E"/>')),
 dict(id="rennpfote", name="Rennpfote", rolle="Events", agent="derner-events", gruppe="input", icon="flagge",
      merk="Plant Weihnachtsfeier, Hunderennen und Tag der offenen Tür bis zum Helferplan.", ruf="„Rennpfote, plan die Weihnachtsfeier.“", hund="Border Collie",
      bg="#F6D2C4", cloth="#C2573F", skin="#E8B98F", hair="#3B2A20", hair_style="bun",
      dog=dict(type="pointed", fur="#2B2B2B", ear="#2B2B2B", muz="#FFFFFF", extra='<path d="M142 125 L150 125 L154 156 L138 156 Z" fill="#fff"/>')),
 dict(id="bandenbuero", name="Bandenbüro", rolle="Büro &amp; Ehrenamt", agent="derner-buero", gruppe="planen", icon="ordner",
      merk="Hält den Zettelkram zusammen: Rundmails, Aushänge, Arbeitsdienste.", ruf="„Bandenbüro, mach 'nen Aushang für den Arbeitsdienst.“", hund="Dackel",
      bg="#D6E2EC", cloth="#4A5C8C", skin="#F5D3B8", hair="#8D9296", hair_style="short",
      dog=dict(type="floppy", fur="#7A4A26", ear="#5E3719", muz="#A36A38")),
 dict(id="revierlaeuferin", name="Revierläuferin", rolle="Partner &amp; Website", agent="derner-partner-web", gruppe="input", icon="kette",
      merk="Läuft das Revier ab: Wer in Scharnhorst kann helfen, und findet man uns online?", ruf="„Revierläuferin, welche Tierärzte in Scharnhorst könnten wir anfragen?“", hund="Husky",
      bg="#D8E7B8", cloth="#2D4A5C", skin="#C98E66", hair="#1F1A17", hair_style="long",
      dog=dict(type="pointed", fur="#8C949C", ear="#8C949C", muz="#FFFFFF", extra='<path d="M122 154 Q132 138 142 148 L144 174 Q128 172 122 154 Z" fill="#fff"/><path d="M170 154 Q160 138 150 148 L148 174 Q164 172 170 154 Z" fill="#fff"/>')),
 dict(id="postschnauze", name="Postschnauze", rolle="Newsletter", agent="derner-newsletter", gruppe="planen", icon="brief",
      merk="Schreibt die Schnauzenpost – wie 'ne Mail vom Verein, kein Werbeprospekt.", ruf="„Postschnauze, schreib die Schnauzenpost für Dezember.“", hund="Cockerspaniel",
      bg="#F9D9A6", cloth="#E05A47", skin="#F7D6BF", hair="#E3C27A", hair_style="short",
      dog=dict(type="floppy", fur="#B5552B", ear="#8E3F1E", muz="#C7673D")),
 dict(id="bastelschnauze", name="Bastelschnauze", rolle="Grafik &amp; Umsetzung", agent="derner-umsetzung", gruppe="fertig", icon="pinsel",
      merk="Baut Aushänge, Flyer und Seiten in Creme und Dunkelgrün.", ruf="„Bastelschnauze, bau 'nen Flyer für den Schnuppertag.“", hund="Labrador",
      bg="#F3D27A", cloth="#7C5235", skin="#C98E66", hair="#1F1A17", hair_style="bun",
      dog=dict(type="floppy", fur="#2A2522", ear="#3A332F", muz="#3C3734")),
 dict(id="platzwart", name="Platzwart", rolle="Foto-Auswahl &amp; Gegenlesen", agent="derner-foto-pruefer", gruppe="pruefen", icon="schild",
      merk="Der letzte Blick, bevor du freigibst. Meldet nur, ändert nix.", ruf="„Platzwart, les den Post ma gegen.“", hund="Deutscher Schäferhund",
      bg="#CFD8DC", cloth="#1F4D3A", skin="#EBC9A6", hair="#8D9296", hair_style="short",
      dog=dict(type="pointed", fur="#3A2A20", ear="#3A2A20", muz="#C9975A", extra='<path d="M126 140 Q146 118 166 140 Q146 132 126 140 Z" fill="#C9975A"/>')),
]
HELFER = [("Witterung", "Trends &amp; Formate"), ("Nasenarbeit", "Zahlen &amp; Analyse"), ("Schnittpfote", "aufwendigere Videos"), ("Macherpfote", "nur noch im Notfall")]

def av(f, u): return '<div class="av">' + avatar(f).replace("{u}", u) + '</div>'
def chip(f): return f'<figure class="chip">{av(f,"f")}<figcaption><b>{f["name"]}</b><span>{f["rolle"]}</span></figcaption></figure>'
def stage(lbl, g): return f'<div class="stage"><div class="stage__lbl">{lbl}</div><div class="stage__chips">' + "".join(chip(f) for f in TEAM if f["gruppe"] == g) + '</div></div>'
cards = "".join(f'<article class="card" id="{f["id"]}"><div class="av av--l">{avatar(f).replace("{u}","k")}</div><div class="card__body"><h3>{f["name"]}</h3><p class="rolle">{f["rolle"]} <span class="agent">· {f["agent"]}</span></p><p class="merk">{f["merk"]}</p><p class="ruf">{f["ruf"]}</p><p class="hund">Hund: {f["hund"]}</p></div></article>' for f in TEAM)
top = "".join(av(f, "t") for f in TEAM)
helfer = "".join(f'<li><b>{n}</b> <span>{r}</span></li>' for n, r in HELFER)

PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Das Derner-Rudel</title>
<style>
:root{--bg:#F6EFDD;--surface:#FFFBF0;--ink:#1D2B22;--muted:#5C6B5F;--line:#DDD2B6;--green:#1F4D3A;--gold:#B98A2E;color-scheme:light}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left,0px)) 56px;display:flex;flex-direction:column;gap:52px}
h1,h2,h3{margin:0;line-height:1.1;text-wrap:balance;font-family:Georgia,"Times New Roman",serif;color:var(--green)}
h1{font-size:clamp(2.1rem,6vw,3.4rem)} h1 em{font-style:normal;color:var(--gold)} h2{font-size:clamp(1.5rem,3.6vw,2rem)}
.eyebrow{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:0 0 8px}
.lead{max-width:60ch;color:var(--muted);margin:12px 0 0;font-size:1.05rem}
.av svg{display:block;width:100%;height:auto}
.rudel{display:flex;flex-wrap:wrap;margin-top:26px;padding-left:10px}
.rudel .av{width:clamp(52px,10vw,84px);margin-left:-10px;border-radius:50%;box-shadow:0 0 0 4px var(--bg)}
.flow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));margin-top:22px}
.stage{display:flex;flex-direction:column;align-items:center;gap:14px;position:relative;padding:0 8px}
.stage::before{content:"";position:absolute;top:44px;left:0;right:0;height:3px;background:linear-gradient(90deg,#8FB395,var(--gold));opacity:.55}
.stage:first-child::before{left:50%}.stage:last-child::before{right:50%}
.stage__lbl{order:-1;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted);text-align:center}
.stage__chips{display:flex;flex-direction:column;gap:14px;align-items:center;position:relative;z-index:1}
.chip{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}
.chip .av{width:72px;border-radius:50%;box-shadow:0 0 0 4px var(--bg)}
.chip figcaption b{display:block;font-family:Georgia,serif;font-size:1rem;color:var(--green)} .chip figcaption span{font-size:.82rem;color:var(--muted)}
.entwurf{width:72px;height:96px;border-radius:14px;border:2px solid var(--line);background:var(--surface);display:grid;place-items:center;position:relative}
.entwurf::after{content:"ENTWURF";position:absolute;bottom:10px;left:50%;transform:translateX(-50%) rotate(-8deg);background:#F0D78C;color:#2A2412;font-weight:800;font-size:.66rem;letter-spacing:.08em;padding:3px 7px;border-radius:5px;border:2px solid #2A2412}
.entwurf i{display:block;width:44px;height:30px;border-radius:6px;background:linear-gradient(135deg,var(--green),var(--gold));margin-bottom:22px}
@media (max-width:700px){.flow{grid-template-columns:1fr;gap:22px}.stage{flex-direction:row;align-items:center;padding:0}.stage::before{display:none}.stage__lbl{order:0;width:84px;flex:none;text-align:left}.stage__chips{flex-direction:row;flex-wrap:wrap;justify-content:flex-start}.chip .av{width:60px}}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;margin-top:22px}@media (min-width:1000px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:14px}
.av--l{width:112px;border-radius:50%} .card__body{display:flex;flex-direction:column;gap:6px;min-width:0} .card p{margin:0}
.rolle{color:var(--green);font-weight:700} .agent{color:var(--muted);font-weight:400;font-size:.85rem}
.ruf{font-style:italic;color:var(--muted)} .hund{font-size:.85rem;color:var(--muted)}
.box{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin-top:18px}
.box ul{margin:8px 0 0;padding-left:18px} .box li span{color:var(--muted)}
footer{color:var(--muted);font-size:.85rem;max-width:62ch}
</style></head><body><div class="wrap">
<header>
 <p class="eyebrow">Derner Schnauzenbande · dein Vereinsteam</p>
 <h1>Das Derner-<em>Rudel</em></h1>
 <p class="lead">Neun Figuren, jede mit ihrem Hund – eigene Stimme, eigene Kanäle, nix mit Pottpic gemischt. Ruf sie beim Spitznamen („Frag ma Schnupperschnauze …“) oder sag einfach „Derner los …“, dann holt die Bandenchefin die Richtigen dazu.</p>
 <div class="rudel" aria-hidden="true">@@TOP@@</div>
</header>
<section aria-labelledby="h-ablauf">
 <p class="eyebrow">So arbeiten sie zusammen</p>
 <h2 id="h-ablauf">Von der Idee zum Entwurf für dich</h2>
 <div class="flow">
  @@STAGES@@
  <div class="stage"><div class="stage__lbl">Für dich</div><div class="stage__chips"><div class="entwurf" role="img" aria-label="Entwurf zum Freigeben"><i></i></div><figure class="chip"><figcaption><b>Du gibst frei</b><span>Nix geht ohne dein Okay raus</span></figcaption></figure></div></div>
 </div>
</section>
<section aria-labelledby="h-team">
 <p class="eyebrow">Steckbriefe</p>
 <h2 id="h-team">Wer macht was</h2>
 <div class="grid">@@CARDS@@</div>
 <div class="box"><h3>Hilft aus (Pottpic-Kolleginnen)</h3><ul>@@HELFER@@</ul><p style="margin:10px 0 0;color:var(--muted);font-size:.9rem">Wer für den Verein hilft, hält sich an die Vereinsregeln: Vereinsstimme, kein #esbeginntmiteinemwau, Ablage unter derner-team/.</p></div>
</section>
<footer>Die Gesichter sind gezeichnet, keine echten Personen. Agent-Namen in Grau, falls du lieber so rufst. Gebaut mit <code>rudel_bauen.py</code>.</footer>
</div></body></html>
"""
out = (PAGE.replace("@@TOP@@", top)
       .replace("@@STAGES@@", stage("Input", "input") + stage("Planen", "planen") + stage("Fertig machen", "fertig") + stage("Gegenlesen", "pruefen"))
       .replace("@@CARDS@@", cards).replace("@@HELFER@@", helfer))
p = pathlib.Path(__file__).with_name("rudel.html"); p.write_text(out, encoding="utf-8"); print("ok", p, len(out))
