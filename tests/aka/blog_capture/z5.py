exec(open('/tmp/rc/base.py').read())
g=new(); ps=g.u32(0x03004FB0); g.cmd(f'poke {ps:08X} 00')
one=bytes([0x79])+struct.pack('<HBH',16,5,0)+bytes(9)
k=0
for r in range(5):
    runscript(g,one*6+b'\x02')
    for i in range(12):
        g.run(10); shot(g,f'bw{k:02d}'); k+=1
g.close()
g=new()
g.tap('S'); g.run(40)
n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); downs(g,order.index(10)); g.tap('A'); g.run(30); g.tap('A')
for i in range(6): g.run(40); shot(g,f'fv{i}')
g.close()
