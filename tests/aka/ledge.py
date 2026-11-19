import sys; sys.path.insert(0,'/tmp/t2'); from common import *
rom=sys.argv[1]; mode=sys.argv[2] if len(sys.argv)>2 else 'run'
g=Game('jp','/tmp/t2/now_fresh.ss',rom=rom); g.run(10)
g.teleport('ROUTE1',10,10); g.run(60)
w,h,cells,beh=g.grid()
def B(x,y): return beh(cells[(y+7)*w+x+7]&0x3FF)
def coll(x,y): return (cells[(y+7)*w+x+7]>>10)&3
cand=[]
for y in range(0,h-14):
  for x in range(0,w-14):
    if B(x,y)==0x3B and all(coll(x,yy)==0 and B(x,yy) not in (0x3B,0x3A,0x38,0x39) for yy in list(range(y-6,y))+[y+1,y+2,y+3,y+4]): cand.append((x,y))
print('ledges',cand[:5])
x,y=[c for c in cand if c[1]>=8][0]; print('use',x,y)
g.teleport('ROUTE1',x,y-6); g.run(80)
# walk 2 steps down so follower is behind
g.hold('D',40); g.run(30)
log=[]
pl=g.pos()
key='D' if mode=='walk' else 'D+B'
for i in range(40):
    g.hold('DB' if mode=='run' else 'D',4)
    objs=g.objects()
    log.append((g.pos(),[(o[1],o[2]) for o in objs]))
for l in log: print(l)
g.close()
