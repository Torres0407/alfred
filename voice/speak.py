import asyncio
import os
import tempfile
import threading
import edge_tts
import pygame
from config import TTS_VOICE

pygame.mixer.init()


def _run_async_in_thread(coro):
    """Runs an async coroutine in a fresh event loop on a separate thread,
    avoiding conflicts with any event loop already running (e.g. Playwright's)."""
    result = {}

    def runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(coro)
        finally:
            loop.close()

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()


async def _generate_speech(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(output_path)


def speak(text: str):
    if not text:
        return

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        temp_path = tmp.name

    try:
        _run_async_in_thread(_generate_speech(text, temp_path))

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"[speak] TTS failed: {e}")
    finally:
        pygame.mixer.music.unload()
        try:
            os.remove(temp_path)
        except OSError:
            pass