from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
import os


MAX_SEARCH_RESULTS = 3
SONG_FILENAME = 'original.mp3'

YDL_OPTIONS = {
    'quiet:': True,
    'restrictfilenames': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


class Youtube:
    def __init__(self) -> None:
        self.songFilepath = None
        self.songFilename = None
        self.songFolder = None

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
            self.songFilename = os.path.basename(msg['filename']).rsplit('.', maxsplit=1)[0] + '.mp3'
            self.songFolder = os.path.split(msg['filename'])[0]

    def download_and_convert_to_mp3(self, link, outputFolder):
        YDL_OPTIONS['outtmpl'] = f'{outputFolder}/%(title)s.%(ext)s'
        YDL_OPTIONS['progress_hooks'] = [self.__ydl_progress_hook]

        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download([link])

        # move song from downloads to its own directory with the same name as the song
        src = os.path.join(self.songFolder, self.songFilename)
        songFilenameWoExt = self.songFilename.rsplit('.', maxsplit=1)[0]
        dst = os.path.join(self.songFolder, songFilenameWoExt)
        try:
            os.mkdir(dst)
        except OSError as e: 
            if e.errno == 17: pass
        
        self.songFolder = dst
        dst = os.path.join(dst, SONG_FILENAME)
        os.replace(src, dst)

        # update song filepath
        self.songFilepath = dst

        return (self.songFilepath, self.songFolder)
