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
def mask(*polys):
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    for poly in polys: d.polygon(poly,fill=1)
    return im.load()
WING =mask([(50,4),(112,4),(112,42),(96,44),(70,56),(62,42),(54,12)])      # 右のつばさ
LWING=mask([(34,22),(62,20),(70,42),(62,52),(44,42),(36,32)])              # 奥のつばさ（うら側が見えているのでオレンジ）
FLAME=mask([(0,34),(8,38),(24,40),(28,48),(28,57),(14,58),(4,52)])         # 炎
HORN =mask([(35,12),(47,12),(47,23),(35,23)])                             # 頭のとがった所（つの）
BELLY=mask([(41,55),(52,53),(58,58),(62,66),(62,90),(54,93),(48,86),(44,76),(40,66)])  # おなか（のどは からだの色）
TAIL =mask([(70,58),(112,58),(112,98),(66,98),(80,90),(80,72)])            # しっぽ（かげで暗いので少し明るく）
TAIL_UNDER=mask([(82,68),(104,68),(104,84),(82,84)])                      # しっぽの うら側
CLAW =mask([(34,90),(50,90),(50,101),(34,101)],[(68,92),(96,92),(96,103),(68,103)],
           [(26,60),(40,60),(40,74),(26,74)],[(44,60),(50,60),(50,66),(44,66)],[(14,26),(20,26),(20,32),(14,32)])  # つめ・きば
def c5(r,g,b): return (r>>3)|((g>>3)<<5)|((b>>3)<<10)
# 色は公式の絵・フィギュアに合わせる：からだ＝オレンジ、おなか＝クリーム、手前のつばさの膜＝青緑、
# 奥のつばさ（うら側）・つばさの骨＝オレンジ、炎＝根もとが黄・先が赤、つめ・きば＝白、しっぽ＝オレンジ（うら側はクリーム）。
# りんかくは黒い線にせず、元の絵と同じく色の濃淡で表す
pal=[c5(0,0,255)]+[0]*15
pal[1]=c5(248,248,240)                                               # つめ・きば（白）
pal[2:9]=[c5(96,32,8),c5(136,48,8),c5(176,72,16),c5(208,96,24),c5(232,120,32),c5(240,144,48),c5(248,184,88)]  # からだ（暗→明）
pal[9:11]=[c5(232,208,112),c5(248,240,176)]                          # おなか（明るい方は つめ・きばにも使う）
pal[11:14]=[c5(24,72,88),c5(40,104,120),c5(64,140,152)]              # つばさの膜
pal[14]=c5(232,40,24); pal[15]=c5(248,224,72)                        # 炎：赤・黄（中の橙は からだの色）
BODY={7:2,8:3,9:4,10:5,11:6,12:7,13:7,14:8,15:8}
def up(n,k): return min(8,n+k)
new={}
for (x,y),v in px.items():
    if v==0: new[x,y]=0; continue
    edge=any(px.get((x+dx,y+dy),0)==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
    if v==1: v=6
    if FLAME[x,y]:
        f=(y-34)/28                                                   # 0＝口に近い根もと、1＝先
        if edge: n=14
        elif v>=14 or f<0.35: n=15
        elif f<0.7: n=6
        else: n=14
    elif v==6: n=11 if WING[x,y] else 2                              # いちばん暗い所は こい色（黒い線にしない）
    elif CLAW[x,y] and v>=14: n=1
    elif HORN[x,y]: n=up(BODY[v],2)
    elif LWING[x,y] and v<=9: n=up(BODY[v],1)                         # 奥のつばさ（元の濃淡のまま少し明るく）
    elif LWING[x,y] and 48<=x<=58 and 24<=y<=36 and v==10: n=up(BODY[9],1)   # まだら模様も濃淡のまま
    elif WING[x,y] and v in (7,8,9): n={7:11,8:12,9:13}[v]
    elif BELLY[x,y] and v>=12: n=10 if v>=13 else 9
    elif TAIL_UNDER[x,y] and v>=10: n=10 if v>=12 else 9               # しっぽの うら側（クリーム）
    elif TAIL[x,y] and v<=9: n=up(BODY[v],2)
    else: n=BODY[v]
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
