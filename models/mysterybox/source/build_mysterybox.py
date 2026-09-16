from pathlib import Path
import math,json,struct,io
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent.parent
SRC=OUT/'source';TEX=SRC/'textures';TEX.mkdir(parents=True,exist_ok=True)
materials={};regions={};rng=np.random.default_rng(51)
def save_tex(name,im):
 im=im.convert('RGB').quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 im.save(TEX/(name+'.bmp'));im.convert('RGB').save(TEX/(name+'.png'));materials[name]=im.convert('RGB')
atlas=Image.open(OUT/'wood-atlas-v2.png').convert('RGB');w,h=atlas.size
save_tex('cabinet',atlas.crop((0,0,w,h//2)).resize((256,128),Image.Resampling.LANCZOS))
wood=atlas.crop((0,h//2,w,h)).resize((256,128),Image.Resampling.LANCZOS)
save_tex('sides',wood);save_tex('rear',wood)
details=Image.new('RGB',(256,256),(60,59,49));d=ImageDraw.Draw(details)
for name,rect,col in [('metal',(2,2,61,61),(82,85,73)),('dark',(66,2,125,61),(29,31,27)),('red',(130,2,189,61),(77,55,34)),('ivory',(194,2,253,61),(110,89,59)),('black',(2,66,61,125),(22,25,22))]:
 regions[name]=rect;d.rectangle(rect,fill=col)
 for i in range(300):
  x=int(rng.integers(rect[0]+1,rect[2]));y=int(rng.integers(rect[1]+1,rect[3]));v=int(rng.integers(-15,16));d.point((x,y),fill=tuple(max(0,min(255,c+v)) for c in col))
 d.line((rect[0],rect[1],rect[2],rect[1]),fill=tuple(c+25 for c in col))
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


def timber(name,x0,x1,y0,y1,z0,z1,top='sides'):
 group(name)
 face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],'sides',[(0,0),(1,0),(1,1),(0,1)],normal=(0,-1,0))
 face([(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)],'rear',[(0,0),(1,0),(1,1),(0,1)],normal=(0,1,0))
 for x,n in [(x0,(-1,0,0)),(x1,(1,0,0))]:
  face([(x,y0,z0),(x,y1,z0),(x,y1,z1),(x,y0,z1)],'sides',[(0,0),(.45,0),(.45,1),(0,1)],normal=n)
 face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],top,[(0,0),(1,0),(1,1),(0,1)],normal=(0,0,1))
 face([(x0,y1,z0),(x1,y1,z0),(x1,y0,z0),(x0,y0,z0)],tile_name='dark',normal=(0,0,-1))
timber('wooden_chest',-37,37,-15,15,2,25)
box('lid_seam',-37.3,37.3,-15.3,15.3,25,25.7,'dark')
timber('closed_lid',-38,38,-16,16,25.7,30,'cabinet')
for x in (-30,30):
 box('front_iron_strap',x-1.6,x+1.6,-15.6,-14.9,2,25,'metal')
 box('back_iron_strap',x-1.6,x+1.6,14.9,15.6,2,25,'metal')
 box('lid_iron_band',x-1.6,x+1.6,-16.4,16.4,30,30.6,'metal')
 box('lid_front_strap',x-1.6,x+1.6,-16.5,-15.9,25.7,30.6,'metal')
 box('rear_hinge',x-2.2,x+2.2,15.4,16.8,23,28,'metal')
 box('foot_skid',x-3,x+3,-15.5,15.5,0,2.2,'dark')
box('latch_backplate',-2.5,2.5,-16.1,-15,19.5,25,'dark')
box('lid_latch',-1.7,1.7,-17,-15.8,22,28,'metal')
box('latch_slot',-.55,.55,-17.15,-16.9,22.7,24,'black')
for side in (-1,1):
 x0,x1=sorted((side*37,side*38.8))
 for y in (-5,5):box('handle_bracket',x0,x1,y-1,y+1,13,18,'metal')
 x0,x1=sorted((side*39,side*40.5))
 box('carry_handle',x0,x1,-6,6,13,14.6,'metal')
 for y in (-5,5):
  x0,x1=sorted((side*37.8,side*40.5));box('handle_arm',x0,x1,y-.7,y+.7,14,16,'metal')
# Widen the chest by 20 percent, retaining its depth and height.
for t in tris:
 for p in t['p']:p[0]*=1.2

# All geometry has one root bone, ground-origin and flat face normals.
(SRC/'mesh.json').write_text(json.dumps({'triangles':tris,'regions':regions}),encoding='utf8')
smd=['version 1','nodes','0 "root" -1','end','skeleton','time 0','0 0 0 0 0 0 0','end','triangles']
for t in tris:
 smd.append(t['mat']+'.bmp')
 for p,uv in zip(t['p'],t['uv']):smd.append('0 '+' '.join(f'{v:.6f}' for v in p+t['n']+uv))
smd.append('end');(SRC/'mysterybox_reference.smd').write_text('\n'.join(smd)+'\n')
(SRC/'idle.smd').write_text('version 1\nnodes\n0 "root" -1\nend\nskeleton\ntime 0\n0 0 0 0 0 0 0\ntime 1\n0 0 0 0 0 0 0\nend\n')
(SRC/'mysterybox.qc').write_text('''// Original Half-Life inspired MysteryBox prop. Units match GoldSrc.
$modelname "../svencoop_addon/models/zombies/mysterybox_hl1.mdl"
$cd "."
$cdtexture "textures"
$scale 1.0
$body "body" "mysterybox_reference"
$sequence "idle" "idle" fps 1 loop
$bbox -49 -18 0 49 18 31
$cbox -49 -18 0 49 18 31
$eyeposition 0 -16 48
''')
(OUT/'svencoop_addon/models/zombies').mkdir(parents=True,exist_ok=True)
obj=['# Original HL1-inspired MysteryBox; Z up; front is -Y; dimensions in GoldSrc units','mtllib mysterybox.mtl']
idx=1
for t in tris:
 obj.extend('v '+' '.join(f'{v:.6f}' for v in p) for p in t['p'])
 obj.extend('vt '+' '.join(f'{v:.6f}' for v in uv) for uv in t['uv'])
 obj.append('vn '+' '.join(f'{v:.6f}' for v in t['n']))
 obj.append('g '+t['group']);obj.append('usemtl '+t['mat']);ni=(idx+2)//3
 obj.append('f '+' '.join(f'{i}/{i}/{ni}' for i in range(idx,idx+3)));idx+=3
(SRC/'mysterybox.obj').write_text('\n'.join(obj)+'\n')
(SRC/'mysterybox.mtl').write_text('\n'.join(f'newmtl {m}\nKa 0.4 0.4 0.4\nKd 1 1 1\nKs 0 0 0\nd 1\nillum 1\nmap_Kd textures/{m}.png\n' for m in materials))

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
gltf={'asset':{'version':'2.0','generator':'Original MysteryBox mesh builder'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'MysteryBox_HL1'}],'meshes':[{'primitives':primitives}],'materials':mats,'textures':textures,'images':images,'samplers':[{'magFilter':9728,'minFilter':9728,'wrapS':33071,'wrapT':33071}],'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':access}
j=json.dumps(gltf,separators=(',',':')).encode();j+=b' '*((-len(j))%4);blob+=b'\0'*((-len(blob))%4)
glb=struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(blob))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(blob),b'BIN\0')+blob
(OUT/'mysterybox_hl1.glb').write_bytes(glb)
stats={'triangles':len(tris),'vertices_unwelded':len(tris)*3,'materials':{k:list(v.size) for k,v in materials.items()},'bounds':[np.min([p for t in tris for p in t['p']],axis=0).tolist(),np.max([p for t in tris for p in t['p']],axis=0).tolist()]}
(OUT/'model-stats.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats))
