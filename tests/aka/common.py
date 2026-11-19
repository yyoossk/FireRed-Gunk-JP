import sys,struct; sys.path.insert(0,'/home/claude/tools')
from walker import *
def runscript(g,data):
    buf=g.R['strbuf']+0x200
    for i,b in enumerate(data): g.cmd(f'poke {buf+i:08X} {b:02X}')
    for a,v in ((0x03000EB1,b'\x01'),(0x03000EB0,b'\x00'),(0x03000EB8,struct.pack('<I',buf)),(0x03000EA8,b'\x00')):
        for i,b in enumerate(v): g.cmd(f'poke {a+i:08X} {b:02X}')
def wild(g,species,level):
    runscript(g,bytes([0xB6])+struct.pack('<HBH',species,level,0)+bytes([0xB7,0x02]))
    for i in range(40):
        g.run(30)
        if g.in_battle(): break
def enemy_hp(g,hp,slot=1):
    a=g.R['bmons']+0x58*slot+0x28
    g.cmd(f'poke {a:08X} {hp&0xff:02X}'); g.cmd(f'poke {a+1:08X} {hp>>8:02X}')
