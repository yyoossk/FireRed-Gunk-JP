exec(open('/tmp/rc/base.py').read())
import walker
g=new(); setlead(g,88,moves=(58,188,85,126),lv=100,nick='ベトベター')
g.setflag(0x2A8,False); g.setflag(0x840,True)
warp(g,10,9,6,13,wait=200); print(walker._events(g)['objs'])
runscript(g,bytes([0x05])+struct.pack('<I',0x088620DE))
for i in range(16): g.run(40); shot(g,f'pa{i:02d}'); g.tap('A')
wait_idle(g)
g.teleport('VERMILION_CITY',24,32); g.run(60); g.face('D'); g.run(10)
g.tap('A')
for i in range(6): g.run(50); shot(g,f'pb{i}'); g.tap('A') if i<1 else None
g.u8(0x02000000); g.close()
