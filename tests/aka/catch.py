import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
ps=g.u32(0x03004FB0); g.cmd(f'poke {ps:08X} 0F')   # current box = 16
one=bytes([0x79])+struct.pack('<HBH',16,5,0)+bytes(9)
runscript(g,one*32+b'\x02'); g.run(120)
print('count',g.u8(g.R['cnt']),'box',g.u8(ps),'var',g.getvar(0x4037))
wild(g,19,3)  # Rattata
g.run(300); g.tap('A'); g.run(200); g.shot('/tmp/t2/ct0.png')
g.tap('l'); g.run(20); g.shot('/tmp/t2/ct1.png')
k=0
for i in range(36):
    g.run(40); g.shot(f'/tmp/t2/cx{k:02d}.png'); k+=1; g.tap('A')
g.run(300)
for i in range(10):
    g.run(40); g.shot(f'/tmp/t2/cy{i}.png'); g.tap('A')
print('box after',g.u8(ps),'var',g.getvar(0x4037))
g.close()
