from typing import List

import requests
from bs4 import BeautifulSoup
import jsonpickle

from API.NarutoCharacter import Character


class NBlazingApi:
    def __init__(self):
        self.character = []
        self.charactersURL = "https://naruto-blazing.fandom.com/wiki/Encyclopedia"

    def searchCharacter(self, name: str) -> List:
        page = requests.get(self.charactersURL)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", class_="table")
        rows = table.find_all('tr')  # find all table rows
        header = [header.text for header in rows[0].find_all('th')]
        header = [res.replace('\n', '') for res in header]
        header = [res.replace('.', '') for res in header]
        lst = []
        lst.append(header)
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            if any(name in substr for substr in result):
                result = [res.replace('\n', '') for res in result]  # remove \n
                links = [data for data in row.find_all('a', href=True)]

                if index > 0:
                    try:
                        result[1] = links[0]['href']
                        result[4] = "https://naruto-blazing.fandom.com/" + links[2]['href']
                        result.append( links[1]['href'])
                        result[-1] = "https://naruto-blazing.fandom.com/" + result[-1]
                        #print(result)
                        character = Character(result[0], result[1], result[2], result[3], result[4], result[5],
                                              result[6])
                        result = character
                    except:
                        continue

                lst.append(result)

        return lst

    def getCharacter(self, name):
        characters = self.searchCharacter(name)
        characters.pop(0)
        CharacterJsonFormat = jsonpickle.dumps(characters, unpicklable=False, indent=4)
        return CharacterJsonFormat


n = NBlazingApi()

n = n.getCharacter('Naruto')
# js = jsonpickle.loads(n)
# print(js)

# page = requests.get(js[0]["Link"])
# soup = BeautifulSoup(page.content, "html.parser")
# f = open("cev.json",'wb')
# f.write(soup.encode('ascii', 'ignore'))
# f.close()
