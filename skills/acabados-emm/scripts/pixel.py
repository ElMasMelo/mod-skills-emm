"""Pixel art desde una cuadrícula de texto (íconos 16x16, logo 128x128).

Formato del .txt:
  B #5e3a63        <- una letra/símbolo por color (hex RGB o RGBA)
  L #b48fb5
  ---
  ....BBBB....     <- filas; '.' = transparente; todas del mismo ancho
Uso:
  python pixel.py <spec.txt> <salida.png> [--scale N] [--bg #RRGGBB]
  python pixel.py --selftest
Logo: dibuja 32x32 y usa --scale 4 (128x128), o 16x16 con --scale 8.
"""
import os, sys
from PIL import Image


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in range(0, len(h), 2)) + ((255,) if len(h) == 6 else ())


def parse(text):
    head, rows = text.split('---', 1)
    pal = {l.split()[0]: hexc(l.split()[1]) for l in head.strip().splitlines() if l.strip()}
    rows = [r.rstrip() for r in rows.strip().splitlines() if r.strip()]
    assert len({len(r) for r in rows}) == 1, 'todas las filas deben tener el mismo ancho'
    bad = {c for r in rows for c in r} - set(pal) - {'.'}
    assert not bad, f'símbolos sin color: {bad}'
    return pal, rows


def render(text, scale=1, bg=None):
    pal, rows = parse(text)
    im = Image.new('RGBA', (len(rows[0]), len(rows)), hexc(bg) if bg else (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.': im.putpixel((x, y), pal[c])
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST) if scale > 1 else im


def selftest():
    im = render('A #ff0000\nB #00ff0080\n---\nA.\n.B', scale=4)
    assert im.size == (8, 8) and im.getpixel((0, 0)) == (255, 0, 0, 255) and im.getpixel((7, 7)) == (0, 255, 0, 128)
    assert im.getpixel((7, 0))[3] == 0
    try: parse('A #000000\n---\nAA\nA'); raise SystemExit('debió fallar')
    except AssertionError: pass
    print('selftest OK')


def main(a):
    if not a or a[0] in ('-h', '--help'): print(__doc__); return
    if a[0] == '--selftest': return selftest()
    opt = dict(zip(a[2::2], a[3::2]))
    with open(a[0], encoding='utf-8') as f:
        im = render(f.read(), int(opt.get('--scale', 1)), opt.get('--bg'))
    os.makedirs(os.path.dirname(os.path.abspath(a[1])), exist_ok=True); im.save(a[1]); print(a[1], im.size)


if __name__ == '__main__':
    main(sys.argv[1:])
