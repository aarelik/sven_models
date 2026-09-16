"""Original low-poly prop: deterministic geometry, UVs, GoldSrc and glTF export."""
from pathlib import Path
import math, json, struct, io, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent.parent
SRC=OUT/'source'; TEX=SRC/'textures'
TEX.mkdir(parents=True,exist_ok=True)
ART=OUT/'front-art.png'
rng=np.random.default_rng(17)
materials={}
def save_tex(name,im):
    im=im.convert('RGB').quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    im.save(TEX/(name+'.bmp')); im.convert('RGB').save(TEX/(name+'.png'))
    materials[name]=im.convert('RGB')
front=Image.open(ART).convert('RGB').resize((128,256),Image.Resampling.LANCZOS)
save_tex('cabinet',front)

def worn_panel(w,h,base):
    n=rng.normal(0,4,(h,w,1)); arr=np.clip(np.array(base)[None,None,:]+n,0,255).astype('uint8')
    return Image.fromarray(arr)
side=worn_panel(64,128,(28,83,94)); dr=ImageDraw.Draw(side)
cream=worn_panel(64,38,(30,87,96))
side.paste(cream,(0,0)); dr=ImageDraw.Draw(side)
dr.line((0,38,64,38),fill=(28,26,22),width=2);dr.line((0,37,64,37),fill=(137,126,106))
for x in (3,60):
 dr.line((x,1,x,125),fill=(48,32,24));dr.line((x+1,2,x+1,125),fill=(47,105,114))
dr.rectangle((14,81,49,104),fill=(25,70,79),outline=(72,55,31))
for y in range(85,102,4):dr.line((18,y,45,y),fill=(28,28,25),width=2);dr.line((18,y+2,45,y+2),fill=(133,76,53))
for i in range(200):
 x=int(rng.integers(0,64));y=int(rng.integers(0,128))
 if x<7 or x>57 or y>118:dr.line((x,y,x+int(rng.integers(1,4)),y),fill=(67,62,49))
font_path=r'C:\Windows\Fonts\arialbd.ttf'
def font(n):return ImageFont.truetype(font_path,n)
def center(d,xy,t,f,fill):
 b=d.textbbox((0,0),t,font=f);d.text((xy[0]-(b[2]-b[0])/2,xy[1]),t,font=f,fill=fill)
dr.rectangle((12,52,52,73),fill=(184,169,132),outline=(55,35,23))
center(dr,(32,54),'ICE COLD',font(7),(80,28,19));center(dr,(32,63),'QUICK REVIVE',font(5),(80,28,19))
save_tex('sides',side)
back=side.copy();dr=ImageDraw.Draw(back)
dr.rectangle((7,8,56,117),fill=(78,76,64),outline=(30,30,26))
for y in range(15,38,4):dr.line((12,y,51,y),fill=(19,23,23),width=2)
dr.rectangle((19,57,44,76),fill=(164,154,125),outline=(41,41,36))
center(dr,(32,59),'SERVICE',font(5),(36,36,29));center(dr,(32,68),'110 V',font(6),(36,36,29))
for y in range(85,110,4):dr.line((12,y,51,y),fill=(22,25,23),width=2)
for x in (10,53):
 for y in (11,113):dr.ellipse((x-1,y-1,x+1,y+1),fill=(151,143,116))
save_tex('rear',back)

# Purpose-made detail atlas, with padded regions for stable indexed UV sampling.
details=worn_panel(256,256,(64,65,59));d=ImageDraw.Draw(details)
regions={}
def tile(name,rect,color):
 regions[name]=rect;d.rectangle(rect,fill=color)
tile('metal',(2,2,61,61),(111,115,103))
tile('dark',(66,2,125,61),(24,28,26))
tile('red',(130,2,189,61),(28,83,94))
tile('ivory',(194,2,253,61),(181,181,145))
for name in ('metal','dark','red','ivory'):
 x0,y0,x1,y1=regions[name]
 for i in range(200):
  x=int(rng.integers(x0,x1));y=int(rng.integers(y0,y1));c=details.getpixel((x,y));v=int(rng.integers(-13,14));d.point((x,y),fill=tuple(max(0,min(255,z+v)) for z in c))
 d.line((x0,y0,x1,y0),fill=tuple(min(255,z+22) for z in details.getpixel((x0+5,y0+5))))
tile('badge',(2,66,125,189),(45,162,164))
d.ellipse((5,69,122,186),fill=(61,190,191),outline=(171,203,181),width=5)
d.ellipse((14,78,113,177),fill=(211,225,194))
d.rectangle((33,99,94,153),fill=(46,151,157))
ink=(221,236,210)
# Person leaning to help someone reclining: original simple rescue pictogram.
d.ellipse((75,100,85,110),fill=ink)
d.line([(79,113),(74,133),(79,148)],fill=ink,width=7)
d.line([(77,117),(62,125)],fill=ink,width=5)
d.ellipse((43,119,52,128),fill=ink)
d.line([(47,131),(63,139),(72,138)],fill=ink,width=6)
d.line([(39,135),(65,149),(88,149)],fill=ink,width=4)
tile('controls',(130,66,189,157),(101,105,94))
d.rectangle((134,71,185,89),fill=(18,24,20),outline=(162,161,136));center(d,(159,74),'READY',font(9),(134,160,91))
d.rectangle((139,98,180,111),fill=(34,35,29),outline=(161,155,127));d.rectangle((148,102,172,105),fill=(8,12,12))
center(d,(159,117),'INSERT COIN',font(6),(214,203,167))
d.rectangle((146,132,173,148),fill=(87,41,30),outline=(201,179,134));center(d,(159,135),'10c',font(8),(211,195,149))
for x in (133,185):
 for y in (69,153):d.ellipse((x,y,x+2,y+2),fill=(183,182,153))
tile('bottle',(194,66,253,189),(66,36,21))
d.rectangle((195,107,252,157),fill=(192,181,145));center(d,(224,115),'QUICK',font(8),(108,31,25));center(d,(224,127),'REVIVE',font(9),(108,31,25));d.rectangle((219,144,228,153),fill=(106,30,25))
tile('vent',(130,164,189,222),(62,63,54))
for y in range(169,220,7):d.rectangle((134,y,185,y+3),fill=(17,24,22));d.line((134,y+4,185,y+4),fill=(133,132,111))
tile('label',(2,196,125,253),(184,188,150))
for i in range(240):
 x=int(rng.integers(3,125));y=int(rng.integers(197,253));d.point((x,y),fill=(153,161,130))
center(d,(64,214),'Quick Revive!',ImageFont.truetype(r'C:\Windows\Fonts\georgiai.ttf',16),(28,83,109))
tile('green',(194,196,221,223),(99,129,65))
tile('black',(228,196,253,223),(15,19,18))
save_tex('details',details)

tris=[];groups=[];current=''
def group(name):
 global current
 current=name
def tri(pts,uv,mat):
 p=np.array(pts,float);n=np.cross(p[1]-p[0],p[2]-p[0]);n/=np.linalg.norm(n)
 tris.append(dict(p=p.tolist(),uv=[list(t) for t in uv],n=n.tolist(),mat=mat,group=current))
def face(pts,mat='details',uv=None,tile_name='metal',normal=None):
 pts=[list(p) for p in pts]
 if uv is None:
  x0,y0,x1,y1=regions[tile_name];u0=(x0+2)/256;u1=(x1-2)/256;v0=1-(y1-2)/256;v1=1-(y0+2)/256
  uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)] if len(pts)==4 else [(u0,v0),(u1,v0),(u1,v1)]
 if normal is not None and np.dot(np.cross(np.subtract(pts[1],pts[0]),np.subtract(pts[2],pts[0])),normal)<0:
  pts.reverse();uv=list(reversed(uv))
 for i in range(1,len(pts)-1):tri([pts[0],pts[i],pts[i+1]],[uv[0],uv[i],uv[i+1]],mat)
def box(name,x0,x1,y0,y1,z0,z1,tile_name='metal',front_tile=None):
 group(name)
 face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],tile_name=front_tile or tile_name,normal=(0,-1,0))
 face([(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)],tile_name=tile_name,normal=(0,1,0))
 face([(x0,y1,z0),(x0,y0,z0),(x0,y0,z1),(x0,y1,z1)],tile_name=tile_name,normal=(-1,0,0))
 face([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],tile_name=tile_name,normal=(1,0,0))
 face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],tile_name=tile_name,normal=(0,0,1))
 face([(x0,y1,z0),(x1,y1,z0),(x1,y0,z0),(x0,y0,z0)],tile_name=tile_name,normal=(0,0,-1))

# Bevelled flat-top cabinet, distinct proportions from Juggernog.
profile=[(-19,3),(19,3),(21,5),(21,74),(19,77),(-19,77),(-21,74),(-21,5)]
inner=[(x*.95,(z-40)*.977+40) for x,z in profile]
group('cabinet_front')
face([(x,-14,z) for x,z in inner],'cabinet',[(.01+.98*(x+21)/42,.01+.98*(z-3)/74) for x,z in inner],normal=(0,-1,0))
group('cabinet_bevel')
for i in range(8):
 j=(i+1)%8;a=inner[i];b=inner[j];c=profile[j];e=profile[i]
 face([(a[0],-14,a[1]),(e[0],-12,e[1]),(c[0],-12,c[1]),(b[0],-14,b[1])],tile_name='red')
group('cabinet_shell')
for i in range(8):
 j=(i+1)%8;a=profile[i];b=profile[j]
 pts=[(a[0],-12,a[1]),(a[0],13,a[1]),(b[0],13,b[1]),(b[0],-12,b[1])]
 if abs(a[1]-b[1])>20:
  us=(.02,.98) if a[0]>0 else (.98,.02)
  face(pts,'sides',[(us[0],(a[1]-3)/74),(us[1],(a[1]-3)/74),(us[1],(b[1]-3)/74),(us[0],(b[1]-3)/74)])
 else:face(pts,tile_name='red' if a[1]>60 else 'dark')
group('rear_service_panel')
face([(x,13,z) for x,z in profile],'rear',[(.99-.98*(x+21)/42,.01+.98*(z-3)/74) for x,z in profile],normal=(0,1,0))
box('base_plinth',-21.5,21.5,-13.5,13.5,1,4,'dark')
for x in (-17,17):
 for y in (-9,9):box('rubber_foot',x-2,x+2,y-2,y+2,0,1.3,'black')
def cylinder_z(name,cx,cy,rings,segments=8,tile_name='bottle'):
 group(name);x0,y0,x1,y1=regions[tile_name]
 for k in range(len(rings)-1):
  z0,r0=rings[k];z1,r1=rings[k+1]
  for i in range(segments):
   a=i*2*math.pi/segments;b=(i+1)*2*math.pi/segments
   pts=[(cx+r0*math.cos(a),cy+r0*math.sin(a),z0),(cx+r0*math.cos(b),cy+r0*math.sin(b),z0),(cx+r1*math.cos(b),cy+r1*math.sin(b),z1),(cx+r1*math.cos(a),cy+r1*math.sin(a),z1)]
   u0=(x0+2+(x1-x0-4)*i/segments)/256;u1=(x0+2+(x1-x0-4)*(i+1)/segments)/256
   v0=1-(y1-2-(y1-y0-4)*(z0-rings[0][0])/(rings[-1][0]-rings[0][0]))/256
   v1=1-(y1-2-(y1-y0-4)*(z1-rings[0][0])/(rings[-1][0]-rings[0][0]))/256
   face(pts,uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)])
 z,r=rings[-1]
 for i in range(segments):
  a=i*2*math.pi/segments;b=(i+1)*2*math.pi/segments
  face([(cx,cy,z),(cx+r*math.cos(a),cy+r*math.sin(a),z),(cx+r*math.cos(b),cy+r*math.sin(b),z)],tile_name='metal')
# Short broad cabinet with sloping blue top and raised cream nameboard.
for t in tris:
 for p in t['p']:p[2]*=.80
box('bottle_hatch',-3.2,3.2,-15.2,-14,27,36.8,'metal',front_tile='dark')
box('hatch_left_trim',-3.8,-3,-16,-14,26.5,37.3,'metal')
box('hatch_right_trim',3,3.8,-16,-14,26.5,37.3,'metal')
box('hatch_tray',-3.8,3.8,-17,-14,26.2,27.2,'metal')
cylinder_z('bottle',0,-15.7,[(27.2,.7),(31.2,.7),(32,.35),(33.3,.35)],8)
box('coin_fitting',13,17,-16,-14,49,56,'metal',front_tile='controls')
group('sloped_top')
face([(-21,-14,60),(21,-14,60),(21,12,67),(-21,12,67)],tile_name='red',normal=(0,0,1))
for x,n in [(-21,(-1,0,0)),(21,(1,0,0))]:
 face([(x,-14,60),(x,12,60),(x,12,67)],tile_name='red',normal=n)
face([(-21,12,60),(21,12,60),(21,12,67),(-21,12,67)],tile_name='red',normal=(0,1,0))
box('nameboard',-19,19,7,9,67,78,'ivory',front_tile='label')
box('sign_support',-1.5,1.5,7,9,77,83,'metal')
def sign():
 group('round_perk_sign');cz=88.5;r=8.7;n=16
 for i in range(n):
  a=i*2*math.pi/n;b=(i+1)*2*math.pi/n
  p=(r*math.cos(a),cz+r*math.sin(a));q=(r*math.cos(b),cz+r*math.sin(b))
  face([(p[0],-3,p[1]),(p[0],0,p[1]),(q[0],0,q[1]),(q[0],-3,q[1])],tile_name='metal')
  # metal ring on front face
  inner_r=8.05
  pi=(inner_r*math.cos(a),cz+inner_r*math.sin(a));qi=(inner_r*math.cos(b),cz+inner_r*math.sin(b))
  face([(pi[0],-3.05,pi[1]),(p[0],-3.05,p[1]),(q[0],-3.05,q[1]),(qi[0],-3.05,qi[1])],tile_name='metal',normal=(0,-1,0))
  x0,y0,x1,y1=regions['badge']
  def uv(x,z):return ((x0+2+(x/inner_r+1)/2*(x1-x0-4))/256,1-(y0+2+(1-(z-cz)/inner_r)/2*(y1-y0-4))/256)
  pts=[(0,-3.08,cz),(pi[0],-3.08,pi[1]),(qi[0],-3.08,qi[1])]
  face(pts,uv=[uv(0,cz),uv(*pi),uv(*qi)],normal=(0,-1,0))
  face([(0,0,cz),(q[0],0,q[1]),(p[0],0,p[1])],tile_name='red',normal=(0,1,0))
sign()


for t in tris:
 if t['group']=='round_perk_sign':
  for p in t['p']:p[1]+=10

# All geometry has one root bone, ground-origin and flat face normals.
(SRC/'mesh.json').write_text(json.dumps({'triangles':tris,'regions':regions}),encoding='utf8')
smd=['version 1','nodes','0 "root" -1','end','skeleton','time 0','0 0 0 0 0 0 0','end','triangles']
for t in tris:
 smd.append(t['mat']+'.bmp')
 for p,uv in zip(t['p'],t['uv']):smd.append('0 '+' '.join(f'{v:.6f}' for v in p+t['n']+uv))
smd.append('end');(SRC/'quickrevive_reference.smd').write_text('\n'.join(smd)+'\n')
(SRC/'idle.smd').write_text('version 1\nnodes\n0 "root" -1\nend\nskeleton\ntime 0\n0 0 0 0 0 0 0\ntime 1\n0 0 0 0 0 0 0\nend\n')
(SRC/'quickrevive.qc').write_text('''// Original Half-Life inspired QuickRevive prop. Units match GoldSrc.
$modelname "../svencoop_addon/models/zombies/quickrevive_hl1.mdl"
$cd "."
$cdtexture "textures"
$scale 1.0
$body "body" "quickrevive_reference"
$sequence "idle" "idle" fps 1 loop
$bbox -22 -20 0 22 14 98
$cbox -22 -20 0 22 14 98
$eyeposition 0 -16 48
''')
(OUT/'svencoop_addon/models/zombies').mkdir(parents=True,exist_ok=True)
obj=['# Original HL1-inspired QuickRevive; Z up; front is -Y; dimensions in GoldSrc units','mtllib quickrevive.mtl']
idx=1
for t in tris:
 obj.extend('v '+' '.join(f'{v:.6f}' for v in p) for p in t['p'])
 obj.extend('vt '+' '.join(f'{v:.6f}' for v in uv) for uv in t['uv'])
 obj.append('vn '+' '.join(f'{v:.6f}' for v in t['n']))
 obj.append('g '+t['group']);obj.append('usemtl '+t['mat']);ni=(idx+2)//3
 obj.append('f '+' '.join(f'{i}/{i}/{ni}' for i in range(idx,idx+3)));idx+=3
(SRC/'quickrevive.obj').write_text('\n'.join(obj)+'\n')
(SRC/'quickrevive.mtl').write_text('\n'.join(f'newmtl {m}\nKa 0.4 0.4 0.4\nKd 1 1 1\nKs 0 0 0\nd 1\nillum 1\nmap_Kd textures/{m}.png\n' for m in materials))

# Standalone embedded GLB, native Y-up metres (1 GoldSrc unit = 1 inch).
blob=bytearray();views=[];access=[]
def buf(data,target=None):
 while len(blob)%4:blob.append(0)
 o=len(blob);blob.extend(data);v={'buffer':0,'byteOffset':o,'byteLength':len(data)}
 if target:v['target']=target
 views.append(v);return len(views)-1
def acc(arr,typ,target=34962):
 arr=np.asarray(arr,dtype='<f4');v=buf(arr.tobytes(),target);a={'bufferView':v,'componentType':5126,'count':len(arr),'type':typ}
 if typ=='VEC3':a.update(min=arr.min(axis=0).tolist(),max=arr.max(axis=0).tolist())
 access.append(a);return len(access)-1
primitives=[];images=[];mats=[];textures=[]
for mi,(name,im) in enumerate(materials.items()):
 ts=[t for t in tris if t['mat']==name]
 ps=[(p[0]*.0254,p[2]*.0254,-p[1]*.0254) for t in ts for p in t['p']]
 ns=[(t['n'][0],t['n'][2],-t['n'][1]) for t in ts for _ in range(3)]
 uvs=[(uv[0],1-uv[1]) for t in ts for uv in t['uv']]
 primitives.append({'attributes':{'POSITION':acc(ps,'VEC3'),'NORMAL':acc(ns,'VEC3'),'TEXCOORD_0':acc(uvs,'VEC2')},'material':mi,'mode':4})
 bb=io.BytesIO();im.save(bb,format='PNG');images.append({'bufferView':buf(bb.getvalue()),'mimeType':'image/png','name':name})
 textures.append({'source':mi,'sampler':0});mats.append({'name':name,'pbrMetallicRoughness':{'baseColorTexture':{'index':mi},'metallicFactor':0,'roughnessFactor':1},'doubleSided':False})
gltf={'asset':{'version':'2.0','generator':'Original QuickRevive mesh builder'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'QuickRevive_HL1'}],'meshes':[{'primitives':primitives}],'materials':mats,'textures':textures,'images':images,'samplers':[{'magFilter':9728,'minFilter':9728,'wrapS':33071,'wrapT':33071}],'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':access}
j=json.dumps(gltf,separators=(',',':')).encode();j+=b' '*((-len(j))%4);blob+=b'\0'*((-len(blob))%4)
glb=struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(blob))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(blob),b'BIN\0')+blob
(OUT/'quickrevive_hl1.glb').write_bytes(glb)
stats={'triangles':len(tris),'vertices_unwelded':len(tris)*3,'materials':{k:list(v.size) for k,v in materials.items()},'bounds':[np.min([p for t in tris for p in t['p']],axis=0).tolist(),np.max([p for t in tris for p in t['p']],axis=0).tolist()]}
(OUT/'model-stats.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats))
