import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
g.setflag(0x82); g.setflag(0x2BE)   # ran from Articuno
g.teleport('SEAFOAM_ISLANDS_B4F',9,5); g.run(40); g.shot('/tmp/t2/lg0.png')
fn=int(sys.argv[2],16)|1
runscript(g,bytes([0x23])+struct.pack('<I',fn)+b'\x02'); g.run(30)
print('flags',g.getflag(0x82),g.getflag(0x2BE))
g.teleport('SEAFOAM_ISLANDS_B4F',9,5); g.run(40); g.shot('/tmp/t2/lg1.png')
g.close()
