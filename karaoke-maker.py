import sys
from youtube import Youtube
from filter import Filter

OUTPUT_FOLDER_PATH = 'download'


def main():
    # get search args
    if len(sys.argv) < 2:
        sys.exit('Too few arguments.')
    search = ' '.join(sys.argv[1:])

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

    sys.exit(0)


if __name__ == "__main__":
    main()
