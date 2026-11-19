import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(10)
g.teleport('CERULEAN_CITY',31,23); g.run(30); g.shot('/tmp/t2/gw0.png')
g.hold('U',40); g.run(120); g.shot('/tmp/t2/gw1.png')
g.hold('U',60); g.run(60); g.shot('/tmp/t2/gw2.png')
g.close()
