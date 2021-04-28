import sys
from youtube import Youtube
from filter import Filter
from lyrics import Lyrics
import time

MIN_ARGS_LEN = 2
DOWNLOAD_FOLDER = 'download'


def main(search):
    # search youtube
    print(f"1. Searching Youtube for '{search}'.")
    youtube = Youtube()
    songs = youtube.search(search, sortByViews=True)

    # pick one with the most views
    song = songs[0]
    print(
        f'Found "{song["title"]}" with {song["views"]} views. Link: {song["link"]}\n')

    # download a song from youtube
    print('2. Downloading and converting to mp3.')
    filepath, folder = youtube.download_and_convert_to_mp3(
        song['link'], DOWNLOAD_FOLDER)
    print('Done.\n')

    print('3. Filtering vocals. This could take a minute.')
    filter = Filter()
    filter.extract_vocals(filepath, folder)
    print(f'Done.\n')

    print('4. Searching for lyrics.')
    lyrics = Lyrics()
    lyricsText = lyrics.get_lyrics(search)
    lyrics.save(folder, lyricsText)
    print('Done.\n')

    print(f'Output folder: {folder}')


if __name__ == "__main__":
    # get search args
    if len(sys.argv) < MIN_ARGS_LEN:
        sys.exit('Too few arguments.')

    # join list with spaces
    search = ' '.join(sys.argv[1:])

    startTime = time.time()
    print('Starting script.\n')

    main(search)

    print(f'Done in {round(time.time() - startTime, 1)} seconds')
    sys.exit(0)
