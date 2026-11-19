import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
rom=sys.argv[1]
g=Game('jp','/tmp/t2/now_fresh.ss',rom=rom); g.run(10)
g.teleport('ROUTE1',16,14); g.run(80)
g.hold('D',40); g.run(30)
def objs():
    b=g.peek(g.R['objs'],0x24*16); out=[]
    for i in range(16):
        e=b[0x24*i:0x24*i+0x24]
        if e[0]&1:
            cx,cy,px,py=struct.unpack('<hhhh',e[0x10:0x18]); out.append((i,cy-7,py-7,e[0x1C]))
    return out
for i in range(60):
    g.hold('DB',2)
    o=objs(); print(i*2,o)
g.close()
