import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/f151.ss',rom=sys.argv[1]); g.run(10)
runscript(g,bytes([0x39,3,5,0xFF])+struct.pack('<HH',20,12)+bytes([0x02])); g.run(300)
g.shot('/tmp/t2/sqpos.png'); g.close()
