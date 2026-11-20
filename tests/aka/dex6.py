import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
grp,num,x,y,tag=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
runscript(g,bytes([0x39,grp,num,0xFF])+struct.pack('<HH',x,y)+bytes([0x02]))
g.run(240)
for k in ['S']: g.tap(k); g.run(40)
# cursor might be remembered; go to top
g.tap('A'); g.run(80); g.tap('A'); g.run(60)
for i in range(128): g.cmd('tap D 1')
g.run(20); g.tap('A'); g.run(60); g.tap('A'); g.run(12); g.shot(f'/tmp/t2/t_{tag}.png')
g.close()
