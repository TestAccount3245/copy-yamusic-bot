from yandex_music import ClientAsync

from app.core.exceptions import AuthError, NotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)


class YandexMusicService:
    def __init__(self, token: str | None = None):
        if not token:
            raise AuthError("Yandex Music token required. Use /link to connect your account.")
        self._token = token
        self._client: ClientAsync | None = None

    async def _get_client(self) -> ClientAsync:
        if self._client is None:
            self._client = await ClientAsync(self._token).init()
        return self._client

    async def search(self, query: str, search_type: str = "track") -> dict:
        client = await self._get_client()
        result = await client.search(query, type_=search_type)
        if not result:
            return {"tracks": [], "albums": [], "artists": []}

        tracks = []
        if result.tracks:
            for t in result.tracks.results:
                tracks.append(self._format_track(t))

        albums = []
        if result.albums:
            for a in result.albums.results:
                albums.append(self._format_album_brief(a))

        artists = []
        if result.artists:
            for a in result.artists.results:
                artists.append(self._format_artist_brief(a))

        return {"tracks": tracks, "albums": albums, "artists": artists}

    async def get_track(self, track_id: str) -> dict:
        client = await self._get_client()
        tracks = await client.tracks([track_id])
        if not tracks:
            raise NotFoundError(f"Track {track_id} not found")
        t = tracks[0]
        return self._format_track(t)

    async def get_album(self, album_id: str) -> dict:
        client = await self._get_client()
        album = await client.albums_with_tracks(int(album_id))
        if not album:
            raise NotFoundError(f"Album {album_id} not found")

        tracks = []
        if album.volumes:
            for volume in album.volumes:
                for t in volume:
                    tracks.append(self._format_track(t))

        cover_url = None
        if album.cover_uri:
            cover_url = f"https://{album.cover_uri.replace('%%', '400x400')}"

        return {
            "id": str(album.id),
            "title": album.title,
            "artist": ", ".join(a.name for a in album.artists) if album.artists else "Unknown",
            "year": album.year,
            "cover_url": cover_url,
            "tracks": tracks,
            "track_count": album.track_count,
        }

    async def get_artist(self, artist_id: str) -> dict:
        client = await self._get_client()
        # Get artist brief info (includes top tracks)
        artist_info = await client.artists([int(artist_id)])
        if not artist_info:
            raise NotFoundError(f"Artist {artist_id} not found")

        artist = artist_info[0]

        # Get top tracks
        top_tracks_result = await client.artists_tracks(int(artist_id), page_size=10)
        top_tracks = []
        if top_tracks_result:
            for t in top_tracks_result.tracks:
                top_tracks.append(self._format_track(t))

        # Get albums
        albums_result = await client.artists_direct_albums(int(artist_id), page_size=20)
        albums = []
        if albums_result:
            for a in albums_result.albums:
                albums.append(self._format_album_brief(a))

        cover_url = None
        if artist.cover and artist.cover.uri:
            cover_url = f"https://{artist.cover.uri.replace('%%', '400x400')}"

        return {
            "id": str(artist.id),
            "name": artist.name,
            "cover_url": cover_url,
            "top_tracks": top_tracks,
            "albums": albums,
        }

    async def get_wave(self) -> list[dict]:
        client = await self._get_client()
        try:
            station_result = await client.rotor_station_tracks("user:onyourwave")
            tracks = []
            if station_result and station_result.sequence:
                for item in station_result.sequence[:20]:
                    if item.track:
                        tracks.append(self._format_track(item.track))
            return tracks
        except Exception as e:
            logger.warning("Failed to fetch wave", error=str(e))
            return []

    async def get_download_info(self, track_id: str) -> list:
        client = await self._get_client()
        info = await client.tracks_download_info(track_id, get_direct_links=True)
        return info or []

    @staticmethod
    def _format_track(track) -> dict:
        cover_url = None
        if track.cover_uri:
            cover_url = f"https://{track.cover_uri.replace('%%', '200x200')}"

        artists_str = ", ".join(a.name for a in track.artists) if track.artists else "Unknown"

        return {
            "id": str(track.id),
            "title": track.title or "Unknown",
            "artist": artists_str,
            "album": track.albums[0].title if track.albums else None,
            "cover_url": cover_url,
            "duration_sec": (track.duration_ms or 0) // 1000,
        }

    @staticmethod
    def _format_album_brief(album) -> dict:
        cover_url = None
        if album.cover_uri:
            cover_url = f"https://{album.cover_uri.replace('%%', '200x200')}"
        return {
            "id": str(album.id),
            "title": album.title,
            "artist": ", ".join(a.name for a in album.artists) if album.artists else "Unknown",
            "year": album.year,
            "cover_url": cover_url,
        }

    @staticmethod
    def _format_artist_brief(artist) -> dict:
        cover_url = None
        if artist.cover and artist.cover.uri:
            cover_url = f"https://{artist.cover.uri.replace('%%', '200x200')}"
        return {
            "id": str(artist.id),
            "name": artist.name,
            "cover_url": cover_url,
        }
