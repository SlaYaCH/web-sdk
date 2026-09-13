import { Container, Graphics, Rectangle, Sprite, Text, Texture, FillGradient } from 'pixi.js';

const C={plum:0x28182F,panel:0x3A2544,cream:0xFFF6EB,card:0xF5EADF,coral:0xEF6680,gold:0xCBA46B,outline:0x452F48};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const ease=v=>1-Math.pow(1-clamp(v),3);
const mix=(a,b,p)=>a+(b-a)*p;
function txt(s,size,color=C.cream){const t=new Text({text:s,style:{fontFamily:'Arial',fontSize:size,fontWeight:'bold',fill:color}});t.anchor.set(.5);return t;}
function card(root){root.addChild(new Graphics().roundRect(.5,.5,115,90,7).fill(C.card).stroke({color:C.outline,width:1}));}
const gradientCache=new Map();
function dome(colors){const key=colors.join();if(!gradientCache.has(key))gradientCache.set(key,new FillGradient({type:'radial',center:{x:.28,y:.22},innerRadius:0,outerCenter:{x:.48,y:.48},outerRadius:.7,colorStops:colors.map((color,i)=>({offset:i/(colors.length-1),color})),textureSize:64}));return gradientCache.get(key);}
function heartShape(g){return g.moveTo(0,-12).bezierCurveTo(-20,-34,-38,-4,0,26).bezierCurveTo(38,-4,20,-34,0,-12).closePath();}
function heart(scale=1,color=C.coral){const g=heartShape(new Graphics()).fill(color).stroke({color:C.gold,width:1.2});g.scale.set(scale);return g;}
function poses(sheet,prefix){
 const root=new Container(),old=new Sprite(sheet.textures[`${prefix}-00`]),now=new Sprite(sheet.textures[`${prefix}-00`]);old.scale.set(.5);now.scale.set(.5);root.addChild(old,now);
 return {root,set(t,keys,blend=40){let k=0;for(let i=1;i<keys.length;i++)if(t>=keys[i][0])k=i;else break;const a=k===0?1:clamp((t-keys[k][0])/blend);old.texture=sheet.textures[`${prefix}-${String(keys[Math.max(0,k-1)][1]).padStart(2,'0')}`];now.texture=sheet.textures[`${prefix}-${String(keys[k][1]).padStart(2,'0')}`];old.alpha=a<1?1:0;now.alpha=a;return keys[k][1];}};
}

export const PORTRAIT_DURATION=2500;
export const PORTRAIT_TIMING=[[0,0],[400,1],[450,2],[530,1],[580,0],[850,3],[1010,4],[1210,5],[1840,4],[2020,3],[2200,0]];
export function createPortraitAnimation(sheet,id,{background=true}={}){
 if(!['h1','h2','h4','h5','h6'].includes(id))throw new Error('Unknown portrait id');
 const root=new Container();root.boundsArea=new Rectangle(0,0,116,91);if(background)card(root);
 const layer=poses(sheet,id);root.addChild(layer.root);
 // Indigo completes her wink before the single head tilt; no second wink on return.
 const keys=id==='h1'?[[0,0],[380,1],[460,0],[700,2],[970,3],[1230,4],[1700,5],[2100,3],[2260,2],[2420,0]]:id==='h5'?[[0,0],[400,1],[450,2],[530,1],[580,0],[850,3],[1010,4],[1210,5],[2050,0]]:PORTRAIT_TIMING;
 const api={root,duration:2500,seek(ms){const t=clamp(ms,0,2500);return {frame:layer.set(t,keys,t<700?1:40),done:t>=2500};}};api.seek(0);return api;
}

export const SUPERLIKE_CYCLE=820;
export const SUPERLIKE_START=550;
export const SUPERLIKE_RELEASE=390;
export const SUPERLIKE_IMPACT=710;
/** Target positions are in banner-local coordinates; negative x means left of it.
 * root = banner artwork; fx = projectiles, to add as a SIBLING in the same coordinates.
 * seek is pure: it returns impacts without mutating game state or firing callbacks.
 */
export function createSuperLikeAnimation(sheet,basketTexture,{targets,multiplier=null,background=true,displayValues=false,drawHearts=false}={}){
 if(!Array.isArray(targets)||targets.length<1||targets.length>6||targets.some(t=>!Number.isFinite(t.x)||!Number.isFinite(t.y)))throw new Error('Supply 1 to 6 finite target positions.');
 const dest=targets.map((t,i)=>({...t,index:i,direction:t.x<58?'left':'right'}));
 const root=new Container(),fx=new Container();root.boundsArea=new Rectangle(0,0,116,455);
 if(background){root.addChild(new Graphics().roundRect(.6,.6,114.8,453.8,10).fill(C.plum).stroke({color:C.gold,width:1.2}),new Graphics().roundRect(4,4,108,447,8).stroke({color:C.coral,width:1}));}
 const title=txt('SUPER',18);title.position.set(58,25);const title2=txt('LIKE',18);title2.position.set(58,45);root.addChild(title,title2);
 const multi=txt(`\u00d7${multiplier}`,25);multi.position.set(58,76);multi.visible=displayValues&&multiplier!==null;root.addChild(multi);
 const layer=poses(sheet,'superlike');layer.root.position.set(4,96);layer.root.scale.set(108/116);root.addChild(layer.root);
 const basket=new Sprite(basketTexture);basket.scale.set(.5);basket.position.set(9,230);root.addChild(basket);
 const slots=[{x:54,y:284},{x:36,y:284},{x:72,y:284},{x:62,y:275},{x:44,y:275},{x:80,y:275}];
 const charges=slots.map((p,i)=>{const h=heart(.25);h.position.set(p.x,p.y);root.addChild(h);return h;});
 const frontTexture=new Texture({source:basketTexture.source,frame:new Rectangle(0,112,196,64)});
 const front=new Sprite(frontTexture);front.scale.set(.5);front.position.set(9,286);root.addChild(front);
 const held=heart(.29);root.addChild(held);
 const counter=txt('',15);counter.position.set(58,346);counter.visible=displayValues;root.addChild(counter);
 const ornament=new Graphics().moveTo(29,374).lineTo(87,374).stroke({color:C.gold,width:1,alpha:.55});root.addChild(ornament);
 const logoHeart=heart(.24);logoHeart.position.set(58,406);root.addChild(logoHeart);
 const bullet=heart(.3),trail=new Graphics(),impact=new Graphics();fx.addChild(trail,bullet,impact);
 const pickup={x:44,y:233},lift={x:46,y:179},wind={left:{x:19,y:136},right:{x:35,y:178}},release={left:{x:16,y:154},right:{x:96,y:151}};
 const duration=SUPERLIKE_START+dest.length*SUPERLIKE_CYCLE+220;
 function flight(start,end,p){const cx=mix(start.x,end.x,.48),cy=Math.min(start.y,end.y)-42;return{x:(1-p)*(1-p)*start.x+2*(1-p)*p*cx+p*p*end.x,y:(1-p)*(1-p)*start.y+2*(1-p)*p*cy+p*p*end.y};}
 const api={root,fx,duration,count:dest.length,targets:dest,seek(ms){
  const t=clamp(ms,0,duration),raw=(t-SUPERLIKE_START)/SUPERLIKE_CYCLE,index=Math.floor(raw),q=t-SUPERLIKE_START-index*SUPERLIKE_CYCLE;
  const active=index>=0&&index<dest.length,shot=active?dest[index]:null,dir=shot?.direction||'left';
  const picked=clamp(Math.floor((t-SUPERLIKE_START-70)/SUPERLIKE_CYCLE)+1,0,dest.length);
  charges.forEach((h,i)=>{h.visible=drawHearts&&i<dest.length&&i>=picked;});
  held.visible=drawHearts&&active&&q>=70&&q<SUPERLIKE_RELEASE;
  bullet.visible=drawHearts&&active&&q>=SUPERLIKE_RELEASE&&q<SUPERLIKE_IMPACT;trail.clear();impact.clear();
  let pose=0;
  if(active){
   const keys=[[0,0],[45,1],[160,2],[265,dir==='left'?3:6],[390,dir==='left'?4:7],[535,dir==='left'?5:8],[735,0]];
   pose=layer.set(q,keys,35);
   if(held.visible){
    let a,b,p;if(q<160){a=slots[index];b=pickup;p=ease((q-70)/90);}else if(q<265){a=pickup;b=lift;p=ease((q-160)/105);}else if(q<325){a=lift;b=wind[dir];p=ease((q-265)/60);}else{a=wind[dir];b=release[dir];p=ease((q-325)/65);}
    held.position.set(mix(a.x,b.x,p),mix(a.y,b.y,p));held.rotation=0;
   }
   if(bullet.visible){const p=clamp((q-SUPERLIKE_RELEASE)/(SUPERLIKE_IMPACT-SUPERLIKE_RELEASE));const pt=flight(release[dir],shot,p);bullet.position.set(pt.x,pt.y);bullet.rotation=(dir==='left'?-1:1)*.15*Math.sin(Math.PI*p);const prev=flight(release[dir],shot,Math.max(0,p-.12));trail.moveTo(prev.x,prev.y).lineTo(pt.x,pt.y).stroke({color:C.coral,width:2,alpha:.35});}
  }else layer.set(0,[[0,0]]);
  const hits=dest.filter((_,i)=>t>=SUPERLIKE_START+i*SUPERLIKE_CYCLE+SUPERLIKE_IMPACT).map(v=>v.index);
  // Short, local impact; no screen shake and no overlapping projectiles.
  for(const hit of hits){const age=t-(SUPERLIKE_START+hit*SUPERLIKE_CYCLE+SUPERLIKE_IMPACT);if(age<180){const p=age/180;impact.circle(dest[hit].x,dest[hit].y,6+16*ease(p)).stroke({color:C.cream,width:2*(1-p),alpha:1-p});}}
  counter.text=`${dest.length-picked} / ${dest.length}`;
  return {pose,remaining:dest.length-picked,picked,impacts:hits,activeIndex:active?index:null,direction:active?dir:null,projectiles:bullet.visible?1:0,held:held.visible,done:t>=duration};
 },destroy(){root.destroy({children:true});fx.destroy({children:true});frontTexture.destroy(false);}};
 api.seek(0);return api;
}

export const LOW_DURATION=1200;
export function createLowAnimation(kind,{background=true}={}){
 if(!['verified','message','flame','heart'].includes(kind))throw new Error('Unknown low symbol');
 const root=new Container();root.boundsArea=new Rectangle(0,0,116,91);if(background)card(root);
 const shape=new Container();root.addChild(shape);const body=new Graphics(),detail=new Graphics();shape.addChild(body,detail);
 const dots=[];const core=new Graphics();
 if(kind==='verified')body.circle(58,45,25).fill(dome([0xB6E5CF,0x55B59C,0x237160])).stroke({color:C.outline,width:1.5});
 if(kind==='message'){
  body.moveTo(39,21).lineTo(77,21).bezierCurveTo(84,21,87,25,87,32).lineTo(87,53).bezierCurveTo(87,60,83,63,77,63).lineTo(48,63).lineTo(35,71).lineTo(35,62).bezierCurveTo(31,61,29,57,29,53).lineTo(29,32).bezierCurveTo(29,25,32,21,39,21).closePath().fill(dome([0xE1D7FA,0xA38BDA,0x655098])).stroke({color:C.outline,width:1.5});
  for(let i=0;i<3;i++){const d=new Graphics().circle(0,0,2.6).fill(C.cream);d.position.set(44+i*14,42);shape.addChild(d);dots.push(d);}
 }
 if(kind==='flame'){
  body.moveTo(57,16).bezierCurveTo(61,31,38,33,37,50).bezierCurveTo(34,63,44,74,58,74).bezierCurveTo(76,74,85,58,77,43).bezierCurveTo(74,38,73,37,72,35).bezierCurveTo(72,43,67,45,65,46).bezierCurveTo(70,32,65,23,57,16).closePath().fill(dome([0xFFE1A5,0xF2A05B,0xBF542D])).stroke({color:C.outline,width:1.5});
  core.moveTo(59,43).bezierCurveTo(59,53,47,54,48,62).bezierCurveTo(49,74,69,71,69,61).bezierCurveTo(69,55,63,49,59,43).closePath().fill(dome([0xFFF5D5,0xFFD19A,0xF5AC55]));shape.addChild(core);core.pivot.set(58,73);core.position.set(58,73);
 }
 if(kind==='heart'){
  const h=heartShape(new Graphics()).fill(dome([0xFFD5DE,0xEF7893,0xAD365C])).stroke({color:0xB24F70,width:1.3});h.scale.set(1.12);h.position.set(58,44);shape.addChild(h);
 }
 const gloss=new Graphics();
 if(kind==='verified')gloss.moveTo(39,38).bezierCurveTo(41,29,48,24,57,24).stroke({color:0xFFFFFF,width:2.3,alpha:.55,cap:'round'});
 if(kind==='message')gloss.moveTo(35,35).lineTo(35,31).quadraticCurveTo(35,27,42,27).lineTo(64,27).stroke({color:0xFFFFFF,width:2,alpha:.55,cap:'round'});
 if(kind==='flame')gloss.moveTo(43,52).quadraticCurveTo(45,43,53,37).stroke({color:0xFFF7DF,width:2.2,alpha:.6,cap:'round'});
 if(kind==='heart')gloss.moveTo(37,34).bezierCurveTo(39,26,47,26,51,30).stroke({color:0xFFFFFF,width:2.5,alpha:.6,cap:'round'});
 shape.addChild(gloss);
 shape.pivot.set(58,kind==='flame'?74:45.5);shape.position.set(58,kind==='flame'?74:45.5);
 const api={root,duration:LOW_DURATION,seek(ms){const t=clamp(ms,0,LOW_DURATION);shape.scale.set(1);shape.rotation=0;detail.clear();
  if(kind==='verified'){
   const p=t===0||t>=600?1:ease((t-60)/220);const pts=[[44,45],[53,53],[72,35]],l1=Math.hypot(9,8),l2=Math.hypot(19,-18),d=p*(l1+l2);
   if(p>0){detail.moveTo(...pts[0]);if(d<=l1)detail.lineTo(mix(44,53,d/l1),mix(45,53,d/l1));else detail.lineTo(53,53).lineTo(mix(53,72,(d-l1)/l2),mix(53,35,(d-l1)/l2));detail.stroke({color:C.cream,width:4.5,cap:'round',join:'round'});}
   const pulse=.045*Math.sin(Math.PI*clamp((t-170)/400));shape.scale.set(1+pulse);
  }
  if(kind==='message')dots.forEach((d,i)=>{const p=clamp((t-100-i*135)/280);d.y=42-3*Math.sin(Math.PI*p);d.alpha=.78+.22*Math.sin(Math.PI*p);});
  if(kind==='flame'){const e=Math.sin(Math.PI*clamp(t/850));shape.rotation=.03*Math.sin(t/110)*e;shape.scale.y=1+.05*e;core.scale.set(1+.07*e,1+.1*Math.sin(t/95)*e);}
  if(kind==='heart'){const beat=.09*Math.exp(-Math.pow((t-190)/65,2))+.06*Math.exp(-Math.pow((t-380)/70,2));shape.scale.set(1+beat);}
  return {kind,done:t>=LOW_DURATION};}};api.seek(0);return api;
}

/** WILD and DATE: raised surfaces, fixed upper-left light, one event-driven reaction. */
export function createSpecialAnimation(kind,{background=true}={}){
 if(!['wild','date'].includes(kind))throw Error('Unknown special');
 const root=new Container();root.boundsArea=new Rectangle(0,0,116,91);if(background)card(root);
 const shape=new Container();shape.position.set(58,44);root.addChild(shape);
 const sparkle=new Graphics();root.addChild(sparkle);let left,right;
 if(kind==='wild'){
  const shadow=heartShape(new Graphics()).fill(0x452F48);shadow.scale.set(1.4,1.24);shadow.position.set(2,5);shadow.alpha=.22;shape.addChild(shadow);
  const h=heartShape(new Graphics()).fill(dome([0xFFE2EA,0xF16C95,0x9B2957])).stroke({color:0xCBA46B,width:3});h.scale.set(1.4,1.24);shape.addChild(h);
  shape.addChild(new Graphics().moveTo(-28,-8).lineTo(-12,-22).lineTo(0,-12).lineTo(12,-22).lineTo(28,-8).lineTo(0,27).closePath().stroke({color:0xFFD9E4,width:.8,alpha:.5}));
  const t=txt('WILD',18,0xFFF6EB);t.position.set(0,3);t.style.stroke={color:0x743248,width:2};shape.addChild(t);
 }else{
  function glass(x,sign){const c=new Container();c.position.set(x,18);const g=new Graphics();g.moveTo(-15,-42).lineTo(15,-42).bezierCurveTo(14,-25,9,-17,0,-17).bezierCurveTo(-9,-17,-14,-25,-15,-42).closePath().fill(dome([0xFFFDF4,0xEAC5BD,0x96758E])).stroke({color:0x997782,width:1});g.moveTo(-12,-34).lineTo(12,-34).bezierCurveTo(10,-23,6,-20,0,-20).bezierCurveTo(-6,-20,-10,-23,-12,-34).closePath().fill(dome([0xFFC6CD,0xED7C9F,0xA94470]));g.moveTo(0,-17).lineTo(0,0).stroke({color:0xCBA46B,width:2.5});g.ellipse(0,1,12,2.5).fill(0xCBA46B);g.moveTo(-10,-39).quadraticCurveTo(-9,-29,-6,-26).stroke({color:0xFFFFFF,width:2,alpha:.85,cap:'round'});c.addChild(g);shape.addChild(c);return c;}
  left=glass(-19,-1);right=glass(19,1);const title=txt('DATE',15,0xA44366);title.position.set(0,33);shape.addChild(title);
 }
 const duration=1500;
 const api={root,duration,seek(ms){const t=clamp(ms,0,duration);sparkle.clear();shape.scale.set(1);
  if(kind==='wild'){const p=Math.sin(Math.PI*clamp((t-100)/550));shape.scale.set(1+.085*p);const q=Math.sin(Math.PI*clamp((t-350)/550));if(q>0){const x=37+40*clamp((t-350)/550),y=25;sparkle.moveTo(x-5*q,y).lineTo(x+5*q,y).moveTo(x,y-5*q).lineTo(x,y+5*q).stroke({color:0xFFF6EB,width:1.5,alpha:q});}}
  else{const p=t<420?ease((t-120)/300):1-ease((t-610)/410);left.rotation=.095*p;right.rotation=-.095*p;left.x=-19+.1*p;right.x=19-.1*p;const q=Math.sin(Math.PI*clamp((t-420)/220));if(q>0)sparkle.moveTo(58,10-5*q).lineTo(58,10-10*q).moveTo(48,14).lineTo(44,10).moveTo(68,14).lineTo(72,10).stroke({color:0xCBA46B,width:1.5,alpha:q});}
  return {kind,done:t>=duration};}};api.seek(0);return api;
}

