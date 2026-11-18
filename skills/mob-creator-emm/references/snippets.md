# Snippets · Mob_Creator_EMM

Scripts que funcionaron con Santa Claus en Blockbench 5.2 y el plugin GeckoLib 4.2.5. Se pasan a `execute_script` como `code`, y los valores variables van en `params`. Son cuerpos de función: llevan `return` explícito.

---

## snap: tamaños a píxeles enteros (conserva el centro)
```js
Undo.initEdit({elements: Cube.all});
let changed = [];
Cube.all.forEach(c => {
  let moved = false;
  for (let i = 0; i < 3; i++) {
    const s = c.to[i] - c.from[i];
    const ns = Math.max(1, Math.round(s));
    if (Math.abs(ns - s) > 1e-6) {
      const mid = (c.to[i] + c.from[i]) / 2;
      c.from[i] = mid - ns / 2; c.to[i] = mid + ns / 2; moved = true;
    }
  }
  if (moved) changed.push(c.name);
});
Canvas.updateAll(); Undo.finishEdit('snap cube sizes to whole pixels');
return {changed: changed.length};
```
Después ejecuta `check_model`: el *snap* puede enterrar filas de detalle o crear caras coplanares.

## move_by_prefix: mover un grupo de cubos (por ejemplo una fila enterrada)
`params: {prefix:"sack_fold", d:[0,0,1]}`
```js
Undo.initEdit({elements: Cube.all});
const f = Cube.all.filter(c => c.name.startsWith(params.prefix));
f.forEach(c => { for (let i=0;i<3;i++){ c.from[i]+=params.d[i]; c.to[i]+=params.d[i]; c.origin[i]+=params.d[i]; } });
Canvas.updateAll(); Undo.finishEdit('move ' + params.prefix);
return {moved: f.length};
```

## add_cubes_quiet: crear cubos sin la salida gigante de add_cubes
`params: {group:"held_gift", cubes:[{name:"held_gift_box", from:[..], to:[..]}, ...]}`
```js
const grp = Group.all.find(g=>g.name===params.group);
Undo.initEdit({outliner:true, elements:[]});
const made = params.cubes.map(s => { const c = new Cube({name:s.name, from:s.from, to:s.to, box_uv:true}).addTo(grp).init(); c.applyTexture(Texture.all[0], true); return c.name; });
Canvas.updateAll(); Undo.finishEdit('add cubes quiet');
return made;
```
Después ejecuta **uv_firstfit** con esos nombres.

## add_cubes_mirror: todas las masas en una llamada (con espejo)
`params: {cubes:[[name, group, from, to, mirror?], ...]}`. Si `mirror:true`, crea también `right_*` en `right_*` con X negada. Usa tamaños enteros. Después: `pack_uv`, asignar la textura y `fix_z_fighting`.
```js
const grpOf = n => Group.all.find(g=>g.name===n);
Undo.initEdit({outliner:true, elements:[]});
const made=[];
const mk = (name, group, from, to) => { new Cube({name, from, to, box_uv:true}).addTo(grpOf(group)).init(); made.push(name); };
for (const [name, group, f, t, mirror] of params.cubes) {
  mk(name, group, f, t);
  if (mirror) mk(name.replace(/^left_/, 'right_'), group.replace(/^left_/, 'right_'), [-t[0], f[1], f[2]], [-f[0], t[1], t[2]]);
}
Canvas.updateAll(); Undo.finishEdit('primary masses');
return {count: made.length, total: Cube.all.length};
```

## verts: posición fiable de un cubo durante una animación
`Box3.setFromObject` falla mientras hay una animación activa. Usa los vértices:
```js
const C = n => Cube.all.find(c=>c.name===n);
const verts = n => { const m=C(n).mesh; m.updateMatrixWorld(true); const p=m.geometry.attributes.position, out=[]; for(let i=0;i<p.count;i++) out.push(new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(m.matrixWorld)); return out; };
const center = n => { const v=verts(n); const c=new THREE.Vector3(); v.forEach(x=>c.add(x)); return c.multiplyScalar(1/v.length); };
// punta de un cubo que apunta a -Z (lengua): vértices con z mínimo
// const v=verts('tongue_main'); const zmin=Math.min(...v.map(p=>p.z)); const tip=v.filter(p=>p.z<zmin+1.2);
```
Para colocar una pieza animada (baba, objeto) en un punto: añade un keyframe temporal de `position`, recorre y/z en pasos de 0.5, quédate con el que deja `center(cubo)` más cerca del objetivo y luego borra el keyframe.

## uv_firstfit: UV en huecos libres sin mover los existentes
`params: {names:["cubo_nuevo_1","cubo_nuevo_2"]}`. Si devuelve `NO SPACE`, la textura está llena: avisa al usuario.
```js
const newN = params.names;
const W=Project.texture_width, H=Project.texture_height; const occ = Array.from({length:H},()=>new Uint8Array(W));
const dims = c => { const s=c.size().map(Math.round); return [2*(s[0]+s[2]), s[1]+s[2]]; };
const mark = (x,y,w,h)=>{ for(let j=Math.max(0,y-1);j<Math.min(H,y+h+1);j++) for(let i=Math.max(0,x-1);i<Math.min(W,x+w+1);i++) occ[j][i]=1; };
Cube.all.filter(c=>!newN.includes(c.name)).forEach(c=>{ if (c.box_uv) { const [w,h]=dims(c); mark(c.uv_offset[0],c.uv_offset[1],w,h); } else { for (const f in c.faces) { const u=c.faces[f].uv; if(!u) continue; mark(Math.floor(Math.min(u[0],u[2])),Math.floor(Math.min(u[1],u[3])),Math.ceil(Math.abs(u[2]-u[0])),Math.ceil(Math.abs(u[3]-u[1]))); } } });
const free=(x,y,w,h)=>{ if(x+w>W||y+h>H) return false; for(let j=y;j<y+h;j++) for(let i=x;i<x+w;i++) if(occ[j][i]) return false; return true; };
Undo.initEdit({elements: Cube.all});
const placed=[];
Cube.all.filter(c=>newN.includes(c.name)).sort((a,b)=>dims(b)[0]*dims(b)[1]-dims(a)[0]*dims(a)[1]).forEach(c=>{
  const [w,h]=dims(c); let done=false;
  for(let y=0;y<H&&!done;y++) for(let x=0;x<W&&!done;x++) if(free(x,y,w,h)){ c.uv_offset=[x,y]; mark(x,y,w,h); placed.push([c.name,x,y]); done=true; }
  if(!done) placed.push([c.name,'NO SPACE']);
});
Canvas.updateAll(); Undo.finishEdit('relocate new UVs');
return placed;
```

## axis_probe: confirmar los signos de rotación y posición
Ajusta los nombres de huesos y cubos (`nose`, `left_boot`, `right_glove` y un ojo).
```js
const G = n => Group.all.find(g=>g.name===n), C = n => Cube.all.find(c=>c.name===n);
const wp = n => { const v=new THREE.Vector3(); C(n).mesh.getWorldPosition(v); return [+v.x.toFixed(1),+v.y.toFixed(1),+v.z.toFixed(1)]; };
const probe = (bone, ch, val, cube) => {
  const a = new Animation({name:'tmp_probe', length:1}).add(true); a.select();
  Timeline.setTime(0); Animator.preview(); const before = wp(cube);
  a.getBoneAnimator(G(bone)).addKeyframe({channel:ch,time:0,data_points:[{x:val[0],y:val[1],z:val[2]}]});
  Timeline.setTime(0); Animator.preview(); const after = wp(cube);
  a.remove(true); Animator.preview(); return {bone, ch, val, before, after};
};
return [probe('head','rotation',[30,0,0],'nose'), probe('left_leg','rotation',[30,0,0],'left_boot'), probe('right_arm','rotation',[0,0,90],'right_glove')];
```
Resultado con Santa: cabeza X+ = mira arriba; pierna o brazo X+ = hacia adelante; brazo derecho Z+ = se levanta hacia +X (el izquierdo usa Z−); posición Z− = adelante, X+ = hacia +X.

## pose_search: ángulos para llevar una mano o un objeto a un punto
`params: {upper:"right_arm", lower:"right_forearm", effector:"right_glove", target:[7,33,-14], ranges:{ax:[-10,0,10,20,30,40], ay:[-40,-20,0], az:[0,-15,-30,-45], fx:[40,60,80,100,120], fy:[0,-25,-50,-75]}}`
```js
const G = n => Group.all.find(g=>g.name===n), C = n => Cube.all.find(c=>c.name===n);
const a = new Animation({name:'tmp_search', length:1}).add(true); a.select();
const k1 = a.getBoneAnimator(G(params.upper)).addKeyframe({channel:'rotation',time:0,data_points:[{x:0,y:0,z:0}]});
const k2 = a.getBoneAnimator(G(params.lower)).addKeyframe({channel:'rotation',time:0,data_points:[{x:0,y:0,z:0}]});
const eff = C(params.effector), box = new THREE.Box3(), T = new THREE.Vector3(...params.target), r = params.ranges;
let best=null;
for (const ax of r.ax) for (const ay of r.ay) for (const az of r.az) for (const fx of r.fx) for (const fy of r.fy) {
  Object.assign(k1.data_points[0],{x:ax,y:ay,z:az}); Object.assign(k2.data_points[0],{x:fx,y:fy,z:0});
  Animator.preview(); box.setFromObject(eff.mesh); const c = box.getCenter(new THREE.Vector3());
  const d = c.distanceTo(T);
  if (!best || d<best.d) best={d:+d.toFixed(2),upper:[ax,ay,az],lower:[fx,fy,0],at:[c.x,c.y,c.z].map(v=>+v.toFixed(1))};
}
a.remove(true); Animator.preview();
return best;
```
Para colocar un objeto oculto (`held_gift`) sobre la mano en una pose: misma idea, pero con la pose del brazo fija y buscando en `position` del hueso del objeto (x −8..8, y −10..10, z −10..10) hacia `centro_del_guante + [0,5,-1]`.

## make_anim: crear una animación desde una especificación
`params: {name:"animation.<mob_id>.laugh", length:1.5, loop:"loop"|"hold"|"once", spec:{bone:{rotation|position:[[t,x,y,z,"linear"?], ...]}}}`
```js
const G = n => Group.all.find(g=>g.name===n);
Animation.all.filter(a=>a.name===params.name).forEach(a=>a.remove(true));
const a = new Animation({name:params.name, length:params.length, loop:params.loop}).add(true);
for (const bone in params.spec) for (const ch in params.spec[bone]) {
  const an = a.getBoneAnimator(G(bone));
  for (const [t,x,y,z,interp] of params.spec[bone][ch]) an.addKeyframe({channel:ch, time:t, interpolation: interp||'catmullrom', data_points:[{x,y,z}]});
}
return a.name;
```
Consejos: una pieza que se mantiene fija usa los mismos valores en `0` y en `length`. Una expresión que aparece de golpe usa keyframes `linear` muy juntos (1.40 y 1.45). Los rebotes alternan valores A/B en tiempos `i*L/(2n)`.

## fix_loops: recortar keyframes pasados de length y cerrar bucles
```js
let fixed = 0;
for (const a of Animation.all) {
  for (const id in a.animators) {
    const an = a.animators[id];
    for (const ch of ['rotation','position','scale']) {
      const ks = (an[ch] || []).slice().sort((p,q)=>p.time-q.time);
      if (ks.length < 2) continue;
      const last = ks[ks.length-1], first = ks[0];
      if (last.time > a.length) { last.time = a.length; fixed++; }
      if (a.loop === 'loop' && Math.abs(last.time - a.length) < 1e-3 && first.time === 0) {
        const d = first.data_points[0];
        last.data_points[0].x = d.x; last.data_points[0].y = d.y; last.data_points[0].z = d.z; fixed++;
      }
    }
  }
}
Animator.preview();
return {fixed};
```

## export_geckolib: escribir geo.json y animation.json
`params: {geo:"C:\\...\\geckolib\\models\\entity\\<mob_id>.geo.json", anim:"C:\\...\\geckolib\\animations\\entity\\<mob_id>.animation.json"}`
```js
let geo = Codecs.bedrock.compile(); if (typeof geo !== 'string') geo = compileJSON(geo);
Blockbench.writeFile(params.geo, {content: geo, savetype:'text'});
const anim = compileJSON(Animator.buildFile(null, true));
Blockbench.writeFile(params.anim, {content: anim, savetype:'text'});
const g = JSON.parse(geo)['minecraft:geometry'][0], A = JSON.parse(anim).animations;
return {id: g.description.identifier, bones: g.bones.map(b=>b.name), anims: Object.keys(A).map(k=>k+':'+A[k].animation_length+':'+A[k].loop)};
```
Las carpetas de destino deben existir antes (`mkdir -p`).
