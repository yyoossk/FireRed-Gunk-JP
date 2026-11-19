import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
one=bytes([0x79])+struct.pack('<HBH',16,5,0)+bytes(9)
runscript(g,one+b'\x02'); g.run(60)   # Pidgey Lv5 -> party slot 3
sb1=g.u32(0x03004FA8)
mon=g.peek(g.R['party']+100*3,80)
dc=sb1+0x3C98
for i,b in enumerate(mon): g.cmd(f'poke {dc+i:08X} {b:02X}')
steps=int(sys.argv[2])
for i,b in enumerate(struct.pack('<I',steps)): g.cmd(f'poke {dc+0x88+i:08X} {b:02X}')
g.teleport('ROUTE5_POKEMON_DAY_CARE',4,5); g.face('U'); g.run(20); g.shot('/tmp/t2/dc_a.png')
g.tap('A')
for i in range(8):
    g.run(50); g.shot(f'/tmp/t2/dc{sys.argv[3]}{i}.png'); g.tap('A')
g.close()
