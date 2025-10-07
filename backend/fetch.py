import os, spotipy, json
from dotenv import load_dotenv
from flask import jsonify


load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-read user-library-modify"))

sanger_1_50 = sp.current_user_top_tracks(limit = 50, time_range = 'long_term')
sanger_51_100 = sp.current_user_top_tracks(limit = 50, offset = 50, time_range = 'long_term')
artister_1_50 = sp.current_user_top_artists(limit = 50, time_range = 'long_term')
artister_51_100 = sp.current_user_top_artists(limit = 50, offset = 50, time_range = 'long_term')

sanger = sanger_1_50['items'] + sanger_51_100['items']
artister = artister_1_50['items'] + artister_51_100['items']

with open('data/sanger.json', 'w') as f:
    json.dump(sanger, f, indent = 4)

with open('data/artister.json', 'w') as f:
    json.dump(artister, f, indent = 4)

print(sp.audio_features(["6MXXY2eiWkpDCezVCc0cMH"]))