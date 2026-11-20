import sys; sys.path.insert(0,'/home/claude/tools')
from walker import *
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(30)
fl=lambda: (g.u8(g.u32(0x03004FA8)+0xEE0+0x4A8//8)>>(0x4A8%8))&1
def opt():
    g.tap('START'); g.run(30)
    for i in range(6): g.tap('DOWN'); g.run(6)
    g.tap('A'); g.run(90)
    for i in range(6): g.tap('DOWN'); g.run(8)
print('flag before',fl())
opt(); g.tap('RIGHT'); g.run(10); g.shot('/tmp/t2/p1.png')
g.tap('A'); g.run(120); print('flag after',fl()); g.tap('B'); g.run(30)
opt(); g.shot('/tmp/t2/p2.png')
g.tap('LEFT'); g.run(10); g.tap('B'); g.run(120); print('flag again',fl())
g.close()
