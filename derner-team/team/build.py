# Baut team/leitwolf.html aus leitwolf.src.html + Vereinsregeln + Postplan (python3 team/build.py, im Ordner derner-team)
import base64, json, re, html, pathlib, datetime
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/'team/leitwolf.src.html').read_text()
logo = 'data:image/webp;base64,' + base64.b64encode((root/'team/logo-small.webp').read_bytes()).decode()
ctx = {k: (root/p).read_text() for k, p in {
    'kontext': 'CLAUDE.md',
    'texter': '.claude/agents/derner-social-texter.md',
    'video': '.claude/agents/derner-video-editor.md'}.items()}
ctx_js = json.dumps(ctx, ensure_ascii=False).replace('</', '<\\/')
rows = []
for line in (root/'ergebnisse/postplan.md').read_text().splitlines():
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) != 5 or cells[0] in ('Datum', '---') or set(cells[0]) <= set('-'):
        continue
    datum, kanal, was, _, status = cells
    cls = 'frei' if 'freigegeben' in status else 'entwurf' if 'Entwurf' in status else 'todo'
    label = re.sub(r'^[^\wÄÖÜäöü]+', '', status)
    was = re.sub(r'`', '', was)
    rows.append(f'<li><span class="d">{html.escape(datum)}</span><span class="w">{html.escape(was)}'
                f'<span class="k">{html.escape(kanal)}</span></span><span class="pill {cls}">{html.escape(label)}</span></li>')
stand = datetime.date.today().strftime('%d.%m.%Y')
out = (src.replace('__LOGO__', logo).replace('__CTX__', ctx_js)
          .replace('__PLAN__', '\n  '.join(rows)).replace('__STAND__', stand))
(root/'team/leitwolf.html').write_text(out)
print(len(rows), 'Termine,', len(out), 'Bytes')
