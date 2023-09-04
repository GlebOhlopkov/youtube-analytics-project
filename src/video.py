import json

from googleapiclient.discovery import build


class Video():
    """Класс для ютуб-канала"""
    YOUTUBE_API_KEY = 'AIzaSyBTJjNk6LFw4u0N7pwX0SrEeVOFGp_ZVbk'

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._video_id = video_id
        video = self.get_service()
        video_response = video.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self._video_id
                                               ).execute()
        self.id = video_response['items'][0]['id']
        self.title = video_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtu.be/' + video_id
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        video = self.get_service()
        video_response = video.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self._video_id
                                               ).execute()
        return print(json.dumps(video_response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=Video.YOUTUBE_API_KEY)


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        playlist = self.get_service()
        playlist_videos = playlist.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.id_video = playlist_videos['items'][0]['id']
        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = 'https://www.youtu.be/' + video_id
        self.view_count = playlist_videos['items'][0]['statistics']['viewCount']
        self.like_count = playlist_videos['items'][0]['statistics']['likeCount']
        self.id_playlist = playlist_videos['items'][0]['snippet']['channelId']
