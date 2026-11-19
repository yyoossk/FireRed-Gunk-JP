#include "constants/global.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/items.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.set FALSE, 0
	.set TRUE, 1
	.section .rodata
	.align 2

@ セキエイこうげんの ショップ: シルフの しゃちょうから マスターボールを もらったら マスターボールも
EventScript_JpIndigoMart::
	goto_if_set FLAG_GOT_MASTER_BALL_FROM_SILPH, EventScript_JpIndigoMartMB
	pokemart 0x08189778
	return
EventScript_JpIndigoMartMB:
	pokemart JpIndigoItemsMB
	return

	.align 2
JpIndigoItemsMB:
	.2byte ITEM_MASTER_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_MAX_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_NONE

@ そだてや: そだった レベルの あとに いまの レベル
EventScript_JpDaycareGrownFourIsland::
	msgbox 0x081A583F
	callnative JpDaycareLevelFourIsland
	msgbox Text_JpDaycareNowLevel
	return

EventScript_JpDaycareGrownRoute5::
	msgbox 0x0818C633
	callnative JpDaycareLevelRoute5
	msgbox Text_JpDaycareNowLevel
	return

EventScript_JpDaycareNotYetRoute5::
	msgbox 0x0818C586
	callnative JpDaycareLevelRoute5
	msgbox Text_JpDaycareNowLevel
	return

Text_JpDaycareNowLevel:
	.string "いまは　レベル{STR_VAR_3}だ！$"

@ 殿堂入り: EventScript_SetDefeatedEliteFourFlagsVars のあとに 伝説の ポケモンを もどす
EventScript_JpHoFFlags::
	call 0x081939A4
	callnative JpRespawnLegends
	return
