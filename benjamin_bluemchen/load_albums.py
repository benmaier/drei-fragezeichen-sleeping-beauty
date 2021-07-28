
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

benblum_uri = "spotify:artist:1l6d0RIxTL3JytlLGvWzYe"


results = sp.artist_albums(benblum_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

rows = []

for album in albums:

    name = album['name']
    if name.startswith("Folge ") and (":" in name or " -" in name):
        try:
            ndx0 = name.index(":")
        except ValueError as e:
            ndx0 = None
        try:
            ndx1 = name.index("-")
            if ndx0 is not None:
                ndx = min(ndx0,ndx1)
        except ValueError as e:
            ndx = ndx0
        episode = int(name[6:ndx])
        print(episode, name)
        this_album = {}
        this_album['episode'] = episode
        this_album['release_date'] = album['release_date']
        this_album['total_tracks'] = album['total_tracks']
        this_album['uri'] = album['uri']
        this_album['name'] = album['name']
        rows.append(this_album)

with open('albums.json','w') as f:
    rows = sorted(rows,key=lambda x: x['episode'])
    json.dump(rows,f, indent=4)
