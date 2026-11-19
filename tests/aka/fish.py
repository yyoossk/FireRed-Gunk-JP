import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
g.teleport('PALLET_TOWN',10,10); g.run(30)
w,h,cells,beh=g.grid()
# find walkable (collision 0) tile with water (behavior 0x10/0x11..) directly below
spot=None
for y in range(7,h-8):
    for x in range(7,w-7):
        c=cells[y*w+x]; d=cells[(y+1)*w+x]
        if (c>>10)&3==0 and beh(c&0x3FF) in (0,) and beh(d&0x3FF) in (0x10,0x11,0x12,0x15):
            spot=(x-7,y-7); break
    if spot: break
print('spot',spot)
g.teleport('PALLET_TOWN',*spot); g.face('D'); g.run(30)
runscript(g,bytes([0x44,0x08,0x01,0x01,0x00,0x02])); g.run(30)
sb1=g.u32(0x03004FA8)
g.cmd(f'poke {sb1+0x296:08X} 08'); g.cmd(f'poke {sb1+0x297:08X} 01')   # SUPER ROD 264
for t in range(3):
    g.tap('s')
    for i in range(10):
        g.run(25); g.shot(f'/tmp/t2/fs{t}{i}.png'); g.tap('A')
        if g.in_battle(): break
    print('try',t,'battle',g.in_battle())
    if g.in_battle(): break
g.close()
