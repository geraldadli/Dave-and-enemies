// scr_config - shared constants for Dave's & Enemies, Chapter I.
// Values marked "contract" come from docs/PROJECT_CONTRACT.md; UI values from docs/ui/UI_SPEC.md.

#macro TPS 60                 // game ticks per second (contract: 60 fps)
#macro TILE 64                // contract: 64 px tiles
#macro GUI_W 1280             // UI_SPEC logical GUI plane
#macro GUI_H 720
#macro SAVE_VERSION 2         // 1 = legacy room-chain draft, 2 = desert_scenes_v2
#macro SAVE_SLOTS 3
#macro INV_SIZE 40            // 8 main slots + 32 storage slots
#macro HOTBAR 8
#macro DAVE_SPEED 4           // px per tick (template move_speed)
#macro DAVE_IFRAMES 60
#macro MAX_LEVEL 10

// UI_SPEC section 2 tokens ($BBGGRR)
#macro C_INK $271B17
#macro C_RAISED $392A24
#macro C_WELL $211510
#macro C_EDGE $957F74
#macro C_GOLD $77C4EA
#macro C_TEXT $DDEBF6
#macro C_MUTED $D3C3B9
#macro C_DISABLED $AF9D92
#macro C_HEALTH $5C4FC1
#macro C_BOSS $C163A6
#macro C_XP $C9B86F
#macro C_ERROR $9FACFF
#macro C_SUCCESS $A0D6A5

// base presentation modes; overlays stack above them
enum MODE { TITLE, CINEMA, PLAY, GAMEOVER, ENDING }
enum OV { INVENTORY, DIALOGUE, PAUSE, SETTINGS, SAVELOAD, CONFIRM }

// terrain collision classes in the scene grid
enum CELL { WALK = 0, LOW = 1, SOLID = 2 }   // LOW blocks walking only (water, chasm, broken span)
