#!/usr/bin/env python3
"""Render one contact sheet per line of a group file (comma-separated asset names).

Usage: python3 tools/render_groups.py <assets_dir> <group_file> <out_dir> [cell]
Each line: sheetname: name1,name2,...   (leading '# name' comment allowed)
"""
import sys, os, subprocess, html

assets, groupfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
CELL = int(sys.argv[4]) if len(sys.argv) > 4 else 300
os.makedirs(out, exist_ok=True)
work = os.path.join(out, '_html')
os.makedirs(work, exist_ok=True)
index = {}

for line in open(groupfile):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    title, names = line.split(':', 1)
    names = [n.strip() for n in names.split(',') if n.strip()]
    cols = min(5, max(3, -(-len(names) // 4)))
    rows = -(-len(names) // cols)
    cells = ''
    for n in names:
        p = os.path.abspath(os.path.join(assets, n + '.svg'))
        cells += f'<figure><img src="file://{p}"><figcaption>{html.escape(n)}</figcaption></figure>'
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font:600 15px system-ui}}
h2{{font:700 20px system-ui;margin:6px 8px}}
.grid{{display:grid;grid-template-columns:repeat({cols},{CELL}px);gap:0}}
figure{{margin:0;padding:4px;width:{CELL}px;height:{CELL}px;display:flex;flex-direction:column;align-items:center;justify-content:center;outline:1px solid #ddd}}
img{{width:{CELL - 44}px;height:{CELL - 44}px;object-fit:contain}}
figcaption{{font-size:14px;color:#333}}
</style></head><body><h2>{html.escape(title)}</h2><div class="grid">{cells}</div></body></html>'''
    hp = os.path.join(work, f'{title}.html')
    open(hp, 'w').write(page)
    png = os.path.join(out, f'{title}.png')
    subprocess.run(['/usr/bin/chromium', '--headless=new', '--no-sandbox', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--default-background-color=FFFFFFFF',
                    f'--window-size={cols * CELL},{rows * CELL + 36}',
                    f'--screenshot={png}', f'file://{hp}'], check=True, capture_output=True)
    index[title] = names
    print('wrote', png, len(names))
