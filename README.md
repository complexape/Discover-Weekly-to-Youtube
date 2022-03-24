# Spotify Playlist to Youtube
 This is a tool for converting your Spotify playlists into a new Youtube playlist. if you found this tool useful, starring this post would be very much appreciated. 

(Note: Please keep in mind that this tool is restricted by the Youtube API's quota feature. Processing larger playlists or spamming this tool may cause it to fail, more info can be [found over here](https://developers.google.com/youtube/v3/getting-started), under **Quota Usage**.)

## Table of Contents
1. [Initial Setup](#setup)
1. [Usage](#usage)
1. [Spotify API](##spotify)
1. [YouTube API](#youtube)

## Inital Setup <a name="setup"></a>
1. Install Requirements:
```bash
pip install -r requirements.txt
```
1. Fill in the appropriate credentials in "secrets.py". 
    1. [Getting your Spotify Credentials](##spotify)
1. Add your "client_secrets.json" file 
    1. [Getting your Youtube Credentials](##youtube)
1. Run the Python File:
    ```bash
    python main.py
    ```
1. (Optional) Find your Spotify playlist's id, then paste it in. 
    ```bash
        Your Spotify playlist id: "Your 
    ```

## Usage <a name="usage"></a>
1. Copy the link to your playlist (your playlist's id is a part of the link. https://open.spotify.com/playlist/<mark>0vvXsWCC9xrXsKd4FyS8kM?</mark>si=c26a519a17144fb0), and add it to `secrets.py`.
![Copy Spotify Playlist Id](assets\copyid.PNG)
2. Run the Python File:
```bash
python main.py
```

## Spotify API <a name="spotify"></a>

Create spotify app

Get client id and secret

use client id and secret with this website to get refresh token
https://getyourspotifyrefreshtoken.herokuapp.com/

<a name="youtube"></a>
## Youtube API 
to do...
