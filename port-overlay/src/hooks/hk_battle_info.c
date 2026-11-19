#include "global.h"
#include "battle.h"
#include "battle_controllers.h"
#include "battle_message.h"
#include "battle_anim.h"
#include "string_util.h"
#include "sound.h"
#include "constants/songs.h"
#include "constants/moves.h"
// 赤フルカラー: バトルで わざの こうかと いりょく・めいちゅう、あいての HP。START で きりかえ (L・R は ヘルプ)
// JP right box: window 7 "PP", 9 PP numbers, 8 "わざタイプ／" label (6 tiles), 10 type name (4 tiles).
// Page 0: type (8) + effectiveness vs the opponent (10). Page 1: いりょく / めいちゅう. Page 2: あいての HP.

#define JpTypeNames      ((const u8 (*)[5])0x0820788C)
#define JpTypeEffectiveness ((const u8 *)0x0820773C)
#define JpDynamicColors  ((const u8 *)0x083C0057)

extern const u8 gJpText_BtlPower[];
extern const u8 gJpText_BtlAccuracy[];
extern const u8 gJpText_BtlFoe[];
extern const u8 gJpText_BtlHp[];
extern const u8 gJpText_BtlSmallFont[];
extern const u8 gJpText_BtlNone[];
extern const u8 gJpText_BtlNoValue[];
extern const u8 *const gJpText_BtlEffect[];

__attribute__((section("ewram_late"))) static u8 sJpMoveInfoPage = 0;

static u8 GetJpEffectiveness(u16 move)
{
    u8 atkType = gBattleMoves[move].type;
    u8 target = GetBattlerAtPosition(B_POSITION_OPPONENT_LEFT);
    u8 t1 = gBattleMons[target].type1, t2 = gBattleMons[target].type2;
    u16 mod = 40;  // x4 scale: 40 = x1
    s32 i;

    for (i = 0; JpTypeEffectiveness[i] != TYPE_ENDTABLE; i += 3)
    {
        if (JpTypeEffectiveness[i] == TYPE_FORESIGHT)
            continue;
        if (JpTypeEffectiveness[i] == atkType)
        {
            if (JpTypeEffectiveness[i + 1] == t1)
                mod = mod * JpTypeEffectiveness[i + 2] / 10;
            if (JpTypeEffectiveness[i + 1] == t2 && t1 != t2)
                mod = mod * JpTypeEffectiveness[i + 2] / 10;
        }
    }
    switch (mod)
    {
    case 0:   return 0;  // x0
    case 10:  return 1;  // x1/4
    case 20:  return 2;  // x1/2
    case 80:  return 4;  // x2
    case 160: return 5;  // x4
    default:  return 3;  // x1
    }
}

static void PutColored(const u8 *text, u8 windowId)
{
    u8 *p = StringCopy(gDisplayedStringBattle, JpDynamicColors);
    StringCopy(p, text);
    BattlePutTextOnWindow(gDisplayedStringBattle, windowId);
}

void JpMoveSelectionDisplayMoveType(void)
{
    struct ChooseMoveStruct *moveInfo = (struct ChooseMoveStruct *)(&gBattleBufferA[gActiveBattler][4]);
    u16 move = moveInfo->moves[gMoveSelectionCursor[gActiveBattler]];
    u8 buf[12];
    u8 *p;

    (void)p;
    switch (sJpMoveInfoPage % 3)
    {
    default:
        PutColored(JpTypeNames[gBattleMoves[move].type], 8);
        if (gBattleMoves[move].power == 0 || move == MOVE_CURSE)
            PutColored(gJpText_BtlNoValue, 10);
        else
            PutColored(gJpText_BtlEffect[GetJpEffectiveness(move)], 10);
        break;
    case 1:  // めいちゅう (PP line) / いりょく (type line)
        StringCopy(gDisplayedStringBattle, gJpText_BtlAccuracy);
        BattlePutTextOnWindow(gDisplayedStringBattle, 7);
        if (gBattleMoves[move].accuracy == 0)
            StringCopy(buf, gJpText_BtlNoValue);
        else
            ConvertIntToDecimalStringN(buf, gBattleMoves[move].accuracy, STR_CONV_MODE_RIGHT_ALIGN, 3);
        PutColored(buf, 9);
        StringCopy(gDisplayedStringBattle, gJpText_BtlPower);
        BattlePutTextOnWindow(gDisplayedStringBattle, 8);
        if (gBattleMoves[move].power <= 1)
            StringCopy(buf, gJpText_BtlNoValue);
        else
            ConvertIntToDecimalStringN(buf, gBattleMoves[move].power, STR_CONV_MODE_RIGHT_ALIGN, 3);
        PutColored(buf, 10);
        break;
    case 2:  // あいて HP / 45/120
    {
        u8 target = GetBattlerAtPosition(B_POSITION_OPPONENT_LEFT);
        u8 hp[24];
        StringCopy(gDisplayedStringBattle, gJpText_BtlFoe);
        BattlePutTextOnWindow(gDisplayedStringBattle, 7);
        StringCopy(gDisplayedStringBattle, gJpText_BtlHp);
        BattlePutTextOnWindow(gDisplayedStringBattle, 9);
        p = StringCopy(hp, gJpText_BtlSmallFont);
        p = ConvertIntToDecimalStringN(p, gBattleMons[target].hp, STR_CONV_MODE_LEFT_ALIGN, 3);
        *p++ = 0xBA;  // '/'
        ConvertIntToDecimalStringN(p, gBattleMons[target].maxHP, STR_CONV_MODE_LEFT_ALIGN, 3);
        PutColored(hp, 8);
        StringCopy(gDisplayedStringBattle, gJpText_BtlNone);
        BattlePutTextOnWindow(gDisplayedStringBattle, 10);
        break;
    }
    }
}

#define JpMoveSelectionDisplayPpString ((void (*)(void))0x0802FF91)
#define JpMoveSelectionDisplayPpNumber ((void (*)(void))0x0802FFC9)

// HandleInputChooseMove: START switches the page
void JpChooseMoveCheckR(void)
{
    if (JOY_NEW(START_BUTTON))
    {
        PlaySE(SE_SELECT);
        sJpMoveInfoPage = (sJpMoveInfoPage + 1) % 3;
        JpMoveSelectionDisplayPpString();
        if (sJpMoveInfoPage == 0)
            JpMoveSelectionDisplayPpNumber();
        JpMoveSelectionDisplayMoveType();
    }
}
