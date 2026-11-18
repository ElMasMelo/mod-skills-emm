# Íconos y logo

## Íconos de items y bloques (16x16)
- Archivo: `entrada/texturas/<id>.png`, RGBA, fondo transparente.
- Estilo vanilla: contorno oscuro de 1 px (no negro puro, usa el tono más oscuro del material), luz arriba a la izquierda, 3-5 tonos por material, sin antialias.
- Silueta reconocible ocupando ~12-14 px; centrado.
- Herramientas y armas en diagonal (mango abajo a la izquierda) como las vanilla.
- Si existe la textura del mob (`entrada/mobs/<Nombre>/assets/.../textures/entity/*.png`), saca la paleta de ahí para que el drop combine con el mob (lee los colores con PIL, no la imagen).

## Cómo dibujar
Escribe un `.txt` por ícono en `entrada/texturas/fuente/` y ejecuta:
```
python pixel.py entrada/texturas/fuente/bear_fur.txt entrada/texturas/bear_fur.png
python pixel.py entrada/texturas/fuente/bear_fur.txt <scratchpad>/bear_fur_x8.png --scale 8   # vista previa para el chat
```
Formato del `.txt`: líneas `<símbolo> #hex`, luego `---`, luego 16 filas de 16 símbolos (`.` = transparente).
Dibuja todos los íconos de un lote en una sola escritura de archivos y un solo bucle de render.

## Logo del mod (`icon.png` 128x128)
Haz 2-3 propuestas y que el usuario elija:
1. Pixel art 32x32 con `pixel.py --scale 4` (cara del mob principal o el item emblema, fondo de color del mod).
2. Render del mob: si hay `.bbmodel` en `entrada/mobs/<Nombre>/fuente_blockbench/` y el usuario quiere, pide la captura a `/mob-creator-emm` (esta skill no abre Blockbench).
3. Generación de imagen (Canva u otra herramienta disponible) reducida a 128x128 con `Image.NEAREST` y paleta limitada.
Destino final: `entrada/logo/icon.png`.
