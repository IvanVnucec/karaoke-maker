from __future__ import unicode_literals
import youtube_dl
from youtube_search import YoutubeSearch
import sys
import os


MAX_SEARCH_RESULTS = 3
OUTPUT_FOLDER_PATH = 'download'

songFilepath = None


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hook(msg):
    global songFilepath

    if msg['status'] == 'finished':
        songFilepath = msg['filename'].split('.')[0] + '.mp3'
        print('Converting to mp3')


def main():
    if len(sys.argv) < 2:
        sys.exit('Too few arguments.')

    search = ' '.join(sys.argv[1:])

    print(f'Searching for "{search}".')
    results = YoutubeSearch(search, max_results=MAX_SEARCH_RESULTS).to_dict()
    songs = []
    print('Done. Found:')
    for result in results:
        title = result['title']
        views = int(result['views'].split(' ')[0].replace('.', ''))
        link = 'https://www.youtube.com/watch?v=' + result['id']
        songs.append((title, link, views))
        print(f'\t"{title}" with {views} views. Link: {link}')

    songTitle, songLink, songViews = sorted(songs, key=lambda tup: tup[2])[-1]

    print(f'\nChoosing "{songTitle}" with {songViews} views. Link: {songLink}')

    ydl_opts = {
        'outtmpl': f'{OUTPUT_FOLDER_PATH}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
    }

    print(f'Downloading {songTitle}.')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songLink])

    print('Filtering vocals.')
    os.system(f'spleeter separate -p spleeter:2stems -o output {songFilepath}')

    print('Done')
    sys.exit(0)


if __name__ == "__main__":
    main()
