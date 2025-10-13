import os, spotipy, json
from dotenv import load_dotenv

# Get environment variables and store them
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope = [
        'user-read-playback-state',
        'user-modify-playback-state',
        'user-read-currently-playing',
        'app-remote-control',
        'streaming',
        'playlist-read-private',
        'playlist-read-collaborative',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-library-read',
        'user-library-modify'
    ]
))

def get_user_top_tracks():
    tracks_1_50 = sp.current_user_top_tracks(limit=50, time_range='long_term')
    tracks_51_100 = sp.current_user_top_tracks(limit=50, offset=50, time_range='long_term')
    return {'items': tracks_1_50['items'] + tracks_51_100['items']}


def get_user_top_artists():
    artists_1_50 = sp.current_user_top_artists(limit = 50, time_range = 'long_term')
    artists_51_100 = sp.current_user_top_artists(limit = 50, offset = 50, time_range = 'long_term')
    return {'items': artists_1_50['items'] + artists_51_100['items']}

def get_top_tracks_artists_genres(tracks):
    ids, genres = [], []
    for track in tracks['items']:
        ids.append(track['album']['artists'][0]['id'])

    artists_info_1_50 = sp.artists(ids[:50])
    artists_info_51_100 = sp.artists(ids[50:100])
    artists_info = {'artists': artists_info_1_50['artists'] + artists_info_51_100['artists']}
    
    for artist in artists_info['artists']:
        genres.extend(artist['genres'])
    return list(set(genres))

def save_to_json(tracks, artists, genres):
    with open('data/tracks.json', 'w') as f:
        json.dump(tracks, f, indent = 4)

    with open('data/artists.json', 'w') as f:
        json.dump(artists, f, indent = 4)

    with open('data/genres.json', 'w') as f:
        json.dump(genres, f, indent = 4)

if __name__ == '__main__':
    tracks = get_user_top_tracks()
    artists = get_user_top_artists()
    genres = get_top_tracks_artists_genres(tracks)
    save_to_json(tracks, artists, genres)