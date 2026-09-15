#!/usr/bin/env python3
"""Asset gate for src/assets/*.svg.

Every card is a standalone 200x200 SVG that shares a big <style> preamble with its siblings and
differs only in the art body between </style> and </svg>. This gate protects that structure:

  1. the <style> preamble of each file still hashes to its frozen baseline value
     (scripts/preamble-baseline.json) — so nothing silently edits the shared CSS;
  2. the body parses as XML inside the <svg> root (catches duplicate attributes, unclosed tags);
  3. the body introduces no <style>/<script>/@media of its own;
  4. every class="..." used in the body is defined by a selector in that file's own preamble;
  5. every var(--x) used in the body is defined in that file's own preamble.

Rules 4 and 5 matter because an undefined class/var paints SOLID BLACK (no fill specified): a bug
class that is invisible in markup review and obvious in a render. Five instances of it were found
and fixed in this deck — book bookmark, piano leg line, donut hole, violin f-holes, giraffe legs.

Usage: python3 tools/check_preamble.py [assets_dir] [baseline.json]
Exit status 1 if any file fails.
"""
import sys, os, re, glob, json, hashlib
import xml.dom.minidom as minidom

DEFAULT_ASSETS = 'src/assets'
DEFAULT_BASELINE = 'scripts/preamble-baseline.json'


def defined_classes(preamble):
    """Class names declared by any selector, grouped selectors included (.a, .b { … })."""
    out = set()
    for m in re.finditer(r'([^{}]+)\{', preamble):
        selector = m.group(1)
        if selector.strip().startswith('@'):
            continue
        for part in selector.split(','):
            out.update(re.findall(r'\.([a-zA-Z0-9_-]+)', part))
    return out


def main(assets, baseline_path):
    baseline = json.load(open(baseline_path))
    bad = warn = 0
    for path in sorted(glob.glob(os.path.join(assets, '*.svg'))):
        name = os.path.basename(path)
        svg = open(path).read()
        if '</style>' not in svg or '</svg>' not in svg:
            print('FAIL', name, 'missing </style> or </svg>'); bad += 1; continue
        cut = svg.index('</style>') + len('</style>')
        preamble, body = svg[:cut], svg[cut:svg.index('</svg>')]
        expected = baseline.get(name)
        if expected is None:
            print('FAIL', name, 'not in the preamble baseline'); bad += 1
        elif hashlib.sha256(preamble.encode()).hexdigest() != expected:
            print('FAIL', name, 'shared <style> preamble was modified'); bad += 1
        text = body.strip()
        if not text:
            print('FAIL', name, 'empty art body'); bad += 1; continue
        if re.search(r'<style|<script|@media|@keyframes', text):
            print('FAIL', name, 'body defines CSS of its own'); bad += 1
        try:
            minidom.parseString(svg)
        except Exception as exc:
            print('FAIL', name, 'not well-formed XML:', exc); bad += 1; continue
        used_classes = set()
        for m in re.finditer(r'class="([^"]+)"', text):
            used_classes.update(m.group(1).split())
        missing_classes = sorted(used_classes - defined_classes(preamble))
        missing_vars = sorted(set(re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', text))
                              - set(re.findall(r'--([a-zA-Z0-9_-]+)\s*:', preamble)))
        if missing_classes:
            print('FAIL', name, 'classes not defined in its preamble (paint black):', missing_classes)
            bad += 1
        if missing_vars:
            print('FAIL', name, 'vars not defined in its preamble (paint black):', missing_vars)
            bad += 1
        if len(text) < 200:
            print('WARN', name, f'art body is only {len(text)} bytes'); warn += 1
    print(f'check_preamble: {len(baseline)} files checked, bad = {bad}, warn = {warn}')
    return 1 if bad else 0


if __name__ == '__main__':
    assets = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ASSETS
    baseline = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BASELINE
    sys.exit(main(assets, baseline))
