import googlesearch as Google
import requests
from bs4 import BeautifulSoup


SITE = 'tekstovi.net'
WRITE = 'w+'
LYRICS_TXT = 'lyrics.txt'


class Lyrics:
    def __init__(self) -> None:
        pass

    def __search(self, str, numRes=3):
        search = f'site:{SITE} {str}'
        return Google.search(search, numRes)[0]

    def get_lyrics(self, str):
        link = self.__search(str)

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        author = soup.find('h1', class_='lyricCapt').text + '\n'
        songName = soup.find('h2', class_='lyricCapt').text + '\n\n'
        lyrics = soup.find_all('p', class_='lyric')

        retval = []
        retval.append(author)
        retval.append(songName)
        for lyric in lyrics:
            retval.append(lyric.text)

        return retval

    def save(self, path, lyrics):
        # TODO: Change path to OS independant
        file = open(path + '/' + LYRICS_TXT, WRITE)
        file.writelines(lyrics)
        file.close()
