#!/usr/bin/env python3
"""Render SVG assets into labelled contact sheets (PNG) for visual audit.

Usage: python3 tools/render_sheet.py <assets_dir> <out_dir> [cols] [rows] [start] [end]
Writes out_dir/sheet-XX.png plus out_dir/index.json mapping sheet -> names in order.
"""
import sys, os, json, subprocess, glob, shutil, html

assets = sys.argv[1]
out = sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
rows = int(sys.argv[4]) if len(sys.argv) > 4 else 5
start = int(sys.argv[5]) if len(sys.argv) > 5 else 0
end = int(sys.argv[6]) if len(sys.argv) > 6 else 10**9

files = sorted(glob.glob(os.path.join(assets, '*.svg')))[start:end]
os.makedirs(out, exist_ok=True)
CELL = 240
per = cols * rows
index = {}
work = os.path.join(out, '_html')
os.makedirs(work, exist_ok=True)

for si in range(0, len(files), per):
    chunk = files[si:si + per]
    cells = ''.join(
        f'<figure><img src="file://{os.path.abspath(f)}"><figcaption>{html.escape(os.path.basename(f)[:-4])}</figcaption></figure>'
        for f in chunk)
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font:600 15px system-ui}}
.grid{{display:grid;grid-template-columns:repeat({cols},{CELL}px);gap:0}}
figure{{margin:0;padding:4px;width:{CELL}px;height:{CELL}px;display:flex;flex-direction:column;align-items:center;justify-content:center;outline:1px solid #ddd}}
img{{width:{CELL - 40}px;height:{CELL - 40}px;object-fit:contain}}
figcaption{{font-size:13px;color:#333;margin-top:2px}}
</style></head><body><div class="grid">{cells}</div></body></html>'''
    p = os.path.join(work, f'p{si:04d}.html')
    open(p, 'w').write(page)
    png = os.path.join(out, f'sheet-{si // per:02d}.png')
    subprocess.run(['/usr/bin/chromium', '--headless=new', '--no-sandbox', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--default-background-color=FFFFFFFF',
                    f'--window-size={cols * CELL},{rows * CELL}',
                    f'--screenshot={png}', f'file://{p}'],
                   check=True, capture_output=True)
    index[f'sheet-{si // per:02d}.png'] = [os.path.basename(f)[:-4] for f in chunk]
    print('wrote', png, '->', len(chunk), 'icons')

json.dump(index, open(os.path.join(out, 'index.json'), 'w'), indent=1)
print('sheets:', len(index))
