
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import simplejson as json
import pathlib

from rich import print

from time import sleep

with open(pathlib.Path.home()/".spotipy"/"identity.json",'r') as f:
    credentials = json.load(f)

with open('albums_with_tracks.json','r') as f:
    albums = json.load(f)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(**credentials))

for j, album in enumerate(albums):
    dur = 0
    for i, track in enumerate(album['tracks']):
        track_uri = track['uri']
        results = sp.track(track_uri)
        dur += track['duration_ms']
        track['cum_duration_ms'] = dur
        track['popularity'] = results['popularity']
        album['tracks'][i] = track

    print(album['name'])
    albums[j] = album

    sleep(0.1)

with open('albums_with_tracks_and_popularities.json','w') as f:
    rows = sorted(albums,key=lambda x: x['release_date'])
    json.dump(rows,f, indent=4)
