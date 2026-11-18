# Plantilla de salida
Se escribe leyendo solo `RESPUESTAS.md` + esta plantilla. `PLAN_<mod_id>.md`: estas secciones, omitiendo las ramas no elegidas. Tablas y listas; cada dato una sola vez.

````markdown
# PLAN · <Nombre> (`<mod_id>`)
> Mod_Creator_EMM · <autor> · <fecha>

## 1. Contexto
- Idea · autor · licencia · idiomas
- <loader> <MC> · versiones exactas (loader, API, plugin de Gradle) o "ver Preguntas abiertas" · Java <v> · dependencias (GeckoLib si hay mobs de mob-creator-emm)
- Pruebas: <launcher> "<instancia>" → `<carpeta_mods>` (o `gradlew runClient`)
- Paquete · mod de referencia: `<ruta>` (o ninguno) y archivos exactos a reusar **solo como configuración** (build, registro, config); nada de su contenido ni mecánicas
- Dificultad · entorno

## 2. Decisiones cerradas
- … (incluye las del perfil que apliquen)

## 3. Contenido
### 3.1 Mobs
| id | es / en | tipo | spawn | vida·daño·vel | drops | XP | animaciones que usa el código |
Ficha por mob: comportamiento, habilidad + contramedida, domesticación/cría, variantes. **Aceptación:** …
### 3.2 Items
| id | es / en | categoría | función/stats | obtención/receta | stack |
### 3.3 Bloques · 3.4 Mundo · 3.5 Sistemas
(tabla + aceptación)

## 4. Assets de entrada
Lista completa en `entrada/ASSETS.md`. Los hacen `/mob-creator-emm` (mobs) y `/acabados-emm` (sonidos, íconos, logo); Code no los diseña.
Code copia cada asset `listo` a `src/main/resources/assets/<mod_id>/…`, sigue el `INSTRUCCIONES_MOD.md` de cada mob y fusiona `entrada/sonidos/sounds.json`. Si una fila sigue `pendiente`: placeholder simple (sonido vanilla, textura de color plano), cambiarla a `placeholder` y avisar.

## 5. Fases
Cada fase: `gradlew build` → subir `mod_version` (grande X.0.0 · mediano x.Y.0 · pequeño x.y.Z) → jar a `<carpeta_mods>` (borrar el anterior) o `gradlew runClient`, según el perfil → prueba → commit (si el perfil usa Git). Reportar versión y porqué.
### Fase 0 · Esqueleto — proyecto desde <la configuración del mod de referencia | la plantilla oficial del loader>, metadata, idiomas, pestaña, config. Aceptación: el juego carga el mod.
### Fase 1 · <elemento más simple, valida el pipeline completo>
- Crear: … · Assets: `entrada/…` · Aceptación: …
### Fase N · …
### Fase final · Entrega
- Build final, jar en `<carpeta_mods>` y copia en `<cwd>/mods listos/` (crear la carpeta si no existe). Reportar ruta y versión.

## 6. Riesgos
- Posibles duplicados en vanilla <v> · dependencias · rendimiento · assets pendientes

## 7. Preguntas abiertas para Code
- … (solo estas + puntos de aprobación)

## 8. Prompt
Ver `PROMPT.md`.
````

`entrada/ASSETS.md` (contrato entre las 3 skills; cada una lee solo sus tipos y cambia solo el estado de sus filas):

```markdown
# ASSETS · <mod_id>
| id | tipo | uso | descripción | archivo | estado |
|---|---|---|---|---|---|
| brown_bear | mob | entidad | oso pardo; anims: idle, walk, attack, sleep, sit | entrada/mobs/Oso Pardo/ | pendiente |
| brown_bear_ambient | sonido | mob | gruñido grave ~1 s, 3 variantes | entrada/sonidos/brown_bear_ambient.ogg | pendiente |
| bear_fur | icono | item | pelaje marrón | entrada/texturas/bear_fur.png | pendiente |
| icon | logo | mod | 128x128, cara del oso | entrada/logo/icon.png | pendiente |
```
- `tipo`: mob · sonido · musica · icono · logo. `estado`: pendiente · listo · placeholder.
- Por mob: una fila `mob` (con las animaciones que usa el código) + filas `sonido` para ambient, hurt, death, step y cada acción especial.
- Por item/bloque con textura propia: una fila `icono`.

`PROMPT.md`:

```markdown
Desarrolla el mod descrito en `<carpeta>/PLAN_<mod_id>.md`.
- Lee solo el plan, una vez; es la fuente de verdad. No leas RESPUESTAS.md ni re-explores lo que ya dice.
- No discutas las "Decisiones cerradas". Pregunta solo las "Preguntas abiertas" y los puntos de aprobación, siempre en este chat.
- Los assets están en `<carpeta>/entrada/` (estado en `entrada/ASSETS.md`); no los diseñes. Si uno sigue pendiente, placeholder, márcalo `placeholder` y avísame.
- Fases en orden. Al cerrar cada una: build, subir versión, jar a `<carpeta_mods>` (o `gradlew runClient`), commit si uso Git, y dime qué quedó listo.
- Al final deja el jar en `<carpeta_mods>` y en `mods listos/` (créala si no existe).
- <Si hay mod de referencia:> De `<ruta referencia>` reusa solo la configuración (Gradle, versiones, estructura base); no copies su contenido ni sus mecánicas. <Si no:> Crea el proyecto desde la plantilla oficial de <loader> <MC>.
- Si algo ya existe en vanilla <MC> o choca con el plan, para y pregúntame. Búsqueda web: solo pidiéndome permiso antes.
Empieza por la Fase 0.
```
