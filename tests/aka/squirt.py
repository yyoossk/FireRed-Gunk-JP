import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
g=Game('jp','/tmp/t2/f151.ss',rom=sys.argv[1]); g.run(10)
S=[]
def sh():
    n=len(S); g.shot(f'/tmp/t2/sq{n}.png'); S.append(n)
def go(addr): runscript(g,bytes([0x04])+struct.pack('<I',addr)+bytes([0x02])); g.run(90)
NB=0x08F805B5
go(NB); sh(); g.tap('A'); g.run(40); sh(); g.tap('A'); g.run(40)
go(0x08F804F0); sh(); g.tap('A'); g.run(40); sh(); g.tap('A'); g.run(40); sh()
g.tap('B'); g.run(60); sh(); g.tap('A'); g.run(60)
go(0x08F804F0); g.tap('A'); g.run(40); g.tap('A'); g.run(40); g.tap('A'); g.run(200); sh()
g.tap('B'); g.run(60); g.tap('A'); g.run(90); g.tap('A'); g.run(60)
go(0x08F804F0); sh()
g.close()
W=Image.new('RGB',(240*4,160*((len(S)+3)//4)))
for i in S: W.paste(Image.open(f'/tmp/t2/sq{i}.png').convert('RGB'),((i%4)*240,(i//4)*160))
W.save('/tmp/t2/sq.png')
