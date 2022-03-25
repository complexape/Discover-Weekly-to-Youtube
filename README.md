# Spotify Playlist to Youtube
 This is a tool for converting your Spotify playlists into a new Youtube playlist. If you found this tool useful, please feel free to star this repo!

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
1. Fill in the appropriate credentials in `secrets.py`. 
    ([Getting your Spotify Credentials](##spotify))
1. Add your `client_secrets.json` file to the same directory as this repo. 
    ([Getting your Youtube Credentials](##youtube))
1. Run the Python File:
    ```bash
    python main.py
    ```
1. (Optional) Find your Spotify playlist's id, then paste it in. Your playlist's id can be found in its share link:
(eg. https://open.spotify.com/playlist/<mark>0vvXsWCC9xrXsKd4FyS8kM</mark>?si=c26a519a17144fb0)
    ```bash
    Your Spotify playlist id: "your-playlist-id-here"
    ```

## Spotify API Credentials<a name="spotify"></a>

1. Go to [Spotify for Developers](https://developer.spotify.com/documentation/web-api/), navigate to your Dashboard, then create an app. 
1. Once you've created an app, you'll be able to find your app's Client ID and Secret.

    ![spotify_credentials](assets\spotify_credentials.png)

1. To save trouble, I would **strongly recommend** using this website: https://getyourspotifyrefreshtoken.herokuapp.com/ to retrieve your Spotify refresh token. Either way, you'll need your Client ID and Secret from the previous step. 
1. Voila! Now paste your Client ID, Client Secret and Refresh Token into `secrets.py`.

## Youtube API Credentials<a name="youtube"></a>
incomplete
