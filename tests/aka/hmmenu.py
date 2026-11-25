import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
rom,mode=sys.argv[1],sys.argv[2]
g=Game('jp','/tmp/t2/now_fresh.ss',rom=rom); g.run(10)
S=[]
def sh(tag): fn=f'/tmp/t2/hm_{mode}_{len(S)}.png'; g.shot(fn); S.append(fn)
def warp(gr,n,x,y): runscript(g,bytes([0x39,gr,n,0xFF])+struct.pack('<HH',x,y)+bytes([0x02])); g.run(300)
def downs(k):
    for i in range(k): g.cmd('tap D 1'); g.run(6)
if mode=='flash':
    warp(1,81,17,4)
    sh('dark'); g.tap('S'); g.run(40); sh('menu')
    downs(5); g.run(10); sh('cursor'); g.tap('A'); g.run(240); sh('after'); g.run(400)
    g.tap('S'); g.run(40); sh('menu2'); g.tap('B'); g.run(30)
elif mode=='flycave':
    g.tap('S'); g.run(40); sh('menu'); downs(4); g.tap('A'); g.run(150); sh('map')
    g.tap('B'); g.run(150); sh('cancel'); g.tap('A'); g.run(150)   # A on fly again
    sh('map2'); g.cmd('tap D 1'); g.run(20); g.cmd('tap D 1'); g.run(20); sh('cur'); g.tap('A'); g.run(400); sh('arrive')
    sb1=g.u32(0x03004FA8); print('map',g.u8(sb1+4),g.u8(sb1+5))
elif mode=='indoor':
    warp(5,4,7,6); g.tap('S'); g.run(40); sh('menu')
    downs(4); g.tap('A'); g.run(150); sh('map'); g.tap('A'); g.run(400); sh('arrive')
    sb1=g.u32(0x03004FA8); print('map',g.u8(sb1+4),g.u8(sb1+5))
elif mode=='flyrt':
    warp(1,81,17,4); g.tap('S'); g.run(40); downs(4); g.tap('A'); g.run(150); sh('map')
    sh('cur'); g.tap('A'); g.run(200); sh('fly'); g.run(300); sh('arrive')
    sb1=g.u32(0x03004FA8); print('map',g.u8(sb1+4),g.u8(sb1+5))
elif mode=='town':
    warp(3,0,10,10); g.tap('S'); g.run(40); sh('menu')
elif mode=='party':   # party menu fly in a cave
    g.tap('S'); g.run(40); downs(1); g.tap('A'); g.run(90); g.tap('A'); g.run(40); sh('sub')
g.close()
W=Image.new('RGB',(240*len(S),160))
for i,f in enumerate(S): W.paste(Image.open(f).convert('RGB'),(i*240,0))
W.save(f'/tmp/t2/hm_{mode}.png')
