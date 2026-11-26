import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
rom,mode=sys.argv[1],sys.argv[2]
g=Game('jp','/tmp/t2/now_fresh.ss',rom=rom); g.run(10)
sys.path.insert(0,'/tmp/blog'); from name import set_name; set_name(g); g.run(2)
S=[]
def sh(): fn=f'/tmp/t2/h2_{mode}_{len(S)}.png'; g.shot(fn); S.append(fn)
def warp(gr,n,x,y): runscript(g,bytes([0x39,gr,n,0xFF])+struct.pack('<HH',x,y)+bytes([0x02])); g.run(300)
def downs(k):
    for i in range(k): g.cmd('tap D 1'); g.run(6)
if mode=='town':
    warp(3,30,14,20)
    g.tap('S'); g.run(40); sh(); downs(4); g.tap('A'); g.run(30); sh(); g.tap('B'); g.run(30); sh()
    downs(1); g.tap('A'); g.run(60); sh(); downs(4); sh(); g.tap('B'); g.run(60); sh()
    g.tap('B'); g.run(30); g.cmd('hold U 20'); g.run(20); sh()
elif mode=='cave':
    warp(1,81,17,4)
    g.tap('S'); g.run(40); downs(4); g.tap('A'); g.run(30); sh(); downs(1); g.tap('A'); g.run(400); sh()
    g.tap('S'); g.run(40); sh(); g.tap('B'); g.run(30)
    g.tap('S'); g.run(40); g.tap('A'); g.run(30); sh(); g.tap('A'); g.run(150); sh(); g.tap('A'); g.run(400); sh()
    sb1=g.u32(0x03004FA8); print('map',g.u8(sb1+4),g.u8(sb1+5))
g.close()
W=Image.new('RGB',(240*len(S),160))
for i,f in enumerate(S): W.paste(Image.open(f).convert('RGB'),(i*240,0))
W.save(f'/tmp/t2/h2_{mode}.png')
