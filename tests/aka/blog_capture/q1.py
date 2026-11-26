exec(open('/tmp/rc/base.py').read())
import walker
g=new(); setlead(g,88,moves=(58,188,85,126),lv=100,nick='ベトベター')
warp(g,10,1,6,6,wait=200); print(walker._events(g)['objs'])
g.u8(0x02000000); g.close()
