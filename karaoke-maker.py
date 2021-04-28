import sys
from youtube import Youtube
from filter import Filter
from lyrics import Lyrics
import time
import os

MIN_ARGS_LEN = 2
DOWNLOAD_FOLDER = 'download'


def main(search):
    # search youtube
    print(f"*** Searching Youtube for '{search}'. ***")
    youtube = Youtube()
    songs = youtube.search(search, sortByViews=True)
    print('Found:')

    # pick one with the most views
    for i, song in enumerate(songs, start=1):
        print(f'{i}. {song["title"]} {song["views"]} {song["link"]}')

    try:
        pick = int(input('\nChoose one song frow the list: '))
        if pick > len(songs):
            exit()
    except ValueError:
        exit()

    song = songs[pick - 1]

    # download a song from youtube
    print('*** Downloading and converting to mp3. ***')
    filepath, folder = youtube.download_and_convert_to_mp3(
        song['link'], DOWNLOAD_FOLDER)
    print('Done.\n')

    print('*** Filtering vocals. This could take a minute. ***')
    filter = Filter()
    vocals, instrum = filter.extract_vocals(filepath, folder)
    filter.mix_vocals_with_instrum(folder, vocals, instrum)
    print(f'Done.\n')

    print('*** Searching for lyrics. ***1')
    lyrics = Lyrics()
    lyricsText = lyrics.get_lyrics(search)
    lyrics.save(folder, lyricsText)
    print('Done.\n')

    absPath = os.path.abspath(folder)
    print(f'Output folder: {absPath}')


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
