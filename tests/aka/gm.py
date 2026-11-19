import sys; sys.path.insert(0,'/tmp/t2'); from common import *
n=int(sys.argv[2])
g=Game('jp','/tmp/t2/s21_fresh.ss',rom=sys.argv[1]); g.run(10)
g.shot(f'/tmp/t2/gm_{n}_a.png')
one=bytes([0x79])+struct.pack('<HBH',16,5,0)+bytes(9)
runscript(g,one*n+b'\x02'); g.run(120)
g.shot(f'/tmp/t2/gm_{n}_b.png')
g.close()
