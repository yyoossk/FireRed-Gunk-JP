exec(open('/tmp/rc/base.py').read())
g=new('/tmp/rc/t_arr.ss')
setslot(g,0,130,(57,58,89,63),nick='ギャラドス'); setslot(g,1,6,(53,17,89,126),nick='リザードン'); setslot(g,2,149,(58,85,89,126),nick='カイリュー')
warp(g,42,2,6,7); g.goto(6,6); g.face('U'); g.run(10)
for k in range(6): g.tap('A'); g.run(50)
g.tap('A'); g.run(50); g.tap('A'); g.run(80)   # レベル50 -> party screen
for s in range(3):
    g.tap('A'); g.run(30); g.tap('A'); g.run(30); g.cmd('tap D 1'); g.run(15)
shot(g,'z_sel')
for i in range(3): g.cmd('tap D 1'); g.run(15)
shot(g,'z_sel2'); g.tap('A'); g.run(60); shot(g,'z_conf'); g.tap('A'); g.run(60)
g.save('/tmp/rc/t_go.ss')
k=0
for i in range(900):
    g.tap('A'); g.run(24)
    if i%2==0: shot(g,f'zz{k:03d}'); k+=1
g.save('/tmp/rc/t_end.ss'); g.close()
