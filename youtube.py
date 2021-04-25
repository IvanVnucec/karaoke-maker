from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

songFilepath = None


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


MAX_SEARCH_RESULTS = 3

YDL_OPTIONS = {
    'restrictfilenames': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger()
}


class Youtube:
    def __init__(self) -> None:
        self.songFilepath = None

    def search(self, keys, max_results=MAX_SEARCH_RESULTS, sortByViews=True):
        results = VideosSearch(keys, limit=max_results).result()['result']

        songs = []
        for result in results:
            title = result['title']
            views = int(result['viewCount']['text'].split(' ')[0].replace(',', ''))
            link = result['link']
            songs.append(dict(title=title, link=link, views=views))

        if sortByViews:
            return sorted(songs, key=lambda tup: tup['views'], reverse=True)
        else:
            return songs

    def __ydl_progress_hook(self, msg):
        if msg['status'] == 'finished':
            self.songFilepath = msg['filename'].rsplit('.', maxsplit=1)[0] + '.mp3'

    def download_and_convert_to_mp3(self, link, outputFolder):
        YDL_OPTIONS['outtmpl'] = f'{outputFolder}/%(title)s.%(ext)s'
        YDL_OPTIONS['progress_hooks'] = [self.__ydl_progress_hook]

        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download([link])

        return self.songFilepath
