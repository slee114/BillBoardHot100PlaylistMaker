from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = str(input("What year do you want to travel to? YYYY-MM-DD: "))
URL = "https://www.billboard.com/charts/hot-100/" + date
song_list = []
CLIENT_ID = "Spotipy API Client ID"
CLIENT_SECRET = "Spotipy API Client Secret ID"
song_uris = []


response = requests.get(URL)


soup = BeautifulSoup(response.text, "html.parser")
song_name = soup.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
for songs in song_name:
    song_text = songs.getText()
    song_text = song_text.replace("\n", "")
    song_text = song_text.replace("\t", "")
    song_list.append(song_text)

print(song_list)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com", scope="playlist-modify-private", show_dialog=True, cache_path="token.txt"))


user_id = sp.current_user()["id"]
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} is not available on Spotify. It has been skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)