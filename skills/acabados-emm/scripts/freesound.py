"""Buscar y bajar sonidos de Freesound (solo licencias libres) y anotar el crédito.

Requiere la variable de entorno FREESOUND_API_KEY (la pone el usuario: https://freesound.org/apiv2/apply).
Uso:
  python freesound.py search "<consulta en inglés>" [--max-dur 3] [--cc-by]
  python freesound.py get <id> <salida.ogg> [--start 0] [--dur 2] [--credits <ruta CREDITS.md>]
Por defecto solo CC0. --cc-by incluye "Attribution" (exige crédito; get lo anota siempre).
get baja la vista previa HQ (.ogg) y la convierte a mono 44.1 kHz con ffmpeg.
"""
import json, os, subprocess, sys, tempfile, urllib.parse, urllib.request

API = 'https://freesound.org/apiv2'


def key():
    k = os.environ.get('FREESOUND_API_KEY')
    if not k and os.name == 'nt':  # setx no llega a procesos ya abiertos: leerla del registro del usuario
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as r: k = winreg.QueryValueEx(r, 'FREESOUND_API_KEY')[0]
        except OSError: pass
    if not k: sys.exit('Falta FREESOUND_API_KEY. El usuario debe crearla en https://freesound.org/apiv2/apply y ejecutar: setx FREESOUND_API_KEY "<su key>" (y reiniciar la terminal).')
    return k


def call(path, **q):
    q['token'] = key()
    with urllib.request.urlopen(f'{API}{path}?{urllib.parse.urlencode(q)}', timeout=30) as r:
        return json.load(r)


def search(query, max_dur=3.0, cc_by=False):
    lic = '("Creative Commons 0" OR "Attribution")' if cc_by else '"Creative Commons 0"'
    res = call('/search/text/', query=query, filter=f'license:{lic} duration:[0 TO {max_dur}]',
               fields='id,name,username,license,duration', page_size=8, sort='rating_desc')
    for s in res['results']:
        print(f"{s['id']:>8}  {s['duration']:5.2f}s  {s['license'].rstrip('/').split('/')[-2]:<8} {s['username']:<16} {s['name']}")
    if not res['results']: print('sin resultados: prueba otra consulta en inglés o sube --max-dur')


def get(sid, out, start=0.0, dur=None, credits=None):
    s = call(f'/sounds/{sid}/', fields='id,name,username,license,url,previews')
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, 'p.ogg')
        urllib.request.urlretrieve(s['previews']['preview-hq-ogg'], src)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        cut = ['-ss', str(start)] + (['-t', str(dur)] if dur else [])
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *cut, '-i', src, '-ac', '1', '-ar', '44100',
                        '-af', 'loudnorm=I=-16:TP=-1.5', '-c:a', 'libvorbis', '-q:a', '5', out], check=True)
    credits = credits or os.path.join(os.path.dirname(os.path.abspath(out)), 'CREDITS.md')
    new = not os.path.exists(credits)
    with open(credits, 'a', encoding='utf-8') as f:
        if new: f.write('| archivo | sonido | autor | licencia | url |\n|---|---|---|---|---|\n')
        f.write(f"| {os.path.basename(out)} | {s['name']} | {s['username']} | {s['license']} | {s['url']} |\n")
    print(out)


def main(a):
    if len(a) < 2 or a[0] not in ('search', 'get'): print(__doc__); return
    opt = dict(zip(a[3::2], a[4::2])) if a[0] == 'get' else dict(zip(a[2::2], a[3::2]))
    if a[0] == 'search':
        search(a[1], float(opt.get('--max-dur', 3)), '--cc-by' in a)
    else:
        get(a[1], a[2], float(opt.get('--start', 0)), opt.get('--dur'), opt.get('--credits'))


if __name__ == '__main__':
    main(sys.argv[1:])
