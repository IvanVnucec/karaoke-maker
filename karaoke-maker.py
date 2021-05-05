import sys
from youtube import Youtube
from filter import Filter
from lyrics import Lyrics
import time
import os

MIN_ARGS_LEN = 2
DOWNLOAD_FOLDER = 'download'


def main(search, verbose):
    print('*** Searching for lyrics. ***')
    ly = Lyrics()
    lyrics = ly.get_lyrics(search)
    
    YT_search = search
    if lyrics == []:
        print("INFO: Could not found lyrics for your search.")
        lyric = None
    else:
        lyric = lyrics[0]
        if verbose:
            # list lyrics for user to choose
            for i, lyric in enumerate(lyrics, start=1):
                print(f'{i}. {lyric["author"]} {lyric["songName"]}')
            print('0. For no lyrics.')

            num = int(input('Choose lyrics: '))
            if num == 0:
                lyric = None
                YT_search = search
            elif num > len(lyrics) or num < 0:
                sys.exit('ERROR: Wrong input.')
            else:
                lyric = lyrics[num-1]
                YT_search = f'{lyric["author"]} {lyric["songName"]}'
        else:
            print(f'Found: {lyric["author"]} - {lyric["songName"]}')
    
    print('Done.\n')

    # search youtube
    print(f"*** Searching Youtube for '{YT_search}'. ***")
    youtube = Youtube()
    songs = youtube.search(YT_search, sortByViews=False)

    song = songs[0]
    if verbose:
        # list youtube songs for use to choose
        for i, song in enumerate(songs, start=1):
            print(f'{i}. {song["title"]}, {song["views"]} views, {song["link"]}')
        print('0. Exit.')

        num = int(input('Choose lyrics: '))
        if num == 0:
            print('INFO: Exiting.')
            sys.exit(0)
        elif num > len(lyrics) or num < 0:
            exit('ERROR: Wrong input.')
        else:
            song = songs[num-1]
    else:
        print(f'Found {song["title"]}, {song["views"]} views, {song["link"]}\n')

    print('Done.\n')

    # download a song from youtube
    print('*** Downloading and converting to mp3. ***')
    filepath, folder = youtube.download_and_convert_to_mp3(song['link'], DOWNLOAD_FOLDER)
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

    search_start = 1
    verbose = False
    if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
        search_start = 2
        verbose = True

    # join list with spaces
    search = ' '.join(sys.argv[search_start:])

    startTime = time.time()
    print('Starting script.\n')

    main(search, verbose)

    print(f'Done in {round(time.time() - startTime, 1)} seconds')
    sys.exit(0)
