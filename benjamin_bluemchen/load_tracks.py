
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import simplejson as json
import pathlib

from rich import print

from time import sleep

with open(pathlib.Path.home()/".spotipy"/"identity.json",'r') as f:
    credentials = json.load(f)

with open('albums.json','r') as f:
    albums = json.load(f)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(**credentials))

rows = []

for album in albums:

    name = album['name']
    album_uri = album['uri']

    print(name)

    results = sp.album_tracks(album_uri, limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    these_tracks = []
    for track in tracks:
        this_track = {
                    'duration_ms': track['duration_ms'],
                    'disc_track_number': "{0:02d}-{1:02d}".format(track['disc_number'], track['track_number']),
                    'uri': track['uri'],
                }
        these_tracks.append(this_track)

    if len(these_tracks) != album['total_tracks']:
        print("tracks missing :(")

    these_tracks = sorted(these_tracks,key=lambda x:x['disc_track_number'])
    album['tracks'] = these_tracks
    rows.append(album)

    sleep(0.1)

with open('albums_with_tracks.json','w') as f:
    rows = sorted(rows,key=lambda x: x['episode'])
    json.dump(rows,f, indent=4)
