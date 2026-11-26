import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
t=sys.argv[2]
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
sys.path.insert(0,'/tmp/blog'); from name import set_name; set_name(g); g.run(2)
if len(sys.argv)>3:
    gr,n,x,y=map(int,sys.argv[3:7]); runscript(g,bytes([0x39,gr,n,0xFF])+struct.pack('<HH',x,y)+bytes([0x02])); g.run(300)
g.tap('S'); g.run(30); g.tap('A'); g.run(150)
S=[]
def sh():
    fn=f'/tmp/t2/dh_{t}_{len(S)}.png'; g.shot(fn); S.append(fn)
for i in range(14): g.cmd('tap D 1'); g.run(4)
g.run(10); sh(); g.tap('A'); g.run(30); sh()
for i in range(6): g.cmd('tap D 1'); g.run(4)
sh(); g.tap('B'); g.run(30); sh(); g.tap('B'); g.run(120); sh()
g.close()
W=Image.new('RGB',(240*len(S),160))
for i,f in enumerate(S): W.paste(Image.open(f).convert('RGB'),(i*240,0))
W.save(f'/tmp/t2/dh_{t}.png')
