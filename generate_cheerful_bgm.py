import numpy as np
import wave
import struct

SAMPLE_RATE = 44100

def generate_note(freq, duration, sample_rate=SAMPLE_RATE, decay=4.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Marimba-like timbre: Fundamental + 2nd harmonic (octave) + 3rd harmonic (twelfth)
    env = np.exp(-decay * t)
    # Attack ramp to prevent clicks
    attack_samples = int(0.008 * sample_rate)
    env[:attack_samples] *= np.linspace(0, 1, attack_samples)
    
    waveform = (0.7 * np.sin(2 * np.pi * freq * t) +
                0.25 * np.sin(2 * np.pi * freq * 2 * t) +
                0.1 * np.sin(2 * np.pi * freq * 3 * t)) * env
    return waveform

def generate_bgm(output_path, total_duration=150.0):
    bpm = 116
    beat_dur = 60.0 / bpm  # ~0.517s per beat
    
    # Note frequencies
    C3, E3, G3 = 130.81, 164.81, 196.00
    C4, D4, E4, F4, G4, A4, B4, C5 = 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25
    D5, E5, G5 = 587.33, 659.25, 783.99
    
    pattern = [
        # Bar 1 (C major)
        (0.0, C4, 0.45, 4.5), (0.0, C3, 0.9, 3.0),
        (0.5, E4, 0.45, 5.0),
        (1.0, G4, 0.45, 5.0), (1.0, G3, 0.9, 3.0),
        (1.5, E4, 0.45, 5.0),
        (2.0, C5, 0.45, 4.0), (2.0, C3, 0.9, 3.0),
        (2.5, G4, 0.45, 5.0),
        (3.0, E4, 0.45, 5.0), (3.0, G3, 0.9, 3.0),
        (3.5, G4, 0.45, 5.0),
        
        # Bar 2 (F / Dm bouncy)
        (4.0, D4, 0.45, 4.5), (4.0, F4, 0.9, 3.0),
        (4.5, F4, 0.45, 5.0),
        (5.0, A4, 0.45, 5.0), (5.0, D4, 0.9, 3.0),
        (5.5, F4, 0.45, 5.0),
        (6.0, D5, 0.45, 4.0), (6.0, F4, 0.9, 3.0),
        (6.5, A4, 0.45, 5.0),
        (7.0, F4, 0.45, 5.0), (7.0, D4, 0.9, 3.0),
        (7.5, D4, 0.45, 5.0),
        
        # Bar 3 (E / Am bouncy)
        (8.0, E4, 0.45, 4.5), (8.0, C4, 0.9, 3.0),
        (8.5, G4, 0.45, 5.0),
        (9.0, C5, 0.45, 5.0), (9.0, E4, 0.9, 3.0),
        (9.5, G4, 0.45, 5.0),
        (10.0, E5, 0.45, 4.0), (10.0, C4, 0.9, 3.0),
        (10.5, C5, 0.45, 5.0),
        (11.0, G4, 0.45, 5.0), (11.0, E4, 0.9, 3.0),
        (11.5, E4, 0.45, 5.0),
        
        # Bar 4 (G7 -> C resolution)
        (12.0, G4, 0.45, 4.5), (12.0, G3, 0.9, 3.0),
        (12.5, B4, 0.45, 5.0),
        (13.0, D5, 0.45, 5.0), (13.0, B4, 0.9, 3.0),
        (13.5, F4, 0.45, 5.0),
        (14.0, C5, 0.8, 3.5), (14.0, C3, 1.2, 2.5),
        (15.0, G4, 0.4, 5.0),
        (15.5, C5, 0.5, 4.0)
    ]
    
    loop_beats = 16.0
    loop_duration = loop_beats * beat_dur
    total_samples = int(SAMPLE_RATE * total_duration)
    
    left_channel = np.zeros(total_samples, dtype=np.float32)
    right_channel = np.zeros(total_samples, dtype=np.float32)
    
    current_time = 0.0
    while current_time < total_duration:
        for beat_off, freq, n_len, decay in pattern:
            t_start = current_time + beat_off * beat_dur
            if t_start >= total_duration:
                break
            note = generate_note(freq, n_len, decay=decay)
            idx_start = int(t_start * SAMPLE_RATE)
            idx_end = min(idx_start + len(note), total_samples)
            actual_len = idx_end - idx_start
            
            # Slight stereo panning
            pan = 0.5 + 0.25 * np.sin(freq * 0.05)
            left_channel[idx_start:idx_end] += note[:actual_len] * (1.0 - pan)
            right_channel[idx_start:idx_end] += note[:actual_len] * pan
            
        current_time += loop_duration
        
    # Normalize gently
    max_val = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
    if max_val > 0:
        left_channel = (left_channel / max_val) * 0.65
        right_channel = (right_channel / max_val) * 0.65
        
    # Interleave to 16-bit PCM stereo
    left_i16 = (left_channel * 32767).astype(np.int16)
    right_i16 = (right_channel * 32767).astype(np.int16)
    
    stereo_data = np.empty((total_samples * 2,), dtype=np.int16)
    stereo_data[0::2] = left_i16
    stereo_data[1::2] = right_i16
    
    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(stereo_data.tobytes())
        
    print(f"Generated cheerful marimba BGM: {output_path} ({total_duration}s)")

if __name__ == "__main__":
    import os
    os.makedirs("/home/quang/video_ai/audio", exist_ok=True)
    generate_bgm("/home/quang/video_ai/audio/bgm_cheerful.wav", total_duration=150.0)
