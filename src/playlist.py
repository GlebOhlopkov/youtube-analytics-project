import json
from datetime import timedelta

import isodate

from googleapiclient.discovery import build


class PlayList():
    """Класс для ютуб-канала"""
    YOUTUBE_API_KEY = 'AIzaSyBTJjNk6LFw4u0N7pwX0SrEeVOFGp_ZVbk'

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        youtube = self.get_service()
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

    def __str__(self):
        return self.title

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        return print(json.dumps(playlists, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=PlayList.YOUTUBE_API_KEY)

    @property
    def total_duration(self):
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        total_duration = timedelta(seconds=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        likes = []
        for video in video_response['items']:
            likes.append(video['statistics']['likeCount'])
        for video in video_response['items']:
            if video['statistics']['likeCount'] == max(likes):
                return 'https://youtu.be/' + video['id']
