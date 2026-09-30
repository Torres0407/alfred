# pyrefly: ignore [missing-import]
import sounddevice as sd
import numpy as np
from scipy.signal import resample
from faster_whisper import WhisperModel
from config import RECORD_SECONDS
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")

DEVICE_SAMPLE_RATE = 48000
WHISPER_SAMPLE_RATE = 16000
INPUT_DEVICE = 12

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "faster-whisper-base")

print("[listen] Loading Whisper model (first run may take a moment)...")
_model = WhisperModel(MODEL_PATH, compute_type="int8")
print("[listen] Whisper model ready.")


def listen_once() -> str:
    """
    Records RECORD_SECONDS of audio from the mic at the device's native
    sample rate, downsamples to 16kHz for Whisper, and transcribes it.
    """
    print(f"[listen] Recording for {RECORD_SECONDS} seconds... speak now.")
    audio = sd.rec(
        int(RECORD_SECONDS * DEVICE_SAMPLE_RATE),
        samplerate=DEVICE_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=INPUT_DEVICE
    )
    sd.wait()
    print("[listen] Transcribing...")

    audio = np.squeeze(audio)

    # Downsample from 48kHz to 16kHz for Whisper
    num_samples = int(len(audio) * WHISPER_SAMPLE_RATE / DEVICE_SAMPLE_RATE)
    audio_resampled = resample(audio, num_samples).astype(np.float32)

    segments, _ = _model.transcribe(audio_resampled, language="en")
    text = " ".join(segment.text for segment in segments).strip()

    return text