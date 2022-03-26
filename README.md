# Spotify Playlist to Youtube
 This is a tool for converting your Spotify playlists into a new Youtube playlist. Please keep in mind that this tool is restricted by Youtube API's quota feature. Processing larger playlists or spamming this tool may cause it to fail, more information can be [found over here](https://developers.google.com/youtube/v3/getting-started), under **Quota Usage**. If you found this tool useful, please feel free to star this repo!

## Inital Setup <a name="setup"></a>
1. Install Requirements:
    ```bash
    pip install -r requirements.txt
    ```
1. Fill in the appropriate credentials in `secrets.py`. ( <a href="#spotify">Getting your Spotify Credentials</a> )

1. Add your `client_secrets.json` file to the same directory as this repo. ( <a href="#youtube">Getting your Youtube Credentials</a> )

1. Run the Python File:
    ```bash
    python main.py
    ```

<div id="spotify"></div>

## Spotify API Credentials 

1. Go to [Spotify for Developers](https://developer.spotify.com/documentation/web-api/), navigate to your Dashboard, then create an app.

1. Once you've created an app, you'll be able to find your app's Client ID and Secret.

    ![spotify_credentials](https://raw.githubusercontent.com/complexape/Spotify-Playlist-to-Youtube/main/assets/spotify_credentials.png)

1. To save trouble, I would **strongly recommend** using this website: https://getyourspotifyrefreshtoken.herokuapp.com/ to retrieve your Spotify refresh token. Either way, you'll need your Client ID and Secret from the previous step. 
1. Voila! Now paste your Client ID, Client Secret and Refresh Token into `secrets.py`.

<div id="youtube"></div> 

## Youtube API Credentials 

1. Go to [Google Developers Console](https://console.cloud.google.com/apis/dashboard), then create a new project. After you've created a new project, enable Youtube API V3 in your project.

1. Under credentials, create an OAuth Client ID, then download the OAuth Client. Rename the downloaded JSON file to `client_secrets.json`, then move it to this repository's folder. 
