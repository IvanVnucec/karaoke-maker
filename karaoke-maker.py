import sys
from youtube import Youtube
from filter import Filter
from lyrics import Lyrics

MIN_ARGS_LEN = 2
OUTPUT_FOLDER_PATH = 'download'


def main(search):
    # search youtube
    print(f"Searching Youtube for '{search}'.")
    youtube = Youtube()
    songs = youtube.search(search, sortByViews=True)

    # pick one with the most views
    song = songs[0]
    print(
        f'Choosing "{song["title"]}" with {song["views"]} views. Link: {song["link"]}')

    # download a song from youtube
    print('Downloading and converting to mp3.')
    filepath = youtube.download_and_convert_to_mp3(
        song['link'], OUTPUT_FOLDER_PATH)

    print('Filtering vocals.')
    filter = Filter()
    path = filter.extract_vocals(filepath)
    print(f'Done. Saved to {path}.')

    lyrics = Lyrics()
    lyricsText = lyrics.get_lyrics(search)
    lyrics.save(OUTPUT_FOLDER_PATH, lyricsText)  # TODO: Change output folder

    sys.exit(0)


if __name__ == "__main__":
    # get search args
    if len(sys.argv) < MIN_ARGS_LEN:
        sys.exit('Too few arguments.')

    # join list with spaces
    search = ' '.join(sys.argv[1:])

    main(search)
