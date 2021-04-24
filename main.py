from __future__ import unicode_literals
import youtube_dl
from youtube_search import YoutubeSearch
import sys


MAX_SEARCH_RESULTS = 3


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def main():
    if len(sys.argv) < 2:
        sys.exit('Too few arguments.')

    search = ' '.join(sys.argv[1:])

    results = YoutubeSearch(search, max_results=MAX_SEARCH_RESULTS).to_dict()

    songs = []
    for result in results:
        link = 'https://www.youtube.com/watch?v=' + result['id']
        views = int(result['views'].split(' ')[0].replace('.', ''))
        songs.append((link, views))

    songLink = sorted(songs, key=lambda tup: tup[1])[-1][0]
    print(songLink)

    exit()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger()
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])


if __name__ == "__main__":
    main()
