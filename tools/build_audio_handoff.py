"""Build the audio designer's documentation. Does not generate or import audio."""
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "audio"
ASSETS = []


def add(asset_id, purpose, direction, duration, variants, trigger, *,
        group="Combat", gain=-6, per=1, total=3, cooldown=90, priority=50,
        loop=False, fade_in=0, fade_out=40, stop=None, music=None, milestone="B"):
    is_music = asset_id.startswith("mus_")
    export = {
        "container": "WAV", "codec": "PCM signed 16-bit little-endian",
        "sample_rate_hz": 44100, "channels": 2 if is_music else 1,
        "peak_ceiling_dbfs": -1,
        "integrated_lufs": -16 if is_music else None,
        "loudness_tolerance_lu": 1 if is_music else None,
        "trim": "No leading dead air; preserve designed decay and 2-5 ms click-free edge envelopes."
    }
    if loop:
        export["trim"] = "Exact whole-file cyclic edit; no head/tail fades or padded silence baked into the loop. Wrap reverb/noise decay across seam."
    if stop is None and (asset_id.endswith("_death") or asset_id == "snd_bat_defeat"):
        stop = "Let the natural death tail finish through the defeated entity's destruction, using scene-level ownership. On room unload, load, silent whiteout cleanup or encounter reset, fade out over 40 ms and discard queued plays. Never start this sound for silent despawn."
    stop = stop or ("Let natural tail finish. On room unload, owner destruction, death-state cleanup or encounter reset, fade out over 40 ms and discard queued plays.")
    names = [f"{asset_id}.wav"] if variants == 1 else [f"{asset_id}_{n}.wav" for n in range(1, variants + 1)]
    loop_info = {"enabled": loop, "method": "whole_file" if loop else "none",
                 "loop_start": 0.0 if loop else None,
                 "loop_end": duration if loop else None,
                 "frames_at_44100": round(duration * 44100) if loop else None}
    prompt = (
        f"Produce original audio for Dave's & Enemies, a smooth cartoon desert action adventure. Asset {asset_id}: {purpose}. "
        f"{direction} Deliver {variants} {'distinct take' if variants == 1 else 'separate distinct takes'}, each {duration:g} seconds long including decay. "
        + ("Keep variants matched in perceived loudness and function; vary performance and texture rather than large pitch changes. " if variants > 1 else "")
        + ("Make the entire file a seamless repeat with constant ambience or musical continuity at the join; no audible restart, baked fade, extra reverb tail or added silence. " if loop else ("This is a complete non-looping score cue; keep its natural ending within the file and do not append another cue or silent padding. " if is_music else "This is a single event, not a loop; do not add a second event or a montage. "))
        + ("No vocals, speech, lyrics, quoted melodies, stock tracks, combat effects or weather baked into the music. " if is_music else "No intelligible words, dialogue sentences, music, background ambience or unrelated actions. ")
        + "Use original recordings or synthesis; do not sample reference games, copy recognizable character voices, or imitate a named performer. "
        + f"Export WAV, signed PCM 16-bit, 44.1 kHz, {'stereo' if is_music else 'mono'}, peak no higher than -1 dBFS. "
        + ("Master to -16 LUFS integrated, tolerance +/-1 LU; retain transient headroom. " if is_music else "Judge short sounds by peak and perceived loudness; do not force an integrated LUFS target. ")
        + export["trim"]
    )
    ASSETS.append({
        "id": asset_id, "purpose": purpose, "group": group,
        "milestone": milestone, "status": "PENDING_AUDIO", "generated": False,
        "generation_or_recording_prompt": prompt,
        "duration_seconds_per_file": duration, "variation_count": variants,
        "planned_filenames": names, "existing_delivered_files": [],
        "loop": loop_info, "trigger": trigger, "stop": stop,
        "fade_in_ms": fade_in, "fade_out_ms_on_stop": fade_out,
        "relative_gain_db": gain, "bus": "music" if is_music else ("dialogue" if group == "Text" else "sfx"),
        "simultaneous_limit_per_emitter": per, "simultaneous_limit_global_for_id": total,
        "minimum_retrigger_ms": cooldown, "priority_0_to_100": priority,
        "export": export, "composition": music,
        "delivery_status_note": "A written prompt and planned filename only; no new audio file has been produced."
    })


def music(asset_id, purpose, direction, duration, trigger, stop, *, loop=False, fade_in=500, fade_out=800, gain=-5, spec=None, milestone="E"):
    add(asset_id, purpose, direction, duration, 1, trigger, group="Music", gain=gain,
        per=1, total=1, cooldown=0, priority=85, loop=loop, fade_in=fade_in,
        fade_out=fade_out, stop=stop, music=spec, milestone=milestone)


DESERT_MOTIF = (
    "Four-bar original lead, C4 = middle C, 4/4; q = quarter, e = eighth: "
    "bar 1 C4(q), Db4(e), E4(e), G4(q), F4(q); "
    "bar 2 E4(q), Db4(e), C4(e), B3(q), C4(q); "
    "bar 3 G4(q), Ab4(e), B4(e), C5(q), G4(q); "
    "bar 4 F4(q), E4(q), Db4(q), C4(q)."
)
PHARAOH_MOTIF = (
    "Two-bar original signature, 4/4; dq = dotted quarter, q = quarter, e = eighth: "
    "bar 1 C3(dq), Db3(e), G3(q), E3(q); "
    "bar 2 B2(e), C3(e), Ab3(q), G3(q), rest(q). "
    "Keep its long-short opening, upward tritone leap from Db3 to G3 (six semitones), and final quarter rest recognizable; "
    "the rest is part of the hook."
)

music("mus_desert", "Desert exploration theme",
    "Compose 32 bars in 4/4 at 80 BPM, exactly 96 seconds, C tonal centre, equal temperament A4=440 Hz. "
    "Use only C, Db, E, F, G, Ab, B in all pitched parts. Give E natural a clear place above C so the major third remains audible. "
    + DESERT_MOTIF + " State it with a breathy flute-like lead, answered by restrained rounded plucked strings. "
    "Use C-G drones, open fifths, occasional C-E-G, F-Ab-C and Db-F-Ab voicings; G-B dyads can lead home without introducing D natural. "
    "Sparse frame-drum bass taps, fingertip hand-drum tones and soft shakers form a walking pulse; no heavy cinematic drums. "
    "Bars 1-8 introduce a sparse motif and an answering phrase; 9-16 shift answers to plucked strings; 17-24 give the flute a higher quiet answer; "
    "25-32 return to the opening texture and reduce activity in the last two bars. Leave rests for exploration feedback. "
    "Let B and Db resolve toward C with restraint. Loop bar 32 into bar 1 with no final cadence, cymbal ending or swell. "
    "Warm, curious and lonely with quiet resolve, never comic or triumphal; keep the middle register open for combat warnings.",
    96, "Enter exploration after intro or resume a desert music zone; preserve playback position across connected desert rooms.",
    "Crossfade out over 1200 ms for boss dialogue or chapter ending; on player death fade out over 250 ms; on main-menu exit 800 ms. Do not restart on each room transition.",
    loop=True, fade_in=1200, fade_out=1200, gain=-7,
    spec={"bpm": 80, "meter": "4/4", "bars": 32, "tonic": "C", "pitch_collection": ["C", "Db", "E", "F", "G", "Ab", "B"], "motif": DESERT_MOTIF})

music("mus_pharaoh", "The Pharaoh boss battle theme",
    "Compose 48 bars in 4/4 at 128 BPM, exactly 90 seconds. Stay in C with pitches C, Db, E, F, G, Ab, B, A4=440 Hz. "
    + PHARAOH_MOTIF + " State this low hook on a dark bowed-string and breath-reed unison, with a short plucked double; repeat in octave answers. "
    "Use insistent low frame drum, sharp hand percussion, restrained metal scrapes and a C-G bass ostinato, with 3+3+2 eighth-note accents against 4/4. "
    "It must have greater rhythmic density and urgency than the exploration cue while retaining separation for warning sounds. "
    "Bars 1-16 establish hook and response; 17-32 add an original upper plucked countermelody; 33-48 intensify the hook in octaves with tighter percussion. "
    "Thin the final bar just enough to reconnect to bar 1 without an ending. No quiet introduction, long riser, choir, final victory cadence or copied score. "
    "Create intensity through arrangement, not excessive limiting or loudness. This is one full stereo mix, not adaptive stems.",
    90, "After the final pre-boss line is dismissed, on the same encounter event that enables combat and shows the boss bar; enter on beat 1.",
    "At confirmed Pharaoh death fade out over 250 ms; at Dave death 250 ms; at encounter abort, load or reset 100 ms. Never continue beneath a restarted attempt.",
    loop=True, fade_in=80, fade_out=250, gain=-4, milestone="F",
    spec={"bpm": 128, "meter": "4/4", "bars": 48, "tonic": "C", "pitch_collection": ["C", "Db", "E", "F", "G", "Ab", "B"], "motif": PHARAOH_MOTIF})

music("mus_intro", "Opening siege aftermath and Dave's vow",
    "Compose a 54-second non-looping atmosphere score, following the narrative storyboard. At 0-13 s use a quiet C-G bowed drone and a few widely separated muted string plucks for the breached city wall and fallen comrades. "
    "At 13-20 s thin the melody under the stolen-Grail text; at 20-27 s give a spare breath-flute lament using C, Db, E, F, G, Ab, B, without a march. At 27-35 s introduce "
    "C4, Db4, E4, G4 from the exploration motif softly beneath Dave's vow. At 35-43 s let E above C and a gentle hand-drum heartbeat broaden his resolve. "
    "At 43-52 s give the eastward walk a measured forward pulse. At 52-54 s fade an open C-G sustain completely inside the file. "
    "Respect fallen comrades without horror gore, battle action or a triumphant recovery of the Grail. Leave space under text. "
    "Do not bake in wind, masonry, cloth or text blips; they are separate cues. Preserve space beneath the storyboard's text windows.",
    54, "Start the 54-second opening storyboard once at t=0 when the ruined city is first shown.",
    "Natural end; on skip fade score and intro ambience over 300 ms before entering exploration. If storyboard timing changes, re-edit this cue; do not stretch indefinitely.",
    fade_in=800, fade_out=300, gain=-9)

music("mus_boss_defeat", "Pharaoh defeat and whiteout musical cue",
    "Compose a 6-second non-looping release from the Pharaoh battle: muted low C-G strike, a fragment C3-Db3-G3-E3 dissolving into a soft C-E-G voicing, "
    "then an airy open fifth. Let impact energy fall rather than build, leaving the final two seconds as fading resonance. "
    "This signals survival and the arena clearing, not the Holy Grail recovered. Leave 150-800 Hz space for the separate death blast and disintegration. "
    "Do not embed an explosion, enemy voices or wind.",
    6, "250 ms after confirmed Pharaoh defeat, following the boss music fade, during the slow whiteout sequence.",
    "Play once and let tail finish. On load, skip or scene abort fade out over 200 ms; do not replay from saved boss-defeated state.",
    fade_in=50, fade_out=200, gain=-6, milestone="F")

music("mus_ending", "Dungeon threshold and To Be Continued",
    "Compose a 10-second non-looping cue following the ending storyboard, with no forced bar count. At 0-2 s revoice the exploration motif's C-Db-E-G opening on warm plucked strings and breathy flute. "
    "At 2-5 s thin to a soft C-G support under Dave's final text. At 6 s support the To Be Continued title with a restrained F-E-Db-C answer, then a long open C-G ending. "
    "Use a single soft frame-drum beat at the start, then no driving rhythm. "
    "Suggest a promise continuing beyond the dungeon door, with quiet relief and remaining mystery. Do not sound like the quest or Grail recovery is complete. "
    "Allow the final resonance to decay from 8-10 s; no separate tail outside the export. The title holds in silence after 10 s.",
    10, "At t=0 enter the ending sequence from the cleared dungeon threshold; play once per entry. Title appears at t=6 s.",
    "Natural end into silence; fade out over 300 ms if returning to main menu or loading a save.",
    fade_in=200, fade_out=300, gain=-7, milestone="F")

music("mus_gameover", "Player death screen musical sting",
    "Compose a 4.5-second restrained failure sting: three descending soft plucked tones G4-E4-Db4 over low C, then a short breathy C-G decay. "
    "Use no grand orchestral hit, mocking gesture, spoken voice or loop. Leave the first 100 ms sparse for Dave's death sound. "
    "Sound regretful but allow a hopeful retry.",
    4.5, "On Game Over state entry, about 250 ms after Dave's death cue, once for that death.",
    "Natural end; on retry/load/menu selection fade out over 150 ms before any new scene score.",
    fade_in=50, fade_out=150, gain=-8)

add("snd_wind_loop", "Sandstorm wind bed", "Synthesize or record a dry broad wind gust moving through fine sand. Use slow 2-4 second gust contours and a light granular hiss, "
    "with no whistling melody, animal cries, thunder or harsh high-frequency spikes. Keep it mono so Claude can position or modulate it; suggest the east-to-west weather through gradual intensity, not baked stereo motion.",
    12, 1, "Weather intensity rises above zero; one persistent bed for the active weather zone, including quiet reuse for opening aftermath.",
    group="Atmosphere", gain=-18, per=1, total=1, cooldown=0, priority=20, loop=True, fade_in=2500, fade_out=3000,
    stop="Fade out over 3000 ms as storm ends; dialogue and boss entry fade to inaudible over 600 ms. Opening overrides fade-in to 1500 ms and transfers or fades at t=53 s; ending fades out over 2000 ms. Room changes preserve the bed only if the weather zone continues; stop on load/reset.", milestone="C")
add("snd_intro_grit", "Opening aftermath loose stone", "Record small limestone fragments settling: one short grit slide, two tiny irregular stone ticks and a soft sandy tail. No collapse, explosion, human distress or movement implying a surviving comrade.",
    .45, 1, "Optional opening storyboard pebble cue at t=14 s; once, not a random gameplay loop.", group="Atmosphere", gain=-16, total=1, cooldown=1500, priority=15, milestone="E")
add("snd_intro_banner", "Torn banner in opening wind", "Record a restrained single billow of heavy woven banner cloth: soft fabric flex, gentle snap and warm rustle. No whip crack, footsteps or metallic armour.",
    .6, 2, "Optional opening banner billow at t=1.5 s; once, not every animation frame.", group="Atmosphere", gain=-18, total=1, cooldown=1400, priority=15, milestone="E")

add("snd_sword_swing", "Dave sword swing through air", "Record or synthesize a compact steel blade air-cut with a small leather grip creak, a rounded fast whoosh and clean falling air tail. Keep it light enough for repeated attacks, without contact, magical sparkle or enemy voice.",
    .28, 3, "Once when Dave's attack first enters active sprite frame 2, nominally 0.10 s into the contracted 0.45 s attack; cancelled windups stay silent.", gain=-6, total=2, cooldown=100, milestone="A")
add("snd_sword_hit", "Successful damage from Dave's sword", "Create a readable cartoon sword impact: crisp dry metal tick, short woody body thump and a tight gritty edge. No wet gore, long ring, whoosh or vocal. It must read in 50 ms and remain pleasant under repetition.",
    .22, 3, "Confirmed sword damage once per swing-target pair, not overlap frames; cap clustered hit feedback at two new starts per 80 ms.", gain=0, total=3, cooldown=40, priority=75, milestone="A")
add("snd_sword_hit_bone", "Optional material accent on skeletal targets", "Record brittle small bone-like ceramic and wooden clicks, a dry chip snap and brief hollow rattle; no glass sparkle or gore. Make this a subtle overlay rather than a second full impact.",
    .18, 3, "Optional overlay on snd_sword_hit against undead or skeletons; use at most one material accent per confirmed hit.", gain=-10, total=2, cooldown=80)
add("snd_sword_hit_armor", "Optional armour or rod impact accent", "Record a short damped steel-on-bronze clink with a tiny lower body resonance. Remove long bell ringing and abrasive top end. No sword swing or voice.",
    .25, 3, "Optional overlay on confirmed hit against armoured bandit or Pharaoh; choose this or bone accent, never both.", gain=-10, total=2, cooldown=80)
add("snd_hurt", "Dave takes nonfatal damage", "Record an original warm firm human nonverbal exhalation with a compact leather-and-armour body thump. A brief strained closed-mouth grunt, no words, screams, gore or exaggerated comic pitch. Keep it distinct from dialogue murmurs.",
    .35, 3, "Accepted nonfatal HP loss after invulnerability checks; do not trigger on blocked or zero damage.", gain=-2, total=1, cooldown=220, priority=90, milestone="A")
add("snd_player_defeated", "Dave's death", "Record an original weary human breath dropping into a quiet armour settling clink on sand. Nonverbal and dignified, no full phrase, prolonged scream or melodramatic fall. A strong onset must remain clear without a loud crash.",
    1.2, 1, "HP crosses to zero; replace snd_hurt for this damage event, once per death.", gain=-2, total=1, cooldown=1500, priority=95,
    stop="Allow death tail even after Dave is destroyed; stop with 100 ms fade on retry/load/menu. Clear it on encounter reset.")
add("snd_potion_drink", "Dave uses health potion", "Record a small cork pop, one compact liquid gulp and bottle movement as one tight nonverbal action. No glass smash, cheerful voice or healing chime.",
    .55, 2, "Potion use is accepted and one item is consumed; do not play on full HP, empty slot or cancelled use.", gain=-7, total=1, cooldown=500, milestone="A")
add("snd_heal", "Actual HP restoration and red aura", "Synthesize warm rounded C5-E5-G5 droplets rising softly into a brief airy shimmer, intimate and restorative. No electric zap, bell alarm or holy choir; colour is warm rather than icy. Keep all decay within the file.",
    .85, 2, "HP actually increases and the red healing aura starts; may layer quietly with potion drink. Checkpoint heal may reuse it only if HP was missing.", gain=-8, total=1, cooldown=600, priority=65, milestone="A")
add("snd_step_sand", "Dave foot contact on sand", "Record a firm boot compressing dry sand with a short gritty crunch and cloth-soft release; four different natural footsteps, no repeated rhythm, armour jangle or wind.",
    .18, 4, "Walk foot-contact broadcasts at frames 2 and 7 while Dave is moving on sand; one take per contact, not per animation update.", gain=-17, total=2, cooldown=80, priority=25, milestone="A")
add("snd_step_stone", "Dave foot contact on ruins", "Record a boot on worn dry sandstone, a rounded sole tap with a little grit and no cavern reverb, echo, other footstep or armour jangle.",
    .16, 4, "Dave foot-contact event on paved or stone surfaces; replaces sand step for that contact.", gain=-18, total=2, cooldown=80, priority=25, milestone="C")
add("snd_step_wood", "Dave foot contact on a bridge", "Record one compact boot tap on a thick old wooden bridge plank with a soft dry creak. Avoid snapping timber or a hollow comedic bong.",
    .2, 4, "Dave foot-contact event on bridge surface; replaces other surface steps.", gain=-18, total=2, cooldown=80, priority=25, milestone="C")

# Enemy actions below describe existing attacks only. Ranged/melee absences are explicit in the plan.
add("snd_undead_attack", "Undead melee windup", "Create a slow dry joint creak with cloth strain and a low closed-mouth breath scrape. Build to a short sandy hand sweep; no impact or words. The first 80 ms should identify a nearby attack.",
    .55, 3, "Undead melee windup entry (frames 0-3); once per attack; damage contact uses snd_enemy_melee_hit.", gain=-6, total=3, cooldown=400, priority=65, milestone="A")
add("snd_undead_move", "Undead dragging walk", "Record a short dragging sandal scrape through sand with one loose dry joint tick, heavy and fatigued. One locomotion contact only; no moan or rhythmic sequence.",
    .3, 3, "Undead actual ground-contact event while locomoting; replaces generic enemy footstep.", gain=-20, total=3, cooldown=220, priority=20, milestone="A")
add("snd_undead_death", "Undead collapses", "Create a dry cloth slump, soft hollow wooden-bone clatter and sand settling. No wet impact, demonic scream, magical explosion or voice.",
    .8, 3, "Undead HP crosses zero; once per defeat, including summons killed normally. Whiteout cleanup must stay silent.", gain=-7, total=3, cooldown=130, milestone="A")
add("snd_undead_rise", "Undead emergence from sand", "Record a compact granular soil split, cloth pulling upward and a small hollow joint creak; rise from low sand friction into dry surface scatter, no explosion. Make the sand break readable immediately.",
    1, 3, "Undead rise animation begins from a summon crack; one cue per emerging unit, clustered starts capped to two per 120 ms.", gain=-7, total=3, cooldown=120, priority=70, milestone="F")

add("snd_skeleton_warrior_attack", "Skeleton warrior melee preparation", "Create a sharp hollow bone joint click followed by a thin steel weapon swish. Weapon may be sword or spear, so keep the gesture neutral. No contact, human grunt or long metal ring.",
    .38, 3, "Skeleton warrior attack windup begins (frames 0-2); no replay on active frames 3-4.", gain=-6, total=3, cooldown=250, priority=65)
add("snd_skeleton_warrior_move", "Skeleton warrior foot contact", "Record a bony foot pad scraping sandstone grit with two tiny dry joint clicks. One light step, slightly heavier than the archer; no loose pile collapse.",
    .2, 3, "Warrior locomotion foot contact, never while idle.", gain=-20, total=3, cooldown=160, priority=20)
add("snd_skeleton_warrior_death", "Skeleton warrior breaks down", "Create a descending small pile of dry wooden and ceramic bone-like pieces with one damped weapon clink into sand. No glass, gore, voice or huge crash.",
    .85, 3, "Skeleton warrior death entry once; suppress for silent despawn.", gain=-7, total=3, cooldown=120)
add("snd_skeleton_archer_move", "Skeleton archer foot contact", "Record a light dry bony toe tap in sand with a tiny leather quiver tick. One delicate contact with less weight than the warrior, no arrow release.",
    .18, 3, "Archer locomotion foot contact; replaces generic footstep.", gain=-21, total=3, cooldown=160, priority=20)
add("snd_skeleton_archer_death", "Skeleton archer falls", "Create a light brittle skeletal rattle falling into sand, a soft bow-wood knock and two quiver taps. No bow firing or human voice.",
    .75, 3, "Skeleton archer death entry once; suppress for silent despawn.", gain=-8, total=3, cooldown=120)
add("snd_bow_draw", "Skeleton archer ranged windup", "Record one taut bowstring draw with low wooden limb flex and a small arrow nock click, dry and readable. No release twang or arrow flight. Keep the end quiet enough to cut if the shot is cancelled.",
    .45, 3, "Archer attack windup, before release frame 5; never delay gameplay to fit the audio.", gain=-9, total=3, cooldown=220, priority=65)
add("snd_bow_release", "Skeleton archer releases arrow", "Record a compact natural bowstring snap and short resonant wood twang, no cartoon boing. No arrow impact, swish or extra shot.",
    .24, 3, "Exactly at archer release frame 5 when an arrow actually spawns; no cue if spawn is cancelled.", gain=-5, total=3, cooldown=120, priority=65)
add("snd_arrow_travel", "Arrow flight", "Synthesize a soft short narrow air hiss with tiny feather flutter, moving energy without a tonal whistle. Keep it subtle; no release, impact or exaggerated ricochet.",
    .6, 2, "Arrow enters Dave's nearby audible area after release; one short flyby per projectile, omitted for distant arrows.", gain=-18, total=3, cooldown=100, priority=30,
    stop="Finish flyby unless arrow hits or despawns, then fade out over 20 ms. On room exit/reset fade out over 40 ms.", fade_out=20)
add("snd_arrow_hit", "Arrow hits body or shielded target", "Create a tight wooden shaft tick with a dry padded impact and tiny feather rattle. No wet gore or voice. It must differ from the brighter metallic sword hit.",
    .25, 3, "Arrow collision actually resolves against a character; world collision uses snd_arrow_hit_world instead. Pair Dave's hurt only when HP decreases.", gain=-5, total=3, cooldown=80)
add("snd_arrow_hit_world", "Arrow hits terrain", "Record a wooden shaft striking sandstone then a brief dry shaft vibration and grit fleck. No body thump, metal clang or cartoon ricochet.",
    .3, 3, "Arrow first resolves against solid scenery; replaces body-impact cue and plays once before destruction.", gain=-11, total=3, cooldown=90)

add("snd_bandit_attack", "Bandit melee windup", "Record a rapid leather brace, an original brief nonverbal breath and a curved steel blade air-cut. Agile and threatening without shouting, contact or words. Start immediately to support the short windup.",
    .3, 3, "Bandit windup frames 0-1; once per attack before active frames 2-4.", gain=-6, total=3, cooldown=200, priority=65)
add("snd_bandit_move", "Bandit running contact", "Record a light sandal jab in dry sand with a short cloth belt flick. One quick foot contact, agile and softer than Dave's armoured step; no vocal.",
    .16, 3, "Bandit locomotion foot contact; one cue per footfall.", gain=-20, total=3, cooldown=110, priority=20)
add("snd_bandit_death", "Bandit defeated", "Record one original short nonverbal exhausted breath with a leather-cloth fall and a muted weapon settling in sand. No words, scream, gore or prolonged suffering.",
    .9, 3, "Bandit death state entry once.", gain=-8, total=3, cooldown=150)
add("snd_bandit_caster_move", "Bandit caster foot contact", "Record one soft robe hem scrape in sand and a tiny wooden staff ferrule tap. Slow and dry, with no magical hum or vocal.",
    .23, 3, "Caster locomotion foot contact; no continuous robe loop while idle.", gain=-21, total=3, cooldown=160, priority=20)
add("snd_bandit_caster_death", "Bandit caster defeated", "Record a robe collapsing into sand, a dry staff knock and an original small nonverbal breath. Add a very brief soft loss-of-charge fizz at the end, not an explosion.",
    .95, 3, "Caster death state entry; cancel any owned charge cue first.", gain=-8, total=3, cooldown=150)
add("snd_cast_charge", "Bandit caster ranged windup", "Synthesize a hollow warm glass-and-air resonance gathering softly toward a small unstable pulse. Use a rounded middle register and no high alarm, electrical crack or voice. Make the onset immediately distinguishable from bow draw.",
    .5, 3, "Caster windup before release frame 5; once per cast, stop if interrupted.", gain=-7, total=3, cooldown=250, priority=65)
add("snd_magic_launch", "Magic orb launched", "Synthesize a compact rounded tonal pop with a short airy suction release, warm glass and sand-like sparkle. No long travel hum, thunder or impact blast.",
    .3, 3, "Exactly at caster release frame 5 only if the magic orb spawns.", gain=-6, total=3, cooldown=120)
add("snd_magic_travel", "Magic orb in flight", "Synthesize a quiet hollow fluttering resonance with smooth low-mid movement and a little granular air. No periodic alarm pulses or identifiable melody. Avoid harsh 2-5 kHz noise that masks danger warnings.",
    1.5, 1, "A live nearby magic orb gains one owned loop handle; never retrigger each step.", gain=-18, total=3, cooldown=0, priority=30, loop=True, fade_in=30, fade_out=30,
    stop="Stop with 30 ms fade on projectile hit, expiry, owner cleanup, room unload or encounter reset; do not leave orphaned travel loops.")
add("snd_magic_hit", "Magic orb impact", "Synthesize a compact hollow glassy pop, warm low body and a short breathy spark scatter. No real breaking glass, sword metal, thunder or voice. Tail should decay quickly during crowded combat.",
    .48, 3, "First resolved orb collision with character or world; one cue, then stop travel loop.", gain=-4, total=3, cooldown=80, priority=65)

add("snd_bat_fly", "Bat wing movement", "Record or synthesize one tiny leathery downstroke with a soft air puff, no flock, squeak, music or horror ambience. One beat only, not a rhythmic chain.",
    .13, 3, "Selected wing downstroke animation events on nearby bats; audition every second downstroke to avoid swarm chatter.", gain=-23, total=3, cooldown=180, priority=15)
add("snd_bat_screech", "Bat dive telegraph", "Create an original small creature chirr, a raspy upper-mid two-part nonverbal squeak that is audible without ultrasonic harshness. Keep it distinct from menu beeps and thunder warning; no horror scream.",
    .26, 3, "Bat commits to dive windup, once per dive, including boss-summoned bats.", gain=-9, total=3, cooldown=500, priority=65)
add("snd_bat_dive", "Bat melee dive motion", "Create a small leathery wing tuck and fast soft downward air sweep. No screech, human voice, collision thud or arrow whistle.",
    .22, 3, "Dive active motion begins; successful contact uses snd_enemy_melee_hit and Dave hurt if applicable.", gain=-12, total=3, cooldown=220)
add("snd_bat_defeat", "Bat death", "Create a small original creature breath-chirp dropping away with a soft wing crumple and dry dust patter. No exaggerated cartoon fall whistle or human voice.",
    .5, 3, "Bat defeat entry once; whiteout deletion of living summons stays silent.", gain=-10, total=3, cooldown=130)
add("snd_python_move", "Python slither", "Record a short broad dry scale friction across sand with tiny gritty ticks. Smooth and grounded, no hiss, rattlesnake rattle or continuous dramatic drone.",
    .35, 3, "One cue per selected slither body-cycle ground contact, not every frame.", gain=-21, total=2, cooldown=280, priority=20)
add("snd_snake_hiss", "Python coil and melee telegraph", "Create an original low breath hiss with a gentle rough edge, rising slightly as the body coils. Keep it broad and soft enough to avoid piercing sibilance. No rattle, words or attack contact.",
    .6, 3, "Python coil animation begins; once per committed lunge preparation.", gain=-8, total=2, cooldown=500, priority=65)
add("snd_snake_lunge", "Python melee lunge", "Create a short wide scale brush and forceful air push with a tiny dry jaw click, no human grunt, hiss layer, wet bite or weapon swish.",
    .25, 3, "Python lunge active motion begins; actual contact may layer shared melee impact.", gain=-6, total=2, cooldown=250)
add("snd_python_death", "Python defeated", "Create a broad soft scale slump in sand, an original small creature exhale and a brief dry granular tail. No rattlesnake tail, gore or prolonged hiss.",
    .85, 3, "Python death entry once.", gain=-9, total=2, cooldown=150)
add("snd_worm_rumble", "Sandworm burrowing movement and warning mound", "Synthesize a dry sandy subterranean grinding rumble, with audible 180-500 Hz grit so it reads on small speakers. Add slow irregular pressure swells, no bass-only effect, explosive eruption or constant tonal note. Warning identity should be clear in the first 150 ms.",
    3, 1, "Sandworm mound/warning becomes active; one loop per nearby worm, not a new play every animation frame.", gain=-10, total=2, cooldown=0, priority=70, loop=True, fade_in=60, fade_out=80,
    stop="Fade out over 80 ms at emergence, return below ground, death, silent despawn or scene reset. Stop this bed before the emergence impact.")
add("snd_worm_emerge", "Sandworm eruption", "Create a large dry sand burst with a rounded earth thump and falling grit. Weight must remain audible above 120 Hz; no cinematic sub-only boom, metal, rock avalanche or voice.",
    1.1, 3, "At surface-break frame in worm emergence, after its warning; once per rise.", gain=-3, total=2, cooldown=350, priority=75)
add("snd_worm_bite", "Sandworm melee bite", "Create a broad muscular air thrust, dry jaw clap and short sandy body scrape. Powerful but cartoon-safe; no wet crunch, scream or contact hit baked in.",
    .42, 3, "Worm attack enters active frame 4 (active 4-5); once per bite; actual damage separately confirms contact.", gain=-4, total=2, cooldown=300, priority=65)
add("snd_worm_burrow", "Sandworm returns under sand", "Create a downward sliding coarse-sand suction with soft body drag and settling grains, a downward energy gesture distinct from the upward eruption. No splash or voice.",
    .9, 3, "Worm burrow animation begins; stop exposed movement cues.", gain=-9, total=2, cooldown=450)
add("snd_sandworm_death", "Sandworm defeated", "Create a large dry body slump into sand, a low original creature exhalation and coarse grains settling. Keep the transient rounded and the decay grounded, no gore, explosion or dragon roar.",
    1.5, 2, "Worm death entry once; first stop its rumble loop.", gain=-5, total=2, cooldown=250, priority=65)
add("snd_enemy_melee_hit", "Confirmed enemy melee contact", "Create a short dry padded body knock with a little leather scrape, clear but less metallic than Dave's sword impact. No voice, wet gore, sword swing or second strike.",
    .18, 3, "Accepted melee damage to Dave from undead, warrior, bandit, bat, python or worm; one per accepted HP-loss event, alongside snd_hurt. No sound for collision without damage.",
    gain=-7, total=2, cooldown=120, priority=75)

add("snd_boss_summon", "Pharaoh summon gesture", "Create a low hollow staff resonance and dry swirling sand inhalation, then a compact outward pulse. Regal and unnatural without chanting, spoken voice, bat squeaks or unit emergence baked in.",
    .9, 2, "Pharaoh summon animation release event for either bat wave or undead wave; once per boss action, not per spawned unit.", gain=-5, total=1, cooldown=700, priority=70, milestone="F")
add("snd_boss_bat_spawn", "Bat materializes from Pharaoh's magic", "Synthesize a tiny dry air pop with a leathery flutter and a short muted granular fizz. No screech or low explosion, so multiple bat spawns remain light.",
    .32, 3, "Actual boss bat spawn; cluster at most two audible starts per 120 ms and omit excess swarm spawns.", gain=-13, total=2, cooldown=120, milestone="F")
add("snd_summon_crack", "Undead summon location warning", "Create a short sandstone crackle underneath soft disturbed sand, immediately recognizable and dry. No eruption, thunder strike or undead vocal; the crack is a small local warning.",
    .45, 3, "Summon ground marker first appears; once per audible marker cluster, before undead rise.", gain=-7, total=2, cooldown=120, priority=75, milestone="F")
add("snd_laser_charge", "Pharaoh rod aim and charge warning", "Synthesize a dry focused bronze-rod hum with a rounded pulsing midrange and restrained rising tension inside a seamless steady-state cycle. Start audible immediately; never hide the warning in a long fade. No alarm beep, firing blast or high piercing whine.",
    1, 1, "Laser aim/charge state begins; one persistent owned loop for the rod during the entire telegraph.", gain=-4, total=1, cooldown=0, priority=95, loop=True, fade_in=20, fade_out=30,
    stop="Stop with 30 ms fade when firing starts, attack is interrupted, Pharaoh dies, or encounter resets. Charge length follows Claude's telegraph, not file duration.", milestone="F")
add("snd_laser_fire", "Pharaoh rod active beam", "Synthesize a sustained narrow dry energy buzz with a warm distorted core, soft crackling edges and limited harsh upper mids. Distinguish it from the hollow magic orb. No baked charge, impact or repeated gunshots; stable repeat suitable for any beam length.",
    .8, 1, "Beam damage-active state begins; one owned loop, reused for continuous or swept beam according to engineering.", gain=-7, total=1, cooldown=0, priority=75, loop=True, fade_in=10, fade_out=50,
    stop="Stop in 50 ms at beam end, interrupted attack, boss defeat, Dave death or reset. For a projectile interpretation attach to projectile life and use the same cap.", milestone="F")
add("snd_laser_hit", "Laser damages Dave", "Create a short dry hot energy snap and compact body knock. No scream, gunshot, electric torture effect or long fire crackle. Keep it distinct from the beam's sustained buzz.",
    .25, 3, "Accepted laser HP loss only, at damage interval chosen by Claude; no per-frame repeats while overlapping.", gain=-5, total=1, cooldown=200, priority=80, milestone="F")
add("snd_thunder_warn", "Thunder tile warning", "Synthesize two muted stone-and-bell taps 120 ms apart, followed by a short airy tension tail. Clear rounded midrange, no major melody, UI click, lightning crack or shrill alarm. The first tap must identify danger within 50 ms.",
    .38, 2, "Committed thunder marker cluster appears; start immediately, before strike. Initial design allows about 1 second warning, controlled by Claude. One cue per wave/cluster rather than one per marked tile.",
    gain=-3, total=2, cooldown=250, priority=100, milestone="F")
add("snd_thunder_strike", "Thunder barrage impact", "Synthesize a compact lightning crack over a rounded low-mid boom with dry sandy reflections. Keep the crack controlled, no startling ultra-loud spike or long storm recording. Readable on small speakers with little sub-bass dependency.",
    1.1, 3, "Strike wave resolves at committed tiles. Consolidate simultaneous nearby tiles into one or two audible strikes; no delayed queue of per-tile sounds.",
    gain=-2, total=2, cooldown=120, priority=90, milestone="F")
add("snd_boss_float", "Pharaoh hovering movement", "Synthesize a very quiet dry robe drag with an airy hollow resonance, a single short hovering glide rather than wind ambience. No footsteps, voice, charge warning or magical attack.",
    .7, 2, "Optional selected visible movement glide start, once per direction change; omit at rest and during attack warnings.", gain=-24, total=1, cooldown=1500, priority=10, milestone="F")
add("snd_boss_teleport_out", "Pharaoh teleport disappearance", "Create a compact dry sand suction with a low bronze resonance folding inward. Short and deliberate, no explosion, words or long reverse cymbal.",
    .48, 2, "Teleport-out animation begins once; no damage confirmation implied.", gain=-9, total=1, cooldown=400, priority=60, milestone="F")
add("snd_boss_teleport_in", "Pharaoh teleport arrival", "Create a small outward dry sand pulse and warm hollow bronze tap, clearly answering an inward suction without copying it in reverse. No thunder, voice or huge boom.",
    .48, 2, "Teleport-in materialization event once; may not be omitted if needed as a positional cue.", gain=-7, total=1, cooldown=400, priority=70, milestone="F")
add("snd_boss_hurt", "Pharaoh reacts to confirmed damage", "Create an original low dry closed-mouth resonant grunt with a tiny crumbling-stone edge. One brief nonverbal reaction, less voice-like than dialogue and without words, scream or weapon hit.",
    .35, 3, "Confirmed nonfatal Pharaoh HP loss; rate-limit independently of sword damage. Final blow uses death cues instead.", gain=-8, total=1, cooldown=300, priority=60, milestone="F")
add("snd_boss_death", "Pharaoh fatal blast", "Create one dramatic but controlled dry magical blast: rounded low-mid stone thump, bronze fracture and sand pressure release. No real-world bomb recording, vocal, music or piercing spike. Leave a clear gap after the onset for disintegration detail.",
    1.2, 1, "Confirmed Pharaoh HP crosses zero, once before whiteout; immediately stop owned attacks and warning sounds.", gain=-1, total=1, cooldown=2000, priority=100,
    stop="Preserve tail during boss instance destruction and whiteout. On scene abort/load/reset fade out over 100 ms. Never replay from boss-defeated save state.", milestone="F")
add("snd_disintegrate", "Pharaoh dissolves into sand", "Create a dry descending granular crumble, tiny brittle bronze flecks and a final soft sandy air release. No second blast, voice, music or continuous storm bed. Design the final second to dissipate naturally.",
    2.4, 1, "Begin at t=0 of confirmed boss defeat alongside the blast, matching the storyboard; use a soft initial texture so the blast reads. One sequence-level cue, not one per particle.", gain=-8, total=1, cooldown=2500, priority=80,
    stop="Preserve decay through whiteout while all living summon/projectile sounds are removed. Fade out over 100 ms on skip/load/reset.", milestone="F")

add("snd_chest_open", "Chest opening", "Record a small weathered wooden treasure chest: latch click, warm hinge creak and a gentle lid stop. One compact action without a loot fanfare, coin spill or magical sparkle.",
    .65, 2, "Persistent chest changes from closed to opening, once; not when restoring an already-open chest.", group="Interaction", gain=-8, total=2, cooldown=350, milestone="A")
add("snd_chest_locked", "Chest or sealed door interaction denied", "Record a short dry wooden latch tug and damped metal catch. No successful opening, alarm or spoken disapproval.",
    .22, 2, "Explicit interact attempt on locked chest or sealed route; once per accepted interaction, not while holding E.", group="Interaction", gain=-12, total=1, cooldown=300)
add("snd_pickup", "Potion, equipment or valuable enters inventory", "Synthesize one small rounded ceramic-pluck and warm upward shimmer, compact and neutral enough for varied items. No coin shower, famous pickup melody or extra rewards.",
    .32, 3, "Item is actually added to inventory; aggregate a batch of chest items into one cue. No cue when inventory is full or rewards are already claimed.", group="Interaction", gain=-10, total=2, cooldown=120, milestone="A")
add("snd_coin", "Gold pickup", "Record two tiny dry metal coin ticks with a soft pouch touch, one compact pickup gesture. No casino cascade, music or long bell ring.",
    .22, 3, "Gold transaction succeeds; replaces generic pickup for that item/batch.", group="Interaction", gain=-13, total=2, cooldown=100)
add("snd_levelup", "Level increases", "Compose a compact original C5-E5-G5-C6 plucked figure with a warm breathy shimmer and soft hand-drum tap. Uplifting but modest, no triumphant orchestra or borrowed game jingle.",
    1.3, 1, "Level actually increases; consolidate multiple levels from one XP award into one cue. Ordinary XP increments stay silent.", group="Interaction", gain=-7, total=1, cooldown=1000, priority=70)
add("snd_checkpoint", "Yellow star checkpoint interaction", "Synthesize a gentle clear rounded C5-G5-E5 star-like plucked shimmer with a warm short resonance. Distinct from saving success and healing; reassuring, original and free of copied save-point tones.",
    .8, 1, "Interaction with star opens the three-slot save menu; once per opening, no proximity loop.", group="Interaction", gain=-10, total=1, cooldown=500, priority=65, milestone="A")
add("snd_save", "Save completed successfully", "Synthesize a quiet precise two-step rounded pluck C5 then C6, ending with a soft warm seal click and no long tail. Clearly completed rather than pending; no familiar operating-system or game notification.",
    .65, 1, "Claude confirms successful save commit to the selected slot; never at the initial Save button press or on failed write. Replaces generic UI confirm on final success.", group="Interaction", gain=-8, total=1, cooldown=500, priority=80, milestone="A")
add("snd_ui_error", "Rejected UI action or failed save", "Synthesize a small soft downward wooden double knock, dry and rounded, neither harsh alarm nor comedic buzzer. No words or melodic reward.",
    .22, 1, "Explicit failed save/load or rejected item action after validation; once with visible error text; never mask a successful save with this cue.", group="UI", gain=-12, total=1, cooldown=300, priority=75, milestone="D")
add("snd_inventory_open", "Inventory panel opens", "Record a short soft leather folio unfold with a tiny wooden clasp release. One light gesture without paper flood, item drops or UI music.",
    .24, 1, "Full inventory changes from closed to open; not every redraw.", group="UI", gain=-14, total=1, cooldown=180)
add("snd_inventory_close", "Inventory panel closes", "Record a short soft leather folio settle and muted clasp touch, lower and briefer than opening. No slam, metal lock or extra click.",
    .2, 1, "Full inventory changes from open to closed; replaces generic cancel for that close event.", group="UI", gain=-15, total=1, cooldown=180)
add("snd_ui_move", "Menu or hotbar selection changes", "Synthesize a very soft dry rounded wooden tick with minimal pitch, no bright beep or ringing tail. It must remain unobtrusive during repeated navigation.",
    .055, 3, "Focus/selection changes to a different enabled menu entry or hotbar slot; not continuous hover or unchanged selection.", group="UI", gain=-18, total=1, cooldown=60, priority=40, milestone="A")
add("snd_ui_confirm", "Menu action accepted", "Synthesize one small warm upward two-tone wooden pluck, short, dry and precise. No reward fanfare or checkpoint sparkle.",
    .14, 1, "Accepted menu command; specialist save/checkpoint/pickup sound replaces this where specified.", group="UI", gain=-14, total=1, cooldown=100, priority=60, milestone="A")
add("snd_ui_cancel", "Back or cancel action", "Synthesize a soft low wooden tap followed by a tiny damped downward tone. Short and neutral, not a failure buzzer.",
    .12, 1, "Accepted back/cancel command; inventory close uses its own cue instead.", group="UI", gain=-16, total=1, cooldown=100, priority=50, milestone="A")
add("snd_gate_open", "Arena or dungeon route gate opens", "Record heavy dry stone runners with a restrained iron chain movement and a gentle final stop. Weighty but compact, no huge crash, dungeon scream or musical reward.",
    1.2, 2, "Gate actually begins opening; once per state transition, not on restoring an already-open saved gate.", group="Interaction", gain=-7, total=1, cooldown=1000, priority=65, milestone="F")
add("snd_gate_slam", "Arena gate closes behind Dave", "Create a short dry iron-and-stone gate slide ending in one solid damped slam and sandy rattle. Clear enclosure without a startling cinematic peak. No crowd, voice or music.",
    .9, 2, "Boss arena entrance closes after Dave is fully inside; align the slam onset to final closed contact by Claude's animation event.", group="Interaction", gain=-5, total=1, cooldown=1000, priority=80, milestone="F")

for n, (duration, gesture) in enumerate([
    (.075, "rounded closed-mouth 'mm' onset with calm weight"),
    (.08, "slightly firmer low-mid closed-mouth hum with a soft breath release"),
    (.09, "gentle rising then level closed-mouth murmur without a vowel word"),
    (.095, "short steady nasal chest murmur with a warmer trailing breath")], 1):
    add(f"snd_voice_dave_{n}", f"Dave dialogue blip take {n}",
        "Record an original adult human performer, or synthesize a human-like formant murmur, warm, grounded and firm with no imitation of an existing character or actor. "
        f"Make exactly one {gesture}. Preserve a compact chest/nasal body with no click at either edge, no reverb and no intelligible syllable or word. "
        "The quoted phonetic description is an articulation direction, not a word to speak. Match the other Dave takes in perceived level and baseline register; runtime supplies only restrained +/-6% pitch variation.",
        duration, 1, "During Dave's progressive text reveal, approximately every second newly revealed non-space, non-punctuation character; choose among four takes without immediate repetition.",
        group="Text", gain=-10, total=1, cooldown=75, priority=80, fade_out=5,
        stop="Finish current blip normally; on punctuation pause schedule none, and on instant reveal, skip, speaker change, line close or scene transition immediately cancel queued blips and stop active blip with 5 ms fade.", milestone="E")
for n, (duration, gesture) in enumerate([
    (.09, "low closed-mouth resonant pulse with a dry papery edge"),
    (.095, "slightly hollow downward nonverbal throat murmur"),
    (.1, "steady low nasal resonance with a tiny breath break"),
    (.11, "compact rough chest resonance that decays without a growled word")], 1):
    add(f"snd_voice_pharaoh_{n}", f"Pharaoh dialogue blip take {n}",
        "Record an original performer or use original formant synthesis for an ancient undead ruler: low, dry and resonant, intelligible as a character presence on small speakers. "
        f"Create one {gesture}; keep useful harmonics above the fundamental rather than relying on sub-bass. "
        "No sentence, word, chant, long growl, spooky reverb or imitation of Undertale recordings. Match the other three Pharaoh takes in level and register; allow runtime +/-6% pitch variation.",
        duration, 1, "During Pharaoh progressive text reveal, approximately every second newly revealed non-space, non-punctuation character; choose among four takes without immediate repetition.",
        group="Text", gain=-9, total=1, cooldown=75, priority=80, fade_out=5,
        stop="Finish current blip normally; pause scheduling for punctuation. On instant reveal, skip, speaker change, line close or scene transition cancel queued blips and stop active blip with 5 ms fade.", milestone="E")
for n, (duration, gesture) in enumerate([
    (.05, "soft brushed-paper tick with a rounded onset"),
    (.06, "tiny felted wooden tap with a breath-soft tail"),
    (.07, "quiet filtered air-and-paper puff without a sharp consonant"),
    (.075, "soft dry parchment touch with a faint warm resonance")], 1):
    add(f"snd_voice_narrator_{n}", f"Narration text appearance take {n}",
        f"Create one original {gesture}. This is a soft text-appearance sound, not a human voice. "
        "No words, typing keyboard, typewriter bell, digital alarm, melody, copied game sample or sustained ambience. "
        "Keep all four narrator takes close in perceived level, quieter than character murmurs and comfortable at rapid reveal cadence.",
        duration, 1, "During narrator progressive text reveal, approximately every second newly revealed non-space, non-punctuation character. Keep narrator speaker key; voice prefix is retained only for contract naming.",
        group="Text", gain=-17, total=1, cooldown=75, priority=70, fade_out=5,
        stop="Pause at punctuation; on instant reveal, skip, line close or scene transition cancel queued appearances and stop current sound with 5 ms fade. Never replay sounds for text revealed in one frame.", milestone="E")


PLAN = """# Dave's & Enemies Chapter I audio production plan

The score follows Dave from the ruined Holy City through desert exploration to the Pharaoh and the dungeon threshold. Effects make attacks, successful actions and danger readable without crowding the text voices. Claude owns resource import, playback, loop handles, mixing, state transitions and event triggers. The values below are proposed audio integration targets, not changes to gameplay or engineering's contract.

**Delivery status: all new audio files are PENDING_AUDIO. Generated WAV files: 0.** This handoff supplies original composition instructions, recording/generation prompts and an auditable cue sheet. Planned filenames do not indicate existing files. Template WAVs already under `sounds/` are existing placeholders, not new productions and not certified against this plan. No project resource, sound, runtime data or GML file is changed.

## Sources and contract decisions

- Original user brief in the chat “Create Dave’s action game prompt”, thread `01a19086-ad27-7ba2-b483-5f550e9c8e07`, original user message `01a19086-b65a-75a3-9fbe-ad191a1daa8e`: siege aftermath, vow, eastward desert journey, enemy roster, Pharaoh encounter, whiteout, dungeon cliffhanger and sound requirements.
- [PROJECT_CONTRACT](../PROJECT_CONTRACT.md), especially sections 5, 8, 9 and 11: naming, attack events, exports, text blips and readable warnings.
- [ASSET_REQUESTS](../ASSET_REQUESTS.md): milestone ordering, requested sound IDs and placeholder inventory.
- [NARRATIVE_SCRIPT](../NARRATIVE_SCRIPT.md) and [NARRATIVE_ASSET_REQUESTS](../NARRATIVE_ASSET_REQUESTS.md): the now-authored 54-second intro, 10-second ending, optional banner/grit IDs, defeat sequence and text timing. The audio plan adopts those timings; the contract's exports take precedence over the narrative request's stereo wind.
- This chat's instructions govern the creative direction. Claude's contract governs exports where the asset request list disagrees. `snd_wind_loop` is **mono**, because the contract says SFX mono even though request E9 says stereo. Narration has **four** takes, including `snd_voice_narrator_4`, following the contract's four variants per speaker rather than request E7's three. These are reported discrepancies; the source documents are unchanged.

No connected tool presently exposes suitable original music/SFX generation. HeyGen exposes speech synthesis and catalog search, which are not used as substitutes for these instrumental compositions or original short nonverbal recordings. Runway was found as an unconnected generation option; using it requires connection. The prompt pack is usable in any suitable generator, DAW or recording session. Nothing has been generated, auditioned or mastered yet.

## Deliverables and how to use them

- [AUDIO_CUE_SHEET.csv](AUDIO_CUE_SHEET.csv): compact production and integration index, one row per stable ID.
- [AUDIO_PROMPTS.md](AUDIO_PROMPTS.md): complete standalone prompt for every ID, with duration, variant count, loop, trigger, stop, fades, loudness, limits and export rules repeated for that asset.
- [AUDIO_MANIFEST.json](AUDIO_MANIFEST.json): the same detailed records in structured form. This is design handoff data under `docs/`, not a new runtime schema. Claude decides whether and how to translate it into game data.

Grouped SFX IDs with several takes use `<id>_1.wav`, `<id>_2.wav`, etc.; the group ID remains the stable event name. Single-take IDs use `<id>.wav`. Dialogue takes are individually stable IDs, e.g. `snd_voice_dave_1.wav`, each with one file. Claude maps groups to resources without renaming existing template assets. Do not use missing-file placeholders or synthetic empty WAVs to suggest completion.

## Desert musical interpretation

“Arabian-major” is treated here as a project-specific tonal colour. The provisional collection is fixed at **C, Db, E, F, G, Ab, B**, with C as tonal centre, twelve-tone equal temperament and A4=440 Hz. Its scale degrees are **1, b2, 3, 4, 5, b6, 7**, and its successive semitone steps are **1, 3, 1, 2, 1, 3, 1**. This matches the pitch-class set indexed as Double Harmonic in [Ian Ring's scale analysis](https://ianring.com/musictheory/scales/2483). The interpretation is a fantasy game composition choice; the pitch list alone is not a specification for a traditional maqam performance.

E natural against C carries the major character. Db-C and B-C provide close tension and release; the Db-E and Ab-B gaps give the phrases their distinctive shape. Use those gaps sparingly within singable lines. Do not silently replace B with Bb, use D/A natural, or substitute an unrelated minor-loop preset. Emphasize open C-G, C major, F minor and Db major colours, and G-B dyads instead of a conventional G major chord containing D natural. Pitched percussion stays on C or G; unpitched percussion need not imply another key.

`mus_desert` is **80 BPM, 4/4, 32 bars, 96 seconds**. It uses restrained plucked strings, a breathy flute-like lead, frame/hand drums and light shaker, with rests and gentle variation over four eight-bar sections. A4=440 Hz; C4 means middle C. The original four-bar melody is:

```text
q = quarter note, e = eighth note; every bar totals four beats
1 | C4 q  Db4 e  E4 e  G4 q  F4 q
2 | E4 q  Db4 e  C4 e  B3 q  C4 q
3 | G4 q  Ab4 e  B4 e  C5 q  G4 q
4 | F4 q  E4 q   Db4 q C4 q
```

Let the motif breathe rather than repeating it continuously. Bars 1-8 establish it, 9-16 shift the answer to strings, 17-24 open the flute register, and 25-32 return to the opening texture. The final two bars hand back to bar 1 without an ending. The full 96-second file loops: **4,233,600 sample frames**, `loop_start=0`, `loop_end=96` seconds. No separate music files are needed for each room.

## The Pharaoh musical identity

`mus_pharaoh` has an independent hook, a darker register, stronger frame-drum/hand-percussion attacks and a C-G bass ostinato. It is **128 BPM, 4/4, 48 bars, 90 seconds**, retaining the desert collection but using sharper 3+3+2 eighth-note accents and more active counterpoint. Intensity comes from arrangement; both music files share the same mastering target.

```text
dq = dotted quarter, q = quarter, e = eighth; every bar totals four beats
1 | C3 dq  Db3 e  G3 q   E3 q
2 | B2 e   C3 e   Ab3 q  G3 q  rest q
```

The long-short opening, Db-G tritone leap, B-C pickup and final rest make the hook identifiable. State it on dark bowed strings and a breath-reed-like colour, answer in octaves with short plucked doubles, and keep the rhythmic identity intact during variation. Develop it across three 16-bar blocks. Do not time gameplay phase changes to the music or require adaptive stems. A single stereo loop covers a long fight without restarting at health thresholds. The full file is **3,969,000 sample frames**, `loop_start=0`, `loop_end=90` seconds.

## Story and music transitions

| Event | Audio proposal for Claude |
|---|---|
| Opening ruined city | Play `mus_intro` once; quiet wind beneath it, sparse optional rubble and cape cues. Narrator uses text appearances; Dave's vow uses his murmurs. No spoken narration or dialogue recording. |
| Intro skip or natural completion | Cancel text scheduling and fade intro assets over 300 ms on skip; start desert loop with a 1200 ms fade. Never play skipped sounds in a burst. |
| Exploration and normal combat | Continue one `mus_desert` instance across connected rooms. Combat uses SFX without restarting music. |
| Arena entry | Gate closes after Dave is inside. Fade exploration over 1200 ms; fade wind to silence over 600 ms. Dialogue is deliberately sparse. |
| Dialogue complete | Start `mus_pharaoh` on beat 1 with the combat-enabled/boss-bar event. Instant text reveal does not start combat until the line is dismissed. |
| Pharaoh fatal hit at t=0 | Cancel scheduling and all laser, warning, projectile and summon loops; start `snd_boss_death`. Fade boss score over 250 ms. Preserve only the intentional sequence-level death tails. |
| Disintegration at t=0 | Play `snd_disintegrate` once alongside the blast, initially soft so the impact reads. Proposed additional `mus_boss_defeat` starts at t=0.25 s and ends at t=6.25 s, leaving room for the authored exploration return at t=6.5 s. |
| Slow whiteout and cleared arena | Continue intentional death/defeat tails across object removal. Silently delete summons and hazards; do not trigger a death sound for every cleanup deletion. Wind returns quietly at t=4.5 s; exploration fades back at t=6.5 s per the narrative. Do not replay defeat sounds on loading a completed boss state. |
| Dungeon threshold | Fade exploration over 1200 ms and start `mus_ending` at sequence t=0; leave space under Dave's 2-5 s final line. To Be Continued appears at t=6 s; let the score end at t=10 s and hold silence. This is not a Grail-recovery fanfare. |
| Dave dies | Stop attack/travel/weather ownership, fade current score over 250 ms, play his death once and `mus_gameover` on Game Over entry about 250 ms later. Suppress the nonfatal hurt cue for the fatal event. Retry clears all old handles before starting the restored area's score. |

The intro follows the narrative's 0-13/13-20/20-27/27-35/35-43/43-52/52-54 s score beats. If shot timing changes, edit/recompose the music; do not force dialogue reveal speed to fit the export. `mus_boss_defeat` is an audio-design addition, explicitly proposed for Claude to bind into the existing defeat sequence; it does not change the whiteout length or delay control return.

## Enemy coverage and intentional absences

These mappings cover every existing family without adding attacks to the game. Successful contact uses the shared `snd_enemy_melee_hit` plus Dave's accepted damage reaction. Sword damage to enemies uses `snd_sword_hit`; do not play damage sounds on overlap alone.

| Contract entity | Melee | Ranged or summoning | Movement | Death |
|---|---|---|---|---|
| `undead` | `snd_undead_attack` | None specified; emergence is `snd_undead_rise` | `snd_undead_move` | `snd_undead_death` |
| `skeleton_warrior` | `snd_skeleton_warrior_attack` | None specified | `snd_skeleton_warrior_move` | `snd_skeleton_warrior_death` |
| `skeleton_archer` | None specified | `snd_bow_draw`, `snd_bow_release`, `snd_arrow_travel`, body/world impacts | `snd_skeleton_archer_move` | `snd_skeleton_archer_death` |
| `bandit` | `snd_bandit_attack` | None specified | `snd_bandit_move` | `snd_bandit_death` |
| `bandit_caster` | None specified | `snd_cast_charge`, `snd_magic_launch`, travel loop, `snd_magic_hit` | `snd_bandit_caster_move` | `snd_bandit_caster_death` |
| `bat` | Dive telegraph `snd_bat_screech`, active `snd_bat_dive` | None specified; same kit for summoned bats | `snd_bat_fly` | `snd_bat_defeat` |
| `python` | Coil `snd_snake_hiss`, active `snd_snake_lunge` | None specified | `snd_python_move` | `snd_python_death` |
| `sandworm` | `snd_worm_bite` | None specified | Rumble warning loop, emergence, burrow | `snd_sandworm_death` |
| `pharaoh` | None specified; do not add contact attack audio | Summon gesture, bat spawn, summon crack and undead rise; rod charge/fire/hit; thunder warn/strike | Float accents, teleport out/in | Fatal blast plus disintegration and musical defeat cue |

Caster/archer windups cancel on interruption; releases sound only when the projectile spawns at animation frame 5. Warrior windup starts at frames 0-2, bandit at 0-1, undead at 0-3. Dave's swing starts at active frame 2, around 0.10 seconds into the contracted 0.45-second animation, not on each click. No enemy frame timing is inferred from the WAV duration. Surface-break, foot-contact and teleport audio events remain Claude's animation integration work.

## Text sound behaviour

Undertale is a **behavioural reference**: a small character-associated sound accompanies progressive text. All timbres, source recordings and synthesized waveforms must be original. No extracted samples, identifiable character voice imitation, full words or spoken sentences.

- Dave: four warm, firm human nonverbal murmurs, 75/80/90/95 ms.
- Pharaoh: four low, dry, resonant nonverbal murmurs with audible upper harmonics, 90/95/100/110 ms.
- Narrator: four soft paper/felt/air text appearances, 50/60/70/75 ms. These are not a third speaking voice.

Use approximately every second newly revealed letter or digit, excluding spaces and punctuation; select a take without immediate repeat. Runtime pitch variation is restrained to **+/-6%**, as contracted; do not bake four widely separated pitches. Match the narrative's minimum 75 ms between onsets, 120 ms comma pauses and 240 ms sentence-punctuation pauses (use the same sentence pause for ellipsis; semicolon may use 120 ms). One active text sound globally across all speakers and variants; all IDs share that cap. Never queue a backlog: if occupied, drop that reveal sound. Stop and clear scheduling on instant reveal, skip, speaker change, line close and scene exit, with a 5 ms click-free stop. No additional sound for every letter in text that is revealed instantly.

## Relative loudness and simultaneous playback

The manifest gives **proposed runtime gain offsets** in dB relative to the audition reference `snd_sword_hit` at 0 dB. These are starting balances, not measured output levels or extra export normalization. Music is first mastered to -16 LUFS integrated; its listed gain is then applied at playback. Short SFX and blips have no integrated LUFS target. Set source levels by listening and preserve peaks at or below -1 dBFS; do not normalize quiet paper ticks and rumbles to sound as loud as a sword hit.

Priority 100 is most protected. Warnings, Dave damage/death and save success must remain understandable. Footsteps, swarm movement and idle accents yield first. Per-ID global caps include all variants; per-emitter caps prevent one object retriggering itself. The per-ID numbers do not override these proposed shared budgets:

| Shared group | Maximum active voices | Arbitration |
|---|---:|---|
| Music | 1 steady state, 2 only during a crossfade | Explicit transition ownership; no room-stack accumulation |
| All SFX including weather | 24 | Drop/steal lowest-priority distant movement first; reserve headroom for danger/death cues |
| Attack warnings within SFX | 6 | Thunder one per wave/cluster, laser one per rod, nearby committed threats first; never queue warning until after damage |
| All movement/footstep cues | 6 | Prefer Dave and nearest enemies; drop distant excess |
| Projectile travel within SFX | 4 | Magic loops plus nearby arrow flybys share this cap; keep nearest, stop on projectile destruction |
| Weather | 1 | One zone-owned wind loop; fade rather than layering a new one |
| Dialogue/narration | 1 total | Drop busy reveal ticks; cancel on skip; never overlap speakers |

Maintain music, SFX and dialogue volume controls from the brief. Proposed sidechain starting points for Claude: text active reduces music 4 dB and wind 8 dB with ~100 ms attack/350 ms release; committed attack warnings reduce music 3 dB and weather 6 dB with 30/250 ms envelopes. Do not add both ducks arithmetically; use the stronger applicable reduction. Boss battle normally suppresses storms. A 30-50 ms fade on stolen ambience prevents clicks; do not steal an active critical warning to admit a footstep. Test final gain structure with worst-case cues for master headroom rather than assuming file peak ceilings prevent mixed clipping.

Single events use the per-asset cooldown. A cooldown drops the new request; it never delays it. Variant selection avoids immediate repeat, with no additional automatic pitch shifts proposed for SFX. Death and special confirmation cues replace generic hurt/confirm where specified. Only one pickup sound plays per transaction/batch, and restore/load never replays persistent rewards or gate interactions.

## Export and loop delivery

Every production file is **WAV, signed PCM 16-bit little-endian, 44,100 Hz**. Music is stereo at **-16 LUFS integrated +/-1 LU**; SFX, wind and all blips are mono. Keep every peak at or below **-1 dBFS**; targeting -1 dBTP for music is an additional production preference. Use 2-5 ms edge envelopes on one-shots to prevent clicks, trim leading dead air, and keep the designed decay inside the stated duration. Blip durations include both edge envelopes. Do not put a fade or silent padding at a whole-file loop seam.

| Loop ID | Seconds | Sample frames at 44,100 Hz | Channels |
|---|---:|---:|---:|
| `mus_desert` | 96 | 4,233,600 | 2 |
| `mus_pharaoh` | 90 | 3,969,000 | 2 |
| `snd_wind_loop` | 12 | 529,200 | 1 |
| `snd_magic_travel` | 1.5 | 66,150 | 1 |
| `snd_worm_rumble` | 3 | 132,300 | 1 |
| `snd_laser_charge` | 1 | 44,100 | 1 |
| `snd_laser_fire` | 0.8 | 35,280 | 1 |

All planned loops use the whole file: start 0 seconds, end equal to its duration. The start frame is inclusive and the end frame exclusive. Seamlessly wrap instrument releases, reverb and noise movement; align DC offset, waveform continuity and musical pulse across the boundary. No pickup intro is assumed. For charge/fire loops, fade at playback boundaries; the warning begins immediately and the runtime state determines how long it persists.

The contract permits whole-file looping without a sidecar, but production should include a factual `<asset>.json` once the **actual** WAV is finalized, for example `{"loop_start":0,"loop_end":96}` for `mus_desert.json`. Do not ship these example values as verified metadata for a file that does not exist. If a generator cannot produce the exact length, edit/recompose in a DAW and validate the resulting frame count, or deliver accurate nonzero points for Claude's review; never label an arbitrary crop seamless. File-loop QA must be passed before placeholders are replaced.

## Production order

1. **Milestone A vertical slice:** sword swing/hit, Dave hurt, sand steps, undead attack/movement/death, chest, potion/heal, pickup, checkpoint/save and UI move/confirm/cancel. Establish the loudness reference with actual combat audition.
2. **Milestone B enemy families:** remaining melee and ranged identities, projectile cleanup, family movement/deaths, worm warning/emergence, inventory and leveling. Material impact accents are optional polish.
3. **Milestone C world:** wind, stone/wood player steps and weather transition audition.
4. **Milestone D saving:** error/denied actions and success-vs-request distinction; three slots reuse one success cue.
5. **Milestone E opening and score:** record/synthesize the 12 text sounds, compose intro/desert/gameover, then optional rubble/cloth details. Lock motif and loop accuracy in a DAW.
6. **Milestone F encounter and ending:** Pharaoh score, summons, laser, thunder, gates, defeat and chapter ending. Telegraphs and death cleanup take priority over optional hover accents.

For each ID, generate or record several candidates from its complete prompt, select the requested matched variations, edit/compose to the required duration, export and validate, then change status only for real reviewed files. Keep source sessions and provenance outside the runtime bundle. Use a progress status such as pending, generated-unreviewed, edited, audio-validated and integrated; the current handoff remains entirely pending.

## Acceptance checks for production and Claude

- Inspect real WAV headers, channels, bit depth, sample rate, peak, duration, DC offset, leading silence and file integrity. Music needs an actual integrated LUFS measurement. Record hashes, source/provenance, measured loudness and exact loop points when files exist; none are measured here.
- Audition at least five repeats of every loop on headphones and speakers, checking the seam for clicks, rhythm jumps, reverb pumping and obvious gust repetition. Verify music note choices and original motif by ear or MIDI, not prompt text alone.
- Check voice takes at normal and +/-6% pitch, with 50-110 ms native durations, one-voice reveal playback, punctuation pauses and rapid skip/reveal input. Confirm no intelligible words and no recognizable borrowed recordings.
- In the IDE, validate active-frame swings, release-frame projectiles, immediate telegraphs, accepted damage only, batch pickup, successful save only and silent persistent-state restoration. No GameMaker compile or play-test is claimed here.
- Stress a boss barrage with summons, travel loops and music. Verify readable warnings, bounded simultaneous playback, safe master headroom, no orphaned sounds after death/reset, no mass enemy-death burst during whiteout and no weather under critical dialogue.
- Listen through intro skip, pre-boss skip, Dave death/retry, boss defeat/load and ending/menu exit. Confirm smooth stop/fades and one owner for each loop. Claude validates all playback and integration behaviour.
"""


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    group_order = {name: n for n, name in enumerate(["Music", "Atmosphere", "Combat", "Interaction", "UI", "Text"])}
    ASSETS.sort(key=lambda a: group_order[a["group"]])
    delivered = []
    for a in ASSETS:
        category = "music" if a["id"].startswith("mus_") else ("voice" if a["group"] == "Text" else "sfx")
        delivery_dir = ROOT / "audio" / category
        metadata = delivery_dir / f"{a['id']}.json"
        if not metadata.exists():
            continue
        report = json.loads(metadata.read_text(encoding="utf-8"))
        if report.get("status") != "GENERATED_TECHNICALLY_VALIDATED":
            continue
        files = report.get("files") or [{"file": report["file"], "sha256": report["sha256"], "measurements": report["measurements"]}]
        assert {f["file"] for f in files} == set(a["planned_filenames"])
        paths = []
        for f in files:
            wav = delivery_dir / f["file"]
            if hashlib.sha256(wav.read_bytes()).hexdigest() != f["sha256"]:
                raise ValueError(f"Delivery hash mismatch: {wav}")
            paths.append(wav.relative_to(ROOT).as_posix())
        assert report["duration_seconds"] == a["duration_seconds_per_file"]
        a.update(status=report["status"], generated=True,
                 existing_delivered_files=paths,
                 delivery_metadata=metadata.relative_to(ROOT).as_posix(),
                 measurements=report.get("measurements") or [{"file": f["file"], **f["measurements"]} for f in files],
                 delivery_status_note="Actual Python-synthesized WAV files generated and objectively checked; human listening review and Claude integration remain pending.")
        delivered.append(a)
    produced = sum(len(a["existing_delivered_files"]) for a in delivered)
    produced_sfx = sum(len(a["existing_delivered_files"]) for a in delivered if a["id"].startswith("snd_"))
    produced_music = sum(len(a["existing_delivered_files"]) for a in delivered if a["id"].startswith("mus_"))
    total_files = sum(a["variation_count"] for a in ASSETS)
    payload = {
        "schema": "daves_enemies_audio_design_handoff_v1",
        "date": "2026-10-31", "owner": "Audio design; Claude owns integration",
        "status": ("ALL_AUDIO_GENERATED" if produced == total_files else "PARTIAL_AUDIO_DELIVERY") if produced else "ALL_AUDIO_PENDING", "generated_audio_file_count": produced,
        "pending_audio_file_count": total_files - produced,
        "asset_id_count": len(ASSETS),
        "planned_wav_count": sum(a["variation_count"] for a in ASSETS),
        "runtime_data": False,
        "sources": ["docs/PROJECT_CONTRACT.md", "docs/ASSET_REQUESTS.md", "docs/NARRATIVE_SCRIPT.md", "docs/NARRATIVE_ASSET_REQUESTS.md",
                    "Original brief in chat 01a19086-ad27-7ba2-b483-5f550e9c8e07"],
        "global_rules": {
            "relative_gain_reference": "snd_sword_hit at 0 dB proposed runtime gain",
            "music_steady_state_limit": 1, "music_crossfade_limit": 2,
            "sfx_total_limit_including_weather": 24, "warning_limit_within_sfx": 6,
            "movement_limit_within_sfx": 6, "projectile_travel_limit_within_sfx": 4,
            "weather_limit_within_sfx": 1, "text_all_speakers_limit": 1,
            "drop_not_queue_on_cooldown_or_cap": True,
            "voice_pitch_variation_percent": [-6, 6],
            "text_reveal_eligible_character_interval": 2,
            "text_minimum_onset_interval_ms": 75,
            "text_punctuation_pause_ms": {"comma": 120, "sentence": 240},
            "contract_discrepancies": ["Wind delivered mono per contract; asset request E9 says stereo.",
                                       "Four narrator takes per contract; request E7 lists three."]
        }, "assets": ASSETS
    }
    (OUT / "AUDIO_MANIFEST.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    plan_text = PLAN
    if produced:
        plan_text = plan_text.replace(
            "**Delivery status: all new audio files are PENDING_AUDIO. Generated WAV files: 0.**",
            f"**Delivery status: {produced} actual Python-synthesized WAVs generated and technically validated; {total_files - produced} planned WAVs remain pending.**")
        plan_text = plan_text.replace(
            "Planned filenames do not indicate existing files.",
            f"Delivered music: {produced_music} actual WAVs, with file links, timing and measured results in the [music delivery notes](../../audio/music/AUDIO_DELIVERY.md). "
            + (f"All {produced_sfx} SFX/blip WAVs are also delivered: see the [SFX delivery notes](../../audio/SFX_DELIVERY.md) and [ZIP pack](../../audio/daves_enemies_sfx_and_blips.zip). " if produced_sfx else "")
            + "Human listening review and Claude integration remain pending. Only entries marked generated have actual files; pending entries remain prompts.")
        plan_text = plan_text.replace(
            "No connected tool presently exposes suitable original music/SFX generation. HeyGen exposes speech synthesis and catalog search, which are not used as substitutes for these instrumental compositions or original short nonverbal recordings. Runway was found as an unconnected generation option; using it requires connection. The prompt pack is usable in any suitable generator, DAW or recording session. Nothing has been generated, auditioned or mastered yet.",
            "The delivered audio is produced locally with original deterministic Python synthesis, without a generation service, sampled game audio or cloned voices. The [theme renderer](../../tools/render_chapter_music.py) writes the two full loops; the [story-cue renderer](../../tools/render_chapter_cues.py) writes intro, boss defeat, ending and Game Over; the [SFX/blip renderer](../../tools/render_chapter_sfx.py) writes sound effects and nonverbal formant blips. Actual file paths, hashes and measurements are recorded in the manifest and delivery sidecars.")
        plan_text = plan_text.replace("the current handoff remains entirely pending.",
                                      f"{produced} delivered WAVs have passed objective audio checks; {total_files-produced} planned WAVs remain pending.")
        plan_text = plan_text.replace("none are measured here.",
                                      "delivered files include measured headers, duration, peak and hashes in their sidecars; every delivered music file also includes integrated loudness.")
    (OUT / "AUDIO_PRODUCTION_PLAN.md").write_text(plan_text, encoding="utf-8")
    csv_buffer = io.StringIO(newline="")
    fields = ["id", "purpose", "group", "milestone", "status", "duration_seconds_per_file", "variation_count",
              "planned_filenames", "existing_delivered_files", "loop", "loop_start_seconds", "loop_end_seconds", "trigger", "stop", "fade_in_ms", "fade_out_ms_on_stop",
              "relative_gain_db", "bus", "simultaneous_limit_per_emitter", "simultaneous_limit_global_for_id", "minimum_retrigger_ms",
              "priority_0_to_100", "export", "generation_or_recording_prompt"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fields)
    writer.writeheader()
    for a in ASSETS:
        row = {k: a[k] for k in fields if k in a}
        row.update(planned_filenames="; ".join(a["planned_filenames"]), existing_delivered_files="; ".join(a["existing_delivered_files"]), loop=a["loop"]["enabled"],
                   loop_start_seconds=a["loop"]["loop_start"], loop_end_seconds=a["loop"]["loop_end"],
                   export=f"WAV PCM16 44100 Hz; {a['export']['channels']} ch; peak <= -1 dBFS" + ("; -16 LUFS integrated +/-1 LU" if a['id'].startswith('mus_') else ""))
        writer.writerow(row)
    (OUT / "AUDIO_CUE_SHEET.csv").write_text(csv_buffer.getvalue(), encoding="utf-8-sig", newline="")
    lines = ["# Dave's & Enemies individual audio prompts", "",
             f"**{len(ASSETS)} stable IDs; {payload['planned_wav_count']} planned WAVs; {produced} actual WAVs generated; {total_files - produced} WAVs pending.**", "",
             "Every block contains a standalone production prompt and proposed playback contract for Claude. Only IDs explicitly marked generated have an actual file; other listed filenames are planned only. "
             "All limits include every take belonging to that ID; the shared limits in [the production plan](AUDIO_PRODUCTION_PLAN.md) also apply. "
             "A listed stop fade applies to interrupted/cancelled playback; normal one-shots keep their designed decay. "
             "Gains are proposed runtime offsets relative to `snd_sword_hit` at 0 dB, not measured loudness. "
             "No short-SFX integrated LUFS target is implied.", ""]
    last_group = None
    for a in ASSETS:
        if a["group"] != last_group:
            lines += [f"## {a['group']}", ""]
            last_group = a["group"]
        loop_text = (f"Whole-file seamless; start 0 s, end {a['duration_seconds_per_file']:g} s, {a['loop']['frames_at_44100']:,} sample frames." if a["loop"]["enabled"] else "None; one-shot including decay.")
        status_text = (f"{a['status']}; {len(a['existing_delivered_files'])} actual WAV file(s), human listening review and integration pending." if a["generated"] else "PENDING_AUDIO; no file generated.")
        lines += [f"### {a['id']}", "", f"**Purpose:** {a['purpose']}. **Status:** {status_text} **Milestone:** {a['milestone']}.", "",
                  "**Complete generation or recording prompt:**", "", a["generation_or_recording_prompt"], "",
                  f"- Duration: {a['duration_seconds_per_file']:g} s per file. Variations: {a['variation_count']}. Planned files: " + ", ".join(f"`{p}`" for p in a["planned_filenames"]) + ".",
                  f"- Loop: {loop_text}", f"- Trigger: {a['trigger']}", f"- Stop: {a['stop']}",
                  f"- Playback fades: {a['fade_in_ms']} ms in; {a['fade_out_ms_on_stop']} ms on stop (specific transition exceptions above take precedence).",
                  f"- Relative level: {a['relative_gain_db']} dB; bus `{a['bus']}`. Simultaneous limit: {a['simultaneous_limit_per_emitter']} per emitter, {a['simultaneous_limit_global_for_id']} globally across this ID's takes. Minimum retrigger: {a['minimum_retrigger_ms']} ms. Priority: {a['priority_0_to_100']}/100.", ""]
        if a["generated"]:
            lines += ["Actual files: " + ", ".join(f"[{Path(p).name}](../../{p})" for p in a["existing_delivered_files"]) + ".", ""]
    (OUT / "AUDIO_PROMPTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"asset_ids": len(ASSETS), "planned_wavs": payload["planned_wav_count"],
                      "generated_wavs": produced, "pending_wavs": total_files - produced, "loops": [a["id"] for a in ASSETS if a["loop"]["enabled"]],
                      "written": [str(OUT / n) for n in ["AUDIO_PRODUCTION_PLAN.md", "AUDIO_PROMPTS.md", "AUDIO_CUE_SHEET.csv", "AUDIO_MANIFEST.json"]]}, indent=2))


if __name__ == "__main__":
    build()
