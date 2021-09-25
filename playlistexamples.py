import os
import dotenv
import spotifyplaylisttools as spt

#load environmental variables containing my Spotify API keys
dotenv.load_dotenv()

#set Spotify API info from environmental variables
cid = os.getenv("spotify_cid") 
secret = os.getenv("spotify_secret")
username = os.getenv("spotify_username")

#Create PlaylistMaker with API info
pm = spt.PlaylistMaker(cid,secret,username)

#Human-created text playlist taken from a radio show's website
playlistfile = open('exampleplaylists/playlistshort.txt','r', encoding="utf8")

#Set up a target Spotify playlist that we will fill with songs from the human-created text playlist
newplaylistname = "Folk Bazaar"
newplaylisturi = pm.sp.user_playlist_create(pm.username,newplaylistname,public=False)['id']

#Read the human-created text playlist and add each song successfully found to the target Spotify playlist
lines = playlistfile.readlines()
trackuris = []  
failedsearches = []  #List of songs that can't be found
for line in lines:
    track = ''
    artist = ''
    if line.find('-') != -1:
        trackparts = line.split('"')
        artistparts = line.split('-')
        if len(trackparts)<2:
            continue
        track = trackparts[1]
        artist = artistparts[0]
        uri = pm.cleverSearch(track, artist, 0)
        if uri != None:
            trackuris.append(uri)
        else:
            failedsearches.append(artist + '|' + track)
pm.addManyTracksToPlaylist(newplaylisturi,trackuris)
#The playlist "Folk Bazaar" contains 10 tracks (3 tracks from the human-created text playlist couldn't be found on Spotify)

#Create another Spotify playlist that we will "explode" the first one into.
#ie, for each song on the original playlist, this new playlist will contain the whole album containing that song.
explodedplaylistname = "Folk Bazaar (exploded)"
explodedplaylisturi = pm.sp.user_playlist_create(pm.username,explodedplaylistname,public=False)['id']
pm.explodePlaylist(newplaylisturi, explodedplaylisturi)
#The exploded playlist contains 210 tracks