import os
import sys

import requests
from functools import lru_cache

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# CLIENT_ID = os.environ.get("CLIENT_ID")
# CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
# logger.debug(CLIENT_ID)
# assert CLIENT_ID, "No client id in ENV"
# assert CLIENT_SECRET, "No client secret in ENV"
#




import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# scope = "user-library-read"
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

class ShuffleMethod:
    def shuffle_playlist(self, playlist_id):
        pass

from dataclasses import dataclass
import sched


@dataclass
class SpotifyTrack:
    name:str
    artist:str

def get_track_artist(track_item):
    assert  track_item
    assert "artists" in track_item.keys()

    names = []
    for artist in track_item['artists']:
        names.append(artist['name'])


    returnval = ", ".join(names)

    assert returnval
    assert isinstance(returnval, str)
    return returnval



class OffsetShuffleMethod(ShuffleMethod):
    """Offsets all items in the playlist by an amount X. ( in other words this can bring the last song to the front, and hte first song to the end"""
    def shuffle_playlist(self, playlist_id, offset=1):
        """Offsets entire playlist by an amount X.
        Negative integer moves first items to the back, pulling the list forward
        Positivte integer moves last items to the front, pushing the list back"""
        logger.info("Shuffeling playlist: %s with offset %s" % (playlist_id, offset))
        assert isinstance(playlist_id, str)
        assert isinstance(offset, int)
        assert offset, "Offset cannot be 0"

        items = sp.playlist_items(playlist_id)
        assert isinstance(items, dict)
        items = items['items']

        for item in items:
            track_artist = get_track_artist(item['track'])
            track = SpotifyTrack(item['track']['name'],track_artist)
            # logger.info(item['track']['name'])
            logger.info(track)
        if offset > 0:
            self._send_to_back(playlist_id, offset)
        else:
            self._send_to_front(playlist_id, abs(offset))


    def _send_to_back(self, playlist_id, count=1):
        """moves front x front items to the back"""
        items = sp.playlist_items(playlist_id)['items']
        assert count > 0

        num_items = len(items)
        logger.info("Sending %s items to back" % count)

        sp.playlist_reorder_items(playlist_id,
                                  range_start=0,
                                  insert_before=num_items,
                                  range_length=count)



    def _send_to_front(self, playlist_id, count):
        """brings last x items to front"""
        items = sp.playlist_items(playlist_id)['items']
        assert count > 0

        num_items = len(items)
        logger.info("Sending %s items to front" % count)

        sp.playlist_reorder_items(playlist_id,
                                  range_start=num_items- count,
                                  insert_before=0,
                                  range_length=count)


@lru_cache()
def get_playlist_by_name(playlist_name):
    if not isinstance(playlist_name,str):
        raise TypeError("playlistbyname requires str argument")

    playlists = sp.current_user_playlists()
    max_iters = 100
    iter_count = 0
    while playlists:
        iter_count += 1
        if iter_count > max_iters:
            raise Exception("Playlist not found")

        for i, playlist in enumerate(playlists['items']):
            sp_playlist_name = playlist['name']
            if playlist_name.lower() in sp_playlist_name.lower():
                return playlist

import

def main():
    max_snooze_pl = get_playlist_by_name("maximum snooze")
    shuffler = OffsetShuffleMethod()
    shuffler.shuffle_playlist(max_snooze_pl['id'], offset=-1)

if __name__ == '__main__':
    main()
