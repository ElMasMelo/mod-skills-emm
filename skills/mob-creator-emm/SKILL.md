---
name: mob-creator-emm
description: "Mob_Creator_EMM (by ElMasMelo): creates a complete Minecraft mob (3D model, texture, animations) in Blockbench via the Blockbench MCP and exports a ready-to-use GeckoLib package to 'MOBS Listos/<Name>/', or to <mod folder>/entrada/mobs/<Name>/ when given a mod folder with entrada/ASSETS.md (from mod-creator-emm), with mod instructions. It ALWAYS starts with a questionnaire (name, optional reference images, palette, size, parts, texture finish, animations, delivery) and stops for approval after model, texture and animations. Use when the user says mob-creator-emm, 'crear un mob', 'modelar un mob', 'nuevo mob', or wants a Minecraft entity modeled/textured/animated for a mod."
---

# Mob_Creator_EMM

Construyes un mob de Minecraft de principio a fin con el **Blockbench MCP** y entregas el paquete listo para un mod GeckoLib. Respondes en el idioma del usuario (por defecto español).

**Requisitos** (compruébalos en §1 de `pipeline.md`): Blockbench abierto con el plugin y servidor **Blockbench MCP**; el plugin GeckoLib de Blockbench se instala solo. Los bloques de código del pipeline están en PowerShell (Windows); en macOS/Linux haz lo mismo con Python (`PIL` para imágenes, `json`/`base64` para el resto).

## Archivos de esta skill
- `references/cuestionario.md`: la ficha del mob (bloques A-G). Léelo al empezar.
- `references/pipeline.md`: el paso a paso en Blockbench. Léelo antes de modelar.
- `references/snippets.md`: scripts probados para `execute_script`. Cópialos tal cual y cambia solo los parámetros.
- `references/plantilla_instrucciones.md`: plantilla de `INSTRUCCIONES_MOD.md` para la entrega final.

## Flujo (no te saltes pasos)
1. **Cuestionario primero.** Usa `AskUserQuestion` con un máximo de 4 preguntas por ronda, 2-4 opciones y la recomendada primero con "(Recommended)". Las preguntas abiertas (nombre, concepto, partes, poses libres) van en texto plano, agrupadas por bloque. Muestra el progreso ("Bloque 2/7 · Referencias"). Salta lo que ya esté respondido. Si el usuario dice "tú decides", elige lo más simple y anótalo como `[decidido por la skill]`.
2. **Ficha aprobada.** Muestra un resumen de unas 20 líneas, pregunta "¿Falta algo o hay algo mal?" y corrige hasta que lo apruebe. Guárdala en `<cwd>/<mob_id>/FICHA_<mob_id>.md`. **No toques Blockbench antes de este punto.**
3. **Pipeline** (`references/pipeline.md`), con fases y un **checkpoint** al final de cada una. En cada checkpoint, dale al usuario 2-3 capturas y espera su aprobación ("Pasar a texturizar" / "Ajustar forma"):
   - Fase 1 · Modelo → checkpoint
   - Fase 2 · Textura → checkpoint
   - Fase 3 · Animaciones → checkpoint
   - Fase 4 · Exportación y entrega (siempre la última, obligatoria)
4. **Respaldos.** Antes de cualquier retoque de textura, poses o cambio de geometría, copia `<mob_id>.bbmodel` y `.png` a `<mob_id>/backup_vN_<etiqueta>/`. Si el usuario pide volver atrás, restaura con `close_project` y luego `load_project`, después de respaldar la versión actual.
5. **Entrega final (obligatoria).** Crea la carpeta de entrega (ver "Modo carpeta del mod") con la estructura de `pipeline.md` §9, valídala y muestra el prompt del mod en un bloque de código.

## Modo carpeta del mod (si el usuario pasa una carpeta con `entrada/ASSETS.md`, o el cwd la tiene)
- Antes del cuestionario lee **solo** la fila `tipo=mob` de ese mob en `ASSETS.md` (id, descripción, animaciones) y del `PLAN_*.md` solo el `mod_id` (primera línea) y la línea de loader/versión de §1 (`grep -m1`), que deciden la versión de GeckoLib. Úsalos como respuestas ya dadas: no preguntes nombre, modid ni las animaciones listadas (solo confirma si quiere añadir poses).
- Entrega en `<carpeta>/entrada/mobs/<Nombre>/` en lugar de `MOBS Listos/<Nombre>/`, con el modid real (nunca `MODID`).
- Al terminar, cambia el estado de esa fila a `listo` en `ASSETS.md`. No toques otras filas ni otros archivos del mod.
- Sin carpeta del mod: flujo normal, entrega en `MOBS Listos/<Nombre>/`.

## Ahorro de tokens
- Construye en lotes: `add_groups` en 1 llamada, `add_cubes` en 2-3 lotes grandes y `generate_array` para filas repetidas.
- Verifica con texto y datos (`check_model`, `audit_complexity`, `analyze_animation`, scripts de medición) antes que con imágenes. Toma como máximo 2-3 capturas por fase, de 400-600 px, con `inspect:false`.
- Lee `get_guide` solo si el tipo de mob es nuevo (por ejemplo `rigging` para cuadrúpedos) y una sola vez.
- Los resultados de `add_cubes` son muy largos. Para cubos sueltos (accesorios, piezas ocultas) usa `execute_script` con `new Cube(...)` (snippet *add_cubes_quiet*).

## Trampas conocidas (ya resueltas, no las repitas)
- `export_project` en formato GeckoLib escribe un `.bbmodel`, no `geo.json`. Usa el snippet *export_geckolib*.
- En `execute_script` no existen `require` ni `fs`. Para escribir archivos usa `Blockbench.writeFile`. El PNG se extrae del `.bbmodel` con PowerShell.
- `save_project` falla si la carpeta no existe: créala antes.
- Las operaciones de `paint_faces` usan `width`/`height`/`fill:true` (con `w`/`h` no pinta nada y no da error).
- `detail_cubes` sobrescribe la pintura manual (ojos, lazos): vuelve a aplicar `paint_faces` después de cada pasada.
- Las luces y sombras en "cuadrícula" vienen de `vary` > 0, del acabado `pixel` y del ruido. Por defecto usa `vary:0` y `noise ≤ 0.04`. Los pliegues de tela por encima de 0.3 parecen código de barras.
- `pack_uv` sobre unos pocos cubos los pone en (0,0), encima del UV existente. Para cubos nuevos usa el snippet *uv_firstfit*.
- `generate_animation` puede dejar el último keyframe distinto del primero o pasado de `length`: aplica *fix_loops*.
- Las capturas engañan con los ángulos de los brazos. Mide posiciones con *pose_search* o *axis_probe* antes de corregir.
- Con piernas de un solo segmento (sin rodilla) no se puede sentar en una silla, solo en el suelo. Avísalo en la ficha si piden la pose "sentado".
- Las imágenes `.jfif` o mayores de 256 KB no se pueden leer: conviértelas a JPG de 800 px en el scratchpad (pipeline §1).
- `create_texture` **no asigna** la textura a las caras: `check_model` devuelve cientos de avisos `no_texture` (muchos tokens). Justo después de `pack_uv` + `create_texture`, asígnala con un script (`Cube.all.forEach(c=>c.applyTexture(Texture.all[0], true))`) antes de cualquier `check_model`.
- Los cubos creados por script no corrigen el z-fighting: después usa la herramienta `fix_z_fighting` (barata y automática).
- `Box3.setFromObject` da valores falsos durante una animación. Para medir posiciones usa los vértices (snippet *verts*).
- Los cubos ocultos (párpados, lengua, babas) salen como `hidden_cube`: es lo esperado, no los borres.
- Con un cuerpo grande (panza, pecho), las piezas que asoman de la boca quedan tapadas: mide si se ven antes de enseñarlas.
- Cuando el usuario elija "Ajustar …" sin detalles, pregúntale con `AskUserQuestion` (multiSelect) con 3-4 propuestas concretas sacadas de la referencia.
