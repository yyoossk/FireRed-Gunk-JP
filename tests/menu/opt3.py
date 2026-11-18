import sys; sys.path.insert(0,'/home/claude/tools')
from walker import *
g=Game('jp','/tmp/t2/after_reload.ss',rom=sys.argv[1]); g.run(30)
sb2=lambda: g.u8(g.u32(0x03004FAC)+0x15)
g.tap('START'); g.run(20); g.tap('DOWN',5); g.tap('A'); g.run(90)
g.tap('DOWN',6); g.run(10); g.tap('LEFT'); g.run(10); g.tap('B'); g.run(120)
print('bit after', hex(sb2()))
g.shot('/tmp/t2/r0.png')     # menu reopened at せってい
g.tap('UP'); g.run(10); g.tap('A'); g.run(60); g.shot('/tmp/t2/r1.png'); g.tap('A'); g.run(400); g.shot('/tmp/t2/r2.png')
g.tap('A'); g.run(900); g.shot('/tmp/t2/rs.png'); g.tap('A'); g.run(60)
g.cmd('reset'); g.run(600)
for i in range(12):
    g.tap('A'); g.run(60)
    if i in (6,8,10,11): g.shot(f'/tmp/t2/r{3+i}.png')
g.close()
