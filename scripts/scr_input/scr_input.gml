// scr_input - the single authoritative input owner.
// obj_game polls devices once per tick (Begin Step) and routes the frame to exactly one state
// handler. Any handler that opens/closes a state consumes the triggering press and blocks every held
// action until it is physically released, so menu clicks never also attack and skips never pass
// through to gameplay.

function input_init() {
    global.inp = {
        map: {
            up: [ord("W"), vk_up], down: [ord("S"), vk_down],
            left: [ord("A"), vk_left], right: [ord("D"), vk_right],
            nav_up: [vk_up], nav_down: [vk_down], nav_left: [vk_left], nav_right: [vk_right],
            interact: [ord("E")], use: [ord("Q")], inventory: [ord("I"), vk_tab],
            pause: [vk_escape], confirm: [vk_enter, vk_space], enter: [vk_enter], space: [vk_space],
            move: [ord("M")], f6: [vk_f6], pgup: [vk_pageup], pgdn: [vk_pagedown],
            home: [vk_home], end_key: [vk_end], shift: [vk_shift], tab: [vk_tab],
            s1: [ord("1")], s2: [ord("2")], s3: [ord("3")], s4: [ord("4")],
            s5: [ord("5")], s6: [ord("6")], s7: [ord("7")], s8: [ord("8")]
        },
        names: [],
        down: {}, pressed: {}, released: {}, held: {}, blocked: {}, consumed: {},
        mx: 0, my: 0, in_content: false, mouse_moved: false, last_mx: 0, last_my: 0,
        wheel_up: false, wheel_down: false, wheel_used: false,
        any_key: false
    };
    var _n = variable_struct_get_names(global.inp.map);
    array_push(_n, "lmb", "rmb");
    global.inp.names = _n;
    for (var i = 0; i < array_length(_n); i++) {
        global.inp.down[$ _n[i]] = false;
        global.inp.pressed[$ _n[i]] = false;
        global.inp.released[$ _n[i]] = false;
        global.inp.held[$ _n[i]] = 0;
        global.inp.blocked[$ _n[i]] = false;
        global.inp.consumed[$ _n[i]] = false;
    }
}

function input_update() {
    var _in = global.inp;
    var _names = _in.names;
    for (var i = 0; i < array_length(_names); i++) {
        var _a = _names[i];
        var _d = false;
        var _p = false;
        if (_a == "lmb") {
            _d = mouse_check_button(mb_left);
            _p = mouse_check_button_pressed(mb_left);
        } else if (_a == "rmb") {
            _d = mouse_check_button(mb_right);
            _p = mouse_check_button_pressed(mb_right);
        } else {
            var _keys = _in.map[$ _a];
            for (var k = 0; k < array_length(_keys); k++) {
                if (keyboard_check(_keys[k])) _d = true;
                if (keyboard_check_pressed(_keys[k])) _p = true;
            }
        }
        if (autotest_active()) {
            var _v = autotest_action(_a);
            _d = _v[0];
            _p = _v[1];
        }
        var _was = _in.down[$ _a];
        _in.released[$ _a] = _was && !_d;
        _in.down[$ _a] = _d;
        _in.pressed[$ _a] = _p;
        _in.held[$ _a] = _d ? _in.held[$ _a] + 1 : 0;
        _in.consumed[$ _a] = false;
        if (_in.blocked[$ _a] && !_d) _in.blocked[$ _a] = false;
    }
    _in.wheel_up = mouse_wheel_up();
    _in.wheel_down = mouse_wheel_down();
    _in.wheel_used = false;
    var _mx = device_mouse_x_to_gui(0);
    var _my = device_mouse_y_to_gui(0);
    if (autotest_active()) {
        _mx = global.autotest.mx;
        _my = global.autotest.my;
        _in.wheel_up = false;
        _in.wheel_down = false;
    }
    _in.mouse_moved = point_distance(_mx, _my, _in.last_mx, _in.last_my) >= 3;
    if (_in.mouse_moved) {
        _in.last_mx = _mx;
        _in.last_my = _my;
    }
    _in.mx = _mx;
    _in.my = _my;
    // clicks in letterbox/pillarbox bars are rejected
    _in.in_content = (_mx >= 0 && _mx < GUI_W && _my >= 0 && _my < GUI_H);
    _in.any_key = keyboard_check_pressed(vk_anykey);
}

function inp_down(_a) {
    return global.inp.down[$ _a] && !global.inp.blocked[$ _a];
}

function inp_pressed(_a) {
    var _in = global.inp;
    if (!_in.pressed[$ _a] || _in.blocked[$ _a] || _in.consumed[$ _a]) return false;
    if ((_a == "lmb" || _a == "rmb") && !_in.in_content) return false;
    return true;
}

/// Navigation repeat: fresh press, then after 300 ms every ~90 ms while held.
function inp_repeat(_a) {
    if (inp_pressed(_a)) return true;
    if (!inp_down(_a)) return false;
    var _h = global.inp.held[$ _a];
    return _h > 18 && ((_h - 18) mod 5 == 0);
}

function inp_held(_a) {
    return inp_down(_a) ? global.inp.held[$ _a] : 0;
}

/// Marks a press as handled this tick and blocks it until released.
function inp_consume(_a) {
    global.inp.consumed[$ _a] = true;
    if (global.inp.down[$ _a]) global.inp.blocked[$ _a] = true;
}

/// Blocks every held action until release (used on every open/close/resume/scene end).
function inp_block_all() {
    var _in = global.inp;
    var _names = _in.names;
    for (var i = 0; i < array_length(_names); i++) {
        var _a = _names[i];
        _in.consumed[$ _a] = true;
        if (_in.down[$ _a]) _in.blocked[$ _a] = true;
    }
    _in.wheel_used = true;
}

function inp_wheel() {
    if (global.inp.wheel_used) return 0;
    if (global.inp.wheel_up) return -1;
    if (global.inp.wheel_down) return 1;
    return 0;
}

function inp_use_wheel() {
    global.inp.wheel_used = true;
}

function inp_slot_pressed() {
    for (var i = 0; i < HOTBAR; i++) {
        if (inp_pressed("s" + string(i + 1))) return i;
    }
    return -1;
}

/// Half-open GUI hit test using the shared logical transform.
function ui_hit(_x, _y, _w, _h) {
    var _in = global.inp;
    if (!_in.in_content) return false;
    return _in.mx >= _x && _in.mx < _x + _w && _in.my >= _y && _in.my < _y + _h;
}

/// True when any activation (confirm, LMB, interact) is still physically held.
function inp_activation_held() {
    return global.inp.down[$ "confirm"] || global.inp.down[$ "lmb"] || global.inp.down[$ "interact"];
}
