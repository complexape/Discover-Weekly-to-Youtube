import os
import base64
import pickle

from secrets import refresh_token, client_id, client_secret, playlist_id

import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

class InvalidAPICredentials(Exception):
    pass

class Spotify:
    def __init__(self,
        refresh_token: str,
        client_id: str,
        client_secret: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        """Fetches your Spotify access token."""

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
            data= {"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers= {
                "Authorization": "Basic " +  base64.b64encode(
                    bytes(f"{self.client_id}:{self.client_secret}", "ISO-8859-1")
                ).decode("ascii")
            }
        )

        response_json = response.json()
        try:
            return response_json["access_token"]
        except KeyError:
            raise InvalidAPICredentials("Invalid Spotify Credentials!")
    
    def find_playlist(self, playlist_id):
        """Gets a given Spotify playlist id's information."""

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = requests.get(query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        response_json = response.json()
        return response_json

class Youtube:
    def __init__(self):
        self.credentials = self.refresh_credentials()
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def refresh_credentials(self):
        """Gets and/or refreshes your Youtube API credentials."""

        # loads in existing credentials if they exist
        if os.path.exists('credentials.pickle'):
            print('Loading Credentials From File...')
            with open('credentials.pickle', 'rb') as token:
                credentials = pickle.load(token)
    
        # if no valid credentials available, either refresh or fetch new token.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...')
                credentials.refresh(Request()) 
            else:
                print('Fetching New Tokens...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=['https://www.googleapis.com/auth/youtube']
                )
                flow.run_local_server(
                    port=6060, prompt='consent', authorization_prompt_message=''
                )
                credentials = flow.credentials
                with open('credentials.pickle', 'wb') as f:
                    print('Saved New Credentials')
                    pickle.dump(credentials, f)
         
        return credentials
    
    def create_playlist(self, title, description):
        """Creates a playlist and returns its id."""

        create_playlist_request = self.youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": str(title),
                    "description": str(description),
                }
            }
        )

        playlist_reponse = create_playlist_request.execute()
        return playlist_reponse["id"]

    def search_and_add(self, query, playlist_id):
        """Searches for a video and adds it to the given playlist id's Youtube playlist."""

        search_response = self.youtube.search().list(
            part="snippet",q=query, maxResults=1, 
            type='video', order='relevance', topicId="/m/04rlf"
        ).execute()

        self.youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlist_id, 
                    'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': search_response["items"][0]["id"]["videoId"]
                            }
                    }
                }
        ).execute()

def main():
    youtube = Youtube()
    spotify = Spotify(refresh_token, client_id, client_secret)

    while True:
        spotify_id = playlist_id
        if not spotify_id:
            spotify_id = input("Your Spotify playlist's id: ")
        spotify_playlist = spotify.find_playlist(spotify_id)
        
        if not "error" in spotify_playlist:
            break
    
    print("Getting Spotify playlist information...")
    song_items = spotify_playlist["tracks"]["items"]
    youtube_id = youtube.create_playlist(
        spotify_playlist["name"], 
        spotify_playlist["description"]
    )

    try:
        for n, song in enumerate(song_items):

            # searches on youtube by relevance using the query term: "artist-name song-name"
            search_query = f'{song["track"]["name"]}'
            full_query = search_query
            
            # uses query: "artist-name1 artist-name2...  song-name" if multiple artists
            for artist in song["track"]["artists"]:
                full_query += f' {artist["name"]}'
            
            try:
                youtube.search_and_add(full_query, youtube_id)
                print(f"({n+1}/{len(song_items)}) added '{full_query}' to playlist")
            except IndexError:
                print(f"({n+1}/{len(song_items)}) '{search_query}' could NOT be found, skipping...")
    except HttpError as e: 
        # prompts user to delete the Youtube playlist if it's incomplete
        print(e)
        if input("Playlist is incomplete. Keep it anyways? (Y/n)").lower() not in ["y" or "yes"]: 
            youtube.playlists().delete(id=youtube_id).execute()
        exit()
    
    print(f"Complete! \nLink to playlist: https://www.youtube.com/playlist?list={youtube_id}")

if __name__ == '__main__':
    main()