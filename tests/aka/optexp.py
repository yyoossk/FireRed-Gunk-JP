import sys; sys.path.insert(0,'/home/claude/tools')
from walker import *
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(30)
sb1=lambda: g.u32(0x03004FA8)
g.tap('START'); g.run(30)
for i in range(6): g.tap('DOWN'); g.run(6)
g.tap('A'); g.run(90); g.shot('/tmp/t2/o1.png')
for i in range(6): g.tap('UP'); g.run(6)   # wraps: 0 -> 6 (exp all) ...
g.shot('/tmp/t2/o2.png')
g.tap('DOWN'); g.run(6); g.shot('/tmp/t2/o3.png')   # back to top
g.tap('UP'); g.run(6); g.tap('RIGHT'); g.run(10); g.shot('/tmp/t2/o4.png')
g.tap('B'); g.run(120); g.shot('/tmp/t2/o5.png')
g.tap('A'); g.run(90); g.shot('/tmp/t2/o6.png')
g.close()
