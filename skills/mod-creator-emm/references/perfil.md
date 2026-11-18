# Perfil del usuario

El perfil guarda los datos que se repiten en todos los mods de un usuario. **No vive en esta skill**: se guarda en `~/.claude/mod-emm/perfil.md` (fuera de la carpeta de la skill, así sobrevive a actualizaciones). Si ese archivo existe, léelo y ofrécelo en la ronda 1 ("¿Uso tu perfil guardado?" con un resumen de 1 línea). Si no existe, o el usuario quiere cambiarlo, haz las rondas P1-P2 y guárdalo.

## P1 · Juego y pruebas (una ronda `AskUserQuestion`)
Antes de preguntar, detecta en silencio: los launchers instalados (rutas de la tabla de abajo que existan) y sus instancias (subcarpetas de `instances/` o `profiles/`).
- **Loader**: Fabric (Recommended) · NeoForge · Forge · Otro.
- **Versión de Minecraft**: ofrece las versiones de las instancias detectadas que usen ese loader + "Otra (escríbela)". Nunca supongas una versión.
- **Launcher**: los detectados primero · Prism Launcher · CurseForge · Modrinth App · Ninguno (probar con `gradlew runClient`).
- **Instancia de prueba**: las instancias detectadas de ese launcher · "Otra (escribe el nombre)". Si el launcher es "Ninguno" o el oficial, no se pregunta.

Luego resuelve la **carpeta mods de la instancia** con la tabla y comprueba que existe; si no existe, pide la ruta exacta en texto (una sola vez).

| launcher | carpeta mods (Windows · macOS · Linux) |
|---|---|
| Prism | `%APPDATA%/PrismLauncher/instances/<inst>/minecraft/mods` (o `.minecraft/mods`) · `~/Library/Application Support/PrismLauncher/instances/<inst>/minecraft/mods` · `~/.local/share/PrismLauncher/instances/<inst>/minecraft/mods` |
| MultiMC | `<carpeta de MultiMC>/instances/<inst>/.minecraft/mods` (pide la carpeta de MultiMC) |
| CurseForge | `%USERPROFILE%/curseforge/minecraft/Instances/<inst>/mods` · `~/Documents/curseforge/minecraft/Instances/<inst>/mods` |
| Modrinth App | `%APPDATA%/ModrinthApp/profiles/<inst>/mods` · `~/Library/Application Support/ModrinthApp/profiles/<inst>/mods` · `~/.local/share/ModrinthApp/profiles/<inst>/mods` |
| Oficial | `%APPDATA%/.minecraft/mods` · `~/Library/Application Support/minecraft/mods` · `~/.minecraft/mods` |

## P2 · Autor y proceso (una ronda `AskUserQuestion`)
- **Autor** que sale en el mod: "Otro (escríbelo)" con el nombre del usuario del sistema como sugerencia.
- **Licencia**: MIT (Recommended si lo vas a compartir) · All-Rights-Reserved · LGPL-3.0 · CC0.
- **Idiomas**: español + inglés (Recommended) · solo español · solo inglés.
- **Git**: un commit local por fase (Recommended) · sin Git.

## Lo que se decide sin preguntar `[planner]`
- **Java**: el que pide esa versión de Minecraft (1.18–1.20.4 → 17 · 1.20.5–1.21.x → 21 · 26.x → 25). Si no estás seguro, va a "Preguntas abiertas para Code".
- **Versiones exactas** (loader, API, Loom/ModDevGradle, GeckoLib): de un mod de referencia si lo hay; si no, "Preguntas abiertas para Code" (las verifica en la web oficial del loader con permiso del usuario).
- Dependencias: solo la API del loader. **GeckoLib** únicamente si el mod usa mobs de `/mob-creator-emm`.
- `environment: "*"`, estilo vanilla-friendly, paquete `com.<modid sin _>`, `mod_version` inicial 0.1.0.
- Cada jar nuevo sube `mod_version` (grande X.0.0 · mediano x.Y.0 · pequeño x.y.Z); Code reporta versión y porqué.
- Config propia para activar/desactivar contenido y tasas.
- Assets: llegan a `<carpeta>/entrada/`. Si falta uno, Code usa un placeholder simple y lo anota; no lo diseña.
- Aprobaciones siempre en el chat de Claude.
- Entrega final: jar en la carpeta mods de la instancia y copia en `<cwd>/mods listos/`.
- GitHub y publicación: se preguntan en la ronda E, nunca se suben sin permiso.

## Formato de `~/.claude/mod-emm/perfil.md`
```markdown
# Perfil mod-emm
- loader: Fabric
- minecraft: 1.21.4
- java: 21
- launcher: Prism
- instancia: Mods 1.21.4
- carpeta_mods: C:/Users/<usuario>/AppData/Roaming/PrismLauncher/instances/Mods 1.21.4/minecraft/mods
- pruebas: jar a carpeta_mods   (o: gradlew runClient)
- autor: <nombre>
- licencia: MIT
- idiomas: es_es, en_us
- git: commit por fase
```
Créalo con `mkdir -p ~/.claude/mod-emm`. Si el usuario cambia algo en un mod concreto (otra versión, otra instancia), pregunta si actualizar el perfil o usarlo solo para este mod.
