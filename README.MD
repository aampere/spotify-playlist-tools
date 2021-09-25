# spotify-playlist-tools
Provides tools for creating a Spotify playlist from a human-created text playlist, and "exploding" an existing Spotify playlist into a larger playlist.

## Summary
The Spotify API provides playlist creation and search functions, but some extra work is required to search reliably for tracks taken from a human-created text playlist. In playlistexamples.py I create a playlist and populate it with songs parsed from a text playlist, playlistsmall.txt, taken from the website of a radio show. Then, I "explode" that playlist into a larger playlist which contains the full album containing each of the songs on the original playlist.

## Clever Spotify search
Although Spotify's built-in search function is quite smart, it cannot find some tracks as written by the human author of the text playlist. For instance, the playlist author has written:
> Ay-Kherel - "Tyvam Hemneri (The Rivers of Tuvai)" (Siberia)

on one line. My code correctly parses "Tyvam Hemneri (The Rivers of Tuvai)" as the title and "Ay-Kherel" as the artist, but searching these terms in Spotify brings up no results. In this is because the playlist author has used a longer version of this track's title that Spotify doesn't recognize. Similar incongruencies sometimes occur with artist names that also prevent Spotify from finding a track as written (featured artists are included/excluded in the search term, for example). 

My strategy for dealing with this is to start with the full track & artist as a search term, then remove words from the back ends of each term until Spotify finds something. In the above example, Spotify successfully locates the correct track after the title term has been pared down to just "Tyvam Hemnari".

## Playlist "explosion"
Given an existing playlist, makes a new playlist that contains the full album containing each song on the original playlist. I used to listen to whole albums, follow specific artists a lot more closely, and keep an organized library of my music. Now my music is saved in various Spotify playlists filled with one-off tracks I like or have recommended to me. "Someday I'll go listen to that whole album, I tell myself. I would probably like that." Then I forget. 😔 Playlist explosion is the answer to that problem--do a deep dive into the other work of the artists whose singles you love!