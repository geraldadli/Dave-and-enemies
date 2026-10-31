"""Original seeded procedural SFX and nonverbal text blips from the cue sheet.

Requires NumPy and SciPy. No downloaded samples, speech model or API.
Does not import sounds into GameMaker or implement any playback behaviour.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import wave
import zipfile
from pathlib import Path

import numpy as np
from scipy import fft, signal

ROOT = Path(__file__).resolve().parents[1]
SR = 44100
TAU = 2 * np.pi
SPEC = ROOT / "docs/audio/AUDIO_MANIFEST.json"


def seed_for(name):
    return int.from_bytes(hashlib.sha256(name.encode()).digest()[:4], "little")


def db(x):
    return float(20 * np.log10(max(float(x), 1e-15)))


class Sound:
    def __init__(self, duration, seed, loop=False):
        self.n = round(duration * SR)
        self.d = self.n / SR
        self.t = np.arange(self.n) / SR
        self.rng = np.random.default_rng(seed)
        self.loop = loop
        self.y = np.zeros(self.n)
        self.tuning = self.rng.uniform(.98, 1.02)

    def band(self, low=100, high=7000):
        low, high = max(20, low), min(18000, high)
        sos = signal.butter(2, [low, high], btype="bandpass", fs=SR, output="sos")
        raw = self.rng.standard_normal(self.n)
        if self.loop:
            f = fft.rfftfreq(self.n, 1 / SR)
            _, h = signal.sosfreqz(sos, worN=f, fs=SR)
            y = fft.irfft(fft.rfft(raw) * h, n=self.n)
        else:
            y = signal.sosfilt(sos, raw)
        return y / max(np.std(y), 1e-8)

    def envelope(self, at, length, decay=4, attack=.002):
        u = self.t - at
        v = np.clip(u / max(length, 1 / SR), 0, 1)
        env = np.exp(-decay * v) * np.minimum(1, np.maximum(u, 0) / max(attack, 1 / SR))
        end = min(.004, length / 5)
        env *= np.minimum(1, np.maximum(at + length - self.t, 0) / end)
        return env * ((u >= 0) & (u < length))

    def noise(self, amp=.1, low=100, high=5000, at=0, length=None, decay=4, attack=.003):
        length = self.d - at if length is None else length
        self.y += amp * self.band(low, high) * self.envelope(at, length, decay, attack)

    def modes(self, freq=240, amp=.15, at=0, length=None, material="wood", decay=6):
        length = self.d - at if length is None else length
        u = self.t - at
        ratios = {"wood": [1, 1.58, 2.37, 3.92], "bone": [1, 1.73, 2.81, 4.14],
                  "metal": [1, 2.13, 3.41, 5.23], "soft": [1, 2, 3]}[material]
        for k, ratio in enumerate(ratios):
            f = freq * self.tuning * ratio
            if f < 17000:
                self.y += amp / (1 + k) ** 1.25 * np.sin(TAU * f * u) * self.envelope(at, length, decay + k * 1.5, .001)

    def thump(self, freq=125, amp=.25, at=0, length=None):
        length = self.d - at if length is None else length
        u = np.maximum(self.t - at, 0)
        phase = TAU * freq * self.tuning * (u + .4 * .013 * (1 - np.exp(-u / .013)))
        self.y += amp * (np.sin(phase) + .2 * np.sin(phase * 2)) * self.envelope(at, length, 5, .002)
        self.noise(amp * .1, 250, 2600, at, min(length, .04), 5, .001)

    def scrape(self, amp=.1, low=300, high=4500, at=0, length=None, rise=False, texture=22):
        length = self.d - at if length is None else length
        u = np.clip((self.t - at) / length, 0, 1)
        rough = .55 + .25 * np.sin(TAU * (texture * self.t + .8 * np.sin(TAU * 7.3 * self.t)))
        env = self.envelope(at, length, 2.6, .006)
        if rise:
            env *= .35 + 2.6 * u
        self.y += amp * self.band(low, high) * rough * env

    def whoosh(self, amp=.14, at=0, length=None, dark=False, reverse=False):
        length = self.d - at if length is None else length
        u = np.clip((self.t - at) / length, 0, 1)
        curve = (1 - u) if reverse else u
        env = (np.sin(np.pi * u) ** .8 + .08 * np.exp(-u * 5))
        env *= self.envelope(at, length, 1.2, .002)
        low = self.band(100 if dark else 350, 1800 if dark else 3600)
        high = self.band(900 if dark else 2200, 5000 if dark else 8000)
        self.y += amp * ((1 - curve) * low + .5 * curve * high) * env

    def creak(self, amp=.08, freq=230, at=0, length=None):
        length = self.d - at if length is None else length
        u = np.maximum(self.t - at, 0)
        f = freq * self.tuning * (1 + .06 * np.sin(TAU * 9 * u) + .015 * np.sin(TAU * 47 * u))
        phase = TAU * np.cumsum(f) / SR
        grain = .35 + .65 * (np.sin(TAU * (28 * u + 16 * u**2)) ** 8)
        self.y += amp * (np.sin(phase) + .25 * np.sin(3 * phase)) * grain * self.envelope(at, length, 3, .004)

    def scatter(self, amp=.05, count=10, at=0, length=None, material="bone", freq=600):
        length = self.d - at if length is None else length
        positions = np.r_[0, np.sort(self.rng.uniform(.02, .9, max(count - 1, 0)))]
        for u in positions:
            start = at + u * length
            tail = min(length * (1 - u), self.rng.uniform(.025, .09))
            self.modes(freq * self.rng.uniform(.7, 1.35), amp * (1 - .75 * u), start, tail, material)
        self.scrape(amp * .35, 700, 5500, at, length)

    def pluck(self, freq, amp=.1, at=0, length=None, decay=5):
        length = self.d - at if length is None else length
        u = self.t - at
        for h, weight in [(1, 1), (2, .24), (3, .08)]:
            self.y += amp * weight * np.sin(TAU * freq * h * u) * self.envelope(at, length, decay + h * .4, .002)

    def chime(self, notes, offsets=None, amp=.12):
        offsets = offsets or np.linspace(0, self.d * .45, len(notes))
        for note, at in zip(notes, offsets):
            freq = 440 * 2 ** ((note - 69) / 12)
            self.pluck(freq, amp, float(at), self.d - float(at), 5)
            self.modes(freq * 2, amp * .12, float(at), self.d - float(at), "soft", 7)
        self.noise(amp * .035, 1300, 6200, length=self.d, decay=4)

    def murmur(self, kind="dave", amp=.2, at=0, length=None, pitch=None, tilt=0):
        length = self.d - at if length is None else length
        u = np.maximum(self.t - at, 0)
        default, formants = {"dave": (145, [(260, 100, 1.2), (950, 280, .35), (1900, 450, .18)]),
                             "pharaoh": (88, [(180, 90, .8), (560, 150, .8), (1350, 300, .35)]),
                             "grunt": (125, [(380, 160, 1), (1000, 300, .45), (2100, 450, .18)])}[kind]
        f0 = (pitch or default) * self.rng.uniform(.985, 1.015)
        jitter = .003 * np.sin(TAU * 31 * self.t) + .0015 * np.sin(TAU * 67 * self.t)
        phase = TAU * np.cumsum(f0 * (1 + jitter + tilt * u / length)) / SR
        y = np.zeros(self.n)
        for h in range(1, min(65, int(7500 / f0))):
            frequency = h * f0
            colour = .16 + sum(weight * np.exp(-.5 * ((frequency - center * self.tuning) / width) ** 2)
                                for center, width, weight in formants)
            y += colour / h ** 1.35 * np.sin(h * phase + .02 * h)
        if kind == "pharaoh":
            y += .022 * self.band(450, 2500) * (.5 + .5 * np.sin(phase / 2))
        else:
            y += .012 * self.band(500, 4200)
        env = self.envelope(at, length, .8, min(.008, length * .1))
        env *= np.minimum(1, np.maximum(length - u, 0) / min(.012, length * .18))
        self.y += amp * y * env


def periodic(asset, p):
    t, d = p.t, p.d
    if asset == "snd_wind_loop":
        slow = .63 + .22 * np.sin(TAU * 4 * t / d - .7) + .1 * np.sin(TAU * 7 * t / d)
        return p.band(70, 2400) * slow + .13 * p.band(2300, 6600) * (.6 + .4 * np.sin(TAU * 11 * t / d) ** 2)
    if asset == "snd_worm_rumble":
        grind = p.band(95, 850)
        return .7 * grind * (.7 + .3 * np.sin(TAU * 2 * t / d) ** 2) + .15 * p.band(450, 2200)
    if asset == "snd_magic_travel":
        f = round(128 * d) / d
        phase = TAU * f * t + .35 * np.sin(TAU * 4 * t / d)
        return (np.sin(phase) + .23 * np.sin(3 * phase)) * (.8 + .15 * np.sin(TAU * 5 * t / d)) + .06 * p.band(500, 2200)
    if asset == "snd_laser_charge":
        f = round(190 * d) / d
        phase = TAU * f * t + .5 * np.sin(TAU * 7 * t / d)
        return (np.sin(phase) + .32 * np.sin(2 * phase) + .15 * np.sin(5 * phase)) * (.82 + .16 * np.sin(TAU * 3 * t / d)) + .07 * p.band(400, 2600)
    if asset == "snd_laser_fire":
        f = round(180 * d) / d
        phase = TAU * f * t + 1.1 * np.sin(TAU * 19 * t / d)
        core = np.tanh(1.6 * (np.sin(phase) + .24 * np.sin(3 * phase)))
        return core + .1 * p.band(700, 4200) * (.6 + .4 * np.sin(TAU * 37 * t / d) ** 2)
    raise KeyError(asset)


def recipe(asset, p):
    """Every non-loop stable ID must have an intentional recipe; no fallback."""
    d, t = p.d, p.t
    if asset.startswith("snd_voice_dave_"):
        take = int(asset[-1])
        p.murmur("dave", .3, pitch=145, tilt=[-.025, -.01, .025, 0][take-1])
    elif asset.startswith("snd_voice_pharaoh_"):
        take = int(asset[-1])
        p.murmur("pharaoh", .32, pitch=88, tilt=[-.02, -.04, 0, -.015][take-1])
    elif asset.startswith("snd_voice_narrator_"):
        take = int(asset[-1])
        p.noise(.15, 400, 3200 + take * 180, decay=3, attack=.003)
        p.modes(270 + take*13, .035, material="wood", decay=5)
    elif asset == "snd_intro_grit":
        p.scatter(.11, 6, material="wood", freq=540)
        p.scrape(.05, 800, 4500)
    elif asset == "snd_intro_banner":
        p.whoosh(.17, dark=True)
        p.scrape(.09, 400, 4400, texture=12)
    elif asset == "snd_sword_swing":
        p.whoosh(.24)
        p.creak(.018, 260, length=d*.28)
    elif asset == "snd_sword_hit":
        p.modes(1150, .1, material="metal", decay=12)
        p.thump(170, .25)
        p.noise(.13, 850, 6200, decay=7, attack=.001)
    elif asset == "snd_sword_hit_bone":
        p.scatter(.14, 6, material="bone", freq=900)
        p.noise(.055, 900, 4500, decay=6)
    elif asset == "snd_sword_hit_armor":
        p.modes(740, .23, material="metal", decay=5.5)
        p.noise(.035, 1200, 5800, decay=9)
    elif asset == "snd_hurt":
        p.murmur("grunt", .34, pitch=133, tilt=-.09)
        p.thump(155, .14, length=d*.65)
        p.scrape(.035, 300, 3300)
    elif asset == "snd_player_defeated":
        p.murmur("grunt", .24, length=d*.55, pitch=120, tilt=-.12)
        p.noise(.045, 250, 2500, decay=3)
        p.modes(350, .09, .38, d-.38, "metal")
        p.scatter(.025, 4, .5, d-.5, "metal", 600)
    elif asset == "snd_potion_drink":
        p.pluck(470, .14, length=.1)
        p.modes(160, .16, .12, d-.12, "soft", 5)
        u = np.maximum(t-.13, 0)
        phase = TAU * (170*u + 70*u*u + .4*np.sin(TAU*9*u))
        p.y += .06*np.sin(phase)*p.envelope(.13, d-.13, 3, .008)
        p.noise(.025, 400, 2200, decay=3)
    elif asset == "snd_heal":
        p.chime([72, 76, 79], [0, .13, .27], .16)
        p.noise(.025, 900, 4500, decay=3)
    elif asset == "snd_step_sand":
        p.thump(95, .13)
        p.scrape(.21, 500, 5200, texture=30)
        p.scatter(.028, 7, material="bone", freq=1000)
    elif asset == "snd_step_stone":
        p.thump(175, .17)
        p.modes(460, .10, material="wood")
        p.noise(.07, 800, 5200, decay=5)
    elif asset == "snd_step_wood":
        p.modes(155, .2, material="wood", decay=4)
        p.thump(100, .13)
        p.creak(.018, 290)
    elif asset == "snd_undead_attack":
        p.creak(.12, 155)
        p.scrape(.08, 250, 3300)
        p.whoosh(.06, at=d*.25, length=d*.75, dark=True)
    elif asset == "snd_undead_move":
        p.scrape(.21, 250, 3700, texture=16)
        p.modes(245, .04, .02, d-.02, "bone")
    elif asset == "snd_undead_death":
        p.scatter(.13, 13, material="bone", freq=510)
        p.scrape(.1, 280, 3200)
        p.thump(120, .07)
    elif asset == "snd_undead_rise":
        p.scrape(.16, 170, 4200, rise=True, texture=28)
        p.scatter(.07, 10, material="wood", freq=370)
        p.creak(.045, 185, at=d*.25, length=d*.75)
    elif asset == "snd_skeleton_warrior_attack":
        p.modes(720, .12, length=d*.3, material="bone")
        p.whoosh(.14, at=.025, length=d-.025)
    elif asset == "snd_skeleton_warrior_move":
        p.modes(450, .12, material="bone")
        p.modes(770, .035, .026, d-.026, "bone")
        p.scrape(.08, 600, 4000)
    elif asset == "snd_skeleton_warrior_death":
        p.scatter(.16, 14, material="bone", freq=630)
        p.modes(570, .08, .3, d-.3, "metal")
    elif asset == "snd_skeleton_archer_move":
        p.modes(680, .075, material="bone")
        p.modes(1100, .025, .035, d-.035, "wood")
        p.scrape(.07, 750, 4200)
    elif asset == "snd_skeleton_archer_death":
        p.scatter(.12, 10, material="bone", freq=800)
        p.modes(310, .10, .1, d-.1, "wood")
        p.modes(1100, .03, .44, d-.44, "wood")
    elif asset == "snd_bow_draw":
        p.creak(.15, 145)
        p.scrape(.045, 450, 2900, rise=True, texture=19)
        p.modes(830, .035, length=.075, material="wood")
    elif asset == "snd_bow_release":
        p.pluck(245*p.tuning, .19, decay=6)
        p.noise(.08, 1500, 6500, decay=10, attack=.001)
        p.modes(180, .08, material="wood")
    elif asset == "snd_arrow_travel":
        p.whoosh(.12)
        p.scrape(.035, 2400, 6500, texture=42)
    elif asset == "snd_arrow_hit":
        p.thump(170, .17)
        p.modes(510, .10, material="wood")
        p.noise(.06, 1800, 6300, decay=6)
    elif asset == "snd_arrow_hit_world":
        p.modes(570, .16, material="wood", decay=5)
        p.modes(1450, .025, material="soft", decay=7)
        p.scrape(.06, 850, 5100)
    elif asset == "snd_bandit_attack":
        p.whoosh(.18)
        p.murmur("grunt", .045, length=d*.3, pitch=155)
        p.creak(.025, 320, length=d*.4)
    elif asset == "snd_bandit_move":
        p.thump(130, .09)
        p.scrape(.16, 700, 4600, texture=24)
        p.noise(.025, 300, 2600, decay=3)
    elif asset == "snd_bandit_death":
        p.murmur("grunt", .15, length=d*.55, pitch=135, tilt=-.1)
        p.scrape(.13, 250, 3500)
        p.modes(540, .045, d*.3, d*.7, "metal")
    elif asset == "snd_bandit_caster_move":
        p.scrape(.13, 350, 3500, texture=12)
        p.modes(280, .09, material="wood")
    elif asset == "snd_bandit_caster_death":
        p.murmur("grunt", .11, length=d*.5, pitch=123, tilt=-.07)
        p.scrape(.11, 250, 3400)
        p.modes(250, .14, d*.2, d*.8, "wood")
        p.noise(.018, 1200, 4200, d*.6, d*.4, 4)
    elif asset == "snd_cast_charge":
        phase = TAU * (225*t + 95*t*t/d + .16*np.sin(TAU*13*t))
        p.y += .17*(np.sin(phase)+.22*np.sin(3*phase))*p.envelope(0,d,.3,.006)*(.55+t/d)
        p.noise(.035, 600, 2800, decay=1)
    elif asset == "snd_magic_launch":
        p.pluck(370*p.tuning, .2, decay=5)
        p.whoosh(.08, dark=True, reverse=True)
        p.noise(.03, 1800, 6500, decay=6)
    elif asset == "snd_magic_hit":
        p.modes(615, .18, material="soft", decay=5)
        p.thump(195, .10)
        p.scatter(.026, 6, material="soft", freq=1600)
        p.noise(.035, 1300, 6200, decay=3)
    elif asset == "snd_bat_fly":
        p.whoosh(.14, dark=True)
        p.scrape(.04, 750, 4900, texture=15)
    elif asset == "snd_bat_screech":
        phase = TAU*(1300*t + 900*t*t - 1500*t**3 + .35*np.sin(TAU*34*t))
        pair = .45+.55*np.sin(np.pi*np.clip(t/d*2,0,2))**2
        p.y += .13*(np.sin(phase)+.2*np.sin(2*phase))*pair*p.envelope(0,d,2,.006)
        p.noise(.024, 1400, 4500, decay=3)
    elif asset == "snd_bat_dive":
        p.whoosh(.17, dark=True)
        p.creak(.028, 500, length=d*.3)
    elif asset == "snd_bat_defeat":
        phase = TAU*(1100*t - 350*t*t/d)
        p.y += .08*np.sin(phase)*p.envelope(0,d*.6,4,.008)
        p.scrape(.09, 650, 3500)
        p.scatter(.02, 5, material="wood", freq=600)
    elif asset == "snd_python_move":
        p.scrape(.17, 450, 3600, texture=14)
        p.scatter(.018, 6, material="bone", freq=1050)
    elif asset == "snd_snake_hiss":
        p.noise(.19, 800, 4900, decay=1, attack=.005)
        p.y *= .7+.3*(t/d)
    elif asset == "snd_snake_lunge":
        p.whoosh(.18, dark=True)
        p.modes(330, .085, .025, d-.025, "wood")
        p.scrape(.04, 800, 4200)
    elif asset == "snd_python_death":
        p.scrape(.16, 400, 3300, texture=9)
        p.noise(.07, 150, 2200, decay=3, attack=.012)
        p.thump(110, .06)
    elif asset == "snd_worm_emerge":
        p.thump(115, .28)
        p.noise(.18, 180, 4200, decay=4)
        p.scatter(.055, 17, material="wood", freq=460)
    elif asset == "snd_worm_bite":
        p.whoosh(.16, dark=True)
        p.modes(170, .2, length=d*.75, material="wood")
        p.scrape(.08, 350, 3600)
    elif asset == "snd_worm_burrow":
        p.whoosh(.16, dark=True, reverse=True)
        p.scrape(.18, 180, 3000, texture=15)
        p.scatter(.024, 11, material="wood", freq=300)
    elif asset == "snd_sandworm_death":
        p.thump(90, .22)
        p.noise(.10, 100, 1400, decay=3, attack=.01)
        p.scrape(.16, 250, 3200, texture=11)
        p.scatter(.035, 15, material="wood", freq=330)
    elif asset == "snd_enemy_melee_hit":
        p.thump(160, .23)
        p.noise(.085, 250, 2600, decay=5)
    elif asset == "snd_boss_summon":
        p.modes(145, .15, material="metal", decay=4)
        p.whoosh(.13, dark=True, reverse=True)
        p.scrape(.10, 350, 4100, rise=True, texture=17)
        p.thump(180, .10, d*.65, d*.35)
    elif asset == "snd_boss_bat_spawn":
        p.noise(.08, 450, 4100, decay=4)
        p.whoosh(.10, dark=True)
        p.creak(.025, 520, length=d*.45)
    elif asset == "snd_summon_crack":
        p.scatter(.13, 10, material="wood", freq=380)
        p.scrape(.08, 650, 3900)
    elif asset == "snd_laser_hit":
        p.thump(195, .17)
        p.noise(.12, 950, 5300, decay=7, attack=.001)
        p.pluck(620*p.tuning, .07, decay=7)
    elif asset == "snd_thunder_warn":
        p.modes(690, .15, material="soft", decay=8)
        p.modes(690, .13, .12, d-.12, "soft", 6)
        p.noise(.023, 700, 2400, decay=3)
    elif asset == "snd_thunder_strike":
        p.noise(.3, 1200, 7800, length=.075, decay=8, attack=.001)
        p.thump(115, .32)
        p.noise(.11, 160, 2500, decay=4)
        p.noise(.05, 600, 4300, .09, d-.09, 5)
        p.noise(.03, 500, 3200, .16, d-.16, 5)
    elif asset == "snd_boss_float":
        p.whoosh(.12, dark=True)
        p.modes(145, .035, material="soft", decay=3)
        p.scrape(.05, 300, 2800, texture=10)
    elif asset == "snd_boss_teleport_out":
        p.whoosh(.15, dark=True, reverse=True)
        phase = TAU*(240*t - 90*t*t/d)
        p.y += .08*np.sin(phase)*p.envelope(0,d,2,.006)
        p.scrape(.05, 500, 4200, rise=True)
    elif asset == "snd_boss_teleport_in":
        p.thump(155, .15)
        p.modes(285, .1, material="metal", decay=6)
        p.scrape(.1, 650, 4300)
    elif asset == "snd_boss_hurt":
        p.murmur("pharaoh", .32, pitch=81, tilt=-.06)
        p.scrape(.045, 450, 3100, texture=20)
    elif asset == "snd_boss_death":
        p.thump(95, .38)
        p.modes(205, .17, material="metal", decay=7)
        p.noise(.16, 220, 4200, decay=5)
        p.scatter(.035, 12, material="metal", freq=650)
    elif asset == "snd_disintegrate":
        p.scatter(.10, 36, material="bone", freq=880)
        p.scrape(.11, 450, 4700, texture=24)
        p.noise(.07, 650, 4400, decay=2.8, attack=.004)
        p.y *= .3+.7*np.exp(-t/d*2)
    elif asset == "snd_chest_open":
        p.modes(780, .12, length=.12, material="metal")
        p.creak(.13, 210, .025, d-.025)
        p.scrape(.065, 250, 3400)
        p.modes(175, .13, d*.72, d*.28, "wood")
    elif asset == "snd_chest_locked":
        p.creak(.075, 280)
        p.modes(650, .11, material="metal", decay=7)
        p.modes(240, .1, .07, d-.07, "wood")
    elif asset == "snd_pickup":
        p.pluck(690*p.tuning, .14)
        phase = TAU*(880*t + 220*t*t/d)
        p.y += .024*np.sin(phase)*p.envelope(0,d,3,.005)
        p.noise(.01, 1600, 5500, decay=4)
    elif asset == "snd_coin":
        p.modes(1450, .12, material="metal", decay=7)
        p.modes(1800, .08, .055, d-.055, "metal", 7)
        p.scrape(.025, 400, 2800)
    elif asset == "snd_levelup":
        p.chime([72, 76, 79, 84], [0, .13, .26, .4], .17)
        p.thump(130, .06)
    elif asset == "snd_checkpoint":
        p.chime([72, 79, 76], [0, .13, .26], .14)
        p.noise(.012, 1400, 5000, decay=3)
    elif asset == "snd_save":
        p.chime([72, 84], [0, .16], .14)
        p.modes(330, .07, .32, d-.32, "wood", 6)
    elif asset == "snd_ui_error":
        p.modes(270, .13, material="wood", decay=7)
        p.modes(235, .11, .08, d-.08, "wood", 6)
    elif asset == "snd_inventory_open":
        p.scrape(.15, 300, 3600, texture=12)
        p.creak(.04, 240)
        p.modes(500, .045, length=d*.45, material="wood")
    elif asset == "snd_inventory_close":
        p.scrape(.12, 240, 2900, texture=9)
        p.modes(175, .1, material="wood", decay=5)
    elif asset == "snd_ui_move":
        p.modes(330, .15, material="wood", decay=5)
        p.noise(.012, 450, 1900, decay=6)
    elif asset == "snd_ui_confirm":
        p.pluck(310, .13, decay=5)
        p.pluck(440, .11, .045, d-.045, 5)
    elif asset == "snd_ui_cancel":
        p.modes(190, .1, material="wood", decay=5)
        p.pluck(145, .07, .035, d-.035, 4)
    elif asset == "snd_gate_open":
        p.scrape(.18, 130, 3400, texture=17)
        p.creak(.06, 135)
        p.scatter(.035, 9, material="metal", freq=420)
        p.thump(110, .11, d*.8, d*.2)
    elif asset == "snd_gate_slam":
        p.scrape(.13, 140, 3200, texture=21)
        p.thump(105, .27, d*.55, d*.45)
        p.modes(280, .12, d*.55, d*.45, "metal", 6)
        p.scatter(.04, 10, material="wood", freq=400)
    else:
        raise KeyError(f"No designed synthesis recipe for {asset}")
    return p.y


def filtered_finish(y, loop):
    sos = signal.butter(2, [40, 12000], btype="bandpass", fs=SR, output="sos")
    if loop:
        f = fft.rfftfreq(len(y), 1 / SR)
        _, h = signal.sosfreqz(sos, worN=f, fs=SR)
        y = fft.irfft(fft.rfft(y) * h, n=len(y))
        y -= y.mean()
    else:
        y = signal.sosfilt(sos, y)
        width = min(round(.0025 * SR), len(y) // 6)
        window = np.ones(len(y))
        window[:width] = np.sin(np.linspace(0, np.pi / 2, width)) ** 2
        window[-width:] = window[:width][::-1]
        y *= window
        y -= y.mean() / window.mean() * window
    return y


def target_peak(asset):
    name = asset["id"]
    if name.startswith("snd_voice_narrator"):
        return -18
    if name.startswith("snd_voice_dave"):
        return -9
    if name.startswith("snd_voice_pharaoh"):
        return -9
    if asset["group"] == "UI":
        return -15 if name == "snd_ui_move" else -11
    if name in ("snd_wind_loop", "snd_boss_float"):
        return -12
    if name.endswith("_move") or name in ("snd_step_sand", "snd_step_stone", "snd_step_wood", "snd_bat_fly", "snd_arrow_travel"):
        return -9
    if name in ("snd_thunder_warn", "snd_laser_charge", "snd_sword_hit", "snd_boss_death", "snd_thunder_strike"):
        return -3
    return -6


def write_pcm(path, y, seed):
    rng = np.random.default_rng(seed)
    y = y + (rng.random(len(y)) - rng.random(len(y))) / 65536
    pcm = np.clip(np.rint(y * 32768), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())


def read_pcm(path):
    with wave.open(str(path), "rb") as f:
        assert f.getnchannels() == 1 and f.getsampwidth() == 2 and f.getframerate() == SR
        assert f.getcomptype() == "NONE"
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(float) / 32768


def inspect(path, asset):
    y = read_pcm(path)
    assert len(y) == round(asset["duration_seconds_per_file"] * SR)
    assert np.isfinite(y).all() and np.sqrt(np.mean(y*y)) > .0001
    oversampled = signal.resample_poly(np.tile(y, 3) if asset["loop"]["enabled"] else y, 4, 1)
    if asset["loop"]["enabled"]:
        oversampled = oversampled[len(y)*4:len(y)*8]
    peak, reconstructed = db(np.max(np.abs(y))), db(np.max(np.abs(oversampled)))
    assert peak <= -1 and reconstructed <= -1, (path, peak, reconstructed)
    assert abs(y.mean()) < .0001, (path, y.mean())
    threshold = np.max(np.abs(y)) * .001
    active = np.flatnonzero(np.abs(y) >= threshold)
    onset_ms = active[0] * 1000 / SR
    trail_ms = (len(y) - 1 - active[-1]) * 1000 / SR
    if not asset["loop"]["enabled"]:
        assert onset_ms <= 15, (path, "leading dead air", onset_ms)
        assert trail_ms <= 30, (path, "trailing dead air", trail_ms)
    result = {"sample_peak_dbfs": round(peak, 5), "oversampled_peak_dbfs_4x": round(reconstructed, 5),
              "peak_measurement": "SciPy 4x polyphase oversampling; not an integrated LUFS target",
              "rms_dbfs": round(db(np.sqrt(np.mean(y*y))), 5), "dc_offset": float(y.mean()),
              "onset_ms_at_minus60_relative": round(onset_ms, 3),
              "trailing_ms_below_minus60_relative": round(trail_ms, 3)}
    if asset["loop"]["enabled"]:
        seam = float(abs(y[0] - y[-1]))
        reference = float(np.quantile(np.abs(np.diff(y)), .999))
        assert seam <= reference, (path, "seam", seam, reference)
        result["loop_boundary"] = {"jump": seam, "ordinary_step_99_9_percentile": reference,
                                    "seam_within_ordinary_step_range": True,
                                    "design": "Periodic oscillators, modulation and circular noise/filtering; no baked fades or padding."}
    return result


def render_asset(asset):
    folder = ROOT / "audio" / ("voice" if asset["group"] == "Text" else "sfx")
    folder.mkdir(parents=True, exist_ok=True)
    signals = []
    for name in asset["planned_filenames"]:
        p = Sound(asset["duration_seconds_per_file"], seed_for(name), asset["loop"]["enabled"])
        y = periodic(asset["id"], p) if p.loop else recipe(asset["id"], p)
        y = filtered_finish(y, p.loop)
        assert np.max(np.abs(y)) > .00001, asset["id"]
        # Match takes by RMS, then apply one common family gain. Never bake
        # the cue sheet's proposed playback gain into the source WAV.
        y /= np.sqrt(np.mean(y*y))
        signals.append(y)
    maximum = max(float(np.max(np.abs(y))) for y in signals)
    gain = 10 ** (target_peak(asset) / 20) / maximum
    reports = []
    for name, y in zip(asset["planned_filenames"], signals):
        path = folder / name
        write_pcm(path, y * gain, seed_for(name) + 11)
        measurements = inspect(path, asset)
        reports.append({"file": name, "path": path.relative_to(ROOT).as_posix(),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "bytes": path.stat().st_size, "frames": len(y), "duration_seconds": len(y) / SR,
                        "seed": seed_for(name), "measurements": measurements})
    assert len({r["sha256"] for r in reports}) == asset["variation_count"]
    rms_range = max(r["measurements"]["rms_dbfs"] for r in reports) - min(r["measurements"]["rms_dbfs"] for r in reports)
    assert rms_range < .02
    metadata = {"asset_id": asset["id"], "purpose": asset["purpose"],
                "status": "GENERATED_TECHNICALLY_VALIDATED", "channels": 1,
                "sample_rate_hz": SR, "bits_per_sample": 16,
                "encoding": "PCM signed 16-bit little-endian WAV",
                "duration_seconds": asset["duration_seconds_per_file"],
                "actual_duration_seconds": reports[0]["duration_seconds"],
                "variation_count": len(reports), "files": reports,
                "loop_start": 0 if asset["loop"]["enabled"] else None,
                "loop_end": reports[0]["duration_seconds"] if asset["loop"]["enabled"] else None,
                "loop_start_frame_inclusive": 0 if asset["loop"]["enabled"] else None,
                "loop_end_frame_exclusive": reports[0]["frames"] if asset["loop"]["enabled"] else None,
                "source": "tools/render_chapter_sfx.py", "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "generation": "Original seeded Python physical-inspired, granular, modal, filtered-noise and formant synthesis; no recordings, extracted samples, cloned voices, words or speech API.",
                "generation_or_recording_prompt": asset["generation_or_recording_prompt"],
                "variant_rms_range_db": round(rms_range, 5),
                "playback_gain_baked_in": False,
                "auditory_review": "Human listening review pending; objective validation passed.",
                "game_integration": "Not imported; Claude owns playback, looping, mixing and event triggers."}
    (folder / f"{asset['id']}.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Render one stable ID instead of all SFX and blips")
    args = parser.parse_args()
    assets = json.loads(SPEC.read_text(encoding="utf-8"))["assets"]
    assets = [a for a in assets if a["id"].startswith("snd_") and (not args.id or a["id"] == args.id)]
    if not assets:
        raise ValueError("No matching SFX ID")
    count = 0
    for i, asset in enumerate(assets):
        report = render_asset(asset)
        count += len(report["files"])
        print(f"{i+1}/{len(assets)} {asset['id']}: {len(report['files'])} WAV(s) validated", flush=True)
    print(json.dumps({"production_ids": len(assets), "production_wavs": count,
                      "format": "Mono PCM16 44100 Hz", "human_listening_review": "Pending"}), flush=True)


if __name__ == "__main__":
    main()
