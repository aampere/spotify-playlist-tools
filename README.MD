# spotify-playlist-tools
Provides tools for creating a Spotify playlist from a human-created text playlist, and "exploding" an existing Spotify playlist into a larger playlist.

## Summary
The Spotify API provides playlist creation and search functions, but some extra work is required to search reliably for tracks taken from a human-created text playlist. In `playlistexamples.py` I create a playlist and populate it with songs parsed from a text playlist taken from the website of a radio show. Then, I "explode" that playlist into a larger playlist which contains the full album containing each of the songs on the original playlist.

## Clever Spotify search
Although Spotify's built-in search function is quite smart, it cannot find some tracks as written by the human author of the text playlist. For instance, the playlist author has written:
> Ay-Kherel - "Tyvam Hemneri (The Rivers of Tuvai)" (Siberia)

on one line. My code correctly parses "Tyvam Hemneri (The Rivers of Tuvai)" as the title and "Ay-Kherel" as the artist, but searching these terms in Spotify brings up no results. In this is because the playlist author has used a longer version of this track's title that Spotify doesn't recognize. Similar incongruencies sometimes occur with artist names that also prevent Spotify from finding a track as written (featured artists are included/excluded in the search term, for example). 

My strategy for dealing with this is to start with the full track & artist as a search term, then remove words from the back ends of each term until Spotify finds something. In the above example, Spotify successfully locates the correct track after the title term has been pared down to just "Tyvam Hemnari".

## Playlist "explosion"
Given an existing playlist, makes a new playlist that contains the full album containing each song on the original playlist. I used to listen to whole albums, follow specific artists a lot more closely, and keep an organized library of my music. Now my music is saved in various Spotify playlists filled with one-off tracks I like or have recommended to me. "Someday I'll go listen to that whole album, I tell myself. I would probably like that." Then I forget. 😔 Playlist explosion is the answer to that problem--do a deep dive into the other work of the artists whose singles you love!

## Setup
- Create and activate virtual environment `spotify-playlist-tools-venv`.
- Install requirements: pip install -r requirements.txt
- This program requires you to have a Spotify account (free or premium), and to register an app with Spotify, which gives you the secret API keys required to modify a user's playlists. See the [Spotify API Quickstart Tutorial](https://developer.spotify.com/documentation/web-api/quick-start/) section "Set Up Your Account."
- Go to https://developer.spotify.com/dashboard/ and log in if necessary.
- Click "Create an app" and fill in the title and description fields however you like.
- Save the Client ID and the Client Secret.
- Create a `.env` file, which will save your API keys as environment variables read by the program, containing:
  > spotify_cid = "your_client_id"  
  > spotify_secret = "your_client_secret"  
  > spotify_username = "your_username"  
- Run `playlistexamples.py`. (When you run the script for the first time, a browser window may open asking you to log in to Spotify.) This script creates a playlist in your Spotify account called "Folk Bazaar" and populates it with songs from an example text playlist `exampleplaylists/playlistshort`. Then it "explodes" the playlist into a larger playlist called "Folk Bazaar (exploded)"
