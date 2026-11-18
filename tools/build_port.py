import sys, os, subprocess, struct, glob, re, pickle
sys.path.insert(0,'/home/claude/tools')
from syms import jp, us, amap, filesyms
PORT='/home/claude/port'
JPROM='/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba'
CODE_BASE=0x08700000
EWRAM_BASE=0x0203FE00
objs=sorted(glob.glob(PORT+'/pb/*.o'))+sorted(glob.glob(PORT+'/gx/o/*.o'))
hint={'hk_eom':'event_object_movement.o','hk_bike':'bike.o','hk_overworld':'overworld.o','hk_load_save':'load_save.o',
      'hk_scrcmd':'scrcmd.o','hk_field_control_avatar':'field_control_avatar.o','hk_field_player_avatar':'field_player_avatar.o',
      'hk_trainer_see':'trainer_see.o','hk_party_menu':'party_menu.o'}
defined=set(); undef={}
for o in objs:
    out=subprocess.check_output(['arm-none-eabi-nm',o]).decode()
    base=os.path.basename(o)[:-2]
    if '/gx/o/' in o: hint[base]=base+'.o'
    for line in out.splitlines():
        p=line.split()
        if len(p)==3 and p[1] in 'TDRBtdrb' and p[1].isupper(): defined.add(p[2])
        elif len(p)==2 and p[0]=='U': undef.setdefault(p[1],set()).add(base)
LIBGCC={'__umodsi3','__udivsi3','__divsi3','__modsi3','_call_via_r0','_call_via_r1','_call_via_r2','_call_via_r3','_call_via_r4','_call_via_r5','_call_via_r6','_call_via_r7','memset','memcpy'}
OVERRIDE={'gJpMapNames':0x083B419C,'gJpMapsecName_CeladonDept':0x083B1723,'JpAppendBattleTowerBannedSpeciesName':0x080E74B1,'JpCreateNPCTrainerParty':0x08010B0D,'JpDrawItemListRow':0x810a345,'JpBag_BuildListMenuTemplate':0x8108f35,'JpBagDestroyPocketScrollArrowPair':0x8109475,'JpCreatePocketScrollArrowPair':0x8109385,'JpBagIsTutorial':0x810b8ad,'JpPocket_CalculateNItemsAndMaxShowed':0x81098c5,'JpPocketCalculateInitialCursorPosAndItemsAbove':0x81094f1,'JpBagPrintTextOnWin1CenteredColor0':0x810c459,'JpSpriteCB_BagVisualSwitchingPockets':0x8097ee1,'JpOpenContextMenu':0x810a381,'gJpPocketNames':0x840f4d4,'JpAddTextPrinterParameterized3':0x0812EC75,'gText_Box':0x083DABA1,'JpGetMenuCursorDimensionByFont':0x80f8a7d,'JpGetStringTilesWide':0x809c30d,'JpCreateWindowFromRect':0x809d005,'JpSetStdWindowBorderStyle':0x80f87f5,'JpAddTextPrinterParameterized':0x8002bb1,'JpStringExpandPlaceholders':0x8008ab5,'JpMenu_PrintFormatIntlPlayerName':0x812ee35,'JpMenu_InitCursor':0x8110311,'JpCreateMCMenuInputHandlerTask':0x809c5c5,'JpScheduleBgCopyTilemapToVram':0x80f7841,'JpFlagGet':0x806de3d,'JpPokeSum_PrintPageHeader':0x081374ED,'JpOpenBagAndChooseItem':0x0802FDED,'gJpBattlerControllerFuncs':0x03004F80,'JpBufferMonSkills':0x08136AC5,'JpPokeSum_PrintRightPaneText':0x08137681,'JpText_OakExplainCatching':0x0817D703,'JpText_MomLookingGreat':0x0817B9E3,'JpText_AideMustBeGoing':0x08170C8E,'gBattleMoveDamage':0x02023CB0,'STR_VAR_1':0,'STR_VAR_2':0,'STR_VAR_3':0,'JpText_RepelWoreOff':0x081A5949,'sJpTextPrinters':0x02020030,'JpRenderFont':0x08002DB9,'Common_Movement_QuestionMark':0x0819473F,'Common_Movement_ExclamationMark':0x08194741}
assign={}; missing=[]; thumbover=[]
for n,users in sorted(undef.items()):
    if n in defined: continue
    if n in LIBGCC and n not in ('memset','memcpy'): continue
    a=j=None
    if n in OVERRIDE:
        v=OVERRIDE[n]
        if v&1: thumbover.append((n,v))
        else: assign[n]=v
        continue
    for u in users:
        a,j=jp(n,hint.get(u))
        if j: break
    if j is None: missing.append((n,users,a)); continue
    if (a>>24)==8 and a<0x081EA000 and (a&1)==0:
        # thumb function? check symbol type via nm
        pass
    assign[n]=j
# thumb bit: functions need |1 for BL? linker handles BL by address; for function pointers need |1.
ftype={}
for line in open('/home/claude/work/us.nm'):
    p=line.split()
    if len(p)==3: ftype.setdefault(p[2],p[1])
if missing:
    print('MISSING:'); [print(' ',m[0],m[1],m[2] and hex(m[2])) for m in missing]
lines=[]; asm=['.thumb']
for n,j in assign.items():
    t=ftype.get(n,'?')
    if t in 'tT': asm.append(f'.global {n}\n.thumb_set {n}, 0x{j|1:08X}')
    else: lines.append(f'{n} = 0x{j:08X};')
asm+=[f'.global {n}\n.thumb_set {n}, 0x{v:08X}' for n,v in thumbover]
open(PORT+'/pb/jpsyms.s','w').write('\n'.join(asm)+'\n')
subprocess.check_call(['arm-none-eabi-as','-mcpu=arm7tdmi','-o',PORT+'/pb/jpsyms.o.tmp',PORT+'/pb/jpsyms.s'])
ld=f'''
SECTIONS {{
  .island 0x0812EEC0 : {{ *(.island) }}
  .island2 0x0802E524 : {{ *(.island2) }}
  .island3 0x0802E5A0 : {{ *(.island3) }}
  . = 0x{CODE_BASE:08X};
  .text : {{ *(.text) *(.text.*) }}
  .rodata : {{ *(.rodata) *(.rodata.*) *(script_data) }}
  .data : {{ *(.data) }}
  rom_end = .;
  . = 0x{EWRAM_BASE:08X};
  ewram (NOLOAD) : {{ *(ewram_data) *(.bss) *(COMMON) }}
  ewram_end = .;
  /DISCARD/ : {{ *(.comment) *(.ARM.attributes) }}
}}
''' + '\n'.join(lines)+'\n'
open(PORT+'/pb/port.ld','w').write(ld)
r=subprocess.run(['arm-none-eabi-ld','-T',PORT+'/pb/port.ld','-o',PORT+'/pb/port.elf']+objs+[PORT+'/pb/jpsyms.o.tmp']+['-L',PORT+'/tools/agbcc/lib','-lgcc','-lc','-Map',PORT+'/pb/port.map'],capture_output=True,text=True)
print(r.stdout[-3000:],r.stderr[-5000:])
if missing: sys.exit(1)
