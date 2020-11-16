from typing import Dict

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from echis.modules.share_playlist import Deezer, Share, Spotify
from echis.modules.token_authorization import SpotifyAuthorization


class MockResponseWithData:
    @staticmethod
    def json() -> Dict:
        return {
            "id": "6492294924",
            "type": "playlist",
            "creator": {
                "name": "random",
            },
            "tracks": {
                "data": [
                    {
                        "id": "82740060",
                        "title": "Fire Up The Night",
                        "rank": "411532",
                        "time_add": 1567684631,
                        "artist": {
                            "id": "407259",
                            "name": "New Medicine",
                        },
                        "album": {
                            "id": "8310422",
                            "title": "Breaking The model",
                            "cover_big": "https://e-cdns-images.dzcdn.net/images/cover"
                                            "/5bf40e45c5aba44a00c6afe697b0a5b9/250x250-000000-80-0-0.jpg "
                        }
                    }
                ],
            }
        }


class MockResponseWithNoData:
    @staticmethod
    def json() -> Dict:
        return {}


class MockSpotifyData:
    @staticmethod
    def json() -> Dict:
        return {
            "items": [
                {
                    "added_at": "2017-09-01T13:46:42Z",
                    "added_by": {
                        "id": "test"
                    },
                    "track": {
                        "album": {
                            "artists": [
                                {
                                    "id": "dfasd2q1asda",
                                    "name": "test"
                                }
                            ],
                            "id": "6gLBQlOZ3j7SND5BLbLkT7",
                            "images": [
                                {
                                    "height": 640,
                                    "url": "https://i.scdn.co/image/ab67616d0000b27377fedcd872b7ebaa93f80f23",
                                    "width": 640
                                }
                            ],
                            "name": "test"
                        },
                        "artists": [
                            {
                                "id": "asdasfwzs das",
                                "name": "test"
                            }
                        ],
                        "id": "asdagasddar213124",
                        "name": "This Is Not Goodbye",
                        "popularity": 42
                    }
                }
            ]
        }


class MockTokenFromSpotify:
    @staticmethod
    def json() -> Dict:
        return {
            'access_token': 'tokedasdasdasd',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': ''
        }

    @property
    def status_code(self) -> int:
        return 200


class PlaylistNotFoundMock:
    @staticmethod
    def json() -> Dict:
        return {"error": {"status": 404}}


class PlaylistExistMock:
    @staticmethod
    def json() -> Dict:
        return {"random_playlist": {"status": 200}}


@pytest.fixture()
def deezer() -> Deezer:
    return Deezer()


@pytest.fixture()
def spotify() -> Spotify:
    return Spotify()


def mock_get_empty_data(*args, **kwargs) -> MockResponseWithNoData:
    return MockResponseWithNoData()


def mock_with_data(*args, **kwargs) -> MockResponseWithData:
    return MockResponseWithData()


def mock_spotify_get_with_data(*args, **kwargs) -> MockSpotifyData:
    return MockSpotifyData()


def mock_token(*args, **kwargs):
    return "123"


def test_deezer_with_get_last_from_deezer(monkeypatch: MonkeyPatch, deezer: Deezer):
    monkeypatch.setattr(requests, "get", mock_with_data)
    deezer.fetch(playlist_id=45489721)
    last = deezer.get_latest

    assert last.title is not None
    assert last.song_id is not None
    assert isinstance(last, Share)


def test_get_latest_with_no_return_data_from_deezer(monkeypatch: MonkeyPatch, deezer: Deezer):
    monkeypatch.setattr(requests, "get", mock_get_empty_data)

    with pytest.raises(Exception) as exception_meme:
        deezer.fetch(playlist_id=45489721)
        _ = deezer.get_latest
        assert exception_meme.value == "Cannot download playlist"


@pytest.mark.parametrize("take, expect", (
        [PlaylistNotFoundMock(), False],
        [PlaylistExistMock(), True]
))
def test_deezer_check_playlist_for_deezer(monkeypatch: MonkeyPatch, deezer: Deezer, take, expect):
    def get_mock(*args, **kwargs):
        return take

    monkeypatch.setattr(requests, "get", get_mock)
    is_exist = deezer.playlist_is_exists("908622995")

    assert is_exist is expect


def test_get_lasted_with_data_from_spotify(monkeypatch: MonkeyPatch, spotify: Spotify):
    monkeypatch.setattr(SpotifyAuthorization, "get_token", mock_token)
    monkeypatch.setattr(requests, "get", mock_spotify_get_with_data)
    spotify.fetch(playlist_id="sdij9iuqsajhd")
    last = spotify.get_latest

    assert last.title is not None
    assert last.song_id is not None
    assert isinstance(last, Share)


def test_get_latest_with_no_return_data_from_spotify(monkeypatch: MonkeyPatch, spotify: Spotify):
    monkeypatch.setattr(requests, "get", mock_get_empty_data)
    with pytest.raises(Exception) as exception_meme:
        spotify.fetch(playlist_id="sdij9iuqsajhd")
        _ = deezer.get_latest
        assert exception_meme.value == "Cannot download playlist"


@pytest.mark.parametrize("take, expect", (
        [PlaylistNotFoundMock(), False],
        [PlaylistExistMock(), True]
))
def test_deezer_check_playlist_for_spotify(monkeypatch: MonkeyPatch, spotify: Spotify, take, expect):
    def get_mock(*args, **kwargs):
        return take

    monkeypatch.setattr(requests, "get", get_mock)
    monkeypatch.setattr(SpotifyAuthorization, "get_token", mock_token)
    is_exist = spotify.playlist_is_exists("908622995")

    assert is_exist is expect