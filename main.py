import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_APP_ID = os.environ['SPOTIFY_APP_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']

date_when_to_went = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
# date_when_to_went = '2000-08-12'
response = requests.get(f'https://www.billboard.com/charts/hot-100/{date_when_to_went}/')
soup = BeautifulSoup(response.text, 'html.parser')
titles = [x.getText().replace('\n', '') for x in soup.select('li > h3#title-of-a-story')]
artists = [x.getText().replace('\n', '') for x in soup.select('li > h3#title-of-a-story ~ span')]

songs = list(zip(artists, titles))
#print([song[0] for song in songs])
#print(len(titles))
#print(len(artists))


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_APP_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private"))
user_id = sp.current_user()['id']
#print(user_id)
song_uris = []
for song in songs:
    results = sp.search(q=f'track: {song[1]} artist:{song[0]}', limit=2)
    try:
        song_uris += [results['tracks']['items'][0]['uri']]
        #print(song_uris)
    except IndexError:
        continue

playlist = sp.user_playlist_create(user_id, f'{date_when_to_went} TOP 100 Billboard', public=False)
#print(playlist)

sp.playlist_add_items(playlist['id'], items=song_uris)