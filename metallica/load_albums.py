
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import simplejson as json
import pathlib

from rich import print

with open(pathlib.Path.home()/".spotipy"/"identity.json",'r') as f:
    credentials = json.load(f)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(**credentials))

#results = sp.search(q='drei ???', limit=20,type='artist')
#print(results)
#for idx, track in enumerate(results['tracks']['items']):
#    print(idx, track['name'])

# found artist uri: spotify:artist:3meJIgRw7YleJrmbpbJK6S

metallica_uri = "spotify:artist:2ye2Wgw4gimLv2eAKyk1NB"


results = sp.artist_albums(metallica_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

rows = []

for album in albums:

    name = album['name']
    this_album = {}
    this_album['release_date'] = album['release_date']
    this_album['total_tracks'] = album['total_tracks']
    this_album['uri'] = album['uri']
    this_album['name'] = album['name']
    rows.append(this_album)

with open('albums.json','w') as f:
    rows = sorted(rows,key=lambda x: x['release_date'])
    json.dump(rows,f, indent=4)
