import googlesearch as Google
import requests
from bs4 import BeautifulSoup
import os

SITE = 'tekstovi.net'
WRITE = 'w+'
LYRICS_TXT = 'lyrics.txt'


class Lyrics:
    def __init__(self) -> None:
        self.links = None

    def __search(self, str, numRes=3):
        search = f'site:{SITE} {str}'
        return Google.search(search, numRes)

    def get_lyrics(self, str):
        self.links = self.__search(str)

        retval = []

        for link in self.links:
            try:
                page = requests.get(link)
                soup = BeautifulSoup(page.content, 'html.parser')
                author = soup.find('h1', class_='lyricCapt').text
                songName = soup.find('h2', class_='lyricCapt').text
                text = ' '.join(
                    [word.text for word in soup.find_all('p', class_='lyric')])
            except:
                pass
            else:
                retval.append(dict(author=author, songName=songName, text=text))

        return retval

    def save(self, path, lyrics):
        path = os.path.join(path, LYRICS_TXT)
        file = open(path, WRITE)

        lyrics_str = f'{lyrics["author"]}\n'
        lyrics_str += f'{lyrics["songName"]}\n\n'
        lyrics_str += lyrics["text"]

        file.writelines(lyrics_str)
        file.close()
