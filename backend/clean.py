import json

def load_from_json(file_path):
    with open(file_path) as f:
        return json.load(f)

tracks = load_from_json('data/tracks.json')
artists = load_from_json('data/artists.json')
# genres = load_from_json('data/genres.json')

tracks_fields = ['id', 'name', 'duration_ms', 'popularity', 'artists', 'albums']
tracks_subfields = ['id', 'name', 'release_date', 'images']

artists_fields = ['id', 'name', 'genres', 'popularity', 'followers', 'images']
artists_subfields = ['total']

def clean_tracks(tracks):
    cleaned_items = [] # Empty list for all cleaned tracks
    for track in tracks['items']: # Loop over all tracks
        cleaned_track = {}
        for field in tracks_fields:
            if field == 'album':
                # Keep only specified subfields for album
                cleaned_track[field] = {
                    subfield: track[field][subfield]
                    for subfield in tracks_subfields if subfield in track[field]
                }
            elif field == 'artists':
                # Keep only specified subfields for each artist in the list
                cleaned_track[field] = [
                    {subfield: artist[subfield] for subfield in tracks_subfields if subfield in artist}
                    for artist in track[field]
                ]
            else:
                # Copy other fields directly if they exist
                if field in track:
                    cleaned_track[field] = track[field]
        cleaned_items.append(cleaned_track)
    return {'items': cleaned_items}

def clean_artists(artists):
    cleaned_items = []
    for artist in artists['items']:
        cleaned_artist = {}
        for field in artists_fields:
            if field == 'followers':
                cleaned_artist[field] = {
                    subfield: artist[field][subfield]
                    for subfield in artists_subfields if subfield in artist[field]
                }
            else:
                if field in artist:
                    cleaned_artist[field] = artist[field]
        cleaned_items.append(cleaned_artist)
    return {'items': cleaned_items}

def save_to_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent = 4)

save_to_json('data/new_tracks.json', clean_tracks(tracks))
save_to_json('data/new_artists.json', clean_artists(artists))