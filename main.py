import os
import base64
import pickle
from datetime import datetime

from secrets import refresh_token, client_id, client_secret, discover_weekly_id

import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

class SpoitifyToYT:
    def __init__(self):
        self.spotify_token = self.refresh_spotify()

    # returns an access token given a client id and client secret
    def refresh_spotify(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post( query,
            data= {"grant_type": "refresh_token",
                "refresh_token": refresh_token},
            headers= {
                "Authorization": "Basic " +  base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")})
        response_json = response.json()
        return response_json["access_token"]
        
    # returns discover weekly playlist items 
    def find_dw_songs(self):
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
                    "title": "Spotify Discover Weekly "+datetime.now().strftime('%m/%d/%Y'),
                    "description": "Your Discover Weekly Playlist imported to Youtube."
                }
            }
        )
        playlist_reponse = create_playlist_request.execute()
        return playlist_reponse["id"]

    def add_songs_to_playlist(self):
        # authorizes youtube and sets up playlist
        credentials = self.refresh_youtube()
        youtube = build('youtube', 'v3', credentials=credentials)
        
        playlist_id = self.create_playlist(youtube)

        spotify_songs = self.find_dw_songs()
        try:
            for n, i in enumerate(spotify_songs):

                # searches on youtube by relevance using the query "artist-name song-name"
                search_query = f'{i["track"]["name"]}'
                for n, artist in enumerate(i["track"]["artists"]):
                    search_query += f' {artist["name"]}'

                search_response = youtube.search().list(
                    part="snippet",q=search_query, maxResults=1, 
                    type='video', order='relevance', topicId="/m/04rlf"
                ).execute()

                if not search_response:
                    print(f"({n}/{len(spotify_songs)}) '{search_query}' NOT FOUND skipping...")
                    continue
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
                print(f"({n}/{len(spotify_songs)}) added '{search_query}' to playlist")
        except HttpError as e:
            # deletes incomplete playlist
            youtube.playlists().delete(id=playlist_id).execute()
            print(e)
            exit()

    
        print(f"Complete! Link to playlist: {playlist_id}")

def main():
    save_songs = SpoitifyToYT()
    save_songs.add_songs_to_playlist()

if __name__ == '__main__':
    main()