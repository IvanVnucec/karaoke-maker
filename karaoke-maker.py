import sys
from youtube import Youtube
from filter import Filter
from lyrics import Lyrics
import time
import os

MIN_ARGS_LEN = 2
DOWNLOAD_FOLDER = 'download'


def main(search):
    print('*** Searching for lyrics. ***')
    ly = Lyrics()
    lyrics = ly.get_lyrics(search)
    if lyrics == []:
        print("INFO: Could not found lyrics for your search.")
        YT_search = search
        lyric = None
    else:
        # get the first one of the list
        lyric = lyrics[0]
        YT_search = f'{lyric["author"]} {lyric["songName"]}'
        print('Done.\n')

    # search youtube
    print(f"*** Searching Youtube for '{YT_search}'. ***")
    youtube = Youtube()
    songs = youtube.search(YT_search, sortByViews=False)
    # pick the first from the top of the list
    song = songs[0]
    print(f'Found {song["title"]}, {song["views"]} views, {song["link"]}\n')

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

    if lyric is not None:
        print('*** Saving lyrics to file ***')
        ly.save(folder, lyric)
        print('Done saving lyrics to file.\n')

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
