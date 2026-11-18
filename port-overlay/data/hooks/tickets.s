#include "constants/global.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/items.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.set FALSE, 0
	.set TRUE, 1
	.set SPECIAL_ShowDiploma, 264
	.section .rodata
	.align 2

@ FRLG+: the GAME FREAK designer gives the しんぴのチケット (Navel Rock) after the Kanto diploma,
@ once the player has the National Pokédex
EventScript_JpDiploma::
	special ShowDiploma
	waitstate
	goto_if_set FLAG_RECEIVED_MYSTIC_TICKET, EventScript_JpDiplomaEnd
	checkitem ITEM_MYSTIC_TICKET, 1
	goto_if_eq VAR_RESULT, TRUE, EventScript_JpDiplomaEnd
	goto_if_unset FLAG_SYS_NATIONAL_DEX, EventScript_JpCantGiveMysticTicket
	msgbox Text_JpGiveMysticTicket
	giveitem ITEM_MYSTIC_TICKET, 1
	goto_if_eq VAR_RESULT, FALSE, EventScript_JpDiplomaEnd
	setflag FLAG_RECEIVED_MYSTIC_TICKET
	setflag FLAG_ENABLE_SHIP_NAVEL_ROCK
	msgbox Text_JpExplainMysticTicket
EventScript_JpDiplomaEnd::
	release
	end

EventScript_JpCantGiveMysticTicket::
	msgbox Text_JpCantGiveMysticTicket
	release
	end

Text_JpGiveMysticTicket::
	.string "ずかんを うめてくれた おれいに\n"
	.string "これを あげよう！$"
Text_JpExplainMysticTicket::
	.string "それは しんぴの チケット！\p"
	.string "クチバの みなとから ふねに のれば\n"
	.string "さいはての ことうへ いけるんだ$"
Text_JpCantGiveMysticTicket::
	.string "じつは ずかんの おれいに\n"
	.string "わたしたい ものが あるんだ\p"
	.string "ぜんこく ずかんに なったら\n"
	.string "また きてくれ！$"
