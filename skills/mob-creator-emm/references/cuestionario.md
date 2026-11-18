# Cuestionario · Mob_Creator_EMM

Convenciones:
- `[texto]`: pregunta abierta en texto plano, junto con las demás del mismo bloque.
- `[AUQ]`: usar `AskUserQuestion` (máximo 4 por ronda).
- `[auto]`: deducirlo antes de preguntar (de las imágenes, de la carpeta o de respuestas anteriores).

Muestra el progreso: "Bloque N/7 · <nombre>".

---

## A · Identidad
- [texto] **Nombre visible** del mob (por ejemplo "Santa Claus").
- [auto] **mob_id** en snake_case a partir del nombre (`santa_claus`). Confírmalo dentro del resumen.
- [texto] **Concepto en una frase** ("Santa voxel robusto con costal de regalos").
- [AUQ] **Tipo**: Pasivo (Recommended) · Neutral · Hostil · Jefe.

## B · Referencias (opcional)
- [texto] Rutas de imágenes o carpeta de referencias (por ejemplo `Inspiracion/`). Se puede omitir.
- [auto] Si las hay: conviértelas a JPG (pipeline §1), míralas y anota partes, proporciones y colores.
- [AUQ, solo si no hay imágenes y es un personaje conocido] ¿Busco referencias en la web con `find_references`? Sí (Recommended) · No, describo yo.

## C · Forma
- [AUQ] **Tamaño**: ~2 bloques (32 px, como un zombie) · ~3 bloques (48 px) · 4-5 bloques (64-80 px) · Otro.
- [AUQ] **Cuerpo**: Humanoide (Recommended si es una persona) · Cuadrúpedo · Volador · Otro (serpiente, slime, etc.).
- [texto] **Partes y accesorios** (sombrero, costal, cola, alas, arma, barba...) y cualquier proporción especial (cabezón, panzón).
- [AUQ] **Nivel de detalle**: Estándar 90-180 cubos (Recommended) · Borrador ~60 · Héroe 180+.
- [AUQ] **Extremidades**: 2 segmentos en brazos y 1 en piernas, estilo Minecraft (Recommended) · Con rodillas y codos completos (necesario para sentarse en una silla, cuesta más).

## D · Paleta
- [AUQ] **Origen**: De las imágenes de referencia (Recommended si hay) · Colores que te doy (hex) · Por estilo o mood.
- [texto según la opción]
  - De las imágenes: no hace falta preguntar. Pide los colores a ojo o con `make_palette` con `regions` sobre la referencia, y nombra cada región (pelo, piel, ropa...).
  - Hex: una lista `parte: #hex` (4-13 colores).
  - Mood: color base y mood (vibrant, pastel, earthy, dark, cute, royal...).

## E · Textura
- [AUQ] **Acabado**: Pixel art con tramado (Recommended, estilo Minecraft) · Painted suave · Cel / toon.
- [AUQ] **Detalle por material**: Medio, con costuras, mechones y pelusa suaves (Recommended) · Plano, solo luz · Alto.
- [texto, opcional] Detalles pintados a mano (lazos, ojos con brillo, cicatrices, logos).

## F · Animaciones
- [AUQ multiSelect] **Básicas**: idle (Recommended) · walk (Recommended) · hurt + death (Recommended para un mob de juego) · attack / run.
- [texto] **Poses libres**: describe cada una (por ejemplo "riendo y tocándose la panza con los ojos cerrados") y, si quieres, adjunta una imagen. Se acepta "elige tú N poses típicas del personaje".
- [AUQ] **Expresiones** (ojos cerrados o boca abierta mediante piezas ocultas): Sí (Recommended si hay risa, sueño o daño) · No.
- [AUQ] **Objeto en la mano** que aparece en una pose (regalo, arma, flor...): Sí, ¿cuál? · No.

## G · Entrega
- [auto en modo carpeta del mod: de la versión de Minecraft del plan] [AUQ si no] **Plataforma**: Java + GeckoLib 5 (MC 1.21.4 o posterior, Recommended) · Java + GeckoLib 4 (MC 1.20.x – 1.21.1) · Bedrock addon.
- [texto] **modid** del mod donde irá (o déjalo como `MODID` y lo cambias después).
- [auto] Carpeta de salida: `<carpeta del mod>/entrada/mobs/<Nombre>/` si hay `entrada/ASSETS.md` (modid tomado del plan, no se pregunta); si no, `MOBS Listos/<Nombre>/` dentro del directorio de trabajo. Avisa si ya existe.

---

## Resumen de la ficha (lo que se aprueba)
```
Mob: <Nombre> (<mob_id>) · <tipo> · <concepto>
Referencias: <rutas o "ninguna">
Tamaño: <alto> px × <ancho> px · Cuerpo: <tipo> · Detalle: <presupuesto> cubos
Partes: <lista>
Paleta: <clave: #hex, ...>
Textura: <acabado> · detalle <nivel> · extras: <lazos, ojos...>
Animaciones: <básicas> + poses: <lista>
Expresiones: <sí/no> · Objeto en mano: <cuál/no>
Entrega: <plataforma> · modid <modid|MODID> · MOBS Listos/<Nombre>/
Avisos: <limitaciones, por ejemplo "sentado solo en el suelo">
```
