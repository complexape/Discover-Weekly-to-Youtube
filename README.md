# Discover-Weekly-to-Youtube
 converts your Discover Weekly playlist on Spotify into a new Youtube playlist.

### Note:
When using this script often or trying to process a big playlist, please note that Youtube's API has a quota. ([more info here](https://developers.google.com/youtube/v3/getting-started))

## Table of Contents
1. [Initial Setup](#setup)
2. [Usage](#usage)
3. [Spotify API](##spotify)
4. [YouTube API](#youtube)
## Inital Setup <a name="setup"></a>
1. Install Requirements:
```bash
pip install -r requirements.txt
```
2. Get Spotify Token
3. Get Youtube Token
4. Run the Python File:
```bash
python main.py
```

## Usage <a name="usage"></a>
1. Copy the link to your playlist (your playlist's id is a part of the link. https://open.spotify.com/playlist/<mark>0vvXsWCC9xrXsKd4FyS8kM?</mark>si=c26a519a17144fb0), and add it to `secrets.py`.
![Copy Spotify Playlist Id](assets\copyid.PNG)
2. Run the Python File:
```bash
python main.py
```

<a name="spotify"></a>
## Spotify API
to do...

<a name="youtube"></a>
## Youtube API 
to do...
