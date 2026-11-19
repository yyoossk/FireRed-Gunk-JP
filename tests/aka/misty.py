import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/cur_fresh.ss',rom=sys.argv[1]); g.run(10)
tid=415
sb1=g.u32(0x03004FA8); f=0x500+tid; a=sb1+0xEE0+f//8; v=g.u8(a)&~(1<<(f%8)); g.cmd(f'poke {a:08X} {v:02X}')
g.teleport('CERULEAN_CITY_GYM',8,7); g.face('U'); g.run(30); g.shot('/tmp/t2/m_0.png')
g.tap('A')
for i in range(40):
    g.run(30)
    if g.in_battle(): break
    g.tap('A')
g.run(600); g.tap('A'); g.run(300); g.shot('/tmp/t2/m_1.png')
for k in range(2):
    g.tap('L'); g.run(8); g.tap('U'); g.run(8); g.tap('A'); g.run(30); g.tap('D'); g.run(8); g.tap('R'); g.run(8); g.tap('A')
    for i in range(14):
        g.run(60); g.tap('B')
for i in range(20):
    g.run(60); g.tap('A')
    if g.in_overworld() and i>5: pass
g.run(200); g.shot('/tmp/t2/m_2.png')
for i in range(6): g.tap('A'); g.run(60)
g.shot('/tmp/t2/m_3.png')
g.close()
