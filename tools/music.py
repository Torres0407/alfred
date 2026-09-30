import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

SCOPE = "user-modify-playback-state user-read-playback-state playlist-read-private"

_sp = None


def _get_client():
    global _sp
    if _sp is None:
        auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SCOPE,
            cache_path=".spotify_cache"
        )
        _sp = spotipy.Spotify(auth_manager=auth_manager)
    return _sp


def _active_device_id():
    sp = _get_client()
    devices = sp.devices().get("devices", [])
    for d in devices:
        if d["is_active"]:
            return d["id"]
    return devices[0]["id"] if devices else None


def play_music(query: str = None) -> str:
    sp = _get_client()
    device_id = _active_device_id()
    if not device_id:
        return "No active Spotify device found. Open Spotify on your phone/PC first, then try again."

    if query:
        results = sp.search(q=query, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            return f"Couldn't find a track matching '{query}'."
        track = tracks[0]

        # Explicitly transfer playback to the device first, then start the track.
        sp.transfer_playback(device_id=device_id, force_play=False)
        import time
        time.sleep(1)
        sp.start_playback(device_id=device_id, uris=[track["uri"]])

        return f"Playing '{track['name']}' by {track['artists'][0]['name']}."
    else:
        sp.transfer_playback(device_id=device_id, force_play=True)
        return "Resumed playback."


def pause_music() -> str:
    sp = _get_client()
    sp.pause_playback()
    return "Music paused."


def skip_track() -> str:
    sp = _get_client()
    sp.next_track()
    return "Skipped to next track."


def previous_track() -> str:
    sp = _get_client()
    sp.previous_track()
    return "Went back to previous track."


def get_current_track() -> str:
    sp = _get_client()
    current = sp.current_playback()
    if not current or not current.get("item"):
        return "Nothing is currently playing."
    track = current["item"]
    artist = track["artists"][0]["name"]
    return f"Currently playing: '{track['name']}' by {artist}."