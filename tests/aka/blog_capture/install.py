import shutil, os
O='/tmp/rc/out/'
M={'/tmp/blog/s/':{'title':'title_29','title_old':'title_old_29','follow_talk1':'follow_talk1','follow_talk2':'follow_talk2','cut2':'cut2','cut3':'cut3',
 'party_sub':'party_sub','pc2n':'pc2n','menupc1':'menupc1','menupc2':'mq0','hm_town':'hm_town','hm_cave':'hm_cave','hm_flash':'hm_flash','hm_flymap':'lb_cave1',
 'lr_party':'lr_party','lr_bag':'lr_bag','mom1':'mm08','mom2':'mm11','cont1':'cc5','cont2':'cc7','nick1':'nick1','nick2':'nick2','boxsw':'bu10',
 'bag2':'bagp2','bag4':'bagp4','bag3':'bagp3','option_expall':'option_expall','quickball':'quickball','btl1':'btl1','btl2':'btl2','foehp':'fj27',
 'sum2':'sum2','sum3':'sum3','sum4':'sum4','dexst1':'dexst1','dexst2':'dexst2','dexhere1':'dh_r12','dexhere2':'dh_cave','here_field':'here_field',
 'dexarea_player':'dexarea','safari':'safari','mbmart':'mbmart'},
 '/tmp/bt/':{'jp_003_menu':'t01','jp_005_arrive':'u10','jp_013_desk':'x03','jp_037_fight':'zz025','tm_jp5':'tm_jp5'},
 '/tmp/bt2/':{'jp_112_between':'zz392','jp_113_between':'zz396'},
 '/tmp/pg/':{'jp_ddn16':'pa03','nv_003_menu2':'pe2'},
 '/tmp/walk/':{'jp_00002':'ma1','jp_00025':'mb002','jp_00027_b':'mb030','jp_00031':'mc2','jp_00034':'sa1','jp_00037':'sc01','jp_00049':'sd0'},
 '/tmp/t151/':{'dy_3':'kdy2','ts1_03':'ksq02','mew1_03':'kmew02','mew1_battle':'kmew14','fossil_13':'kfos06','pq_0':'pq_0'}}
n=0
for d,m in M.items():
    bd='/tmp/blog_bak/'+d.strip('/').split('/')[-1]+'/'; os.makedirs(bd,exist_ok=True)
    for k,v in m.items():
        if os.path.exists(d+k+'.png') and not os.path.exists(bd+k+'.png'): shutil.copy(d+k+'.png',bd+k+'.png')
        shutil.copy(O+v+'.png', d+k+'.png'); n+=1
print(n)
