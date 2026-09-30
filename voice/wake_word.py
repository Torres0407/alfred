import sounddevice as sd
import numpy as np
from scipy.signal import resample
from openwakeword.model import Model

DEVICE_SAMPLE_RATE = 48000
WAKE_SAMPLE_RATE = 16000
CHUNK_SAMPLES_48K = int(DEVICE_SAMPLE_RATE * 0.08)
INPUT_DEVICE = 12
THRESHOLD = 0.5

print("[wake_word] Loading model...")
_oww_model = Model(wakeword_models=["hey_mycroft"], inference_framework="onnx")
print("[wake_word] Model ready.")


def wait_for_wake_word():
    """
    Blocks until 'Hey Mycroft' is detected, then returns.
    Starts a fresh stream each call, so no leftover state carries over
    and causes repeat/double triggers.
    """
    detected = {"flag": False}

    def callback(indata, frames, time_info, status):
        if detected["flag"]:
            return
        audio = np.squeeze(indata)
        num_samples = int(len(audio) * WAKE_SAMPLE_RATE / DEVICE_SAMPLE_RATE)
        resampled = resample(audio, num_samples)
        int16_audio = (resampled * 32767).astype(np.int16)

        prediction = _oww_model.predict(int16_audio)
        score = prediction.get("hey_mycroft", 0)

        if score > THRESHOLD:
            detected["flag"] = True

    with sd.InputStream(
        samplerate=DEVICE_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=INPUT_DEVICE,
        blocksize=CHUNK_SAMPLES_48K,
        callback=callback
    ):
        while not detected["flag"]:
            sd.sleep(50)