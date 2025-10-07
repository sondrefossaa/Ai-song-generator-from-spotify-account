import os
from flask import Flask, redirect, request, session, render_template, jsonify
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
auth_manager = spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope='user-read-currently-playing playlist-modify-private user-top-read',
    cache_handler=cache_handler,
    show_dialog=True
)

@app.route("/", methods=["GET", "POST"])
def index():
    # Handle POST request FIRST (before callback check)
    if request.method == "POST" and request.form.get("login"):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # THEN handle Spotify callback
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')
    
    # FINALLY check authentication status
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # User is not logged in - show login page
        return render_template("not_logged.html")
    else:
        # User is logged in - show dashboard
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        user_name = spotify.me()["display_name"]
        return render_template("logged_in.html", user_name=user_name)

@app.route("/top_tracks")
def top_tracks():
    
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    user_name = spotify.me()["display_name"]
    
    # Get top tracks
    try:
        results = spotify.current_user_top_tracks(limit=50, time_range='medium_term')
        tracks = []
        for idx, item in enumerate(results['items']):
            track_data = {
                'rank': idx + 1,
                'name': item['name'],
                'artists': [artist['name'] for artist in item['artists']],
                'album': item['album']['name'],
                'image': item['album']['images'][0]['url'] if item['album']['images'] else None,
                'preview_url': item['preview_url']
            }
            tracks.append(track_data)
    except Exception as e:
        tracks = []
    
    return render_template("top_tracks.html", user_name=user_name, tracks=tracks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)