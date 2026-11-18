# Sonidos

## Nombres y formato
- Archivo: `entrada/sonidos/<id>.ogg`; con variantes `<id>1.ogg`…`<id>N.ogg` (Minecraft elige al azar).
- `<id>` = `<mob>_<evento>` (`brown_bear_ambient`, `brown_bear_hurt`, `goblin_steal`) o `<cosa>_<acción>` (`goblin_whistle_use`).
- .ogg mono 44.1 kHz (los scripts ya lo hacen). Mono es obligatorio para que el sonido tenga posición en el mundo.
- Duración típica: ambient 0.6-1.5 s · hurt 0.2-0.4 · death 0.6-1.2 · step ≤ 0.15 · interfaz ≤ 0.1.

## Qué fuente usar
| caso | fuente |
|---|---|
| Voces de animales/criaturas (gruñido, ulular, chillido) | Freesound primero; si no hay nada bueno, `sfx.py` (`growl`, `hoot`, `squeak`, `hiss`) |
| Golpes, pasos, escarbar, magia, interfaz, proyectiles, impactos | `sfx.py` |
| Ambiente (viento de cueva, zumbido del End) | Freesound |

## Síntesis local
```
python sfx.py list                                   # presets y duración base
python sfx.py growl <ruta>/brown_bear_ambient.ogg --pitch 0.8 --variants 3
python sfx.py stomp <ruta>/rock_golem_stomp.ogg --dur 1.3
```
- `--pitch` < 1 = más grave y largo (mob grande); > 1 = más agudo y corto (mob pequeño).
- `--dur` escala la duración base. `--seed` cambia la textura del ruido.
- Mismo mob, mismo pitch base en todos sus eventos: así suena coherente.
- Si un preset no encaja, combina dos con ffmpeg (`amix`) antes de escribir un preset nuevo.

## Freesound
- Requiere `FREESOUND_API_KEY` en el entorno. Si falta, el script lo dice: pásale al usuario el mensaje tal cual; **nunca** pidas la key en el chat.
```
python freesound.py search "bear growl" --max-dur 2
python freesound.py get 123456 <ruta>/brown_bear_ambient1.ogg --start 0.2 --dur 1.2
```
- Busca en inglés. Muestra 3-5 candidatos (id, duración, autor, licencia) y baja solo los que el usuario elija.
- Solo CC0 por defecto. `--cc-by` solo si el usuario acepta dar crédito.
- `get` recorta, normaliza a -16 LUFS y anota el crédito en `CREDITS.md`.

## sounds.json (fragmento final)
```json
{
  "brown_bear_ambient": { "subtitle": "subtitles.<mod_id>.brown_bear_ambient",
    "sounds": ["<mod_id>:brown_bear_ambient1", "<mod_id>:brown_bear_ambient2", "<mod_id>:brown_bear_ambient3"] }
}
```
Code copia los .ogg a `assets/<mod_id>/sounds/` y registra cada evento.
