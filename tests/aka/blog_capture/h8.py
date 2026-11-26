exec(open('/tmp/rc/base.py').read())
g=new('/tmp/rc/t_go.ss')
k=0; wins=0; prev=False
for i in range(1400):
    ib=g.in_battle()
    if ib and g.u32(g.R['bcf'])==g.R['act']:
        enemy_hp(g,1)
    g.tap('A'); g.run(24)
    if i%2==0: shot(g,f'zz{k:03d}'); k+=1
    if ib!=prev:
        print(i,'battle' if ib else 'out', g.pos(), flush=True)
        prev=ib
g.save('/tmp/rc/t_end.ss'); g.u8(0x02000000); g.close()
