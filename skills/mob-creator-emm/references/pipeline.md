# Pipeline · Mob_Creator_EMM

Proceso probado con Santa Claus (91 cubos, 15 huesos, 10 animaciones). Convenciones del MCP: el modelo **mira a −Z**, su **derecha es +X** y 1 unidad = 1 px. Rutas: `<cwd>/<mob_id>/` es el directorio de trabajo; `MOBS Listos/<Nombre>/` es la entrega.

Carga las herramientas diferidas en una sola llamada `ToolSearch` por fase (`select:a,b,c`).

---

## §1 Preparación
1. `get_status`. Si falla, pide al usuario que abra Blockbench con el servidor del plugin BlockbenchMCP iniciado (puerto 8787).
2. `list_plugins {query:"geckolib"}`. Si `installed:false`, ejecuta `install_plugin {id:"geckolib"}` (para Bedrock no hace falta).
3. Crea `<cwd>/<mob_id>/` antes de cualquier `save_project`.
4. Referencias: si son `.jfif` o pesan más de 256 KB, conviértelas con PowerShell y léelas con `Read`:
```powershell
Add-Type -AssemblyName System.Drawing
$out = "<scratchpad>"
Get-ChildItem "<carpeta_refs>\*" -Include *.jfif,*.jpg,*.jpeg,*.png,*.webp | ForEach-Object {
  $img = [System.Drawing.Image]::FromFile($_.FullName)
  $w = 800; $h = [int]($img.Height * $w / $img.Width)
  $bmp = New-Object System.Drawing.Bitmap $img, $w, $h
  $bmp.Save((Join-Path $out ($_.BaseName + ".jpg")), [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $bmp.Dispose(); $img.Dispose() }
```
(`.webp` puede no abrirse con System.Drawing. En ese caso, pide al usuario que la pegue en el chat).

## §2 Proyecto y paleta
- `new_project {format:"geckolib_model", name:<mob_id>, geometry_name:<mob_id>, texture_width:256, texture_height:256}`. Para Bedrock, `format:"bedrock"`.
- `make_palette {name:<mob_id>, source:"text", colors:{red:"#c8302c", fur:"#ede3cc", ...}}`. Nombra las claves por material o región; se usan como `$clave`, `$clave.shadow`, `$clave.light` y `$clave.deep`.

## §3 Huesos (una llamada `add_groups`)
Humanoide (lo que funcionó):
```
root[0,0,0] › body[0,hip,0] › head[0,neck,z] › hat/…
body › left_arm[-sx,shoulder,0] › left_forearm[-sx,elbow,0]
body › right_arm[+sx,shoulder,0] › right_forearm[+sx,elbow,0]
body › <accesorio_espalda>
root › left_leg[-lx,hip,0] , right_leg[+lx,hip,0]
```
Las piernas cuelgan de `root`, no de `body`, para que el cuerpo pueda inclinarse sin arrastrarlas. Para cuadrúpedos o voladores lee `get_guide {topic:"rigging"}` una sola vez.

Si la ficha pide comer, rugir o babear, usa una **mandíbula articulada** (`head › jaw`, pivote atrás y abajo; X− abre), en lugar de una boca oculta. `generate_animation` la detecta y la usa en idle, hurt y death. Dentro de `jaw` van `tongue` (pivote en la raíz) y `drool`; dentro de `head`, `mouth_inner` (oscuro, oculto entre el cráneo y la mandíbula), `eyes_open` y `eyes_closed`. Para agarrar, añade `*_hand` en el antebrazo (X+ cierra los dedos). Los brazos pueden tener rotación de reposo en el hueso (por ejemplo Z ±14° para abrirlos en A).

## §4 Modelo
0. **La forma más barata**: el snippet *add_cubes_mirror* crea todas las masas (con espejo izquierda/derecha) en una sola llamada y sin la salida enorme de `add_cubes`. Después: `pack_uv` → `create_texture` → asignar la textura (SKILL, trampas) → `fix_z_fighting` → `check_model`. Para el checkpoint 1, haz una pasada rápida de `detail_cubes` con colores planos por zona (`finish:"painted", noise:0, vary:0`): con un solo color la forma no se entiende.
   - Volúmenes redondos (panzas): 3-5 capas grandes escalonadas (frontal grande, colgante baja, unión superior y costados). Los anillos finos de 2 px se ven como escalones y el usuario los rechazó.
1. **Capa 1** (masas): `add_cubes` en 2 lotes (piernas, torso y brazos; luego cabeza, accesorios y espalda). Cada cubo lleva `parent` (su hueso), `side` (left/right) y un nombre con palabra clave de material (`_fur`, `_leather`, `beard`, `sole`...), porque las reglas de `detail_cubes` funcionan por regex sobre el nombre.
   - Ejemplos de proporciones de Santa (72 px de alto): botas 0-6, pierna 9-19, falda del abrigo 18-30, cinturón 28-32, torso 31-46, cabeza 46-60 (16×14×14), gorro 58-72, brazo superior 34-46, antebrazo 25-34, guante 15-22.
   - Las piezas superpuestas deben penetrarse ≥0.1. Las capas exteriores sobresalen 0.3-0.8.
2. **Ajuste a la cuadrícula**: snippet *snap* (box UV necesita tamaños enteros).
3. **Capas 2-4** (detalle): `generate_array` (barba en grid 4×3 con `depth_stagger 0.2`, mechones en línea con `anchor:"top"`, pliegues). `add_cubes` para suelas, hombreras, nudillos, pasadores y parches. Comprueba que las filas no queden enterradas: compara su z con la cara del cubo base después del *snap* y muévelas con un script si hace falta.
4. **Revisión**: `audit_complexity {target:"character"}` hasta "acceptable", y `check_model` hasta tener 0 `hidden_cube`/`coplanar_overlap`. Corrige con un script (`inflate:0.05` en uno de cada par coplanar y mover los cubos ocultos).
5. `save_project {path:"<cwd>/<mob_id>/<mob_id>.bbmodel"}`, `screenshot_views {views:["front_right","front","back_left"], inspect:false, width:600, height:600}` y luego **CHECKPOINT 1**.

## §5 Textura
1. Respaldo `backup_vN_modelo/`.
2. `pack_uv` (todos los cubos) y `create_texture {name:<mob_id>, fill:<color base>}`.
3. `detail_cubes` con `materials` ordenados de lo más específico a lo más general (gana la primera coincidencia) y una regla final `{match:".", ...}` para el material dominante. Base probada:
   - Acabado pixel (el preferido del usuario con Santa): `{finish:"pixel", seed:12}` + materiales.
   - Sin cuadrícula: `{finish:"painted", noise:0.04, vary:0, bevel:0.6, blur:0.6, ao:0.5}`.
   - Por material: fur `strands 0.6` + speckle `$fur.shadow` 0.12; hair `strands 0.7, shine 0.15`; cuero `stitch 0.5`; cinturón con trim discontinuo `$belt.light` arriba y abajo; tela `folds ≤0.2` + speckle `$x.shadow` 0.08-0.1.
4. `paint_faces` para detalles (las coordenadas son relativas a la cara): brillo de ojos `{type:"pixel",x,y,color}` y lazos `{type:"rect",x,y,width,height,fill:true,color}`. Repítelo después de cada `detail_cubes`.
5. `check_model` (debe dar 0), guardar, 2 capturas y **CHECKPOINT 2**. Si el usuario quiere probar otro estilo, haz primero un respaldo de la versión actual.

## §6 Expresiones y objetos ocultos (si la ficha lo pide)
- Huesos dentro de `head`: `eyes_open` (mueve ahí los cubos de ojos), `eyes_closed` y `mouth_open`. Dentro del antebrazo: `held_<obj>`.
- Las piezas ocultas quedan **dentro** del volumen. Con Santa: ojos cerrados "^ ^" con 3 cubos por ojo en z −8.9…−7.9 (la cara estaba en −9.05); boca, dientes y lengua en z −11.5…−10.5, dentro de la barba; regalo de 4³ dentro del guante.
- Crea los cubos con *add_cubes_quiet* (o `add_cubes`), luego **uv_firstfit** y luego `paint_faces {face:"all", base:<color>}`.
- En las animaciones, aparecen con keyframes de posición: `eyes_open [0,0,1.2]` (se esconde), `eyes_closed [0,0,-0.95]`, `mouth_open [0,0,-2.3]` (adelante) y `held_gift [-1,0,-5]`. Calcula los valores con *pose_search* según el modelo.

## §7 Animaciones
1. Respaldo `backup_vN_<etiqueta>/`.
2. Básicas: `generate_animation {type, name:"animation.<mob_id>.<type>", intensity:0.8}` (idle 4 s, walk ~1.2 s, hurt, death con `direction`).
3. Añade seguimiento a los accesorios (gorro, costal, cola) con *make_anim* o con keyframes extra (±2-4°).
4. Poses libres: ejecuta *axis_probe* una vez para confirmar los signos. Luego escribe la pose con *make_anim*. Si una mano debe tocar algo (panza, objeto), calcula los ángulos con *pose_search*. Valores que funcionaron con Santa:
   - Mano en la panza: `right_arm [-10,0,-30]` y `right_forearm [100,0,0]`.
   - Brazo arriba saludando: `right_arm [10,0,145]` y `forearm z ±25`.
   - Sentado en el suelo: `root y −13`, piernas `[88,±4,∓4]`.
   - Ofrecer objeto: `right_arm [75,0,-8]` y `forearm [10,0,0]`.
   - Lengua afuera: lengua **larga** (unos 10 px) escondida dentro de la mandíbula, con el pivote en la raíz. Se saca con una posición pequeña hacia adelante y hacia arriba, por encima de los dientes (con el Goblin: `[0,3.5,-8]`), más rotación X−25° para que caiga. Mover una lengua corta hace que flote.
   - Babas: con el snippet *verts* calcula la posición de la punta de la lengua o del labio. Las gotas nacen ahí y caen pocos píxeles.
   - Comer: con *pose_search* lleva las palmas frente a la boca (hace falta probar también el eje Y del brazo, ±40°).
5. Ejecuta *fix_loops* y `analyze_animation` (`loop_gap` 0). Después `preview_animation` con 1-2 tiempos por animación (400 px) y **CHECKPOINT 3**.

## §8 Guardar
`save_project`, luego extrae el PNG del `.bbmodel`:
```powershell
$d = "<cwd>\<mob_id>"; $j = Get-Content "$d\<mob_id>.bbmodel" -Raw | ConvertFrom-Json
[IO.File]::WriteAllBytes("$d\<mob_id>.png", [Convert]::FromBase64String($j.textures[0].source.Split(',')[1]))
```

## §9 Entrega final (obligatoria): `MOBS Listos/<Nombre>/`
En modo carpeta del mod, sustituye `MOBS Listos/<Nombre>/` por `<carpeta del mod>/entrada/mobs/<Nombre>/` en todo este apartado y, al validar, marca la fila del mob como `listo` en `entrada/ASSETS.md`.
```
MOBS Listos/<Nombre>/
  INSTRUCCIONES_MOD.md                                   ← desde plantilla_instrucciones.md
  assets/<modid|MODID>/geckolib/models/entity/<mob_id>.geo.json
  assets/<modid|MODID>/geckolib/animations/entity/<mob_id>.animation.json
  assets/<modid|MODID>/textures/entity/<mob_id>.png
  fuente_blockbench/<mob_id>.bbmodel
```
1. Crea las carpetas con `mkdir -p`.
2. Ejecuta *export_geckolib* con `dir` = la carpeta `geckolib` del paso anterior (escribe el geo en `models/entity` y la animación en `animations/entity`; ajusta las rutas en `params`).
3. Copia el PNG y el `.bbmodel`.
4. Escribe `INSTRUCCIONES_MOD.md` rellenando la plantilla con los datos de la ficha (hitbox ≈ ancho del cuerpo y alto del modelo / 16 + 0.1, huesos, tabla de animaciones y comportamiento según el tipo).
5. Valida con PowerShell:
```powershell
$b = "<MOBS Listos>\<Nombre>\assets\<modid>"
$g = (Get-Content "$b\geckolib\models\entity\<mob_id>.geo.json" -Raw | ConvertFrom-Json).'minecraft:geometry'[0]
$a = Get-Content "$b\geckolib\animations\entity\<mob_id>.animation.json" -Raw | ConvertFrom-Json
$bones = $g.bones.name
$used = $a.animations.PSObject.Properties | % { $_.Value.bones.PSObject.Properties.Name } | Sort-Object -Unique
"geo $($g.description.identifier) $($g.description.texture_width)x$($g.description.texture_height) bones $($bones.Count) anims $($a.animations.PSObject.Properties.Name.Count)"
"faltan: " + (($used | ? { $bones -notcontains $_ }) -join ',')
```
6. Muestra al usuario el árbol de archivos y el prompt de la sección 6 de `INSTRUCCIONES_MOD.md` en un bloque de código.
