"""Original deterministic music composition/synthesis; no samples or API calls.

Requires numpy, scipy, soundfile, imageio-ffmpeg. Run from any directory:
    python tools/render_chapter_music.py
Writes only audio/music/ and a temporary float WAV which it removes after metering.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import wave
from dataclasses import asdict, dataclass
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from scipy import fft, signal

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audio" / "music"
SR = 44100
SCALE = {0, 1, 4, 5, 7, 8, 11}
TWOPI = 2 * np.pi


def midi(name: str) -> int:
    match = re.fullmatch(r"([A-G])(b?)([0-8])", name)
    assert match, name
    letter, flat, octave = match.groups()
    return 12 * (int(octave) + 1) + {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[letter] - bool(flat)


def hz(note: int) -> float:
    return 440 * 2 ** ((note - 69) / 12)


@dataclass
class Event:
    instrument: str
    beat: float
    note: int | None
    gate_beats: float
    velocity: float
    pan: float
    seed: int


class Score:
    def __init__(self, asset_id: str, bpm: int, bars: int, seed: int):
        self.id, self.bpm, self.bars = asset_id, bpm, bars
        self.beat_seconds = 60 / bpm
        self.seconds = bars * 4 * self.beat_seconds
        self.frames = round(self.seconds * SR)
        self.events: list[Event] = []
        self.rng = np.random.default_rng(seed)
        self.seed = seed

    def put(self, inst, beat, note=None, gate=.5, vel=.1, pan=0, humanize=True):
        if isinstance(note, str):
            note = midi(note)
        if note is not None:
            assert note % 12 in SCALE, (inst, note)
        # Very small performance variation, without changing the tempo grid.
        offset = self.rng.uniform(-.005, .005) / self.beat_seconds if humanize else 0
        self.events.append(Event(inst, beat + offset, note, gate,
                                 vel * self.rng.uniform(.94, 1.06),
                                 float(np.clip(pan + self.rng.uniform(-.025, .025), -.9, .9)),
                                 int(self.rng.integers(1, 2**31))))

    def phrase(self, start_bar, bars, inst="flute", octave=0, vel=.15, pan=.08):
        for bar, notes in enumerate(bars):
            at = 0
            for note, beats in notes:
                if note is not None:
                    self.put(inst, (start_bar + bar) * 4 + at,
                             midi(note) + octave, beats * .86, vel, pan)
                at += beats
            assert abs(at - 4) < 1e-8, (bar, at)


DUNE = [
    [("C4", 1), ("Db4", .5), ("E4", .5), ("G4", 1), ("F4", 1)],
    [("E4", 1), ("Db4", .5), ("C4", .5), ("B3", 1), ("C4", 1)],
    [("G4", 1), ("Ab4", .5), ("B4", .5), ("C5", 1), ("G4", 1)],
    [("F4", 1), ("E4", 1), ("Db4", 1), ("C4", 1)],
]
DUNE_ANSWER = [
    [(None, 1), ("G4", 1), ("F4", .5), ("E4", .5), ("Db4", 1)],
    [("C4", 1.5), (None, .5), ("E4", 1), ("G4", 1)],
    [("Ab4", 1), ("G4", .5), ("F4", .5), ("E4", 1), ("Db4", 1)],
    [("B3", 1), ("C4", 2), (None, 1)],
]
PHARAOH = [
    [("C3", 1.5), ("Db3", .5), ("G3", 1), ("E3", 1)],
    [("B2", .5), ("C3", .5), ("Ab3", 1), ("G3", 1), (None, 1)],
]
PHARAOH_ANSWER = [
    [("Ab3", .5), ("G3", .5), ("E3", 1), ("Db3", 1), ("C3", 1)],
    [("G3", .75), ("E3", .25), ("Db3", .5), ("C3", .5), ("B2", 1), (None, 1)],
]


def compose_desert() -> Score:
    s = Score("mus_desert", 80, 32, 63107)
    chords = [
        ["C3", "E3", "G3", "C4"], ["C3", "G3", "C4", "E4"],
        ["Db3", "F3", "Ab3", "Db4"], ["C3", "E3", "G3", "B3"],
        ["F3", "Ab3", "C4", "F4"], ["C3", "G3", "C4", "E4"],
        ["G3", "B3", "G4", "Db4"], ["C3", "E3", "G3", "C4"],
    ]
    for bar in range(32):
        b, local, section = bar * 4, bar % 8, bar // 8
        chord = chords[local]
        # Restrained plucked accompaniment, alternating left/right answers.
        positions = [0, 1.5, 2.5, 3.25] if bar < 30 else [0, 2.5]
        for k, beat in enumerate(positions):
            s.put("oud", b + beat, chord[k % len(chord)], .8,
                  .095 if section != 2 else .08, -.33 if k % 2 == 0 else .25)
        if local in (1, 5) and bar < 30:
            for k, note in enumerate(chord[1:]):
                s.put("oud", b + 3.5 + .06 * k, note, .5, .045, .4)
        root = "Db2" if local == 2 else "F2" if local == 4 else "G2" if local == 6 else "C2"
        s.put("bass", b, root, 1.75, .105, -.03)
        if bar < 30:
            s.put("bass", b + 2.5, "G2" if local not in (2, 4) else root, 1, .055, .03)
        # Soft skin percussion and fingertip patterns, humanised at a fixed tempo.
        s.put("doum", b, None, .5, .105, -.13)
        if local % 2 == 1 and bar < 30:
            s.put("doum", b + 2.75, None, .4, .065, -.09)
        for beat, strength in [(1.5, .045), (3, .055)]:
            if bar < 31:
                s.put("tek", b + beat, None, .2, strength, .2)
        for k in range(8 if bar < 30 else 4):
            s.put("shaker", b + k * .5, None, .13,
                  .012 if k % 2 == 0 else .009, -.45 if k % 2 else .4)
        if local == 7 and bar < 30:
            for beat in [3.25, 3.5, 3.75]:
                s.put("finger", b + beat, None, .1, .022, .12)
    # Long quiet harmonic swells, no unwindowed oscillator at the file boundary.
    for bar in range(0, 32, 4):
        for note, pan in [("C3", -.28), ("G3", .28)]:
            s.put("pad", bar * 4 - .3, note, 13.5, .022, pan, humanize=False)
    s.phrase(0, DUNE, vel=.17)
    s.phrase(4, DUNE_ANSWER, vel=.145)
    s.phrase(8, DUNE, inst="lute_lead", vel=.21, pan=-.12)
    s.phrase(12, DUNE_ANSWER, vel=.14, pan=.18)
    s.phrase(16, DUNE, octave=12, vel=.115, pan=.12)
    s.phrase(20, DUNE_ANSWER, inst="lute_lead", octave=12, vel=.155, pan=-.16)
    s.phrase(24, DUNE, vel=.16)
    s.phrase(28, [DUNE_ANSWER[0], DUNE_ANSWER[1],
                  [("G4", 1.5), ("E4", 1), (None, 1.5)],
                  [("Db4", 1), ("B3", 1), (None, 2)]], vel=.13)
    return s


def compose_pharaoh() -> Score:
    s = Score("mus_pharaoh", 128, 48, 93128)
    chords = [["C3", "E3", "G3"], ["Db3", "F3", "Ab3"],
              ["F3", "Ab3", "C4"], ["G2", "B2", "Db3"]]
    for bar in range(48):
        b, local, section = bar * 4, bar % 8, bar // 16
        final = bar == 47
        chord = chords[[0, 0, 1, 0, 2, 0, 3, 0][local]]
        # 3+3+2 eighth-note accent groups over a firm 4/4 ostinato.
        for beat in ([0, 1.5] if final else [0, 1.5, 3]):
            for j, note in enumerate(chord):
                s.put("bow_stab", b + beat + j * .008, note, .42,
                      .055 + section * .006, -.22 + j * .22)
        bass = ["C2", "G2", "C3", "G2", "C2", "Db2", "E2", "G2"]
        if local == 2:
            bass = ["Db2", "Ab2", "Db3", "Ab2", "Db2", "F2", "Ab2", "F2"]
        elif local == 4:
            bass = ["F2", "C3", "Ab2", "C3", "F2", "Ab2", "C3", "Ab2"]
        elif local == 6:
            bass = ["G2", "B2", "Db3", "B2", "G2", "Db3", "B2", "G2"]
        for k, note in enumerate(bass[:4] if final else bass):
            s.put("bass", b + k * .5, note, .38, .13 if k in (0, 3, 6) else .082, -.04)
        for beat in ([0, 1.5] if final else [0, 1.5, 3]):
            s.put("doum", b + beat, None, .4, .17 + section * .01, -.13)
        for beat in ([] if final else [1, 2.5, 3.5]):
            s.put("tek", b + beat, None, .18, .07 + section * .009, .22)
        subdivisions = 16 if section == 2 and not final else 8
        for k in range(subdivisions if not final else 4):
            s.put("shaker", b + k * (4 / subdivisions), None, .12,
                  (.019 if k % 2 == 0 else .011), -.45 if k % 2 else .45)
        for beat in ([] if final else [.75, 2.75]):
            s.put("finger", b + beat, None, .1, .032, .12)
        if local == 7 and not final:
            for k in range(4):
                s.put("tek", b + 3 + .25 * k, None, .15, .035 + .008 * k, .28)
        if local in (0, 4) and section > 0:
            s.put("metal", b, None, .8, .04 if section == 1 else .055, -.3)
        if section >= 1 and not final:
            # Sparse high counterline leaves the boss hook's quarter-rest intact.
            notes = ["C5", "G4", "E5", "Db5"] if local % 2 == 0 else ["B4", "C5", "Ab4", "G4"]
            for k, pos in enumerate([.5, 1.25, 2.5, 3.25]):
                if local % 4 == 1 and pos >= 3:
                    continue
                s.put("oud", b + pos, notes[k], .4, .065 + .012 * section, -.35)
    for bar in range(0, 48, 4):
        section = bar // 16
        s.phrase(bar, PHARAOH, inst="reed", vel=.14 + section * .012, pan=.05)
        s.phrase(bar + 2, PHARAOH_ANSWER, inst="reed", vel=.12 + section * .01, pan=.06)
        # Warm lower bowed unison retains the exact motif pitches.
        s.phrase(bar, PHARAOH, inst="bow_lead", vel=.075, pan=-.12)
        if section == 2:
            s.phrase(bar, PHARAOH, inst="reed", octave=12, vel=.07, pan=.17)
        if bar % 8 == 0:
            s.phrase(bar, PHARAOH, inst="lute_lead", octave=12, vel=.075, pan=-.2)
    # A low, breathing string bed appears in the second and third sections.
    for bar in range(16, 48, 4):
        for note, pan in [("C3", -.32), ("G3", .32)]:
            s.put("pad", bar * 4 - .2, note, 13.4, .03, pan, humanize=False)
    return s


def shape(n, attack, gate, release, sustain=1):
    t = np.arange(n) / SR
    e = np.ones(n) * sustain
    a = min(round(attack * SR), n)
    if a:
        e[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    off = round(gate * SR)
    if off < n:
        e[off:] *= np.cos(np.linspace(0, np.pi / 2, n - off)) ** 2
    return e


def noise_band(rng, n, lo, hi):
    sos = signal.butter(2, [lo, hi], btype="bandpass", fs=SR, output="sos")
    y = signal.sosfilt(sos, rng.standard_normal(n))
    return y / (np.std(y) + 1e-10)


def voice(inst: str, note: int | None, gate: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    release = {"oud": 1.1, "lute_lead": .7, "flute": .22, "reed": .12,
               "bow_stab": .09, "bow_lead": .16, "bass": .12, "pad": .9}.get(inst, .3)
    if inst in ("doum", "tek", "finger", "shaker", "metal"):
        length = {"doum": .65, "tek": .22, "finger": .12, "shaker": .14, "metal": 1.4}[inst]
    else:
        length = gate + release
    n = round(length * SR)
    t = np.arange(n) / SR
    f = hz(note) if note is not None else 0
    if inst in ("oud", "lute_lead"):
        y = np.zeros(n)
        pick = rng.uniform(.19, .28)
        for k in range(1, min(17, int(18000 / f))):
            partial = f * k * (1 + .00006 * k * k)
            decay = np.exp(-t * (1.5 + .27 * k + (.3 if inst == "oud" else 0)))
            amp = abs(np.sin(np.pi * k * pick)) / k ** 1.18
            y += amp * decay * np.sin(TWOPI * partial * t + .04 * k)
        y += .045 * noise_band(rng, n, 650, 6500) * np.exp(-t / .012)
        y *= shape(n, .004, gate, release)
        y *= 1.5
    elif inst == "flute":
        vib = .0015 * np.sin(TWOPI * 5.15 * t) * (1 - np.exp(-t / .16))
        phase = TWOPI * f * np.cumsum(1 + vib) / SR
        y = np.sin(phase) + .20 * np.sin(2 * phase + .13) + .065 * np.sin(3 * phase)
        air = noise_band(rng, n, 1200, 7500)
        y += .037 * air * (.7 + .3 * np.sin(phase))
        y *= shape(n, .045, gate, release) * (.97 + .03 * np.sin(TWOPI * 3.7 * t))
    elif inst in ("reed", "bow_stab", "bow_lead", "pad"):
        vib = (.0012 if inst == "reed" else .0007) * np.sin(TWOPI * 4.9 * t)
        phase = TWOPI * f * np.cumsum(1 + vib) / SR
        y = np.zeros(n)
        for k in range(1, min(18, int(14000 / f))):
            formant = .3 + .7 * np.exp(-((f * k - (700 if inst == "reed" else 450)) / 1600) ** 2)
            amp = formant / k ** (1.35 if inst == "reed" else 1.65)
            if inst == "pad":
                amp /= 1 + .3 * k
            y += amp * np.sin(phase * k + .07 * k)
        y += .014 * noise_band(rng, n, 300, 3200)
        att = {"reed": .022, "bow_stab": .012, "bow_lead": .045, "pad": .6}[inst]
        y *= shape(n, att, gate, release)
        if inst == "bow_stab":
            y *= np.exp(-t * 4.5)
        if inst == "pad":
            y *= .8 + .2 * np.sin(np.pi * t / length) ** 2
    elif inst == "bass":
        phase = TWOPI * f * t
        y = np.sin(phase) + .23 * np.sin(2 * phase) + .055 * np.sin(3 * phase)
        y *= np.exp(-t * 2.1) * shape(n, .007, gate, release)
    elif inst == "doum":
        base = hz(midi("C2"))
        phase = TWOPI * base * (t + .6 * .018 * (1 - np.exp(-t / .018)))
        y = np.sin(phase) * np.exp(-t / .16)
        y += .28 * np.sin(TWOPI * base * 2.19 * t) * np.exp(-t / .07)
        y += .15 * np.sin(TWOPI * base * 3.08 * t) * np.exp(-t / .045)
        y += .12 * noise_band(rng, n, 350, 3500) * np.exp(-t / .012)
        y *= shape(n, .002, length - .02, .02) * 1.5
    elif inst in ("tek", "finger"):
        base = hz(midi("G4" if inst == "tek" else "C4"))
        y = .6 * np.sin(TWOPI * base * t) * np.exp(-t / .034)
        y += .33 * np.sin(TWOPI * base * 1.57 * t) * np.exp(-t / .02)
        y += .35 * noise_band(rng, n, 1400, 8000) * np.exp(-t / .013)
        y *= shape(n, .001, length - .01, .01)
    elif inst == "shaker":
        y = noise_band(rng, n, 2500, 11000)
        y *= np.exp(-t / .025) * shape(n, .004, .1, .04)
    elif inst == "metal":
        y = np.zeros(n)
        for k, freq in enumerate([811, 1279, 2087, 3019, 4283, 5711]):
            y += np.sin(TWOPI * freq * t + k) * np.exp(-t * (3 + k)) / (k + 2)
        y += .08 * noise_band(rng, n, 2500, 10000) * np.exp(-t * 8)
        y *= shape(n, .004, length - .1, .1)
    else:
        raise ValueError(inst)
    return y.astype(np.float64)


def wrap_add(bus, data, start, gains):
    start %= len(bus)
    count = min(len(data), len(bus) - start)
    bus[start:start + count] += data[:count, None] * gains
    if count < len(data):
        bus[:len(data) - count] += data[count:, None] * gains


def circular_filter(audio, sos):
    frequencies = fft.rfftfreq(len(audio), 1 / SR)
    _, response = signal.sosfreqz(sos, worN=frequencies, fs=SR)
    spectrum = fft.rfft(audio, axis=0)
    return fft.irfft(spectrum * response[:, None], n=len(audio), axis=0)


def room(send, seed):
    rng = np.random.default_rng(seed)
    n = len(send)
    out = np.zeros_like(send)
    for ch in range(2):
        count = round(1.65 * SR)
        t = np.arange(count) / SR
        ir = rng.standard_normal(count) * np.exp(-t * 5.4)
        ir[:round(.022 * SR)] = 0
        ir *= np.minimum(1, t / .07)
        ir = signal.sosfilt(signal.butter(2, [200, 4700], btype="bandpass", fs=SR, output="sos"), ir)
        ir *= .36 / np.sqrt(np.sum(ir * ir))
        for delay, amp in [(.037, .32), (.061, -.24), (.101, .15), (.151, .10)]:
            ir[round((delay + .003 * ch) * SR)] += amp
        excitation = send[:, ch] + .14 * send[:, 1 - ch]
        out[:, ch] = fft.irfft(fft.rfft(excitation) * fft.rfft(ir, n=n), n=n)
    return out


def synthesize(score):
    dry = np.zeros((score.frames, 2), dtype=np.float64)
    send = np.zeros_like(dry)
    echo = np.zeros_like(dry)
    cache = {}
    for i, e in enumerate(score.events):
        # A small bank of original performances per instrument/pitch/duration.
        key = (e.instrument, e.note, round(e.gate_beats, 4), e.seed % 4)
        if key not in cache:
            cache[key] = voice(e.instrument, e.note, e.gate_beats * score.beat_seconds, e.seed)
        y = cache[key] * e.velocity
        pan = (e.pan + 1) * np.pi / 4
        gains = np.array([np.cos(pan), np.sin(pan)])
        at = round(e.beat * score.beat_seconds * SR)
        wrap_add(dry, y, at, gains)
        amount = {"flute": .28, "reed": .17, "bow_lead": .2, "pad": .3,
                  "oud": .17, "lute_lead": .23, "bow_stab": .12, "bass": .025,
                  "doum": .065, "tek": .12, "finger": .08, "shaker": .06, "metal": .18}[e.instrument]
        wrap_add(send, y * amount, at, gains)
        if e.instrument in ("flute", "oud", "lute_lead"):
            wrap_add(echo, y * (.13 if score.id == "mus_desert" else .07), at, gains)
        if i % 350 == 0:
            print(f"{score.id}: rendered {i}/{len(score.events)} events", flush=True)
    result = dry + room(send, score.seed + 10)
    echo = circular_filter(echo, signal.butter(2, 2900, fs=SR, output="sos"))
    delay = round(.75 * score.beat_seconds * SR)
    result += np.roll(echo[:, ::-1], delay, axis=0)
    result += .35 * np.roll(echo, delay * 2, axis=0)
    result = circular_filter(result, signal.butter(2, 32, btype="highpass", fs=SR, output="sos"))
    result = circular_filter(result, signal.butter(2, 11500, fs=SR, output="sos"))
    result -= result.mean(axis=0)
    return result


def meter(path):
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", str(path),
           "-af", "loudnorm=I=-16:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True, check=True)
    block = re.search(r'\{\s*"input_i"[\s\S]*?\}', p.stderr)
    if not block:
        raise RuntimeError(p.stderr[-3000:])
    raw = json.loads(block.group())
    return {"integrated_lufs": float(raw["input_i"]),
            "true_peak_dbtp": float(raw["input_tp"]),
            "loudness_range_lu": float(raw["input_lra"]),
            "meter": "FFmpeg loudnorm input measurements (EBU R128/BS.1770)"}


def measure_float(audio, temp):
    sf.write(temp, audio, SR, subtype="FLOAT")
    return meter(temp)


def master(audio, temp):
    # Constant gain, or gentle memoryless peak shaping if needed; no start/end
    # limiter states, fades or resampling that could break periodic continuity.
    x = audio / np.max(np.abs(audio)) * .8
    stats = measure_float(x, temp)
    x *= 10 ** ((-16 - stats["integrated_lufs"]) / 20)
    stats = measure_float(x, temp)
    shaping_passes = 0
    while stats["true_peak_dbtp"] > -1.12 and shaping_passes < 8:
        threshold = .52
        magnitude = np.abs(x)
        x = np.sign(x) * np.where(magnitude <= threshold, magnitude,
                                 threshold + .33 * np.tanh((magnitude - threshold) / .33))
        stats = measure_float(x, temp)
        x *= 10 ** ((-16 - stats["integrated_lufs"]) / 20)
        stats = measure_float(x, temp)
        shaping_passes += 1
    if stats["true_peak_dbtp"] > -1.05:
        raise RuntimeError(f"Unable to meet true peak ceiling: {stats}")
    return x, shaping_passes


def validate(path, score):
    with wave.open(str(path), "rb") as f:
        assert (f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getnframes()) == (2, 2, SR, score.frames)
        assert f.getcomptype() == "NONE"
    data, _ = sf.read(path, dtype="float64", always_2d=True)
    stats = meter(path)
    stats["sample_peak_dbfs"] = round(20 * np.log10(np.max(np.abs(data))), 5)
    stats["rms_dbfs"] = round(20 * np.log10(np.sqrt(np.mean(data ** 2))), 5)
    stats["dc_offset_per_channel"] = [round(v, 10) for v in data.mean(axis=0)]
    stats["stereo_correlation"] = round(float(np.corrcoef(data.T)[0, 1]), 5)
    differences = np.abs(np.diff(data, axis=0))
    seam = np.abs(data[0] - data[-1])
    reference = np.quantile(differences, .999, axis=0)
    stats["loop_boundary"] = {
        "jump_per_channel": seam.tolist(),
        "ordinary_step_99_9_percentile_per_channel": reference.tolist(),
        "seam_within_ordinary_step_range": bool(np.all(seam <= reference)),
        "tail_policy": "All notes, delays, filters and reverb wrap circularly; no file fades or padding.",
    }
    peaks_per_second = np.max(np.abs(data).reshape(-1, SR, 2), axis=(1, 2))
    assert np.min(peaks_per_second) > .003, "Unexpected silent section"
    assert np.all(np.isfinite(data))
    assert -16.2 <= stats["integrated_lufs"] <= -15.8, stats
    assert stats["sample_peak_dbfs"] <= -1 and stats["true_peak_dbtp"] <= -1, stats
    assert max(abs(v) for v in stats["dc_offset_per_channel"]) < .0001
    assert stats["loop_boundary"]["seam_within_ordinary_step_range"], stats
    return stats


def write_score(score):
    payload = {"asset_id": score.id, "bpm": score.bpm, "bars": score.bars,
               "meter": "4/4", "seed": score.seed, "seconds": score.seconds,
               "beat_unit": "quarter", "tuning": "A4=440 Hz; C4=MIDI 60",
               "pitch_collection": ["C", "Db", "E", "F", "G", "Ab", "B"],
               "events": [asdict(e) for e in score.events]}
    path = OUT / f"{score.id}.score.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def render(score):
    print(f"Composing {score.id}: {score.bars} bars, {score.seconds:g} s, {len(score.events)} events", flush=True)
    temp = OUT / f"_{score.id}_metering_float.wav"
    try:
        audio = synthesize(score)
        audio, shaping_passes = master(audio, temp)
        # Original seeded TPDF dither at 1 LSB before PCM16 quantisation.
        rng = np.random.default_rng(score.seed + 20)
        audio += (rng.random(audio.shape) - rng.random(audio.shape)) / 65536
        pcm = np.clip(np.rint(audio * 32768), -32768, 32767).astype("<i2")
        path = OUT / f"{score.id}.wav"
        with wave.open(str(path), "wb") as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(SR)
            f.writeframes(pcm.tobytes())
        stats = validate(path, score)
        write_score(score)
        info = {
            "asset_id": score.id, "status": "GENERATED_TECHNICALLY_VALIDATED",
            "file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size, "channels": 2, "sample_rate_hz": SR,
            "bits_per_sample": 16, "encoding": "PCM signed 16-bit little-endian WAV",
            "bpm": score.bpm, "meter": "4/4", "bars": score.bars,
            "duration_seconds": score.seconds, "frames": score.frames,
            "loop_start": 0, "loop_end": score.seconds,
            "loop_start_frame_inclusive": 0, "loop_end_frame_exclusive": score.frames,
            "whole_file_seamless_design": True,
            "generation": "Original Python composition and additive/physical-inspired synthesis; no sampled instruments, external music, vocals, or AI music API.",
            "source": "tools/render_chapter_music.py", "seed": score.seed,
            "score_file": f"{score.id}.score.json", "event_count": len(score.events),
            "soft_peak_shaping_passes": shaping_passes, "measurements": stats,
            "auditory_review": "Pending human listening review; objective audio checks passed.",
            "game_integration": "Not imported; Claude owns playback, looping, mixing and triggers.",
        }
        (OUT / f"{score.id}.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"file": str(path), "seconds": score.seconds,
                          "lufs": stats["integrated_lufs"], "true_peak": stats["true_peak_dbtp"],
                          "seam_check": stats["loop_boundary"]["seam_within_ordinary_step_range"]}), flush=True)
        return info
    finally:
        if temp.exists():
            temp.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["all", "desert", "pharaoh"], default="all")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    scores = []
    if args.track in ("all", "desert"):
        scores.append(compose_desert())
    if args.track in ("all", "pharaoh"):
        scores.append(compose_pharaoh())
    for score in scores:
        render(score)


if __name__ == "__main__":
    main()
