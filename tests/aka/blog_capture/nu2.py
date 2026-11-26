exec(open('/tmp/rc/base.py').read())
ed=sys.argv[1]; fast=sys.argv[2]=='1'
rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
g=new(st,rom=rom)
if fast: g.setflag(0x4AB,True)
P=g.R['party']; g.cmd(f'poke {P+0x56:08X} 01'); g.cmd(f'poke {P+0x57:08X} 00')
g.teleport('VIRIDIAN_CITY_POKEMON_CENTER_1F', 7, 4); g.run(30); g.face('U'); g.run(10)
tag=f'nv_{ed}{int(fast)}'; done=None; f0=g.u32(0x03003090+0x24)
for i in range(200):
    g.tap('A'); g.run(6)
    if g.u16(P+0x56)>1 and done is None: done=g.u32(0x03003090+0x24)-f0
    if g.u32(0x0203FF54) and g.idle():
        # script finished: keep mashing ~1.5 s like a player would
        for j in range(12): g.tap('A'); g.run(6); shot(g,f'{tag}_m{j:02d}')
        break
oid=g.u8(g.R['avatar']+5)
print(tag,'heal frames',done,'end frames', g.u32(0x03003090+0x24)-f0, 'facing', g.u8(g.R['objs']+oid*0x24+0x18)&0xF, 'idle', g.idle(), 'hp', g.u16(P+0x56))
g.run(150); g.tap('A'); g.run(60); shot(g,f'{tag}_later')
g.u8(0x02000000); g.close()
