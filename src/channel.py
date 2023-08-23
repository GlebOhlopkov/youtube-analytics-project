import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    YOUTUBE_API_KEY = 'AIzaSyBTJjNk6LFw4u0N7pwX0SrEeVOFGp_ZVbk'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=Channel.YOUTUBE_API_KEY)
        channel_info = youtube.channels().list(id="UCwHL6WHUarjGfUM_586me8w", part='snippet,statistics')
        response = channel_info.execute()
        return print(json.dumps(response, indent=2, ensure_ascii=False))
