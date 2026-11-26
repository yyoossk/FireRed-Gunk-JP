exec(open('/tmp/rc/base.py').read())
g=new(); setlead(g,88,moves=(58,188,85,126),lv=100,nick='ベトベター')
warp(g,3,0,10,8,wait=200); print(g.objects()); g.face('U'); g.tap('A')
for i in range(8): g.run(40); shot(g,f'ma{i}'); g.tap('A')
wait_idle(g)
warp(g,3,6,28,20,wait=200); print(g.objects()); g.face('U'); g.tap('A')
k=0; prev=False
for i in range(260):
    ib=g.in_battle()
    if ib and g.u32(g.R['bcf'])==g.R['act']: enemy_hp(g,1)
    g.run(24); shot(g,f'mb{k:03d}'); k+=1; g.tap('A')
    if ib!=prev: print(i,ib,flush=True); prev=ib
    if i>40 and not ib and g.idle(): break
wait_idle(g)
warp(g,10,9,6,13,wait=200); print(g.pos(),g.objects()); g.face('U'); g.tap('A')
for i in range(10): g.run(40); shot(g,f'mc{i}'); g.tap('A') if i<3 else None
g.u8(0x02000000); g.close()
