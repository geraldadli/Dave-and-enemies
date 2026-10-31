# Dave's & Enemies Chapter I narrative handoff

The 54-second opening moves from the Holy City's ruined fortifications to Dave's vow and his departure east. The desert chapter keeps its story brief: the Pharaoh blocks the dungeon route, Dave defeats him, and the chapter ends at the threshold. The original Holy Grail remains in enemy hands.

Claude owns cutscene execution, dialogue rendering, triggers, save handling and project integration. This handoff supplies final content and the state each presentation must leave behind.

## Sources and continuity

Use the original user brief from the chat titled "Create Dave’s action game prompt" (chat ID `01a19086-ad27-7ba2-b483-5f550e9c8e07`), this narrative assignment, [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md) sections 8-11 and the existing milestone E/F requests in [ASSET_REQUESTS.md](ASSET_REQUESTS.md).

Dave is the sole survivor of the siege. His fallen comrades lie motionless among stone rubble. He stands before the breached Holy City fortifications with windblown sand, long golden-brown hair, shining but battle-worn armor and a red cape. The enemy took the original Holy Grail. His vow has two parts: return it to the Holy Sanctuary and reunite the city's people. Do not show another living survivor, explain the absent people's history, identify the Pharaoh as the Grail's thief, or imply that the Pharaoh possesses it. His ankh is a separate boss reward. No additional major character appears.

## Files and dialogue format

- `datafiles/data/dialogue.json`: exact contract shape, an object keyed by scene ID, each containing `lines` of `speaker`, `text` and `mood`.
- `datafiles/data/narrative_manifest.json`: stable line IDs, speaker names, portrait IDs, expressions, exact text copies, blip profiles, event bindings, later storyboards and completion requirements.
- `datafiles/data/intro_storyboard.json`: the 60 fps opening shot list, camera coordinates, animation directions, text windows and audio cues.
- `docs/NARRATIVE_ASSET_REQUESTS.md`: art and sound requests for this script.

Each manifest line binds to canonical dialogue through `scene_id` plus zero-based `line_index`. Reference and persist the stable `id`, not its array position. An expression is the same value as the contract's `mood`; the sidecar calls it `expression` for art handoff. Portrait IDs identify the base portrait family. Optional expression artwork resolves through `portrait_expression_assets` and falls back to the base portrait. Narrator and UI messages have a null portrait. UI messages use the allowed `narrator` speaker for schema compatibility, with no visible speaker label and the `silent` blip profile.

Added metadata and semantic completion-event names describe Claude's integration requirements; they are not claims about existing engine functions. Room anchors resolve to the authored room graph. No engine files, room resources or Included Files registration are changed by this handoff. Claude should register the three data JSON files as Included Files and bind the sidecar fields in the systems they own.

## Final opening narration and dialogue

There are seven lines. They use nonverbal text blips, without spoken voiceover. Spoken-performance pacing is suggested by the text windows; the silent holds give the aftermath room to register.

| Stable line ID | Speaker | Portrait ID | Expression | Final text | Vocal blip profile |
|---|---|---|---|---|---|
| `intro_010` | Narrator | none | neutral | The Holy City had fallen. | `voice_narrator` |
| `intro_020` | Narrator | none | neutral | Dave alone had survived the siege. | `voice_narrator` |
| `intro_030` | Narrator | none | neutral | The enemy had taken the original Holy Grail. | `voice_narrator` |
| `intro_040` | Dave | `spr_portrait_dave` | solemn | I could not save you. | `voice_dave` |
| `intro_050` | Dave | `spr_portrait_dave` | determined | I will return the Holy Grail to the Holy Sanctuary. | `voice_dave` |
| `intro_060` | Dave | `spr_portrait_dave` | determined | I swear it. I will reunite our people and bring them home. | `voice_dave` |
| `intro_070` | Narrator | none | neutral | Beyond the broken walls, the desert waited. | `voice_narrator` |

## Opening storyboard

Default runtime is exactly 54 seconds, or 3,240 game frames at 60 fps, including fades. Authored timing excludes player pauses and manual-reading holds. All intervals below are seconds from sequence start. Text appears at 24 characters per second, remains through its window, and clears at the next shot.

The cinematic stage is 1920×1080. The wall is drawn at (0,0), size 1920×640, with a roughly 400-pixel breach between x=760 and x=1160. Dave starts at ground point (1040,790). Camera points are the centres of a 1280×720 view. Use the existing top-down three-quarter perspective, with native-scale camera pans; do not enlarge 96×96 character art for a close-up. Portraits carry fine facial acting. All wind, sand, hair, cape and banner movement travels from east to west.

Fade from black during 0-1 s. The last shot fades to black during 53-54 s. No Grail model, theft flashback, additional survivor or title card interrupts the opening.

| Shot and time | Camera action | Character pose | Environmental movement | Text and timing | Audio cues |
|---|---|---|---|---|---|
| `intro_shot_010`, 0-6 s | Pan centre (640, 500) to (760, 540); native scale, smooth ease. | Dave stands alone before the breached wall, sword lowered, head bowed; no other figure moves. | Thin sand ribbons drift right to left. A torn banner pulls west; dust slips from masonry. | `intro_010` at 1-5.5 s | 0 s: `snd_wind_loop`, fade in loop / 0 s: `mus_intro`, start non loop / 1.5 s: `snd_intro_banner`, play once optional |
| `intro_shot_020`, 6-13 s | Pan centre (760, 540) to (900, 620); native scale, smooth ease. | Pass three motionless fallen comrades in the foreground; Dave remains the only standing figure behind them. | A veil of sand passes over still cloaks and broken spears; no gore, twitching or ghost imagery. | `intro_020` at 6.5-12.5 s | 6 s: `mus_intro`, score direction; Low sustained strings; leave space around the narrator blips. |
| `intro_shot_030`, 13-20 s | Pan centre (900, 620) to (1040, 600); native scale, smooth ease. | Dave remains still beneath the gap in the fortification. Hold the empty breach as the theft is named. | Sand streams through the breach toward screen left; one loose pebble settles. | `intro_030` at 13.5-19.5 s | 13 s: `mus_intro`, score direction; Thin out the melody; the absence of the Grail is carried by the text, with no flashback. / 14 s: `snd_intro_grit`, play once optional |
| `intro_shot_040`, 20-27 s | Pan centre (1040, 600) to (1040, 650); native scale, smooth ease. | Dave bows his head toward his fallen comrades. His sword stays lowered; his free hand closes slowly. | Cape and golden-brown hair pull west; the bodies and their weapons remain still. | `intro_040` at 20.5-26.5 s | 20 s: `mus_intro`, score direction; A quiet, spare phrase; no sobbing or spoken voice. |
| `intro_shot_050`, 27-35 s | Pan centre (1040, 650) to (1040, 650); native scale, smooth ease. | Dave raises his head. His free hand rests against his breastplate; posture straightens without raising the sword. | Wind continues at the same direction and restrained density. | `intro_050` at 27.5-34.5 s | 27 s: `mus_intro`, score direction; Introduce the adventure motif softly beneath the vow. |
| `intro_shot_060`, 35-43 s | Pan centre (1040, 650) to (1100, 650); native scale, smooth ease. | Hold Dave's steady vow pose. His gaze shifts toward the eastern route at the line's end. | The torn banner strains west; drifting sand leaves the eastward path readable. | `intro_060` at 35.5-42.5 s | 35 s: `mus_intro`, score direction; Broaden the motif with restrained resolve; avoid a victory cadence. |
| `intro_shot_070`, 43-49 s | Pan centre (1100, 650) to (1220, 650); native scale, smooth ease. | Dave turns down to down_side to side over 0.5 s, then walks east from ground (1040,790) to (1232,790). | Cape trails left; dust lifts gently behind his feet. Fallen comrades stay behind. | `intro_070` at 43.5-48.5 s | 43 s: `mus_intro`, score direction; Begin a measured forward pulse. / 43.5 s: `snd_step_sand`, animation step events; Use actual walk contacts, not an extra independent footstep loop. |
| `intro_shot_080`, 49-54 s | Pan centre (1220, 650) to (1280, 650); native scale, smooth ease. | Track Dave continuing east to ground (1536,790); keep the broken city behind him. Cut before any gameplay movement. | Foreground sand crosses left; the path ahead remains open. | No text. | 49 s: `snd_step_sand`, animation step events / 52 s: `mus_intro`, fade out / 53 s: `snd_wind_loop`, transfer to exploration or fade |

## Objective and checkpoint messages

These are event-driven UI messages, never a conversation to play in sequence. Objective toasts are nonblocking and silent: desert 3.5 s after arrival is ready, boss 2.5 s after encounter initialization, dungeon 3.5 s after victory cleanup. The overall quest text is available to an existing pause-menu objective field if the UI provides one; do not add a permanent quest HUD.

A checkpoint is a safe yellow star. The save menu offers exactly three independent slots. Show the save-success message only after the chosen slot successfully commits a snapshot with restored health. An overwrite prompt uses the existing Confirm/Cancel controls. No cutscene silently writes over a save slot.

| Stable line ID | Speaker | Portrait ID | Expression | Final text | Vocal blip profile |
|---|---|---|---|---|---|
| `objective_quest_010` | Narrator | none | neutral | Return the Holy Grail to the Holy Sanctuary. Reunite the people of the Holy City. | `silent` |
| `objective_desert_010` | Narrator | none | neutral | Travel east through the desert. | `silent` |
| `objective_pharaoh_010` | Narrator | none | neutral | Defeat the Undead Pharaoh. | `silent` |
| `objective_dungeon_010` | Narrator | none | neutral | Enter the dungeon. | `silent` |
| `checkpoint_prompt_010` | Narrator | none | neutral | Interact with the star to save. | `silent` |
| `checkpoint_choose_010` | Narrator | none | neutral | Choose a save slot. | `silent` |
| `checkpoint_overwrite_010` | Narrator | none | neutral | Replace this slot with your current journey? | `silent` |
| `checkpoint_saved_010` | Narrator | none | neutral | Journey saved. Health restored. | `silent` |
| `checkpoint_failed_010` | Narrator | none | neutral | Could not save. Try again. | `silent` |
| `checkpoint_restored_010` | Narrator | none | neutral | Journey restored. | `silent` |

## Final pre-boss exchange

Keep these exact words, punctuation and order. Display names are Dave and The Undead Pharaoh. Both portraits occupy the same left-hand portrait area, facing right toward the text. No additional taunt or reply follows.

| Stable line ID | Speaker | Portrait ID | Expression | Final text | Vocal blip profile |
|---|---|---|---|---|---|
| `boss_intro_010` | Dave | `spr_portrait_dave` | neutral | Step aside. | `voice_dave` |
| `boss_intro_020` | The Undead Pharaoh | `spr_portrait_pharaoh` | menace | You shall not pass. This desert will be your grave. | `voice_pharaoh` |

Target reading pace is approximately eight seconds including the closing gate and combat handoff. Unlike the opening, both dialogue lines wait for acknowledgement; the four storyboard durations are minimum staging targets and stretch for reading. Start only when Dave is fully inside, the entry trigger is consumed for this attempt, and damage is paused. Keep Pharaoh's rod inactive while he speaks.

| Shot and time | Camera action | Character pose | Environmental movement | Text and timing | Audio cues |
|---|---|---|---|---|---|
| `boss_shot_010`, 0-1 s | Hold the arena gameplay camera with Dave inside the gate and the Pharaoh ahead. | Dave halts facing up. Pharaoh floats facing down, rod grounded visually; no attack pose. | Gate closes behind Dave; sand density decreases so portraits and the arena remain clear. | No text. | 0 s: `snd_gate_slam`, play once / 0 s: `mus_desert`, fade out |
| `boss_shot_020`, 1-3 s | Keep Dave and Pharaoh visible at native scale; no camera shake. | Dave squares his shoulders, sword held low, facing up; use his neutral portrait on the left. | Only cape movement and a faint dust drift continue. | `boss_intro_010` at 1-3 s | Carry the current ambience and score; blips follow any text. |
| `boss_shot_030`, 3-7 s | Hold the same camera. Change only the current speaker portrait. | Pharaoh tilts his headdress downward and inclines the rod without charging it; menace portrait on the left. | He floats gently; no lightning, summons or damage effects. | `boss_intro_020` at 3-7 s | Carry the current ambience and score; blips follow any text. |
| `boss_shot_040`, 7-8 s | Settle onto the normal arena camera. | Both return to combat-ready idle. Clear dialogue and reveal the boss name and health bar. | Gate stays closed. Keep all damage inactive through the handoff. | `ui_boss_name_010` at 7-8 s | 7 s: `mus_pharaoh`, start loop |

After the final line is acknowledged, finish the one-second handoff and initialize combat. The boss health bar and theme appear once. Keep Dave's current health and inventory. The first attack begins with its normal readable telegraph at least 0.75 s after control returns.

## Boss defeat and the dungeon route

There is no spoken victory line. The Pharaoh disintegrates, the screen fades slowly to white, and the cleared courtyard returns. Total staging is 7.5 seconds. Reduced-flash mode substitutes a slow dark dissolve; screen shake obeys its setting.

| Shot and time | Camera action | Character pose | Environmental movement | Text and timing | Audio cues |
|---|---|---|---|---|---|
| `defeat_shot_010`, 0-1.5 s | Hold arena camera; optional restrained shake obeys the user's setting. | Dave stops. Pharaoh begins the 16-frame disintegration at 12 fps, holding its last frame if necessary. | Disable all encounter damage immediately. Summons stop; hazards and projectiles cannot hurt Dave. | No text. | 0 s: `mus_pharaoh`, fade out / 0 s: `snd_boss_death`, play once / 0 s: `snd_disintegrate`, play once |
| `defeat_shot_020`, 1.5-3.5 s | Hold position while a smooth two-second fade reaches white. | Dave remains safe and still. Pharaoh dissolves completely. | One continuous fade, never repeated flashing. Reduced-flash mode uses a slow dark dissolve. | No text. | Carry the current ambience and score; blips follow any text. |
| `defeat_shot_030`, 3.5-4.5 s | Full white hold, or full dark hold under reduced flash. | Remove Pharaoh, summoned enemies, projectiles, telegraphs and hazards while obscured. | Stop encounter loops; open the entry gate and dungeon route; make the unique reward available once. | No text. | Carry the current ambience and score; blips follow any text. |
| `defeat_shot_040`, 4.5-6.5 s | Fade smoothly back to the unchanged arena camera over two seconds. | Dave stands in the cleared courtyard. Boss and summons are absent. | Exit is visibly open. Resume low wind; remove the boss health bar. | No text. | 4.5 s: `snd_wind_loop`, resume quietly |
| `defeat_shot_050`, 6.5-7.5 s | Return camera control to gameplay. | Dave resumes normal idle. Release control and show objective_dungeon only when this sequence completes. | The courtyard stays clear of encounter threats. | No text. | 6.5 s: `mus_desert`, fade in loop |

Display `objective_dungeon_010` for its full 3.5-second toast only after the sequence finishes or is skipped. Keep the Grail quest unresolved. Defeating the boss opens the route; Dave must walk to the dungeon threshold himself.

## Final transition to To Be Continued

The final sequence starts when Dave crosses the dungeon doorway in `rm_d18_dungeon_threshold` after victory. It lasts ten seconds through the musical tail, then the title waits indefinitely for a fresh menu input. The title appears at six seconds; the menu button becomes available when the sequence completes. A skip goes straight to that same held title with its button available.

| Stable line ID | Speaker | Portrait ID | Expression | Final text | Vocal blip profile |
|---|---|---|---|---|---|
| `ending_010` | Dave | `spr_portrait_dave` | determined | My vow still stands. | `voice_dave` |
| `ui_ending_title_010` | Narrator | none | neutral | To Be Continued | `silent` |
| `ui_return_menu_010` | Narrator | none | neutral | Return to Main Menu | `silent` |

| Shot and time | Camera action | Character pose | Environmental movement | Text and timing | Audio cues |
|---|---|---|---|---|---|
| `ending_shot_010`, 0-2 s | Track Dave's last two steps toward the dark doorway; never reveal a playable interior. | Dave faces up into the entrance, red cape trailing. Halt him just beyond the threshold. | Sand passes left outside; the interior remains still and dark. | No text. | 0 s: `mus_desert`, fade out / 0 s: `mus_ending`, start non loop / 0 s: `snd_wind_loop`, fade out |
| `ending_shot_020`, 2-5 s | Hold the doorway composition. | Dave stands upright in silhouette; his determined portrait appears for the final brief line. | Let the last sand drift fade at the entrance. | `ending_010` at 2-5 s | Carry the current ambience and score; blips follow any text. |
| `ending_shot_030`, 5-6 s | Fade evenly to black over one second. | Dave disappears only beneath the fade. | Do not show the Grail, a new enemy or an interior location. | No text. | Carry the current ambience and score; blips follow any text. |
| `ending_shot_040`, 6-10 s | Static rm_ending presentation; title centred on the black or restrained entrance background. | No characters appear. Show the title; enable Return to Main Menu at sequence completion, after the music tail. | Hold still; no flashing effects. | `ui_ending_title_010` at 6-10 s | 6 s: `mus_ending`, score direction; Leave the motif unresolved; tail ends at 10 s, then remain quiet. |

Do not reveal a playable interior, recover the Grail, reunite the people, or suggest that the quest has ended. The music closes this chapter with forward intent and unresolved harmony.

## Remaining interface text

These labels belong to the existing dialogue controls and boss health bar. Bind action glyphs through the input system; no keyboard name is baked into the script.

| Stable line ID | Speaker | Portrait ID | Expression | Final text | Vocal blip profile |
|---|---|---|---|---|---|
| `ui_reveal_010` | Narrator | none | neutral | Reveal | `silent` |
| `ui_advance_010` | Narrator | none | neutral | Advance | `silent` |
| `ui_skip_010` | Narrator | none | neutral | Hold to skip | `silent` |
| `ui_boss_name_010` | Narrator | none | neutral | The Undead Pharaoh | `silent` |

## Advance and skip behavior

Use abstract actions `cutscene_advance` and `cutscene_skip`, mapped through Claude's input system. Suggested defaults are Enter/Space and a 0.6-second hold of Escape, with controller equivalents. During a cutscene Escape belongs to that context; it must not also pause gameplay. Show the current Reveal or Advance label and Hold to skip with the resolved action glyphs.

An advance press during typewriter reveal displays the rest of that line immediately and stops its blips. It does not also advance the shot. A second fresh press advances after the text is complete. The opening and ending normally move on at their scheduled times; advancing completed text jumps to the next shot and shortens the presentation. In a textless shot, advance moves to the next shot. Optional manual-reading mode holds text shots after their minimum windows. The two pre-boss lines always wait for acknowledgement.

Track timing locally to each shot after a jump. Never execute abandoned shot callbacks. Non-loop music may seek to the new shot time if supported; otherwise fade it smoothly and continue, without replaying gates, footsteps or impacts from skipped time. An advance is distinct from skipping a whole sequence.

Holding skip for 0.6 s calls that sequence's completion event. It works during fades and textless shots. It cancels blips, footsteps, pending text events, camera interpolation, particle spawns and scheduled cinematic callbacks. It must not fast-forward pending events by executing them in a burst.

Every normal finish, final advance, seen-scene suppression and skip funnels through one idempotent completion routine for that scene instance. A scene-instance token prevents stale or duplicate callbacks from completing again. Release world control only after the required room, gate and camera state exists. Consume advance/skip input until release before allowing attacks, interaction, pause or menu activation. The same held key must never skip and activate the ending's menu button.

## Required state after completion or skip

The manifest contains the same requirements as structured lists. Map proposed flag names to existing equivalents in Claude's serializer. Apply state only for the permitted scene context.

### intro complete

Allowed context: intro.

- Set intro_seen = true in the current run.
- Enter rm_d01_arrival at its authored safe player start, facing east (direction index 0).
- Keep starter loadout and health established by New Game; do not grant or reset either here.
- Set the active local objective to objective_desert; retain objective_quest as the overall quest.
- Keep boss_pharaoh_defeated = false and grail_recovered = false for this new run.
- Clear cinematic overlays, input locks and pending shot callbacks; restore gameplay camera, health HUD, hotbar, normal damage rules and exploration audio only after the destination room is ready.
- Show the same objective_desert toast after normal playback or skip. Establish a safe initial restart snapshot if no checkpoint has been saved.

Do not:

- Overwrite a save slot.
- Spawn Dave inside the cinematic backdrop or teleport him east of the authored arrival.
- Replay New Game inventory grants.

### boss intro complete

Allowed context: boss_intro.

- Keep Dave fully inside the boss arena at the authored entry staging point; preserve current HP, equipment and inventory.
- Ensure the entrance gate is closed, collidable and exits are locked before releasing control.
- Ensure exactly one Pharaoh exists and is initialized for this attempt, with full HP only if this is a fresh encounter.
- Set boss_intro_seen = true and consume the attempt-local entry trigger; boss_pharaoh_defeated stays false.
- Clear dialogue, restore the arena camera and health/hotbar, show ui_boss_name and boss HP, start mus_pharaoh once, and set objective_pharaoh.
- Enable the combat controller only after all entry conditions hold. Schedule the first telegraphed attack no earlier than 0.75 s after control returns.
- Consume held advance/skip inputs until release before attack, interact or pause can trigger.

Do not:

- Advance to a defeated boss state.
- Reset an already active boss's HP or duplicate the boss, gates, music or summons.

### boss defeat complete

Allowed context: boss_defeat_after_zero_hp.

- Stop all attack scheduling and damage immediately.
- Set boss_pharaoh_defeated = true; remove the Pharaoh, encounter summons, projectiles, warnings and hazards; stop their looping audio.
- Open the arena entrance and the route to the dungeon; remove the boss health bar.
- Call engineering's idempotent boss reward routine once for pharaoh_ankh, using the authored boss reward's persistent ID. If inventory is full, keep the unique reward available under the existing loot rules; do not silently claim or discard it.
- Set objective_dungeon. Keep grail_recovered = false and chapter_1_complete = false.
- Clear fades and input locks, restore gameplay camera/HUD/audio, consume held inputs and release Dave in the cleared arena.

Do not:

- Allow skipping before a legitimate zero-HP event.
- Count the Pharaoh's ankh as the Holy Grail.
- Enter the dungeon or complete the chapter on the player's behalf.
- Write over a player-selected save slot.

### ending complete

Allowed context: ending_after_threshold_and_victory.

- Retain boss_pharaoh_defeated = true and grail_recovered = false.
- Set chapter_1_complete = true and ending_seen = true in current run state; preserve inventory and reward status.
- Enter rm_ending, remove world control/HUD/damage and all remaining scene callbacks; show ui_ending_title and ui_return_menu.
- Stop wind, footsteps and dialogue blips; fade any abandoned music to the ending tail or silence.
- Keep the title visible until a fresh explicit menu input. Consume the input that skipped the scene so it cannot also activate Return to Main Menu.

Do not:

- Set grail_recovered = true or reunite the city on screen.
- Start a dungeon level.
- Automatically leave the title, grant an item or overwrite any save slot.

A skipped opening creates the same safe first-death restart state as a normally finished opening. A boss retry restores the chosen checkpoint snapshot, including inventory and reward claims. The two-line exchange may replay on a fresh attempt; a consumed entry trigger must not retrigger while an attempt is running. Loading a saved completed-boss state keeps the boss absent and routes open.

These completions affect the current run. Any subsequent player-initiated save includes the resulting flags. Returning to an older pre-boss snapshot legitimately restores an undefeated encounter; skip must never rewrite that snapshot or grant rewards retroactively.

## Readability and vocal direction

Use the contract's 1280×720 GUI, 28 px dialogue, 23 px UI and 46 px titles. Base portraits are 512×512, drawn at 208×208 on the left. Narration has no portrait. Word-wrap at word boundaries, with a maximum of two dialogue rows; every entry is below the 140-character cap. Use one OFL family and the contract's supported glyph set.

Use four 50-110 ms nonverbal variants per speaking profile. Dave is warm and firm; narrator is soft and subdued; Pharaoh is low, dry and resonant. Do not synthesize spoken words or recognizable samples from another game. Trigger about every second letter or digit, no punctuation/space blips, with pitch 0.94-1.06, at least 75 ms between onsets and one blip voice at a time. Pause 120 ms for commas and 240 ms for sentence punctuation. Reveal, advance and skip stop all pending and playing blips.

All UI and objective messages are silent. Save and checkpoint interface sounds use the existing UI/SFX system. Keep wind below the blips and reduce sand density during the boss exchange. All music/ambience changes must respect separate music, SFX and dialogue-blip volume settings.

## Content acceptance

Check the seven opening lines against their eight timed shots and verify a 54-second unpaused playback. Verify the exact two-line Pharaoh exchange, speaker switching, two-row wrapping and glyph coverage in the IDE. Exercise reveal, advance and skip from every shot, especially the intro's last fade, the gate close, the boss whiteout and the ending title. Compare the resulting state with normal playback, including a full inventory at the unique reward and loading pre-boss versus completed-boss snapshots.

The delivered data is content, not a runtime implementation. Compilation, layout rendering, playback, save behavior, asset availability and listening checks remain Claude's integration work in GameMaker.

