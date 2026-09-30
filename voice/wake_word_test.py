import sounddevice as sd
import numpy as np
from scipy.signal import resample
from openwakeword.model import Model

DEVICE_SAMPLE_RATE = 48000
WAKE_SAMPLE_RATE = 16000
CHUNK_SAMPLES_48K = int(DEVICE_SAMPLE_RATE * 0.08)  # ~80ms chunks
INPUT_DEVICE = 12
THRESHOLD = 0.5

print("[wake_word_test] Loading model...")
oww_model = Model(wakeword_models=["hey_mycroft"], inference_framework="onnx")
print("[wake_word_test] Model loaded. Listening for 'Hey Mycroft'... (Ctrl+C to stop)")


def callback(indata, frames, time_info, status):
    if status:
        print(f"[stream status] {status}")

    audio = np.squeeze(indata)
    num_samples = int(len(audio) * WAKE_SAMPLE_RATE / DEVICE_SAMPLE_RATE)
    resampled = resample(audio, num_samples)

    # Scale float32 [-1.0, 1.0] to proper int16 PCM range before feeding the model
    int16_audio = (resampled * 32767).astype(np.int16)

    prediction = oww_model.predict(int16_audio)
    score = prediction.get("hey_mycroft", 0)
    print(f"score: {score:.4f}", end="\r")

    if score > THRESHOLD:
        print(f"\n🔔 WAKE WORD DETECTED! (score: {score:.2f})\n")


with sd.InputStream(
    samplerate=DEVICE_SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=INPUT_DEVICE,
    blocksize=CHUNK_SAMPLES_48K,
    callback=callback
):
    while True:
        sd.sleep(100)