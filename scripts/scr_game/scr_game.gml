// scr_game - the persistent controller's state machine (obj_game).
// Base mode (title, cinema, play, game over, ending) plus an overlay stack (inventory, dialogue,
// pause, settings, save/load, confirmation). Priority: transition > confirmation > child menu >
// pause > dialogue > inventory > gameplay. Exactly one handler receives each tick's input.

function game_init() {
    data_load_all();
    settings_load();
    input_init();
    autotest_init();
    global.mode = MODE.TITLE;
    global.ui = { stack: [] };
    global.transition = undefined;
    global.pending_arrival = undefined;
    global.damage_paused = false;
    global.cine_lock = false;
    global.cine_ctl = undefined;
    global.cam_cx = 0;
    global.cam_cy = 0;
    global.cam_shake_amp = 0;
    global.cam_shake_t = 0;
    global.hp_ghost = 0;
    global.hp_ghost_t = 0;
    global.toast = { goal_text: "", goal_t: 0, goal_dur: 0, msg_text: "", msg_t: 0, msg_col: C_TEXT, prompt: "" };
    global.checkpoint_snapshot = undefined;
    global.initial_snapshot = undefined;
    global.active_slot = -1;
    global.last_saved_playtime = -1;
    global.scene = undefined;
    global.world = undefined;
    global.dlg = undefined;
    global.boss_ui = { visible: false, hp: 1, hp_max: 1, ghost: 1, ghost_t: 0, zero_hold: 0 };
    global.whiteout = { alpha: 0, dark: false };
    global.fade_black = 0;
    global.hot_hover_t = 0;
    global.hot_hover = -1;
    global.swing_counter = 0;
    global.cam_target = undefined;
    global.after_arrival = "";
    global.gui_s = 1;
    global.gui_ox = 0;
    global.gui_oy = 0;
    global.win_w = -1;
    global.win_h = -1;
    global.run = undefined;
    run_new();
    aud_init();
    ui_screens_init();
    window_set_fullscreen(global.settings.fullscreen);
    gui_update_transform(true);
}

// ------------------------------------------------------------------ GUI transform
/// Aspect-correct fit of the 1280x720 plane, shared by drawing, clipping and pointer mapping.
function gui_update_transform(_force) {
    var _ww = window_get_width();
    var _wh = window_get_height();
    if (_ww <= 0 || _wh <= 0) return;
    if (!_force && _ww == global.win_w && _wh == global.win_h) return;
    global.win_w = _ww;
    global.win_h = _wh;
    var _s = min(_ww / GUI_W, _wh / GUI_H);
    global.gui_s = _s;
    global.gui_ox = (_ww - GUI_W * _s) / 2;
    global.gui_oy = (_wh - GUI_H * _s) / 2;
    display_set_gui_maximise(_s, _s, global.gui_ox, global.gui_oy);
}

// ------------------------------------------------------------------ overlay stack
function ui_push(_ov) {
    array_push(global.ui.stack, _ov);
}

function ui_top() {
    var _n = array_length(global.ui.stack);
    return (_n == 0) ? -1 : global.ui.stack[_n - 1];
}

function ui_has(_ov) {
    return array_contains(global.ui.stack, _ov);
}

function ui_remove(_ov) {
    var _s = global.ui.stack;
    for (var i = array_length(_s) - 1; i >= 0; i--) {
        if (_s[i] == _ov) {
            array_delete(_s, i, 1);
            return;
        }
    }
}

function ui_clear() {
    global.ui.stack = [];
    global.dlg = undefined;
    global.aud.text_duck = false;
}

/// Gameplay input is accepted only in plain exploration/combat.
function game_input_ok() {
    return world_active() && !global.cine_lock;
}

function hotbar_visible() {
    return global.mode == MODE.PLAY && !global.cine_lock && !ui_has(OV.DIALOGUE) &&
           !ui_has(OV.PAUSE) && !ui_has(OV.SAVELOAD) && !ui_has(OV.SETTINGS);
}

// ------------------------------------------------------------------ per-tick
function game_begin_step() {
    autotest_tick();
    input_update();
    gui_update_transform(false);
    aud_update(world_active());
    if (global.hp_ghost_t > 0) global.hp_ghost_t -= 1;
    else if (is_struct(global.run)) global.hp_ghost = global.run.hp;
    if (is_struct(global.transition)) {
        transition_step();
        return;
    }
    var _top = ui_top();
    switch (_top) {
        case OV.CONFIRM: confirm_step(); break;
        case OV.SAVELOAD: saveload_step(); break;
        case OV.SETTINGS: settings_step(); break;
        case OV.PAUSE: pause_step(); break;
        case OV.DIALOGUE: dialogue_step(); break;
        case OV.INVENTORY: inventory_step(); break;
        default:
            switch (global.mode) {
                case MODE.TITLE: title_step(); break;
                case MODE.CINEMA: cine_input_step(); break;
                case MODE.PLAY:
                    if (global.cine_lock) cine_input_step();
                    else hud_step();
                    break;
                case MODE.GAMEOVER: gameover_step(); break;
                case MODE.ENDING: ending_step(); break;
            }
    }
}

function game_step() {
    if (world_active()) global.run.playtime += 1;
    toast_step();
    if (global.cam_shake_t > 0) {
        global.cam_shake_t -= 1;
        if (global.cam_shake_t <= 0) global.cam_shake_amp = 0;
    }
}

// ------------------------------------------------------------------ toasts and prompts
function toast_objective(_objective) {
    global.run.objective = _objective;
    global.toast.goal_text = scene_text(_objective);
    global.toast.goal_dur = objective_duration_ticks(_objective);
    global.toast.goal_t = global.toast.goal_dur;
}

/// Temporary feedback line (failed action etc.); a repeat extends rather than stacks.
function toast_show(_text, _ticks = 108, _col = C_TEXT) {
    global.toast.msg_text = _text;
    global.toast.msg_t = _ticks;
    global.toast.msg_col = _col;
}

function toast_step() {
    var _t = global.toast;
    if (_t.goal_t > 0 && world_active()) _t.goal_t -= 1;
    if (_t.msg_t > 0) _t.msg_t -= 1;
}

// ------------------------------------------------------------------ flows
function game_new() {
    ui_clear();
    run_new();
    global.checkpoint_snapshot = undefined;
    global.initial_snapshot = undefined;
    global.active_slot = -1;
    global.last_saved_playtime = -1;
    global.boss_ui.visible = false;
    global.cine_lock = false;
    global.damage_paused = false;
    mus_stop(800);
    global.mode = MODE.CINEMA;
    inp_block_all();
    room_goto(rm_intro);
}

/// Shared by Game Over restore, Load Game and Restart Chapter. Restores the whole snapshot.
function game_restore(_snap, _from_load) {
    ui_clear();
    aud_stop_world(100);
    aud_loops_stop_prefix("", 100);
    snapshot_restore(_snap);
    global.boss_ui.visible = false;
    global.cine_lock = false;
    global.cine_ctl = undefined;
    global.whiteout.alpha = 0;
    global.fade_black = 0;
    global.run.hp = player_max_hp();
    global.last_saved_playtime = global.run.playtime;
    if (mus_current() != "mus_desert") mus_stop(300);
    global.mode = MODE.PLAY;
    scene_go(global.run.scene_room, global.run.pos_x, global.run.pos_y, global.run.facing, _from_load ? "load" : "restore");
}

function game_load_slot(_slot) {
    var _r = save_read(_slot);
    if (_r.state != "ok") return { ok: false, msg: _r.reason };
    global.active_slot = _slot;
    global.checkpoint_snapshot = variable_clone(_r.data.run);
    game_restore(global.checkpoint_snapshot, true);
    toast_show(scene_text("checkpoint_restored"), 120, C_SUCCESS);
    return { ok: true, msg: "" };
}

function game_to_menu() {
    ui_clear();
    aud_stop_world(100);
    aud_loops_stop_prefix("", 300);
    mus_stop(800);
    global.boss_ui.visible = false;
    global.cine_lock = false;
    global.cine_ctl = undefined;
    global.whiteout.alpha = 0;
    global.fade_black = 0;
    global.transition = undefined;
    global.damage_paused = false;
    global.mode = MODE.TITLE;
    inp_block_all();
    room_goto(rm_menu);
}

function session_unsaved() {
    if (global.mode != MODE.PLAY) return false;
    return global.run.playtime != global.last_saved_playtime;
}

/// Called by obj_player when the death presentation finishes.
function game_over_begin() {
    ui_clear();
    aud_stop_world(250);
    aud_loops_stop_prefix("boss:", 100);
    global.boss_ui.visible = false;
    global.cine_lock = false;
    global.mode = MODE.GAMEOVER;
    gameover_open();
}

// ------------------------------------------------------------------ room start
function game_room_start() {
    transition_room_started();
    var _rn = room_get_name(room);
    if (_rn == "rm_menu") {
        global.mode = MODE.TITLE;
        title_open();
    } else if (_rn == "rm_ending") {
        global.mode = MODE.ENDING;
    }
}
