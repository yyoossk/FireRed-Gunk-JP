exec(open('/tmp/rc/base.py').read())
g=new(); g.teleport('VERMILION_CITY',24,32); g.run(60); g.face('D'); g.run(10)
g.tap('A'); g.run(60); g.tap('A'); g.run(60); g.cmd('tap D 1'); g.run(10); g.tap('A')
for i in range(30):
    g.run(40); shot(g,f'u{i:02d}')
    if i in (2,4,6): g.tap('A')
print(g.pos(), g.objects())
g.save('/tmp/rc/t_arr.ss'); g.close()
