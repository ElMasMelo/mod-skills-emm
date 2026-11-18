"""Síntesis local de efectos de sonido estilo Minecraft (numpy + scipy + ffmpeg).

Uso:
  python sfx.py list
  python sfx.py <preset> <salida.ogg> [--pitch 1.0] [--dur 1.0] [--variants N] [--seed S]
  python sfx.py --selftest
--dur escala la duración base del preset. --variants N escribe <salida>1.ogg..N.ogg con pitch y semilla distintos
(Minecraft elige una al azar). Salida: .ogg mono 44.1 kHz (libvorbis), pico a -1 dBFS.
"""
import os, subprocess, sys, tempfile
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100


def t(d): return np.arange(int(SR * d)) / SR
def env(d, a=0.005, k=6.0): x = t(d); return np.minimum(x / a, 1) * np.exp(-k * x / d)
def noise(d, r): return r.uniform(-1, 1, len(t(d)))
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x)
def sweep(f0, f1, d): x = t(d); return np.sin(2 * np.pi * np.cumsum(np.geomspace(f0, f1, len(x))) / SR)
def pad(x, d): return np.pad(x, (0, max(0, int(SR * d) - len(x))))[:int(SR * d)]


def _hoot(d, r):
    x = t(d); f = 380 * np.exp(-0.4 * x / d) * (1 + 0.01 * np.sin(2 * np.pi * 6 * x))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, 0.04, 3)


PRESETS = {  # nombre: (duración base s, función(d, rng), descripción)
    'hit':     (0.25, lambda d, r: lp(noise(d, r), 900) * env(d) + 0.6 * sweep(140, 60, d) * env(d), 'golpe sordo'),
    'step':    (0.09, lambda d, r: bp(noise(d, r), 300, 2500) * env(d, 0.002, 9), 'paso / pisada'),
    'dig':     (0.35, lambda d, r: sum(np.roll(pad(bp(noise(0.07, r), 200, 1500) * env(0.07, 0.002, 7), d), int(SR * d * i / 3)) for i in range(3)), 'escarbar / cepillar'),
    'click':   (0.04, lambda d, r: np.sin(2 * np.pi * 1800 * t(d)) * env(d, 0.001, 10), 'clic de interfaz'),
    'pop':     (0.09, lambda d, r: sweep(400, 950, d) * env(d, 0.002, 6), 'pop / recoger'),
    'pickup':  (0.28, lambda d, r: np.concatenate([np.sin(2 * np.pi * 988 * t(d / 2)) * env(d / 2), np.sin(2 * np.pi * 1319 * t(d / 2)) * env(d / 2)]), 'objeto obtenido'),
    'whoosh':  (0.5,  lambda d, r: bp(noise(d, r), 400, 3000) * np.sin(np.pi * t(d) / d) ** 2, 'movimiento rápido / lanzar'),
    'magic':   (0.7,  lambda d, r: sum(np.sin(2 * np.pi * f * t(d)) * np.roll(env(d, 0.01, 4), int(SR * d * i / 8)) for i, f in enumerate([523, 659, 784, 1047])) / 2 + 0.15 * hp(noise(d, r), 6000) * env(d, 0.01, 3), 'hechizo / brillo'),
    'growl':   (0.9,  lambda d, r: (lp(noise(d, r), 380) * 2 + 0.5 * np.sign(np.sin(2 * np.pi * 70 * t(d)))) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * t(d))) * env(d, 0.08, 2.5), 'gruñido grande (oso, golem)'),
    'hiss':    (0.6,  lambda d, r: hp(noise(d, r), 2500) * env(d, 0.05, 3), 'siseo (escorpión, serpiente)'),
    'hoot':    (0.9,  lambda d, r: np.concatenate([_hoot(d * 0.4, r), np.zeros(int(SR * d * 0.15)), _hoot(d * 0.45, r)]), 'ulular (búho)'),
    'squeak':  (0.16, lambda d, r: sweep(1800, 3000, d) * (1 + 0.2 * np.sin(2 * np.pi * 30 * t(d))) * env(d, 0.01, 4), 'chillido pequeño (goblin, roedor)'),
    'hurt':    (0.22, lambda d, r: np.sign(sweep(320, 150, d)) * 0.5 * env(d, 0.003, 4), 'mob herido'),
    'death':   (0.8,  lambda d, r: (np.sign(sweep(300, 55, d)) * 0.5 + 0.3 * lp(noise(d, r), 600)) * env(d, 0.01, 3), 'muerte de mob'),
    'stomp':   (0.6,  lambda d, r: (np.sin(2 * np.pi * 48 * t(d)) + 1.5 * lp(noise(d, r), 250)) * env(d, 0.003, 5), 'pisotón / impacto pesado'),
    'shoot':   (0.2,  lambda d, r: hp(noise(d, r), 1500) * env(d, 0.002, 7) + 0.4 * sweep(900, 300, d) * env(d), 'disparo / proyectil'),
    'shell':   (0.18, lambda d, r: bp(noise(d, r), 1500, 5000) * env(d, 0.001, 8) + 0.3 * np.sin(2 * np.pi * 2400 * t(d)) * env(d, 0.001, 12), 'caparazón / cerámica'),
}


def render(name, pitch=1.0, dur=1.0, seed=0):
    base, fn, _ = PRESETS[name]
    x = np.asarray(fn(base * dur, np.random.default_rng(seed)), float)
    if pitch != 1.0:  # mismo efecto que el pitch de Minecraft: más agudo = más corto
        x = np.interp(np.arange(0, len(x), pitch), np.arange(len(x)), x)
    n = min(len(x), int(SR * 0.005)); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    return x / (np.max(np.abs(x)) or 1) * 0.89


def write_ogg(x, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'a.wav'); wavfile.write(w, SR, (x * 32767).astype(np.int16))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', w, '-ac', '1', '-ar', str(SR), '-c:a', 'libvorbis', '-q:a', '5', out], check=True)


def selftest():
    for k in PRESETS:
        x = render(k, seed=1)
        assert np.all(np.isfinite(x)) and 0.5 < np.max(np.abs(x)) <= 0.9, k
        assert len(render(k, pitch=2.0)) < len(x), k
    with tempfile.TemporaryDirectory() as d:
        o = os.path.join(d, 't.ogg'); write_ogg(render('hit'), o); assert os.path.getsize(o) > 500
    print(f'selftest OK ({len(PRESETS)} presets)')


def main(a):
    if not a or a[0] in ('list', '-h', '--help'):
        print(__doc__); [print(f'  {k:8} {v[0]:.2f}s  {v[2]}') for k, v in PRESETS.items()]; return
    if a[0] == '--selftest': return selftest()
    name, out, opt = a[0], a[1], dict(zip(a[2::2], a[3::2]))
    p, dur, n, s = float(opt.get('--pitch', 1)), float(opt.get('--dur', 1)), int(opt.get('--variants', 1)), int(opt.get('--seed', 0))
    if name not in PRESETS: sys.exit(f'preset desconocido: {name}. Usa: python sfx.py list')
    if n == 1: write_ogg(render(name, p, dur, s), out); print(out); return
    stem = out[:-4] if out.endswith('.ogg') else out
    for i in range(1, n + 1):  # variantes: ±6% de pitch y otra semilla
        write_ogg(render(name, p * (1 + 0.06 * (i - (n + 1) / 2) / max(1, n - 1) * 2), dur, s + i), f'{stem}{i}.ogg'); print(f'{stem}{i}.ogg')


if __name__ == '__main__':
    main(sys.argv[1:])
