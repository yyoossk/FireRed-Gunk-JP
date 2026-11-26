exec(open('/tmp/rc/base.py').read())
P151='/tmp/rc/post151.ss'
def go(tag, gr,n,x,y,face,pre=None,steps=10,ans=None):
    g=new(P151,rom=ROM151)
    if pre: pre(g)
    warp(g,gr,n,x,y,wait=200); g.face(face); g.run(10); g.tap('A')
    for i in range(steps):
        g.run(40); shot(g,f'{tag}{i:02d}'); g.tap('A')
    g.u8(0x02000000); g.close()
def mew(g): g.setflag(0xF7,False)
def fos(g):
    for f in (47,48,0x27C,0x27D,0x27E): pass
    g.setflag(47,False); g.setflag(48,False)
def sq(g): g.setflag(0xF2,False)
go('kmew',1,62,21,28,'U',mew,steps=16)
go('kfos',1,3,13,8,'U',fos,steps=12)
go('ksq',3,5,20,9,'U',sq,steps=6)
go('kpa',10,15,2,3,'U',None,steps=4)
go('kpb',10,15,6,3,'U',None,steps=4)
