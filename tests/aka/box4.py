import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
ps=g.u32(0x03004FB0); g.cmd(f'poke {ps:08X} 0F')
one=bytes([0x79])+struct.pack('<HBH',16,5,0)+bytes(9)
runscript(g,one*33+b'\x02')
for i in range(14):
    g.run(30); g.shot(f'/tmp/t2/b4_{i:02d}.png'); g.tap('A')
g.close()
