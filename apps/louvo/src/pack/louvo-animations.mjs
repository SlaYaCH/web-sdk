import { Container, Graphics, Rectangle, Sprite, Text } from 'pixi.js';

export const MATCH_DURATION = 2400;
export const SHANNA_DURATION = 2500;
export const MATCH_TIMING = {
  higher: [[0, 0], [500, 1], [640, 2], [800, 3], [960, 4]],
  lower: [[0, 0], [500, 6], [690, 7], [880, 8], [1080, 9]],
};
export const SHANNA_TIMING = [[0,0],[420,1],[465,2],[540,3],[590,0],[840,4],[980,5],[1120,6],[1820,5],[1960,4],[2100,0]];
const P = { dark: 0x28182F, panel: 0x3A2544, cream: 0xFFF6EB, card: 0xF5EADF, coral: 0xEF6680, gold: 0xCBA46B, muted: 0xB9A8BC };
const clamp = (v,a=0,b=1) => Math.max(a,Math.min(b,v));
const ease = v => 1-Math.pow(1-clamp(v),3);

function label(text,size,color=P.cream) {
  const t=new Text({text,style:{fontFamily:'Arial',fontSize:size,fontWeight:'bold',fill:color}});
  t.anchor.set(.5);return t;
}
function poseLayer(sheet,prefix) {
  const root=new Container();
  const old=new Sprite(sheet.textures[`${prefix}-00`]);
  const current=new Sprite(sheet.textures[`${prefix}-00`]);
  old.scale.set(.5);current.scale.set(.5);root.addChild(old,current);
  return {root,old,current,set(t,keys,blend=45){
    let k=0;for(let i=1;i<keys.length;i++)if(t>=keys[i][0])k=i;else break;
    const prev=keys[Math.max(0,k-1)][1];const next=keys[k][1];
    const a=k===0?1:clamp((t-keys[k][0])/blend);
    old.texture=sheet.textures[`${prefix}-${String(prev).padStart(2,'0')}`];
    current.texture=sheet.textures[`${prefix}-${String(next).padStart(2,'0')}`];
    // Short pose dissolve, not optical-flow interpolation or a skeletal rig.
    old.alpha=a<1?1:0;current.alpha=a;
    return next;
  }};
}
function heartPath(g,part='whole') {
  g.moveTo(0,-12);
  if(part==='whole'){
    g.bezierCurveTo(-20,-34,-38,-4,0,26).bezierCurveTo(38,-4,20,-34,0,-12).closePath();
  } else {
    if(part==='left')g.bezierCurveTo(-20,-34,-38,-4,0,26);
    else g.bezierCurveTo(20,-34,38,-4,0,26);
    g.lineTo(-2,15).lineTo(3,7).lineTo(-3,-1).lineTo(2,-7).lineTo(0,-12).closePath();
  }
  return g;
}
function heart(part='whole',color=P.coral) {
  return heartPath(new Graphics(),part).fill(color).stroke({color:P.gold,width:1.15});
}

/** Pure presentation. `higher` = larger multiplier wins; `lower` = smaller wins.
 * No RNG, no bet logic, no payout calculation. Call seek from your own timeline.
 * Loaded spritesheet textures are shared; destroying this view does not unload them.
 */
export function createMatchAnimation(sheet,{small,large,background=true,displayValues=false}={}) {
  if(!(Number.isFinite(small)&&Number.isFinite(large)&&small>0&&large>small))throw new Error('Expected 0 < small < large.');
  const root=new Container();
  root.boundsArea=new Rectangle(0,0,116,455);
  if(background){
    root.addChild(new Graphics().roundRect(.6,.6,114.8,453.8,10).fill(P.dark).stroke({color:P.gold,width:1.2}));
    root.addChild(new Graphics().roundRect(4,4,108,447,8).stroke({color:P.coral,width:1}));
  }
  const title=label('MATCH',20);title.position.set(58,26);root.addChild(title);
  const pills=[new Graphics(),new Graphics()];
  const values=[label(`×${small}`,18),label(`×${large}`,18)];
  values.forEach(v=>v.visible=displayValues);
  pills.forEach((p,i)=>{p.visible=displayValues;p.roundRect(10+i*52,43,44,29,7).fill(P.panel);root.addChild(p);values[i].position.set(32+i*52,57.5);root.addChild(values[i]);});
  const layer=poseLayer(sheet,'match');layer.root.position.set(4,87);layer.root.scale.set(108/116);root.addChild(layer.root);
  const line=new Graphics().moveTo(16,302).lineTo(100,302).stroke({color:P.gold,width:.7,alpha:.45});root.addChild(line);
  const heartRoot=new Container();heartRoot.position.set(58,342);root.addChild(heartRoot);
  const halos=[1.85,1.5,1.25].map(s=>{const h=heartPath(new Graphics()).fill(P.coral);h.scale.set(s);heartRoot.addChild(h);return h;});
  const intact=heart();const left=heart('left');const right=heart('right');heartRoot.addChild(intact,left,right);
  const flecks=new Graphics();heartRoot.addChild(flecks);
  const result=label('',32);result.visible=displayValues;result.position.set(58,408);root.addChild(result);
  const under=new Graphics().moveTo(34,434).lineTo(82,434).stroke({color:P.gold,width:1,alpha:.55});root.addChild(under);
  const api={root,duration:MATCH_DURATION,seek(ms,outcome='higher'){
    if(outcome!=='higher'&&outcome!=='lower')throw new Error('outcome must be higher or lower.');
    const t=clamp(ms,0,MATCH_DURATION),high=outcome==='higher';
    const frame=layer.set(t,MATCH_TIMING[outcome],45);
    const winner=high?1:0;
    pills.forEach((p,i)=>{p.clear().roundRect(10+i*52,43,44,29,7).fill(t>=460&&i===winner?P.cream:P.panel);values[i].style.fill=t>=460&&i===winner?P.dark:P.cream;});
    const hit=high?820:1100;
    const v=clamp((t-hit)/310);
    const pulse=high&&t>=hit?1+.08*Math.exp(-(t-hit)/320)*Math.sin((t-hit)/65):1;
    intact.scale.set(pulse);intact.visible=high||t<hit;
    left.visible=right.visible=!high&&t>=hit;
    const split=ease(v);
    left.position.set(-9*split,4*split);right.position.set(9*split,4*split);
    left.rotation=-.2*split;right.rotation=.2*split;
    left.alpha=right.alpha=1-.16*split;
    halos.forEach((h,i)=>{h.alpha=high&&t>=hit?(0.035+i*.032)*(0.65+0.35*Math.exp(-(t-hit)/650)):0;h.scale.set([1.85,1.5,1.25][i]*pulse);});
    flecks.clear();
    if(t>=hit&&t<hit+580){
      const q=clamp((t-hit)/580);
      for(let i=0;i<8;i++){
        const a=i*Math.PI/4+.18;
        const x=Math.cos(a)*(23+22*ease(q));const y=Math.sin(a)*(24+18*ease(q));
        const r=(high?2.2:1.6)*(1-q);
        flecks.poly([x,y-r,x+r*.6,y,x,y+r,x-r*.6,y]).fill({color:high?P.cream:P.coral,alpha:1-q});
      }
    }
    result.text=t>=hit?`×${high?large:small}`:'';
    result.alpha=ease((t-hit)/160);result.y=408+6*(1-ease((t-hit)/180));
    return {frame,outcome,heart:high?(t>=hit?'illuminated':'intact'):(t>=hit?'torn':'intact'),winner:t>=460?(high?large:small):null,done:t>=MATCH_DURATION};
  }};
  api.seek(0);return api;
}

export function createShannaAnimation(sheet,{background=true}={}) {
  const root=new Container();
  if(background)root.addChild(new Graphics().roundRect(.5,.5,115,90,7).fill(P.card).stroke({color:P.dark,width:1}));
  const layer=poseLayer(sheet,'shanna');root.addChild(layer.root);
  const api={root,duration:SHANNA_DURATION,seek(ms){
    const t=clamp(ms,0,SHANNA_DURATION);
    // Blinks are discrete drawn poses, smile transitions have a short dissolve.
    const frame=layer.set(t,SHANNA_TIMING,t<700?1:40);
    return {frame,done:t>=SHANNA_DURATION};
  }};
  api.seek(0);return api;
}
