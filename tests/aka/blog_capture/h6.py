exec(open('/tmp/rc/base.py').read())
g=new('/tmp/rc/t_arr.ss')
setslot(g,0,130,(57,58,89,63),nick='ギャラドス'); setslot(g,1,6,(53,17,89,126),nick='リザードン'); setslot(g,2,149,(58,85,89,126),nick='カイリュー')
warp(g,42,2,6,7); g.goto(6,6); g.face('U'); g.run(10)
for k in range(6): g.tap('A'); g.run(50)
shot(g,'y_menu'); g.tap('A')
for i in range(24):
    g.run(40); shot(g,f'y{i:02d}'); g.tap('A')
g.save('/tmp/rc/t_sel.ss'); g.close()
