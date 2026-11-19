#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "overworld.h"
#include "pokemon.h"
#include "pokedex.h"
#include "string_util.h"
#include "sound.h"
#include "constants/songs.h"
#include "constants/region_map_sections.h"
#include "constants/flags.h"
#include "constants/species.h"
// 赤フルカラーの機能を ファイアレッドに

bool8 TryRunOnFrameMapScript(void);
#define FLAG_JP_BIKE_GEAR 0x0E3

// ProcessPlayerFieldInput: bl TryRunOnFrameMapScript -> here. FRLG+ bike gear: B on the bike switches gears
bool8 JpOnFrameScriptAndBikeGear(void)
{
    if (TryRunOnFrameMapScript() == TRUE)
        return TRUE;
    if (JOY_NEW(B_BUTTON) && (gPlayerAvatar.flags & (PLAYER_AVATAR_FLAG_MACH_BIKE | PLAYER_AVATAR_FLAG_ACRO_BIKE))
     && GetCurrentRegionMapSectionId() != MAPSEC_ROUTE_17)
    {
        if (FlagGet(FLAG_JP_BIKE_GEAR))
            FlagClear(FLAG_JP_BIKE_GEAR);
        else
            FlagSet(FLAG_JP_BIKE_GEAR);
        PlaySE(SE_BIKE_BELL);
    }
    return FALSE;
}

// そだてや: いまの レベル -> gStringVar3
static void BufferDaycareLevel(struct BoxPokemon *mon, u32 steps)
{
    struct BoxPokemon temp = *mon;
    u32 exp = GetBoxMonData(&temp, MON_DATA_EXP) + steps;
    SetBoxMonData(&temp, MON_DATA_EXP, &exp);
    ConvertIntToDecimalStringN(gStringVar3, GetLevelFromBoxMonExp(&temp), STR_CONV_MODE_LEFT_ALIGN, 3);
}

void JpDaycareLevelRoute5(void)
{
    BufferDaycareLevel(&gSaveBlock1Ptr->route5DayCareMon.mon, gSaveBlock1Ptr->route5DayCareMon.steps);
}

void JpDaycareLevelFourIsland(void)
{
    struct DaycareMon *dm = &gSaveBlock1Ptr->daycare.mons[gSpecialVar_0x8004 & 1];
    BufferDaycareLevel(&dm->mon, dm->steps);
}

// 殿堂入りのたびに、捕まえていない伝説のポケモン (フリーザー・サンダー・ファイヤー・ミュウツー) が元の場所に戻る
static const u16 sLegends[][3] =
{
    {SPECIES_ARTICUNO, 0x082, 0x2BE},
    {SPECIES_ZAPDOS,   0x05D, 0x2BF},
    {SPECIES_MOLTRES,  0x052, 0x2BD},
    {SPECIES_MEWTWO,   0x081, 0x2BC},
};

void JpRespawnLegends(void)
{
    u8 i;
    for (i = 0; i < ARRAY_COUNT(sLegends); i++)
    {
        if (!GetSetPokedexFlag(SpeciesToNationalPokedexNum(sLegends[i][0]), FLAG_GET_CAUGHT))
        {
            FlagClear(sLegends[i][1]);
            FlagClear(sLegends[i][2]);
        }
    }
}
