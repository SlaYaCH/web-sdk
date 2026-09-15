import {Container,Sprite,Rectangle,Graphics} from 'pixi.js';

export const SIDE_CHARACTER_SIZE={width:320,height:600};
function gesture(first,step,hold){const a=[[0,0]];for(let i=0;i<9;i++)a.push([(i+1)*step,first+i]);const peak=9*step;for(let i=7;i>=0;i--)a.push([peak+hold+(8-i)*step,first+i]);a.push([peak+hold+9*step,0]);return a;}
export const SIDE_REACTION_TIMINGS={
 win:gesture(2,65,280),celebrate:gesture(2,80,650),noWin:gesture(11,70,300),
 frustrated:[[0,0],[100,20],[200,21],[330,22],[460,23],[600,24],[760,25],[910,26],[1210,27],[1450,28],[1650,0]],
 bonus:[[0,0],[80,29],[220,30],[360,31],[500,32],[620,33],[690,34],[750,35],[810,36],[860,37],[970,36],[1030,35],[1090,34],[1150,33],[1240,34],[1300,35],[1360,36],[1410,37],[1520,36],[1580,35],[1640,34],[1700,33],[1790,34],[1850,35],[1910,36],[1960,37],[2110,36],[2180,35],[2250,34],[2320,33],[2410,32],[2500,31],[2620,30],[2740,29],[2880,0]]
};
export const SIDE_REACTION_DURATION={win:1550,celebrate:2230,noWin:1660,frustrated:1850,bonus:3080};
export const SIDE_IDLE_TIMINGS=[[0,0]];
export const SIDE_INSO_IDLE_TIMINGS=[[0,0]];
const clamp=v=>Math.max(0,Math.min(1,v));
function sample(keys,age,blendMs){let k=0;for(let i=1;i<keys.length;i++)if(age>=keys[i][0])k=i;else break;return{index:keys[k][1],prev:keys[Math.max(0,k-1)][1],alpha:k===0?1:clamp((age-keys[k][0])/blendMs)};}
function character(sheet,prefix,phase){
 const root=new Container();root.boundsArea=new Rectangle(-160,-790,320,790);
 const shadow=new Graphics();for(let i=3;i>0;i--)shadow.ellipse(0,-7,(prefix==='ler'?64:43)+i*5,5+i*2).fill({color:0x28182F,alpha:.045});root.addChild(shadow);
 const body=new Container();root.addChild(body);
 const before=new Sprite(),after=new Sprite();body.addChild(before,after);
 // Closed-eye art is masked to each eye; the face and body never change at rest.
 const eyes=[];
 const centers=prefix==='ler'?[[91,56],[109,56]]:[[97,57],[113,57]];
 for(const [x,y] of centers){
  const lid=new Sprite(sheet.textures[prefix+'-01']);lid.position.set(-160,-600);lid.scale.set(1.6);
  const mask=new Graphics().ellipse(-160+x*1.6,-600+y*1.6,9.6,6.4).fill(0xffffff);
  body.addChild(lid,mask);lid.mask=mask;lid.alpha=0;eyes.push(lid);
 }
 function pulse(t,start,duration){if(t<start||t>=start+duration)return 0;return Math.min(1,(t-start)/65,(start+duration-t)/85);}
 function pose({index,prev=index,alpha=1}){
  for(const [s,i] of [[before,prev],[after,index]]){const t=sheet.textures[prefix+'-'+String(i).padStart(2,'0')];if(!t)throw Error('Missing '+prefix+' frame '+i);s.texture=t;s.scale.set(1.6);s.position.set(-160,-t.orig.height*1.6);}
  before.alpha=alpha<1?1:0;after.alpha=alpha;
 }
 return {root,seek(ms,reaction,reducedMotion){
  // Fixed body at rest, only masked eyelids may move.
  for(const eye of eyes)eye.alpha=0;
  body.position.set(0,0);body.scale.set(1);shadow.scale.set(1);shadow.alpha=1;
  if(reducedMotion){pose({index:0});return{frame:0,reaction:null,jumpY:0};}
  if(reaction&&ms>=reaction.start){
   
   const age=ms-reaction.start,p=sample(SIDE_REACTION_TIMINGS[reaction.kind],age,reaction.kind==='bonus'?(age<620||age>=2410?110:45):reaction.kind==='frustrated'?45:40);
   pose(p);return{frame:p.index,reaction:reaction.kind,jumpY:body.y};
  }
  pose({index:0});
  const blink=pulse((ms+phase)%6500,4800,230);
  const wink=prefix==='inso'?pulse(ms%21000,14500,360):0;
  eyes[0].alpha=Math.max(blink,wink);eyes[1].alpha=blink;
  return{frame:0,reaction:null,jumpY:0,blink,wink};
 }};
}
/** Rendering only. Use the separate director for frequency and result filtering. */
export function createSideCharacters(sheets,options={}){
 if(!sheets?.ler||!sheets?.inso)throw Error('Load ler and inso spritesheets before creating side characters.');
 const root=new Container(),ler=character(sheets.ler,'ler',0),inso=character(sheets.inso,'inso',1900);root.addChild(ler.root,inso.root);
 const state={mode:options.mode??'base',isMobile:options.isMobile??false,reducedMotion:options.reducedMotion??false};
 const reactions={ler:null,inso:null};let now=0;
 const visible=()=>!state.isMobile&&['base','speedDating'].includes(state.mode);
 function clear(){reactions.ler=null;reactions.inso=null;}
 const api={root,ler:ler.root,inso:inso.root,
  layout({left={x:240,y:795},right={x:1435,y:795},height=500}={}){const s=height/600;ler.root.position.set(left.x,left.y);inso.root.position.set(right.x,right.y);ler.root.scale.set(s);inso.root.scale.set(s);},
  setContext(next){Object.assign(state,next);root.visible=visible();if(!root.visible||state.reducedMotion)clear();return root.visible;},
  react(kind,startMs=now,{target='both',staggerMs=kind==='bonus'?120:kind==='frustrated'?160:0}={}){
   if(!Object.hasOwn(SIDE_REACTION_TIMINGS,kind))throw Error('Unknown side reaction: '+kind);
   if(!['both','ler','inso'].includes(target))throw Error('Invalid reaction target.');
   if(!visible()||state.reducedMotion)return false;
   if(kind!=='bonus'&&Object.values(reactions).some(r=>r?.kind==='bonus'&&now-r.start<SIDE_REACTION_DURATION.bonus))return false;
   if(target!=='inso')reactions.ler={kind,start:startMs};
   if(target!=='ler')reactions.inso={kind,start:startMs+(target==='both'?staggerMs:0)};
   return true;
  },
  reset(){clear();},
  seek(ms){now=ms;root.visible=visible();if(!root.visible)return{visible:false};for(const who of ['ler','inso'])if(reactions[who]&&ms-reactions[who].start>=SIDE_REACTION_DURATION[reactions[who].kind])reactions[who]=null;return{visible:true,ler:ler.seek(ms,reactions.ler,state.reducedMotion),inso:inso.seek(ms,reactions.inso,state.reducedMotion)};},
  destroy(){root.destroy({children:true});}
 };
 api.layout(options.layout);api.setContext(state);api.seek(0);return api;
}
