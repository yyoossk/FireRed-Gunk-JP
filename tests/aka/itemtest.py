import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
rom=sys.argv[1]; st=sys.argv[2]; mp=sys.argv[3]
g=Game('jp',st,rom=rom); g.run(10)
g.teleport(mp,5,5); g.run(80)
items=[o for o in g.objects() if o[3]==92]
print('items',items)
w,h,cells,beh=g.grid()
def free(x,y): return (cells[(y+7)*w+x+7]>>10)&3==0 and not any(o[1]==x and o[2]==y for o in g.objects())
it=items[0]; x,y=it[1],it[2]
for dx,dy,d in ((0,1,'U'),(0,-1,'D'),(1,0,'L'),(-1,0,'R')):
    if free(x+dx,y+dy): break
g.teleport(mp,x+dx,y+dy); g.run(80); g.tap(d); g.run(20)
print('pos',g.pos(),'facing',g.facing())
g.tap('A'); g.run(60); g.shot('/tmp/t2/it.png')
g.close()
