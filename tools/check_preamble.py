#!/usr/bin/env python3
"""Gate for src/assets/*.svg: shared <style> preamble untouched, bodies valid and self-contained.

Usage: python3 tools/check_preamble.py [assets_dir] [variants.json]
Exit 1 on any violation.

Rules enforced:
  1. preamble (everything up to and including </style>) hash must equal the snapshot hash for this file
  2. body (between </style> and </svg>) parses as XML inside the <svg> root
  3. body introduces no <style>, no <script>, no new CSS selectors
  4. every class used in the body is defined in this file's own preamble
  5. every var(--x) used in the body is defined in this file's own preamble
"""
import sys, os, re, glob, json, hashlib
import xml.dom.minidom as minidom

assets = sys.argv[1] if len(sys.argv) > 1 else 'src/assets'
snap_path = sys.argv[2] if len(sys.argv) > 2 else '/tmp/cardaudit/preamble-variants.json'
snap = json.load(open(snap_path))
owner_of = {f: vid for vid, fs in snap.items() for f in fs}
bad = 0
warn = 0

def selectors(pre):
    """class names defined by any selector in the preamble, grouped selectors included."""
    out = set()
    for m in re.finditer(r'([^{}]+)\{', pre):
        sel = m.group(1)
        if sel.strip().startswith('@'):
            continue
        for part in sel.split(','):
            for c in re.findall(r'\.([a-zA-Z0-9_-]+)', part):
                out.add(c)
    return out

for f in sorted(glob.glob(os.path.join(assets, '*.svg'))):
    name = os.path.basename(f)
    s = open(f).read()
    if '</style>' not in s or '</svg>' not in s:
        print('FAIL', name, 'missing </style> or </svg>'); bad += 1; continue
    cut = s.index('</style>') + len('</style>')
    pre, body = s[:cut], s[cut:s.index('</svg>')]
    owner = owner_of.get(name)
    if owner is None:
        print('FAIL', name, 'not in preamble snapshot'); bad += 1
    elif hashlib.sha256(pre.encode()).hexdigest()[:8] != owner:
        print('FAIL', name, 'style preamble was modified'); bad += 1
    b = body.strip()
    if not b:
        print('FAIL', name, 'empty body'); bad += 1; continue
    if re.search(r'<style|<script|@media|@keyframes', b):
        print('FAIL', name, 'body contains style/script'); bad += 1
    try:
        minidom.parseString(s)
    except Exception as e:
        print('FAIL', name, 'not well-formed XML:', e); bad += 1; continue
    defined_cls = selectors(pre)
    defined_var = set(re.findall(r'--([a-zA-Z0-9_-]+)\s*:', pre))
    used_cls = set()
    for m in re.finditer(r'class="([^"]+)"', b):
        used_cls.update(m.group(1).split())
    used_var = set(re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', b))
    miss_cls = sorted(used_cls - defined_cls)
    miss_var = sorted(used_var - defined_var)
    if miss_cls:
        print('FAIL', name, 'uses classes not defined in its preamble:', miss_cls); bad += 1
    if miss_var:
        print('FAIL', name, 'uses vars not defined in its preamble:', miss_var); bad += 1
    if '<g' not in b:
        print('WARN', name, 'body has no <g> wrapper'); warn += 1
    if len(b) < 120:
        print('WARN', name, f'body suspiciously small ({len(b)} bytes)'); warn += 1

print(f'check_preamble: bad = {bad}, warn = {warn}')
sys.exit(1 if bad else 0)
