import numpy as np
import wave
import struct
import os

SFX_DIR = "/home/quang/video_ai/audio"
os.makedirs(SFX_DIR, exist_ok=True)

# 1. Chime / Ting sound (Success sound for Quiz)
sample_rate = 44100
dur_ding = 1.0
t = np.linspace(0, dur_ding, int(sample_rate * dur_ding), False)
# Harmonic chime (880Hz + 1760Hz with exponential decay)
envelope = np.exp(-4 * t)
wave_ding = 0.5 * np.sin(2 * np.pi * 880 * t) + 0.3 * np.sin(2 * np.pi * 1760 * t)
wave_ding = (wave_ding * envelope * 32767).astype(np.int16)

with wave.open(os.path.join(SFX_DIR, "sfx_ding.wav"), "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes(wave_ding.tobytes())

# 2. Tick / Countdown click (Gentle woodblock/beep for countdown)
dur_tick = 0.2
t_tick = np.linspace(0, dur_tick, int(sample_rate * dur_tick), False)
env_tick = np.exp(-25 * t_tick)
wave_tick = np.sin(2 * np.pi * 1200 * t_tick) * env_tick
wave_tick = (wave_tick * 32767 * 0.4).astype(np.int16)

with wave.open(os.path.join(SFX_DIR, "sfx_tick.wav"), "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes(wave_tick.tobytes())

print("Sound effects created: sfx_ding.wav, sfx_tick.wav")
