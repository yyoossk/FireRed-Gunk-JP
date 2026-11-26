exec(open('/tmp/rc/base.py').read())
import walker
P151='/tmp/rc/post151.ss'
for gr,n,x,y in ((1,62,10,10),(1,3,10,10),(10,15,4,6),(3,5,20,10)):
    g=new(P151,rom=ROM151); warp(g,gr,n,x,y,wait=200); e=walker._events(g)
    print((gr,n),'objs',[(o['lid'],o['x'],o['y'],hex(o['script']),o['flag']) for o in e['objs']],'bgs',[(b['x'],b['y'],hex(b['data'])) for b in e['bgs']])
    g.u8(0x02000000); g.close()
