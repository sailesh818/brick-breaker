import numpy as np
import wave

def generate_beep(filename, freq=440, duration=0.1, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound = volume * np.sin(2 * np.pi * freq * t)

    # Convert to 16-bit PCM
    sound = np.int16(sound * 32767)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(sound.tobytes())

# Generate basic game sounds
generate_beep("paddle_hit.wav", freq=500)
generate_beep("brick_hit.wav", freq=700)
generate_beep("game_over.wav", freq=200, duration=0.3)
