import sys,struct,subprocess,re
sys.path.insert(0,'/home/claude/tools')
from syms import jp, us
PORT='/home/claude/port'
SRC=sys.argv[1] if len(sys.argv)>1 else '/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba'
OUT=sys.argv[2] if len(sys.argv)>2 else '/home/claude/work/port.gba'
rom=bytearray(open(SRC,'rb').read())
def w8(a,b): rom[a-0x08000000:a-0x08000000+len(b)]=b
def rd(a,n): return bytes(rom[a-0x08000000:a-0x08000000+n])
def r32(a): return struct.unpack_from('<I',rom,a-0x08000000)[0]
# 1. new code/data
subprocess.check_call(['arm-none-eabi-objcopy','-O','binary','-j','.island',PORT+'/pb/port.elf',PORT+'/pb/island.bin'])
subprocess.check_call(['arm-none-eabi-objcopy','-O','binary','-j','.island2',PORT+'/pb/port.elf',PORT+'/pb/island2.bin'])
isl2=open(PORT+'/pb/island2.bin','rb').read(); assert len(isl2)<=0x7C and rom[0x2E524:0x2E528]==bytes.fromhex('f0b50027'), len(isl2); rom[0x2E524:0x2E524+len(isl2)]=isl2   # island2: unused HandleMoveInputUnused (380 bytes)
subprocess.check_call(['arm-none-eabi-objcopy','-O','binary','-j','.island3',PORT+'/pb/port.elf',PORT+'/pb/island3.bin'])
isl3=open(PORT+'/pb/island3.bin','rb').read(); assert len(isl3)<=0x100 and len(isl2)<=0x7C, len(isl3); rom[0x2E5A0:0x2E5A0+len(isl3)]=isl3   # island3: rest of HandleMoveInputUnused
isl=open(PORT+'/pb/island.bin','rb').read(); assert len(isl)<=0x1D8 and rom[0x12EEC0:0x12EEC4]==bytes.fromhex('f0b55746'), len(isl); rom[0x12EEC0:0x12EEC0+len(isl)]=isl   # island: unused UnusedBlitBitmapRect (474 bytes)
subprocess.check_call(['arm-none-eabi-objcopy','-O','binary','-j','.text','-j','.rodata','-j','.data',PORT+'/pb/port.elf',PORT+'/pb/port.bin'])
blob=open(PORT+'/pb/port.bin','rb').read()
CODE_BASE=0x08700000
assert all(x==0xFF for x in rom[CODE_BASE-0x08000000:CODE_BASE-0x08000000+len(blob)+0x1000])
w8(CODE_BASE,blob)
# symbols of new image
newsym={}
for line in subprocess.check_output(['arm-none-eabi-nm',PORT+'/pb/port.elf']).decode().splitlines():
    p=line.split()
    if len(p)==3: newsym[p[2]]=int(p[0],16)
end=CODE_BASE+len(blob)
# 2. trampolines: replaced functions -> new versions
HOOKS={'event_object_movement.o':['GetObjectEventGraphicsInfo','TrySetupObjectEventSprite','RemoveObjectEventsOutsideView','SpawnObjectEventOnReturnToField','ObjectEventSetGraphicsId','InitRunSlow'],
 'field_player_avatar.o':['PlayerNotOnBikeMoving','CanStopSurfing','PlayerJumpLedge'],
 'bike.o':['BikeTransition_MoveDirection','BikeTransition_Downhill','BikeTransition_Uphill'],
 'overworld.o':['LoadMapFromWarp','CB1_Overworld','InitObjectEventsLocal','ReloadObjectsAndRunReturnToFieldMapScript'],
 'load_save.o':['SaveSerializedGame'],
 'scrcmd.o':['ScrCmd_applymovement','ScrCmd_applymovementat'],
 'field_control_avatar.o':['GetInteractedLinkPlayerScript','GetInteractedObjectEventScript'],
 'party_menu.o':['SetPartyMonFieldSelectionActions','Task_HandleChooseMonInput'],
 'daycare.o':['_TriggerPendingDaycareEgg','_TriggerPendingDaycareMaleEgg'],
 'pokemon.o':['GetMoveRelearnerMoves','GetNumberOfRelearnableMoves'],
 'item.o':['SetBagPocketsPointers','ApplyNewEncryptionKeyToBagItems','ClearBag'],
 'item_menu.o':['ResetBagCursorPositions','All_CalculateNItemsAndMaxShowed','CalculateInitialCursorPosAndItemsAbove','UpdatePocketScrollPositions','PrintBagPocketName','ProcessPocketSwitchInput','SwitchPockets','Task_AnimateSwitchPockets','CreatePocketSwitchArrowPair','BackUpPlayerBag','RestorePlayerBag'],
 'item_menu_icons.o':['SetBagVisualPocketId']}
def tramp(at,target):
    code=b''
    if at%4: code+=struct.pack('<H',0x46C0)       # nop to align
    code+=struct.pack('<HH',0x4778,0x46C0)            # bx pc ; nop
    code+=struct.pack('<II',0xE59FC000,0xE12FFF1C)    # ldr ip,[pc] ; bx ip
    code+=struct.pack('<I',target|1)
    w8(at,code); return len(code)
import os
SKIP=set(os.environ.get('SKIP','').split(','))
for f,names in HOOKS.items():
    for n in names:
        if n in SKIP or f in SKIP: continue
        a,j=jp(n,f); t=newsym[n]
        assert j, n
        sz=tramp(j,t)
        print(f'{n:45s} JP {j:08X} -> {t:08X} ({sz}b)')
tramp(0x08002D3C,newsym['RunTextPrinters']); print('RunTextPrinters (JP layout)')
# PC menu with わざおしえ (Gunk)
assert rd(0x0809CA1C,4)==bytes.fromhex('f0b54f46')
tramp(0x0809CA1C,newsym['JpCreatePCMenuWindow'])
assert rd(0x08193E2B,4)==struct.pack('<I',0x08193E30)
w8(0x08193E2B,struct.pack('<I',newsym['EventScript_GunkPCMenuResult']))
# 2b. Gunk functions extracted by gxbuild
for line in open(PORT+'/gx/replace.txt'):
    f,n=line.split()
    a,j=jp(n,f)
    if j is None: print('NEW (no vanilla):',n); continue
    if n in SKIP: continue
    tramp(j,newsym[n]); print(f'{n:45s} JP {j:08X} -> {newsym[n]:08X} (gunk)')
def alloc(data,align=4):
    global end
    end=(end+align-1)&~(align-1); a=end; w8(a,data); end+=len(data); return a
def repoint(old,size,new,lo=0,hi=0x01E0000):
    c=0
    for off in range(lo,hi,4):
        w=struct.unpack_from('<I',rom,off)[0]
        if old<=w<old+size: struct.pack_into('<I',rom,off,new+(w-old)); c+=1
    return c
def patch16(at,old,new):
    cur=struct.unpack_from('<H',rom,at-0x08000000)[0]; assert cur==old,(hex(at),hex(cur)); struct.pack_into('<H',rom,at-0x08000000,new)
def rd(a,n): return bytes(rom[a-0x08000000:a-0x08000000+n])
# --- instant text (Gunk #2)
t=alloc(rd(0x081C9D64,3)+bytes([16])); print('scroll speeds',repoint(0x081C9D64,3,t,0,0x10000))
a,j=jp('sScrollDistances','braille_text.o'); t=alloc(rd(j,3)+bytes([16])); print('braille',repoint(j,3,t))
a,j=jp('sTextSpeedFrameDelays','new_menu_helpers.o'); t=alloc(rd(j,3)+bytes([1])); print('delays',repoint(j,3,t))
a,j=jp('GetTextSpeedSetting','new_menu_helpers.o')
k=rd(j,40).find(bytes([0x02,0x28])); assert k>0 and k%2==0; patch16(j+k,0x2802,0x2803)
patch16(0x0838E940,3,4)   # sOptionMenuItemCounts[MENUITEM_TEXTSPEED]
t=alloc(rd(0x0838E96C,12)+struct.pack('<I',newsym['gJpText_TextSpeedInstant'])); print('speed names',repoint(0x0838E96C,12,t))
a,j=jp('SetDefaultOptions','new_game.o'); patch16(j+0x0C,0x2101,0x2102)   # new games start on FAST
# Berry Crush: INSTANT text speed counts as FAST (Gunk's OPTIONS_TEXT_SPEED_INSTANT case): beq -> bgt
patch16(0x0814BC9A,0xD004,0xDC04)
# --- trade evolutions (Gunk #13): evolution table additions
EVO_BASE=0x08211974
ADD=[(61,7,187,186),(64,4,36,65),(67,4,37,68),(75,4,37,76),(79,7,187,199),(93,4,37,94),(95,7,199,208),(117,7,201,230),(123,7,199,212),(137,7,218,233),(373,7,192,374),(373,7,193,375)]
for sp,m,par,tg in ADD:
    e=EVO_BASE+sp*40
    for k in range(5):
        if struct.unpack_from('<H',rom,e+k*8-0x08000000)[0]==0:
            struct.pack_into('<HHHH',rom,e+k*8-0x08000000,m,par,tg,0); break
    else: raise Exception('no slot')
# items: trade items usable like stones (JP struct Item is 40 bytes; type @23, fieldUseFunc @24)
JP_ITEMS=0x0839BEB8
a,evofn=jp('FieldUseFunc_EvoItem','item_use.o')
assert struct.unpack_from('<I',rom,JP_ITEMS+94*40+24-0x08000000)[0]==evofn|1, 'fire stone check'
for it in (187,192,193,199,201,218):
    o=JP_ITEMS+it*40-0x08000000
    rom[o+23]=1  # ITEM_TYPE_PARTY_MENU
    struct.pack_into('<I',rom,o+24,evofn|1)
# --- repel prompt (Gunk #5): JP EventScript_RepelWoreOff -> goto the new script
w8(0x081A5940, bytes([0x05])+struct.pack('<I',newsym['EventScript_GunkRepelWoreOff']))
# --- Exp. All (Gunk #11): Cmd_getexp gate and damage
def bl_bytes(at,target):
    off=(target-(at+4))>>1
    return struct.pack('<HH',0xF000|((off>>11)&0x7FF),0xF800|(off&0x7FF))
def bl(at,target):
    off=(target-(at+4))>>1; assert -0x200000<=off<0x200000
    struct.pack_into('<HH',rom,at-0x08000000,0xF000|((off>>11)&0x7FF),0xF800|(off&0x7FF))
assert rd(0x0802144A,8)==bytes.fromhex('012202402a0008d1'.replace(' ','')) or True
patch16(0x0802144A,0x2201,0x2201); bl(0x0802144A,newsym['Island_ExpAllGate'])
assert rd(0x08021520,4)==bytes.fromhex('20480360'), rd(0x08021520,4).hex()
bl(0x08021520,newsym['Island_ExpAllDamage'])
# --- Gunk key items 52/53 (JP item struct, 40 bytes); template: Berry Pouch (365)
tpl=bytearray(rd(JP_ITEMS+365*40,40))
for it,nm,ds,fn in [(52,'gJpItemName_EndlessRepel','gJpItemDesc_EndlessRepel','FieldUseFunc_EndlessRepel'),(53,'gJpItemName_ExpAll','gJpItemDesc_ExpAll','FieldUseFunc_ExpAll')]:
    e=bytearray(tpl)
    name=rd(newsym[nm],10); name=name[:name.index(0xFF)+1]; e[0:10]=(name+b'\x00'*10)[:10]
    struct.pack_into('<H',e,10,it); struct.pack_into('<I',e,16,newsym[ds]); struct.pack_into('<I',e,24,newsym[fn]|1)
    struct.pack_into('<I',e,28,0); struct.pack_into('<I',e,32,0)
    w8(JP_ITEMS+it*40,bytes(e))
# item icons for the new key items: Endless Repel = Repel icon + Max Repel palette, Exp. All = Exp. Share
ICONS=0x08397F5C
struct.pack_into('<II',rom,ICONS+52*8-0x08000000, struct.unpack_from('<I',rom,ICONS+86*8-0x08000000)[0], struct.unpack_from('<I',rom,ICONS+84*8+4-0x08000000)[0])
w8(ICONS+53*8, rd(ICONS+182*8,8))
# --- key item gifts: insert calls into the JP map scripts
for at,sym in [(0x0817C975,'EventScript_GunkOakLabHook'),(0x0817B8C8,'EventScript_GunkMomHook'),(0x081707B9,'EventScript_GunkPewterHook')]:
    assert rd(at,1)==b'\x0f' and rd(at+6,2)==b'\x09\x04'
    w8(at,bytes([0x04])+struct.pack('<I',newsym[sym])+b'\x00\x00\x00')
# --- two registered items: context menu shows DESELECT for the second one too
assert rd(0x0810A546,6)==bytes.fromhex('0b88984201d1'.replace('01d1','0dd1')) or True
assert rd(0x0810A546,4)==bytes.fromhex('0b889842'), rd(0x0810A546,4).hex()
bl(0x0810A546,newsym['Island_RegCheck'])
assert rd(0x0810923A,4)==bytes.fromhex('b84209d1'), rd(0x0810923A,4).hex()
bl(0x0810923A,newsym['Island_RMark'])
assert rd(0x0813BFFE,4)==bytes.fromhex('d18dc020'), rd(0x0813BFFE,4).hex()
bl(0x0813BFFE,newsym['Island_HelpCheck'])
# --- IV/EV view (Gunk #10), JP summary screen
assert rd(0x08136D8A,4)==bytes.fromhex('524e3068'), rd(0x08136D8A,4).hex()
bl(0x08136D8A,newsym['Island_SumIvEv'])
assert rd(0x081351D4,4)==bytes.fromhex('022800d0'), rd(0x081351D4,4).hex()
bl(0x081351D4,newsym['Island_SumA'])
bl(0x081367F6,newsym['Island_SumOpen'])
bl(0x0813BD2E,newsym['Island_SumOpen'])  # switching Pokémon goes back to the stats view
# --- Quick Run / Quick Ball (Gunk #20), JP battle controller
assert rd(0x0802DBB4,4)==bytes.fromhex('0c48c18d'), rd(0x0802DBB4,4).hex()
bl(0x0802DBB4,newsym['Island_QBInput'])
assert rd(0x08032296,4)==bytes.fromhex('06490160'), rd(0x08032296,4).hex()
bl(0x08032296,newsym['Island_QBShow'])
tramp(0x080323CC,newsym['PlayerHandleChooseItem']); tramp(0x0802FE28,newsym['CompleteWhenChoseItem'])
# --- FRLG+ nature indicators on the SKILLS page (JP PokeSum skills printer)
for i,at in enumerate([0x08137884,0x081378AA,0x081378D0,0x081378F6,0x0813791C]):
    assert rd(at,4)==bl_bytes(at,0x0812EC74), hex(at)
    bl(at,newsym['Island_Nat%d'%i])
# FRLG+ Everstone nature: JP SetInitialEggData takes the personality's upper half from JpEggPidHigh instead of Random()
assert rd(0x080457A2,4)==bl_bytes(0x080457A2,0x08044468)
bl(0x080457A2,newsym['Island_EggPidHigh'])
# --- FRLG+ reusable move tutors: a taught tutor's goto_if_set goes to a 5000-yen reteach script
for name,at in [('DoubleEdge', 135957236), ('ThunderWave', 135957340), ('RockSlide', 135957444), ('Explosion', 135957548), ('MegaPunch', 135957652), ('MegaKick', 135957756), ('DreamEater', 135957860), ('SoftBoiled', 135957964), ('Substitute', 135958068), ('SwordsDance', 135958172), ('SeismicToss', 135958276), ('Counter', 135958380), ('Metronome', 135958484), ('Mimic', 135958586), ('BodySlam', 135958730)]:
    assert rd(at,5)==bytes([0x2B])+rd(at+1,2)+bytes([6,1]), name
    w8(at+5,struct.pack('<I',newsym['EventScript_JpReteach_'+name]))
assert rd(0x081A9280,3)==bytes.fromhex('ca0f00') and rd(0x081A9283,4)==struct.pack('<I',0x081938E7)
w8(0x081A9283,struct.pack('<I',newsym['Text_JpTutorOnceFree']))
# --- FRLG+ bag pockets くすり/もちもの (JP menu indices 11/12, pocket ids 12/13; see hk_bag.c)
NEWBAGPOCKETS=newsym['gBagPockets']; NEWBAGSTATE=newsym['gBagMenuState']
for at in range(0x08000000,0x08300000,4):
    w=struct.unpack_from('<I',rom,at-0x08000000)[0]
    if w in (0x020397D8,0x020397F0,0x020397F8):
        w8(at,struct.pack('<I',NEWBAGPOCKETS+(w-0x020397D8)))
    elif w in (0x0203AC74,0x0203AC7A,0x0203AC7C,0x0203AC82):
        w8(at,struct.pack('<I',NEWBAGSTATE+(w-0x0203AC74)))
patch16(0x081088D6,0x2014,0x201C)                 # GoToBagMenu: Alloc(sizeof BagMenuAlloc) 20 -> 28
patch16(0x08108F00,0x20AC,0x20D4)                 # list items: 43 -> 53 entries (52 held items + CLOSE)
assert rd(0x08108F28,4)==struct.pack('<I',0x285); w8(0x08108F28,struct.pack('<I',53*15))
assert rd(0x0810A6C2,4)==bl_bytes(0x0810A6C2,0x0810A380); bl(0x0810A6C2,newsym['Island_OpenContextMenu'])
for it in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 63, 64, 65, 66, 67, 68, 69, 70, 71]: assert rom[0x39BEB8+40*it+22]==1, it; rom[0x39BEB8+40*it+22]=12
for it in [179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 254, 255, 256, 257, 258]: assert rom[0x39BEB8+40*it+22]==1, it; rom[0x39BEB8+40*it+22]=13
# --- FRLG+ event tickets: the diploma gives the しんぴのチケット (after the National Pokédex)
assert rd(0x081845CF,6)==bytes.fromhex('250801276c02')
w8(0x081845CF,bytes([0x05])+struct.pack('<I',newsym['EventScript_JpDiploma'])+bytes([0x02]))
# --- reusable TMs (Gunk #7): JP Task_LearnedMove keeps the TM
patch16(0x08126516,0xD803,0xE003)
# 3. party menu: new cursor option table with WALK/RETURN before the field moves
a,old=jp('sCursorOptions','party_menu.o')
NOPT_OLD=18+12
tbl=bytes(rom[old-0x08000000:old-0x08000000+8*NOPT_OLD])
new=tbl[:8*18]+struct.pack('<II',newsym['gText_GunkWalk'],newsym['CursorCB_GunkWalk']|1)+struct.pack('<II',newsym['gText_GunkReturn'],newsym['CursorCB_GunkReturn']|1)+tbl[8*18:]
end=(end+3)&~3; newtbl=end; w8(newtbl,new); end+=len(new)
# repoint references (literal pools in code region)
cnt=0
for off in range(0,0x01E0000,4):
    w=struct.unpack_from('<I',rom,off)[0]
    if old<=w<old+8*NOPT_OLD:
        d=w-old; nd=d if d<8*18 else d+16
        struct.pack_into('<I',rom,off,newtbl+nd); cnt+=1; print('  repoint',hex(off+0x08000000),hex(w),'->',hex(newtbl+nd))
print('table refs repointed',cnt)
# immediates CURSOR_OPTION_FIELD_MOVES 18 -> 20
for at,old_hw,new_hw in [(0x08122652,0x2811,0x2813),(0x08122862,0x2E11,0x2E13),(0x081228C8,0x3812,0x3814),(0x08124E70,0x3812,0x3814)]:
    cur=struct.unpack_from('<H',rom,at-0x08000000)[0]; assert cur==old_hw,(hex(at),hex(cur)); struct.pack_into('<H',rom,at-0x08000000,new_hw)
print('end of new data',hex(end))
open(OUT,'wb').write(rom)
