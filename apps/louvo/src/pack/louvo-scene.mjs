import {Container,Graphics,Text,Rectangle,Sprite,FillGradient,Filter,GlProgram,GpuProgram} from 'pixi.js';
const palette={plum:0x28182F,night:0x21132F,gold:0xCBA46B,coral:0xEF6680,cream:0xFFF6EB};
function label(text,size,color=palette.cream){const t=new Text({text,style:{fontFamily:'Arial',fontSize:size,fontWeight:'bold',fill:color}});t.anchor.set(.5);return t;}
function heart(g,x,y,s=1){return g.moveTo(x,y-8*s).bezierCurveTo(x-16*s,y-24*s,x-28*s,y-1*s,x,y+21*s).bezierCurveTo(x+28*s,y-1*s,x+16*s,y-24*s,x,y-8*s).closePath();}
/** Measured artwork openings, not assumed frontend cell geometry. Override from actual layout. */
export const FRAME_LAYOUT={base:{x:489,y:130,width:679,height:529},afterDark:{x:468,y:130,width:726,height:539}};
export const AMBIENCE_POINTS={
 base:{hearts:[[153,187],[442,152],[478,40],[677,48],[982,92],[1390,43]],candles:[[235,653],[536,648],[670,643],[1005,642],[1136,647],[1410,655],[1499,560]],city:[[290,534],[240,410],[286,428],[136,414],[250,536],[78,428],[328,532],[168,526],[336,468],[132,536],[246,466],[124,480],[46,412],[224,444],[370,428],[458,538],[368,536],[58,462],[398,524],[452,490],[338,412],[416,426],[436,450],[448,420],[1342,525]]},
 afterDark:{hearts:[[149,157],[307,100],[334,175],[440,225],[1288,158],[76,364],[61,552],[1624,477]],candles:[[149,723],[309,648],[348,642],[373,650],[458,667],[489,660],[1177,668],[1293,618],[1320,624],[1366,704],[1540,724]],city:[[274,282],[334,470],[224,326],[368,362],[172,348],[178,462],[128,396],[138,316],[404,474],[286,474],[188,316],[280,400],[222,464],[180,284],[370,394],[316,314],[364,474],[232,370],[444,472],[278,330],[228,270],[122,470],[372,432],[174,424],[1350,377]]}
};
const vertex=`precision highp float;in vec2 aPosition;out vec2 vTextureCoord;uniform vec4 uInputSize;uniform vec4 uOutputFrame;uniform vec4 uOutputTexture;void main(){vec2 p=aPosition*uOutputFrame.zw+uOutputFrame.xy;p.x=p.x*(2.0/uOutputTexture.x)-1.0;p.y=p.y*(2.0*uOutputTexture.z/uOutputTexture.y)-uOutputTexture.z;gl_Position=vec4(p,0.,1.);vTextureCoord=aPosition*(uOutputFrame.zw*uInputSize.zw);}`;

/** Same local displacement and protected wheel zone for Pixi's WebGPU filter pipeline. */
export function createSkyWgsl(points){
 const terms=points.map(([x,y],i)=>`let r${i}=(p-vec2<f32>(${x}.0,${y}.0))/48.0;d+=vec2<f32>(sin(skyUniforms.uTime*0.95+${(i*.8).toFixed(2)}),cos(skyUniforms.uTime*0.8+${(i*.7).toFixed(2)}))*vec2<f32>(7.0,9.0)*exp(-dot(r${i},r${i}));`).join('\n');
 return `
struct GlobalFilterUniforms {
 uInputSize:vec4<f32>, uInputPixel:vec4<f32>, uInputClamp:vec4<f32>,
 uOutputFrame:vec4<f32>, uGlobalFrame:vec4<f32>, uOutputTexture:vec4<f32>,
};
struct SkyUniforms { uTime:f32, };
@group(0) @binding(0) var<uniform> gfu:GlobalFilterUniforms;
@group(0) @binding(1) var uTexture:texture_2d<f32>;
@group(0) @binding(2) var uSampler:sampler;
@group(1) @binding(0) var<uniform> skyUniforms:SkyUniforms;
struct VSOutput { @builtin(position) position:vec4<f32>, @location(0) uv:vec2<f32>, };
@vertex
fn mainVertex(
  @location(0) aPosition : vec2<f32>,
) -> VSOutput {
 var position=aPosition*gfu.uOutputFrame.zw+gfu.uOutputFrame.xy;
 position.x=position.x*(2.0/gfu.uOutputTexture.x)-1.0;
 position.y=position.y*(2.0*gfu.uOutputTexture.z/gfu.uOutputTexture.y)-gfu.uOutputTexture.z;
 return VSOutput(vec4<f32>(position,0.0,1.0),aPosition*(gfu.uOutputFrame.zw*gfu.uInputSize.zw));
}
@fragment fn mainFragment(@location(0) coord:vec2<f32>)->@location(0) vec4<f32> {
 let p=coord*gfu.uInputSize.xy/gfu.uOutputFrame.zw*vec2<f32>(1672.0,941.0);
 var d=vec2<f32>(0.0);${terms}
 let outsideWheel=max(max(vec2<f32>(1370.0,260.0)-p,p-vec2<f32>(1550.0,530.0)),vec2<f32>(0.0));
 d*=smoothstep(0.0,20.0,length(outsideWheel));
 let uv=coord-d/vec2<f32>(1672.0,941.0)*gfu.uOutputFrame.zw*gfu.uInputSize.zw;
 return textureSample(uTexture,uSampler,clamp(uv,gfu.uInputClamp.xy,gfu.uInputClamp.zw));
}`;
}

/** Optional single-pass WebGL / WebGPU local warp: moves baked sky hearts by at most 9 source pixels. */
function skyFilter(points){const terms=points.map(([x,y],i)=>`d+=vec2(sin(uTime*.95+${(i*.8).toFixed(2)}),cos(uTime*.8+${(i*.7).toFixed(2)}))*vec2(7.,9.)*exp(-dot((p-vec2(${x}.0,${y}.0))/48.0,(p-vec2(${x}.0,${y}.0))/48.0));`).join('');
 const fragment=`precision highp float;in vec2 vTextureCoord;out vec4 finalColor;uniform sampler2D uTexture;uniform vec4 uInputSize;uniform vec4 uOutputFrame;uniform vec4 uInputClamp;uniform float uTime;void main(){vec2 p=vTextureCoord*uInputSize.xy/uOutputFrame.zw*vec2(1672.,941.);vec2 d=vec2(0.);${terms}vec2 outsideWheel=max(max(vec2(1370.,260.)-p,p-vec2(1550.,530.)),vec2(0.));d*=smoothstep(0.,20.,length(outsideWheel));vec2 uv=vTextureCoord-d/vec2(1672.,941.)*uOutputFrame.zw*uInputSize.zw;finalColor=texture(uTexture,clamp(uv,uInputClamp.xy,uInputClamp.zw));}`;
 const wgsl=createSkyWgsl(points);
 const gpuProgram=GpuProgram.from({vertex:{source:wgsl,entryPoint:'mainVertex'},fragment:{source:wgsl,entryPoint:'mainFragment'}});
 return new Filter({gpuProgram,glProgram:GlProgram.from({vertex,fragment}),resources:{skyUniforms:{uTime:{value:0,type:'f32'}}},resolution:1,padding:0});}
export function createAmbience(texture,{mode='base',skyMotion=true,reducedMotion=false}={}){
 const root=new Container();root.boundsArea=new Rectangle(0,0,1672,941);const background=new Sprite(texture);root.addChild(background);const points=AMBIENCE_POINTS[mode];const filter=skyMotion&&!reducedMotion?skyFilter(points.hearts):null;if(filter)background.filters=[filter];
 const glows=points.candles.map(([x,y],i)=>{const g=new Graphics();for(let r=36;r>=4;r-=4)g.ellipse(0,0,r,r*1.3).fill({color:0xFFD090,alpha:.024});g.ellipse(0,0,2,4).fill({color:0xFFF2CE,alpha:.65});g.position.set(x,y);g.blendMode='add';root.addChild(g);return g;});
 const windows=points.city.map(([x,y])=>{const g=new Graphics().circle(0,0,5).fill({color:0xFFD29A,alpha:.13}).roundRect(-1,-2,2,4,.5).fill(0xFFE3B5);g.position.set(x,y);g.blendMode='add';root.addChild(g);return g;});
 const terrace=new Graphics();for(let r=300;r>=50;r-=50)terrace.ellipse(800,760,r,r*.24).fill({color:mode==='base'?0xFFE0BB:0xEEA7D3,alpha:.007});terrace.blendMode='add';root.addChild(terrace);
 return {root,background,filter,seek(ms){const t=reducedMotion?0:ms/1000;if(filter)filter.resources.skyUniforms.uniforms.uTime=t;glows.forEach((g,i)=>{g.alpha=.6+.3*Math.sin(t*3.3+i*1.9)+.16*Math.sin(t*5.7+i);g.scale.y=1+.08*Math.sin(t*4.2+i);});windows.forEach((g,i)=>g.alpha=.48+.42*Math.sin(t*1.7+i*1.7));terrace.alpha=.7+.1*Math.sin(t*.35);},destroy(){if(filter)filter.destroy();root.destroy({children:true});}};
}

