# タイトル画面のリザードン（BG1、パレット13）をフルカラーにする。
# 日本版（後期版）の絵（0x08380A08）と並び（0x083812E4）を組み立てて色を塗り分け、
# 新しいタイル・並び（LZ）とパレットを port/data/title/ に書き出す。patch_port.py が読み込む。
import sys,struct; sys.path.insert(0,'/home/claude/tools')
from lzgba import unlz, lz
from PIL import Image, ImageDraw
ROM=open('/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba','rb').read()
OUT='/home/claude/port/data/title/'
tiles=unlz(ROM,0x380A08); m=struct.unpack('<640H',unlz(ROM,0x3812E4))
cells=[(i,e&0x3FF) for i,e in enumerate(m) if e&0x3FF]
assert all(e>>10==52 for e in m if e&0x3FF)          # パレット13、反転なし
R0=min(i//32 for i,_ in cells); C0=min(i%32 for i,_ in cells)
W,H=112,104
px={}
def tpx(t,x,y):
    b=tiles[t*32+y*4+x//2]; return (b>>4) if x&1 else (b&15)
for i,t in cells:
    for y in range(8):
        for x in range(8): px[((i%32-C0)*8+x,(i//32-R0)*8+y)]=tpx(t,x,y)
def mask(poly):
    im=Image.new('L',(W,H),0); ImageDraw.Draw(im).polygon(poly,fill=1); return im.load()
WING =mask([(50,4),(112,4),(112,42),(96,44),(70,56),(62,42),(54,12)])      # 右のつばさ
LWING=mask([(34,22),(62,20),(70,42),(62,52),(44,42),(36,32)])              # 奥のつばさ
FLAME=mask([(0,34),(8,38),(24,40),(31,50),(29,63),(10,63)])                # はいている炎
BELLY=mask([(34,44),(46,46),(58,54),(64,64),(64,84),(58,94),(44,94),(36,82),(38,64),(32,56)])  # のど・おなか
def c5(r,g,b): return (r>>3)|((g>>3)<<5)|((b>>3)<<10)
pal=[c5(0,0,255)]+[0]*15
pal[1:6]=[c5(24,56,104),c5(40,88,144),c5(72,128,184),c5(232,192,104),c5(248,232,160)]   # つばさの膜3・おなか2
ramp=[(40,16,8),(96,32,8),(136,48,8),(176,72,16),(208,96,24),(232,120,32),(240,144,48),(248,168,64),(248,200,96),(248,224,136)]
for k,c in enumerate(ramp): pal[6+k]=c5(*c)                                  # からだ（オレンジ）
new={}
for (x,y),v in px.items():
    if v==0: new[x,y]=0; continue
    if v==1: v=6
    n=v
    if (WING[x,y] or LWING[x,y]) and v in (7,8,9): n={7:1,8:2,9:3}[v]
    elif BELLY[x,y] and v>=11: n=5 if v>=13 else 4
    if FLAME[x,y] and 7<=n<=15: n=min(15,n+1)
    new[x,y]=n
# タイルを作り直す（同じタイルはまとめる）。0番は空のまま
outt=[bytes(32)]; idx={bytes(32):0}; nm=list(m)
for i,_ in cells:
    bx,by=(i%32-C0)*8,(i//32-R0)*8; b=bytearray(32)
    for y in range(8):
        for x in range(0,8,2): b[y*4+x//2]=new[bx+x,by+y]|(new[bx+x+1,by+y]<<4)
    b=bytes(b)
    if b not in idx: idx[b]=len(outt); outt.append(b)
    nm[i]=(52<<10)|idx[b]
open(OUT+'charizard_pal.bin','wb').write(struct.pack('<16H',*pal))
open(OUT+'charizard_tiles.lz','wb').write(lz(b''.join(outt)))
open(OUT+'charizard_map.lz','wb').write(lz(struct.pack('<640H',*nm)))
img=Image.new('RGB',(W,H))
for (x,y),v in new.items():
    c=pal[v]; img.putpixel((x,y),((c&31)<<3,((c>>5)&31)<<3,((c>>10)&31)<<3))
img.resize((W*3,H*3),Image.NEAREST).save('/tmp/ttl/w/preview.png')
print('tiles',len(outt))
