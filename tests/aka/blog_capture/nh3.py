exec(open('/tmp/rc/base.py').read())
g=new(); setlead(g,6); g.setvar(0x4020,250)
P=g.R['party']; g.cmd(f'poke {P+0x56:08X} 01'); g.cmd(f'poke {P+0x57:08X} 00')
g.teleport('VIRIDIAN_CITY_POKEMON_CENTER_1F', 7, 7); g.run(60)
for d in 'UUU': g.step(d)
g.run(30); g.face('U'); g.tap('A')
for i in range(80):
    g.run(8)
    if g.u32(0x0203FF54) and g.idle(): break
    g.tap('A')
g.run(20); shot(g,'heal_down')
g.u8(0x02000000); g.close()
