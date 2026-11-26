exec(open('/tmp/rc/base.py').read())
import walker
g=new(); g.teleport('SEVEN_ISLAND',10,10); g.run(60)
ev=walker._events(g); print(ev)
g.close()
