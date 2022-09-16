import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# billboard section

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

resource = requests.get(URL).text
soup = BeautifulSoup(resource, "html.parser")

song_tags = soup.find_all("h3", id="title-of-a-story", class_="u-letter-spacing-0021")
trash = ["Songwriter(s):", "Producer(s):", "Imprint/Promotion Label:"]
top = []
for song in song_tags:
    text = song.getText().strip()
    if text not in trash:
        top.append(text)

print(top)


# spotify section

# import your credentials as environment variable
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_ID = os.environ["USER_ID"]

URL_REDIRECT = "http://example.com"
SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=URL_REDIRECT,
                                               scope=SCOPE,
                                               cache_path="token.txt"))

songs_uri = []
for song in top:
    results = sp.search(q=song, type='track')
    uri = results["tracks"]["items"][0]["uri"]
    songs_uri.append(uri)


playlist_name = f"{date} Billboard Top 100"
create = sp.user_playlist_create(USER_ID, playlist_name, public=False, collaborative=False, description="")
playlist_id = create["id"]
sp.playlist_add_items(playlist_id, songs_uri, position=None)
