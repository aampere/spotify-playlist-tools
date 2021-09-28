import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


class PlaylistMaker:
    """
    PlaylistMaker contains tools to add albums to a playlist,
    perform a smarter search using Spotify's search tool,
    "explode" a playlist into a larger playlist containing full albums,
    and other misc playlist tools.
    """
    def __init__(self, clientid, clientsecret, user):
        self.cid = clientid
        self.secret = clientsecret
        self.username = user

        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.cid, client_secret=self.secret
        )
        self.sp = spotipy.Spotify(
            client_credentials_manager=self.client_credentials_manager
        )

        self.scope = "user-library-read playlist-read-private playlist-modify-private"
        self.token = util.prompt_for_user_token(
            self.username,
            self.scope,
            client_id=self.cid,
            client_secret=self.secret,
            redirect_uri="http://localhost:8888/callback",
        )
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            print("Can't get token for", self.username)

    def getAlbumTracks(self, aid):
        albumtrackids = []
        for item in self.sp.album_tracks(aid)["items"]:
            albumtrackids.append(item["id"])
        return albumtrackids

    def addAlbumToPlaylist(self, aid, pid):
        albumtrackids = []
        for item in self.sp.album_tracks(aid)["items"]:
            albumtrackids.append(item["id"])
        self.sp.user_playlist_add_tracks(self.username, pid, albumtrackids)

    def addAlbumsToPlaylist(self, alist, pid):
        added = []
        alltracks = []
        for aid in alist:
            if aid not in added:  # don't add duplicate albums
                added.append(aid)
                self.addAlbumToPlaylist(aid, pid)
                time.sleep(0.1)
                alltracks += self.getAlbumTracks(aid)

    def listMyPlaylists(self):
        playlists = self.sp.user_playlists(self.username)
        for playlist in playlists["items"]:
            if playlist["owner"]["id"] == self.username:
                print(playlist["name"])

    def deletePlaylistsStartingWith(self, start):
        playlists = self.sp.user_playlists(self.username)
        for p in playlists["items"]:
            if p["name"].startswith("start"):
                self.sp.user_playlist_unfollow(self.username, p["uri"])

    def explodePlaylist(self, playlistid, targetplaylistid):
        """
        Takes an input playlist and "explodes" it.
        That is, for each song in the original playlist, the entire album containing that song is added to the target playlist.
        The result is a much larger playlist containing the full albums of the orignal playlist's songs.
        """
        playlistoriginal = self.sp.user_playlist(self.username, playlistid)
        playlistexpandedid = targetplaylistid
        tracks = playlistoriginal["tracks"]
        albumlist = []
        for item in tracks["items"]:
            t = item["track"]
            albumlist.append(t["album"]["id"])
        while tracks["next"]:
            tracks = self.sp.next(tracks)
            for item in tracks["items"]:
                t = item["track"]
                albumlist.append(t["album"]["id"])
        self.addAlbumsToPlaylist(albumlist, playlistexpandedid)

    def pauseSearch(self, query):
        time.sleep(0.1)
        return self.sp.search(query, limit=1, market="US")

    def cleverSearch(self, track, artist, i):
        """
        Spotify API provides the same excellent search function available in the UI app.
        It is already smart and allows for a mixture of artist name, title, misspellings, etc
        However, with a human-created playlist, there are errors, or the creator was playing a version of the song
        not available on Spotify (eg, "Remastered 2005" or "Live at X"), or the artist name differs, even though it's an identical track
        (eg, "Bruce Springsteen and the E Street Band" or a featured artist is included/excluded, etc)
        My strategy for dealing with this is to start with the full-length combined artist and track from the human-created playlist.
        If that search turns up anything, take the first result. If it doesn't, remove words from the back of the title phrase until it does.
        If still nothing turns up, search the full title, but remove words from the artist phrase.
        If still nothing turns up, remove words from both title and artist phrases until something turns up.
        """
        mintitlewords = 3
        minartistwords = 2
        titlewords = track.split(" ")
        artistwords = artist.split(" ")
        query = query = track + " " + artist
        if i == 0:
            query = track + " " + artist
        elif i == 1:
            while len(titlewords) > mintitlewords:
                query = " ".join(titlewords[0:-1]) + " " + " ".join(artistwords)
                r = self.pauseSearch(query)
                if len(r["tracks"]["items"]) > 0:
                    break
                else:
                    titlewords = titlewords[0:-1]
        elif i == 2:
            while len(artistwords) > minartistwords:
                query = " ".join(titlewords) + " " + " ".join(artistwords[0:-1])
                r = self.pauseSearch(query)
                if len(r["tracks"]["items"]) > 0:
                    break
                else:
                    artistwords = artistwords[0:-1]
        elif i == 3:
            while len(titlewords) > mintitlewords or len(artistwords) > minartistwords:
                query = (
                    " ".join(
                        titlewords[
                            0 : -1
                            if len(titlewords) > mintitlewords
                            else len(titlewords)
                        ]
                    )
                    + " "
                    + " ".join(
                        artistwords[
                            0 : -1
                            if len(artistwords) > minartistwords
                            else len(artistwords)
                        ]
                    )
                )
                r = self.pauseSearch(query)
                if len(r["tracks"]["items"]) > 0:
                    break
                else:
                    titlewords = titlewords[
                        0 : -1 if len(titlewords) > mintitlewords else len(titlewords)
                    ]
                    artistwords = artistwords[
                        0 : -1
                        if len(artistwords) > minartistwords
                        else len(artistwords)
                    ]
        else:
            print("XXXXX:", query)
            return None
        r = self.pauseSearch(query)
        if len(r["tracks"]["items"]) > 0:
            print("found:", query)
            return r["tracks"]["items"][0]["id"]  # return found uri
        else:
            return self.cleverSearch(track, artist, i + 1)

    def addManyTracksToPlaylist(self, playlisturi, largeurilist):
        """
        The API function user_playlist_add_tracks only allows you to add 100 tracks at once.
        This is a convenience function that can add a large list of tracks 100 at a time.
        """
        i = 0
        j = 100
        while i < len(largeurilist):
            self.sp.user_playlist_add_tracks(
                self.username, playlisturi, largeurilist[i:j]
            )
            i = i + 100
            j = j + 100
            time.sleep(0.1)
