import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-120b"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.6-flash"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Alfred can only read/write files inside this folder, for safety.
# Change this path to wherever you want Alfred to work.
FILES_ROOT = os.path.join(os.path.expanduser("~"), "AlfredFiles")
os.makedirs(FILES_ROOT, exist_ok=True)

TTS_VOICE = "en-US-GuyNeural"  # a male voice; try en-US-JennyNeural for female
VOICE_ENABLED = True

WHISPER_MODEL_SIZE = "tiny"  # tiny/base/small/medium/large — base is a good speed/accuracy balance
RECORD_SECONDS = 5  # how long to record when you speak

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

CODE_WORKSPACE = os.path.join(os.path.expanduser("~"), "AlfredCode")
os.makedirs(CODE_WORKSPACE, exist_ok=True)

ASSISTANT_NAME = "Alfred"