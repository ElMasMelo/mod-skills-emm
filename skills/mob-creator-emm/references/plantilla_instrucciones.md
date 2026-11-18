# Plantilla · INSTRUCCIONES_MOD.md

Copia todo lo que hay debajo de la línea a `MOBS Listos/<Nombre>/INSTRUCCIONES_MOD.md` y sustituye cada `{{...}}` con los datos de la ficha y de la exportación. Ejemplo real: `MOBS Listos/Santa Claus/INSTRUCCIONES_MOD.md`.

---

# {{Nombre}} – paquete listo para mod (Java + GeckoLib)

Modelo, textura y animaciones listos para registrar una entidad GeckoLib.
Copia esta carpeta al proyecto del mod y sigue los pasos, o pega el **Prompt para Claude Code** del final.

## 1. Contenido

| Archivo | Qué es |
|---|---|
| `assets/{{modid}}/geckolib/models/entity/{{mob_id}}.geo.json` | Geometría (formato Bedrock 1.12.0, `geometry.{{mob_id}}`) |
| `assets/{{modid}}/geckolib/animations/entity/{{mob_id}}.animation.json` | {{n_anims}} animaciones |
| `assets/{{modid}}/textures/entity/{{mob_id}}.png` | Textura {{tex_w}}×{{tex_h}} |
| `fuente_blockbench/{{mob_id}}.bbmodel` | Proyecto editable en Blockbench (no va dentro del mod) |

## 2. Dónde copiar

1. {{si modid == MODID: "Renombra la carpeta `MODID` al id real de tu mod (minúsculas)."}}
2. Copia `assets/` dentro de `src/main/resources/` del mod.

Rutas según la versión de GeckoLib:
- **GeckoLib 5** (MC 1.21.4 o posterior): se usa tal cual, con `geckolib/models/` y `geckolib/animations/`.
- **GeckoLib 4** (MC 1.20.x – 1.21.1): mueve los archivos a `assets/{{modid}}/geo/entity/` y `assets/{{modid}}/animations/entity/`.

La textura siempre va en `assets/{{modid}}/textures/entity/`.

## 3. Datos de la entidad

- **Id sugerido:** `{{modid}}:{{mob_id}}`
- **Tamaño del modelo:** {{alto_px}} px de alto (≈{{alto_bloques}} bloques), ~{{ancho_px}} px de ancho.
- **Hitbox sugerida:** ancho `{{hit_w}}`, alto `{{hit_h}}` (`EntityType.Builder.sized({{hit_w}}f, {{hit_h}}f)`).
- **Mira hacia** −Z (estándar). Escala del renderer: `1.0`. Sombra: `{{sombra}}`.
- **Huevo de spawn:** primario `{{color1}}`, secundario `{{color2}}`.

### Huesos (no renombrar: las animaciones dependen de ellos)
{{arbol_de_huesos}}

{{si hay piezas ocultas: "`{{lista_ocultos}}` están **escondidos dentro del modelo** y solo aparecen cuando una animación los mueve. No hay que ocultarlos por código."}}

## 4. Animaciones

| Nombre en el JSON | Duración | Bucle | Uso sugerido |
|---|---|---|---|
{{fila por animación: | `animation.{{mob_id}}.<nombre>` | <s> s | loop / hold / una vez | <cuándo usarla> |}}

Estructura recomendada de controladores GeckoLib:
- **`main`**: `walk` si se mueve; si no, el estado ({{estados}}), y si no hay ninguno, `idle`.
- **`action`** (triggerable): {{acciones}}, lanzadas con `triggerAnim("action", "...")` desde el servidor.
- **`death`**: se activa cuando `isDeadOrDying()`.

## 5. Comportamiento sugerido (opcional)

{{3-6 viñetas según el tipo (pasivo/neutral/hostil/jefe) y las poses: vida, velocidad, interacción con clic derecho, cuándo dispara cada acción, bioma de spawn}}

## 6. Prompt para Claude Code

> Crea (o completa) un mod de Minecraft Java con GeckoLib que añada la entidad `{{mob_id}}`. Los assets ya están en `src/main/resources/assets/<modid>/` (modelo `{{mob_id}}.geo.json`, animaciones `{{mob_id}}.animation.json`, textura `textures/entity/{{mob_id}}.png`). Lee `INSTRUCCIONES_MOD.md` para las rutas, la hitbox ({{hit_w}} × {{hit_h}}), los nombres de huesos y la tabla de animaciones. Pregúntame primero el loader (NeoForge/Fabric/Forge), la versión de Minecraft y el modid. Luego implementa: el registro de la entidad y sus atributos; `GeoEntity` con controladores `main`, `action` (triggerables: {{acciones}}) y `death`; `GeoModel` + `GeoEntityRenderer`; el huevo de spawn ({{color1}} / {{color2}}); las traducciones es/en; y el comportamiento de la sección 5. No modifiques los archivos de modelo ni de animación. Verifica compilando y probando en `runClient`.
