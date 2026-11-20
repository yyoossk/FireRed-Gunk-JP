#include "constants/global.h"
#include "constants/flags.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.set FALSE, 0
	.set TRUE, 1
	.set JpEventScript_BufferItemsPocket, 0x08193B81
	.set JpEventScript_BufferKeyItemsPocket, 0x08193B91
	.set JpEventScript_BufferPokeBallsPocket, 0x08193BA1
	.set JpEventScript_BufferTMCase, 0x08193BB1
	.set JpEventScript_BufferBerryPouch, 0x08193BC1
	.set JpEventScript_PlayFanfareObtainedItem, 0x08193BEC
	.section .rodata
	.align 2

@ EventScript_BufferPocketNameTryFanfare (0x08193B44) は ポケット 1〜5 しか みないので、
@ くすり(12)・もちもの(13) ポケットの どうぐは ひろえず もらえなかった（スクリプトが とちゅうで おわる）。
@ さいしょの copyvar を ここへの goto に かえる。
EventScript_JpBufferPocketName::
	copyvar VAR_0x8000, VAR_RESULT
	goto_if_eq VAR_0x8000, 1, JpEventScript_BufferItemsPocket
	goto_if_eq VAR_0x8000, 2, JpEventScript_BufferKeyItemsPocket
	goto_if_eq VAR_0x8000, 3, JpEventScript_BufferPokeBallsPocket
	goto_if_eq VAR_0x8000, 4, JpEventScript_BufferTMCase
	goto_if_eq VAR_0x8000, 5, JpEventScript_BufferBerryPouch
	goto_if_eq VAR_0x8000, 12, EventScript_JpBufferMedicinePocket
	goto_if_eq VAR_0x8000, 13, EventScript_JpBufferHeldItemsPocket
	end

EventScript_JpBufferMedicinePocket:
	bufferstring STR_VAR_3, Text_JpMedicinePocket
	call_if_eq VAR_0x8007, TRUE, JpEventScript_PlayFanfareObtainedItem
	return

EventScript_JpBufferHeldItemsPocket:
	bufferstring STR_VAR_3, Text_JpHeldItemsPocket
	call_if_eq VAR_0x8007, TRUE, JpEventScript_PlayFanfareObtainedItem
	return

Text_JpMedicinePocket:
	.string "くすりポケット$"
Text_JpHeldItemsPocket:
	.string "もちものポケット$"

@ Std_PutItemAway（giveitem_msg・msgreceiveditem の「〜ポケットに しまった」）の ポケットの なまえ（0x08195FD0）も
@ 1〜5 しか みず、くすり・もちものの どうぐを もらうと スクリプトが とちゅうで おわっていた
@（オーキドの じょしゅの かわらずのいし：フラグが たたず なんども もらえる）。
	.set JpEventScript_PutAwayItems, 0x0819600D
	.set JpEventScript_PutAwayKeyItems, 0x08196012
	.set JpEventScript_PutAwayPokeBalls, 0x08196017
	.set JpEventScript_PutAwayTMCase, 0x0819601C
	.set JpEventScript_PutAwayBerryPouch, 0x08196021
EventScript_JpBufferPutAwayPocketName::
	copyvar VAR_0x8000, VAR_RESULT
	goto_if_eq VAR_0x8000, 1, JpEventScript_PutAwayItems
	goto_if_eq VAR_0x8000, 2, JpEventScript_PutAwayKeyItems
	goto_if_eq VAR_0x8000, 3, JpEventScript_PutAwayPokeBalls
	goto_if_eq VAR_0x8000, 4, JpEventScript_PutAwayTMCase
	goto_if_eq VAR_0x8000, 5, JpEventScript_PutAwayBerryPouch
	goto_if_eq VAR_0x8000, 12, EventScript_JpPutAwayMedicine
	goto_if_eq VAR_0x8000, 13, EventScript_JpPutAwayHeldItems
	end
EventScript_JpPutAwayMedicine:
	bufferstring STR_VAR_3, Text_JpMedicinePocket
	return
EventScript_JpPutAwayHeldItems:
	bufferstring STR_VAR_3, Text_JpHeldItemsPocket
	return
