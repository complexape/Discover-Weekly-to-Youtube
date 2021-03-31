import os
import json
import base64
import pickle
from datetime import datetime
from secrets import *

import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SaveSongs:
    def __init__(self):
        
        self.spotify_token = self.refresh_spotify()

    def refresh_spotify(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
        data={"grant_type": "refresh_token","refresh_token": refresh_token},
        headers={"Authorization": "Basic " +  base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")})
        response_json = response.json()
        return response_json["access_token"]
        

    # returns discover weekly playlist items 
    def find_songs(self):
        print("getting songs in discover weekly...")
        query = f"https://api.spotify.com/v1/playlists/{discover_weekly_id}/tracks"
        response = requests.get(query,
            headers={"Content-Type": "application/json",
            "Authorization": f"Bearer {self.spotify_token}"})
        response_json = response.json()
        return response_json["items"]
    
    def refresh_youtube(self):
        credentials = None
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
                    scopes=['https://www.googleapis.com/auth/youtube'])
                flow.run_local_server(
                    port=6060, prompt='consent', authorization_prompt_message='')
                credentials = flow.credentials
                with open('credentials.pickle', 'wb') as f:
                    print('Saved New Credentials')
                    pickle.dump(credentials, f)
        return credentials
    
    def create_playlist(self, youtube):
        create_playlist_request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": "Spotify Discover Weekly"+datetime.now().strftime('%m/%d/%Y'),
                    "description": "All Discover Weekly Tracks from Spotify"
                }
            }
        )
        playlist_reponse = create_playlist_request.execute()
        return playlist_reponse["id"]
    
    def add_songs_to_playlist(self):
        youtube = build('youtube', 'v3', credentials=self.refresh_youtube())

        playlist_id = self.create_playlist(youtube)
        response_items = self.find_songs()
        
        songsAdded = 0
        for i in response_items:
            search_name = f'{i["track"]["artists"][0]["name"]} {i["track"]["name"]}'
            if (i["track"]["artists"].__len__() > 1):
                search_name = f'{i["track"]["artists"][0]["name"]} {i["track"]["artists"][1]["name"]} {i["track"]["name"]}'

            # search for video on youtube
            search_response = youtube.search().list(
                part="snippet",q=search_name, maxResults=1, 
                type='video', order='relevance'
            ).execute()

            # add search result to the new playlist
            youtube.playlistItems().insert(
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
            songsAdded+=1
        print(f'{str(songsAdded)} Songs added.')

if __name__ == '__main__':
    save_songs = SaveSongs()
    save_songs.add_songs_to_playlist()