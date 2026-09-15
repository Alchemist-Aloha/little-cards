#!/usr/bin/env python3
"""Render named assets to one PNG you can look at (/tmp/show.png by default).

Usage: python3 tools/show.py cat dog bunny            # one big row
       python3 tools/show.py --grid a b c d e f        # wrap after 4
       python3 tools/show.py -o /tmp/x.png --size 420 a b
"""
import subprocess, html, sys, os, tempfile

args = sys.argv[1:]
out = '/tmp/show.png'
size = 380
grid = False
names = []
i = 0
while i < len(args):
    a = args[i]
    if a == '-o': out = args[i + 1]; i += 2
    elif a == '--size': size = int(args[i + 1]); i += 2
    elif a == '--grid': grid = True; i += 1
    else: names.append(a); i += 1

if not names:
    sys.exit('usage: show.py [-o out.png] [--size px] [--grid] name [name ...]')

assets = '/home/likun/toddler-cards/src/assets'
cells = ''.join(
    f'<figure><img src="file://{assets}/{n}.svg"><figcaption>{html.escape(n)}</figcaption></figure>'
    for n in names)
cols = 4 if grid else len(names)
rows = -(-len(names) / cols)
pad = 8
w = cols * (size + pad)
h = rows * (size + 30) + pad
page = (f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff;'
        f'font:600 16px system-ui">'
        f'<div style="display:flex;flex-wrap:wrap;gap:{pad}px">{cells}</div><style>'
        f'figure{{margin:0;width:{size}px;text-align:center;outline:1px solid #e5e5e5}}'
        f'img{{width:{size}px;height:{size}px}}figcaption{{font-size:15px;color:#333}}</style>')
html_path = out.replace('.png', '.html')
open(html_path, 'w').write(page)
profile = tempfile.mkdtemp(prefix='cr-profile-')
subprocess.run(['/usr/bin/chromium', '--headless=new', '--no-sandbox', '--hide-scrollbars',
                f'--user-data-dir={profile}',
                '--force-device-scale-factor=1', '--default-background-color=FFFFFFFF',
                '--run-all-compositor-stages-before-draw', '--virtual-time-budget=15000',
                f'--window-size={w},{h}', f'--screenshot={out}', f'file://{html_path}'],
               check=True, capture_output=True)
print(out, f'{w}x{h}', len(names), 'icons')
