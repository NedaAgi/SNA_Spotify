import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

""" 
program to get the duet-singer pairs from Spotify, applying filters on them


applied filters on the artists:
    - popularity > 50

applied filters on the tracks:
    - exactly 2 artists
    - popularity > 20
    - album -> release date : year between 1960-2018
"""


# def suitable_artist(artist_uri):
#     artist = sp.artist(artist_uri)
#     if artist['popularity'] < 50:
#         return False
#     return True


def suitable_track(track):
    artists = track['artists']
    if len(artists) != 2:
        return False
    if track['popularity'] < 20:
        return False
    # if not suitable_artist(artists[0]['uri']):
    #     return False
    # if not suitable_artist(artists[1]['uri']):
    #     return False
    return True


def unique_by_first_n(n, coll):
    seen = set()
    for item in coll:
        compare = tuple(item[:n])    # Keep only the first `n` elements in the set
        if compare not in seen:
            seen.add(compare)
            yield item


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="464dc682299743999e48f1a3339e7fa8",
                                                           client_secret="fdeaebf00a2043cba3817a8c2da977f7"))


duets = []
count = 0
genres = ['pop', 'soul', 'romance', 'rock', 'hip-hop', 'country', 'reggae', 'rap', 'disco', 'dance', 'blues']
# genres = ['pop']
for year in range(1960, 2018):
    for genre in genres:
        for i in range(0, 1000, 50):
            track_results = sp.search(q='genre:'+genre+' year:'+str(year), type='track', limit=50,
                                      offset=i)
            for idx, t in enumerate(track_results['tracks']['items']):
                if suitable_track(t):
                    count += 1
                    duets.append([t['name'], t['artists'][0]['name'], t['artists'][1]['name'],
                                  t['popularity'], year, genre])

            # print(idx, t)

# print(duets)
duets = list(unique_by_first_n(3, duets))
print(len(duets))
print(count)

duets = pd.DataFrame(duets, columns=['Track', 'Artist_1', 'Artist_2', 'Popularity', 'Year', 'Genre'])
duets.to_csv("duets.csv", index=False, encoding='utf-8-sig')
