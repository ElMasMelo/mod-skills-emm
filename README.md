# Mod Skills EMM · crea mods de Minecraft con Claude Code

Tres skills para [Claude Code](https://claude.com/claude-code) que te llevan de una idea a un `.jar` funcionando, sin escribir código tú mismo. Las hizo ElMasMelo para sus propios mods.

| skill | qué hace | escribe código |
|---|---|---|
| `/mod-creator-emm` | Cuestionario para planear el mod. Escribe el plan, el prompt para Code y la lista de assets | No |
| `/mob-creator-emm` | Modela, texturiza y anima cada mob en Blockbench (GeckoLib) | No |
| `/acabados-emm` | Sonidos, íconos 16x16 y logo 128x128 | No |
| Claude Code (sesión nueva) | Programa, compila y prueba siguiendo el plan | Sí |

Funciona con **cualquier loader** (Fabric, NeoForge, Forge), **cualquier versión de Minecraft** y **cualquier launcher** (Prism, CurseForge, Modrinth App, MultiMC, el oficial o sin launcher con `gradlew runClient`). La primera vez te pregunta tus datos y los guarda como perfil.

## Requisitos

**Para todo:**
- Claude Code: plan **Claude Pro** o superior, en la app de escritorio (pestaña Code) o en la terminal.
- Windows: **Git for Windows**.
- **JDK** de la versión que pide tu Minecraft (1.18–1.20.4 → 17 · 1.20.5–1.21.x → 21 · 26.x → 25).
- Minecraft Java Edition y un launcher con una instancia del loader que vayas a usar.

**Solo para `/mob-creator-emm`:**
- [Blockbench](https://www.blockbench.net) con el plugin y servidor **Blockbench MCP** conectado a Claude Code.
- El plugin GeckoLib de Blockbench (la skill lo instala sola).

**Solo para `/acabados-emm`:**
- Python 3 con `pip install numpy scipy pillow`.
- `ffmpeg` en el PATH.
- Opcional: clave gratis de [Freesound](https://freesound.org/apiv2/apply) en la variable `FREESOUND_API_KEY`. Sin ella, los sonidos se sintetizan en tu PC.
  ```bash
  setx FREESOUND_API_KEY "TU_KEY"
  ```
  (macOS/Linux: `export FREESOUND_API_KEY="TU_KEY"` en tu `~/.zshrc` o `~/.bashrc`). Nunca pegues la clave en el chat.

## Instalación

Descarga el repo (botón verde **Code → Download ZIP** y descomprímelo, o `git clone https://github.com/ElMasMelo/mod-skills-emm`). Copia las tres carpetas de `skills/` a tu carpeta de skills de Claude Code y reinicia Claude.

Windows (PowerShell, desde la carpeta del repo):
```powershell
Copy-Item -Recurse -Force skills\* "$env:USERPROFILE\.claude\skills\"
```

macOS / Linux:
```bash
mkdir -p ~/.claude/skills && cp -R skills/* ~/.claude/skills/
```

Comprueba que quedó `~/.claude/skills/mod-creator-emm/SKILL.md`. Para actualizar, repite la copia: tu perfil no se borra porque vive aparte, en `~/.claude/mod-emm/perfil.md`.

## Cómo crear un mod

Abre Claude Code siempre en la misma carpeta de trabajo (por ejemplo `Mis Mods/`). Ahí se crean los mods.

1. **Planear** · `/mod-creator-emm`
   - La primera vez te pregunta tu perfil: loader, versión de Minecraft, launcher, instancia de prueba, autor, licencia, idiomas y Git. Detecta tus launchers e instancias para que solo elijas.
   - Te pregunta si ya tienes un mod hecho con esa misma versión (ver abajo).
   - Responde las rondas y aprueba el resumen.
   - Crea `<carpeta del mod>/` con `PLAN_<mod_id>.md`, `PROMPT.md`, `RESPUESTAS.md` y `entrada/ASSETS.md`.
2. **Mobs** · `/mob-creator-emm <carpeta del mod>`, una vez por mob. Apruebas modelo, textura y animaciones.
3. **Sonidos, íconos y logo** · `/acabados-emm <carpeta del mod>`.
4. **Programar** · abre una sesión **nueva** de Code en la carpeta de trabajo y pega el contenido de `PROMPT.md`. Code avanza por fases: en cada una compila, sube la versión, pone el jar en tu instancia y te dice qué probar.
5. **Entrega** · el jar final queda en tu instancia y en `mods listos/`.

Los pasos 2 y 3 se pueden hacer antes, durante o después del 4. Si falta un asset, Code pone uno temporal (`placeholder`); cuando lo hagas, dile «reemplaza los placeholders».

## ¿Por qué pregunta si ya tengo un mod hecho?

Si tienes un mod que ya compila con el mismo loader y versión, Code reusa **solo su configuración**: el Gradle, las versiones exactas y la estructura base (cómo se registran las cosas, el archivo de config). Así se salta la parte que más errores da y genera el mod nuevo más rápido y gastando menos uso.

**No copia ninguna mecánica, contenido ni funcionalidad** de ese mod: todo lo que hace el mod nuevo se escribe desde cero según su plan. Si no tienes ninguno, Code parte de la plantilla oficial del loader.

## ASSETS.md, la lista que une todo

`entrada/ASSETS.md` lista todo lo que el mod necesita y no es código. Cada skill solo lee y cambia sus filas, así ninguna depende de la conversación de otra.

| estado | significa |
|---|---|
| `pendiente` | nadie lo ha hecho |
| `listo` | ya está en `entrada/`; Code lo usa |
| `placeholder` | Code puso uno temporal; hazlo con su skill y pide a Code que lo reemplace |

## Mapa de carpetas

```
<carpeta de trabajo>/                 ← donde abres Claude Code
├─ <carpeta del mod>/
│  ├─ PLAN_<mod_id>.md                lo único que lee Code
│  ├─ PROMPT.md                       lo que pegas en Code
│  ├─ RESPUESTAS.md                   notas del cuestionario
│  ├─ entrada/                        assets: mobs/, sonidos/, texturas/, logo/, ASSETS.md
│  └─ src/, build.gradle …            el proyecto (lo crea Code)
├─ <mob_id>/                          taller de cada mob (ficha y respaldos)
├─ MOBS Listos/<Nombre>/              mobs hechos sin carpeta de mod
└─ mods listos/                       jar final de cada mod
~/.claude/mod-emm/perfil.md           tu perfil (fuera de las skills)
```

## Licencia

[MIT](LICENSE) © 2026 ElMasMelo. Puedes usar, modificar y compartir estas skills; solo mantén el aviso de licencia.
