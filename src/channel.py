import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    YOUTUBE_API_KEY = 'AIzaSyBTJjNk6LFw4u0N7pwX0SrEeVOFGp_ZVbk'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=Channel.YOUTUBE_API_KEY)
        channel_info = youtube.channels().list(id=self.channel_id, part='snippet,statistics')
        self.response = channel_info.execute()
        self.id = self.response['items'][0]['id']
        self.title = self.response['items'][0]['snippet']['title']
        self.description = self.response['items'][0]['snippet']['description']
        self.url = self.response['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.response['items'][0]['statistics']['subscriberCount']
        self.video_count = self.response['items'][0]['statistics']['videoCount']
        self.view_count = self.response['items'][0]['statistics']['viewCount']

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=Channel.YOUTUBE_API_KEY)
        channel_info = youtube.channels().list(id=self.channel_id, part='snippet,statistics')
        response = channel_info.execute()
        return print(json.dumps(response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        pass

    def to_json(self, file_name):
        data = {}
        data[self.channel_id].append({
            'channel_id': self.id,
            'channel_tittle': self.title,
            'channel_description': self.description,
            'channel_url': self.url,
            'channel_sub_count': self.subscriber_count,
            'channel_video_count': self.video_count,
            'channel_view_count': self.view_count
        })
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file)
