"""Compose/render four original non-looping story cues; preserve existing audio.

Uses the instrument palette and metering from render_chapter_music.py, with a
linear signal path: notes, echo and room tails never wrap to the file start.
Requires numpy, scipy, soundfile and imageio-ffmpeg.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import wave
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy import signal

from render_chapter_music import ROOT, OUT, SR, SCALE, midi, voice, master, meter


@dataclass
class CueEvent:
    instrument: str
    start_seconds: float
    note: int | None
    gate_seconds: float
    velocity: float
    pan: float
    seed: int


class Cue:
    def __init__(self, asset_id, seconds, seed, fade_from, markers):
        self.id, self.seconds, self.seed = asset_id, seconds, seed
        self.frames = round(seconds * SR)
        self.fade_from = fade_from
        self.markers = markers
        self.events = []
        self.rng = np.random.default_rng(seed)

    def put(self, inst, at, note=None, gate=.5, vel=.05, pan=0):
        if isinstance(note, str):
            note = midi(note)
        if note is not None:
            assert note % 12 in SCALE
        assert 0 <= at < self.seconds and gate > 0
        self.events.append(CueEvent(inst, at, note, gate,
                         vel * float(self.rng.uniform(.97, 1.03)),
                         float(np.clip(pan + self.rng.uniform(-.02, .02), -.8, .8)),
                         int(self.rng.integers(1, 2**31))))

    def bed(self, at, gate, notes=("C3", "G3"), velocities=(.035, .023)):
        for note, vel, pan in zip(notes, velocities, np.linspace(-.28, .28, len(notes))):
            self.put("pad", at, note, gate, vel, float(pan))

    def line(self, inst, notes, vel=.08, pan=.08):
        for at, note, gate in notes:
            self.put(inst, at, note, gate, vel, pan)


def intro():
    c = Cue("mus_intro", 54, 540631, 52, [
        [0, "Breached city and fallen comrades: quiet C-G bed, isolated plucks"],
        [13, "Thin the melody under the stolen-Grail text"],
        [20, "Quiet breath-flute lament"], [27, "Dave's vow: adventure motif enters"],
        [35, "Broaden restrained resolve"], [43, "Eastward walk: measured pulse"],
        [52, "Fade open C-G resonance to silence by 54 seconds"],
    ])
    c.bed(0, 12, velocities=(.042, .025))
    c.put("bow_lead", 0, "C2", 7.8, .018, -.12)
    c.line("oud", [(0, "C3", .35), (3.1, "G3", .55), (7.2, "E3", .6), (10.1, "Db4", .5)], .042, -.2)
    c.bed(13, 6.1, velocities=(.022, .014))
    c.line("oud", [(13, "C4", .55), (17.8, "B3", .45)], .026, .15)
    c.bed(20, 6.2, velocities=(.028, .018))
    c.line("flute", [(20.5, "F4", 1.3), (22, "E4", 1.1), (23.4, "Db4", .85),
                      (24.5, "C4", 1.3), (26.2, "B3", .35)], .06)
    c.bed(27, 7.7, velocities=(.035, .024))
    vow = [(27,"C4",.75), (27.9,"Db4",.35), (28.35,"E4",.35), (28.8,"G4",.75),
           (29.7,"F4",.75), (30.6,"E4",.75), (31.5,"Db4",.35), (31.95,"C4",.35),
           (32.4,"B3",.75), (33.3,"C4",1.05)]
    c.line("flute", vow, .082)
    for at in [27,28.8,30.6,32.4,34.2]:
        c.put("doum", at, gate=.3, vel=.024, pan=-.1)
    c.bed(35, 6.6, ("C3","E3","G3"), (.042,.023,.027))
    c.line("flute", [(35,"G4",.7),(35.8,"Ab4",.32),(36.2,"B4",.32),(36.6,"C5",.7),
                      (37.4,"G4",.7),(38.4,"F4",.7),(39.2,"E4",.7),(40,"Db4",.7),
                      (40.8,"C4",1.15)], .093)
    c.line("oud", [(36.4,"C4",.65),(38,"E4",.65),(40.4,"G4",.65)], .05, -.25)
    for at in [35,36.6,38.2,39.8,41.4]:
        c.put("doum", at, gate=.3, vel=.029, pan=-.1)
    c.bed(43, 6.4, velocities=(.035,.024))
    for k, note in enumerate(["C3","G3","E3","G3","C3","G3","E3","G3"]):
        c.put("oud", 43+k*1.125, note, .65, .052, -.23 if k%2==0 else .22)
    for k in range(12):
        at=43+k*.75
        if k%2==0:
            c.put("doum",at,gate=.3,vel=.032,pan=-.1)
        c.put("shaker",at,gate=.1,vel=.007,pan=.35)
        c.put("shaker",at+.375,gate=.1,vel=.005,pan=-.35)
    c.line("flute", [(43.5,"C4",.62),(44.25,"Db4",.29),(44.625,"E4",.29),
                      (45,"G4",.62),(45.75,"F4",.62),(46.5,"E4",.62),
                      (47.25,"Db4",.29),(47.625,"C4",.29),(48,"B3",.62),
                      (48.75,"C4",.9)], .075)
    c.bed(49.5, 4.7, velocities=(.03,.021))
    return c


def boss_defeat():
    c = Cue("mus_boss_defeat", 6, 606319, 4, [
        [0,"Muted low C-G, leaving room for separate boss death SFX"],
        [.22,"Dissolving C-Db-G-E Pharaoh motif fragment"],
        [2,"Soft C-E-G release"], [4,"Final two seconds of fading open-fifth resonance"],
    ])
    c.put("bass",0,"C2",.65,.055,-.05)
    c.put("oud",0,"G2",.5,.032,.1)
    c.line("bow_lead",[(.22,"C3",.32),(.70,"Db3",.26),(1.08,"G3",.3),(1.5,"E3",.35)],.052,-.12)
    c.line("lute_lead",[(.22,"C3",.3),(.70,"Db3",.25),(1.08,"G3",.3),(1.5,"E3",.35)],.045,.12)
    for j,note in enumerate(["C4","E4","G4"]):
        c.put("lute_lead",2+j*.045,note,.8,.055,-.25+j*.25)
    c.bed(2.15, 3.8, ("C4","G4"), (.018,.014))
    c.line("flute",[(2.65,"C5",.75),(2.72,"G5",.75)],.025,.12)
    return c


def ending():
    c=Cue("mus_ending",10,100631,8,[
        [0,"Threshold: C-Db-E-G exploration motif"],
        [2,"Sparse C-G support beneath Dave's final line through second 5"],
        [6,"To Be Continued title: F-E-Db-C answer"],
        [8,"Open fifth decays to silence by second 10"],
    ])
    c.bed(0,4.8,velocities=(.026,.018))
    c.put("doum",0,gate=.3,vel=.022,pan=-.1)
    fragment=[(0,"C4",.35),(.45,"Db4",.2),(.7,"E4",.28),(1.1,"G4",.45)]
    c.line("lute_lead",fragment,.085,-.17)
    c.line("flute",fragment,.048,.15)
    answer=[(6,"F4",.3),(6.4,"E4",.3),(6.8,"Db4",.3),(7.2,"C4",.7)]
    c.line("lute_lead",answer,.08,-.12)
    c.line("flute",answer,.052,.12)
    c.bed(7.5,2.5,("C3","G3"),(.028,.019))
    return c


def gameover():
    c=Cue("mus_gameover",4.5,450631,3.3,[
        [0,"Sparse low C beneath Dave's separate death sound"],
        [.15,"Regretful descending G-E-Db plucks"],
        [2,"Short breathy C-G decay, permitting a hopeful retry"],
    ])
    c.put("pad",0,"C3",2.1,.018,-.18)
    c.put("oud",0,"C2",.3,.017,-.05)
    c.line("lute_lead",[(.15,"G4",.42),(.75,"E4",.42),(1.35,"Db4",.52)],.083,-.12)
    c.line("flute",[(2,"C4",2.4),(2.045,"G4",2.4)],.037,.15)
    return c


def add_linear(bus, data, start, gains):
    assert start>=0
    count=min(len(data),len(bus)-start)
    if count>0:
        bus[start:start+count] += data[:count,None]*gains


def linear_room(send, seed):
    rng=np.random.default_rng(seed)
    out=np.zeros_like(send)
    count=round(1.65*SR)
    t=np.arange(count)/SR
    for ch in range(2):
        ir=rng.standard_normal(count)*np.exp(-t*5.4)
        ir[:round(.022*SR)]=0
        ir*=np.minimum(1,t/.07)
        ir=signal.sosfilt(signal.butter(2,[200,4700],btype="bandpass",fs=SR,output="sos"),ir)
        ir*=.36/np.sqrt(np.sum(ir*ir))
        for delay,amp in [(.037,.32),(.061,-.24),(.101,.15),(.151,.1)]:
            ir[round((delay+.003*ch)*SR)]+=amp
        excitation=send[:,ch]+.14*send[:,1-ch]
        out[:,ch]=signal.fftconvolve(excitation,ir,mode="full")[:len(send)]
    return out


def synthesize(c):
    dry=np.zeros((c.frames,2))
    send=np.zeros_like(dry)
    echo=np.zeros_like(dry)
    for e in c.events:
        y=voice(e.instrument,e.note,e.gate_seconds,e.seed)*e.velocity
        angle=(e.pan+1)*np.pi/4
        gains=np.array([np.cos(angle),np.sin(angle)])
        at=round(e.start_seconds*SR)
        add_linear(dry,y,at,gains)
        amount={"oud":.17,"lute_lead":.23,"flute":.27,"pad":.3,"bow_lead":.2,
                "bass":.03,"doum":.06,"shaker":.05}[e.instrument]
        add_linear(send,y*amount,at,gains)
        if e.instrument in ("oud","lute_lead","flute"):
            add_linear(echo,y*.075,at,gains)
    result=dry+linear_room(send,c.seed+10)
    echo=signal.sosfilt(signal.butter(2,2900,fs=SR,output="sos"),echo,axis=0)
    for delay,gain in [(.34,1),(.68,.3)]:
        frames=round(delay*SR)
        result[frames:]+=echo[:-frames,::-1]*gain
    result=signal.sosfilt(signal.butter(2,32,btype="highpass",fs=SR,output="sos"),result,axis=0)
    result=signal.sosfilt(signal.butter(2,11500,fs=SR,output="sos"),result,axis=0)
    taper=np.ones(c.frames)
    fade_at=round(c.fade_from*SR)
    taper[fade_at:]=np.cos(np.linspace(0,np.pi/2,c.frames-fade_at))**2
    edge=round(.004*SR)
    taper[:edge]*=np.sin(np.linspace(0,np.pi/2,edge))**2
    result*=taper[:,None]
    result-=result.mean(axis=0)[None,:]/taper.mean()*taper[:,None]
    return result


def inspect(path,c):
    with wave.open(str(path),"rb") as f:
        assert (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())==(2,2,SR,c.frames)
        assert f.getcomptype()=="NONE"
        data=np.frombuffer(f.readframes(c.frames),dtype="<i2").reshape(-1,2).astype(float)/32768
    stats=meter(path)
    stats["sample_peak_dbfs"]=float(20*np.log10(np.max(np.abs(data))))
    stats["dc_offset_per_channel"]=data.mean(axis=0).tolist()
    stats["last_100ms_rms_dbfs"]=float(20*np.log10(max(np.sqrt(np.mean(data[-4410:]**2)),1e-12)))
    stats["first_100ms_rms_dbfs"]=float(20*np.log10(max(np.sqrt(np.mean(data[:4410]**2)),1e-12)))
    stats["final_sample_abs_max"]=float(np.max(np.abs(data[-1])))
    active=np.flatnonzero(np.max(np.abs(data),axis=1)>1/32768)
    stats["terminal_quantized_silence_ms"]=(len(data)-1-int(active[-1]))*1000/SR
    stats["stereo_correlation"]=float(np.corrcoef(data.T)[0,1])
    assert np.isfinite(data).all()
    assert -16.2<=stats["integrated_lufs"]<=-15.8
    assert stats["true_peak_dbtp"]<=-1 and stats["sample_peak_dbfs"]<=-1
    assert max(abs(v) for v in stats["dc_offset_per_channel"])<.0001
    assert stats["last_100ms_rms_dbfs"]<-45
    assert stats["final_sample_abs_max"]<=1/32768
    assert stats["terminal_quantized_silence_ms"]<45
    # Every one-second block before the intended fade must contain real score.
    for start in range(int(c.fade_from)):
        assert np.max(np.abs(data[start*SR:(start+1)*SR]))>.001
    stats["non_looping_tail"]={"fade_from_seconds":c.fade_from,"all_decay_inside_file":True,
        "no_wrapped_reverb_or_echo":True,"natural_end_check":"PASS"}
    return stats


def render(c,asset):
    assert c.seconds==asset["duration_seconds_per_file"]
    assert asset["loop"]["enabled"] is False
    print(f"Rendering {c.id}: {c.seconds:g} s, {len(c.events)} events",flush=True)
    temp=OUT/f"_{c.id}_metering_float.wav"
    try:
        data,shaping_passes=master(synthesize(c),temp)
        rng=np.random.default_rng(c.seed+20)
        data+=(rng.random(data.shape)-rng.random(data.shape))/65536
        pcm=np.clip(np.rint(data*32768),-32768,32767).astype("<i2")
        path=OUT/f"{c.id}.wav"
        with wave.open(str(path),"wb") as f:
            f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
        stats=inspect(path,c)
        score={"asset_id":c.id,"duration_seconds":c.seconds,"loop":False,"tempo":"Free timing against storyboard seconds",
               "tuning":"A4=440 Hz; C4=MIDI 60","pitch_collection":["C","Db","E","F","G","Ab","B"],
               "seed":c.seed,"markers":c.markers,"end_fade_from_seconds":c.fade_from,
               "events":[asdict(e) for e in c.events]}
        (OUT/f"{c.id}.score.json").write_text(json.dumps(score,indent=2)+"\n",encoding="utf-8")
        info={"asset_id":c.id,"purpose":asset["purpose"],"status":"GENERATED_TECHNICALLY_VALIDATED",
              "file":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size,
              "channels":2,"sample_rate_hz":SR,"bits_per_sample":16,"encoding":"PCM signed 16-bit little-endian WAV",
              "duration_seconds":c.seconds,"frames":c.frames,"loop":False,"loop_start":None,"loop_end":None,
              "generation":"Original seeded Python composition, additive instrument synthesis and linear room/delay rendering; no samples, vocals, dialogue, weather or battle SFX.",
              "source":"tools/render_chapter_cues.py","source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "instrument_source":"tools/render_chapter_music.py","seed":c.seed,"score_file":f"{c.id}.score.json",
              "event_count":len(c.events),"markers":c.markers,"soft_peak_shaping_passes":shaping_passes,
              "measurements":stats,"generation_or_recording_prompt":asset["generation_or_recording_prompt"],
              "trigger":asset["trigger"],"stop":asset["stop"],"playback_gain_baked_in":False,
              "auditory_review":"Pending human listening review; objective audio checks passed.",
              "game_integration":"Not imported; Claude owns playback, fades, mixing and triggers."}
        (OUT/f"{c.id}.json").write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"file":str(path),"seconds":c.seconds,"lufs":stats['integrated_lufs'],
                          "true_peak":stats['true_peak_dbtp'],"tail_rms_dbfs":stats['last_100ms_rms_dbfs']}),flush=True)
    finally:
        if temp.exists():
            temp.unlink()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cue",choices=["all","intro","boss_defeat","ending","gameover"],default="all")
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    specs={a["id"]:a for a in json.loads((ROOT/"docs/audio/AUDIO_MANIFEST.json").read_text(encoding="utf-8"))["assets"]}
    for name,factory in [("intro",intro),("boss_defeat",boss_defeat),("ending",ending),("gameover",gameover)]:
        if args.cue in ("all",name):
            c=factory()
            render(c,specs[c.id])


if __name__=="__main__":
    main()
