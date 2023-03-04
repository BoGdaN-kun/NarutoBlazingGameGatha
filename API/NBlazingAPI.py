from typing import List

import lxml.html
from lxml import etree

import requests
from bs4 import BeautifulSoup
import jsonpickle

from API.CharacterInfo import CharacterInfo
from API.NarutoCharacter import Character
from API.Tables import Tables


class NBlazingApi:
    def __init__(self):
        self.character = []
        self.charactersURL = "https://naruto-blazing.fandom.com/wiki/Encyclopedia"
        self.fandomSite = "https://naruto-blazing.fandom.com"

    def searchCharacter(self, name: str) -> List:
        """
        Searches for all characters that match the given names
        :param name: name of the character to search for
        :return:  a list of all the characters that match the name
        """

        # get the page and initialize the soup

        page = requests.get(self.charactersURL)
        soup = BeautifulSoup(page.content, "html.parser")

        # get the table with all the characters

        table = soup.find("table", class_="table")

        # get all the rows in the table
        rows = table.find_all('tr')

        # get the header of the table and remove the \n and . from the header
        header = [header.text for header in rows[0].find_all('th')]
        header = [res.replace('\n', '') for res in header]
        header = [res.replace('.', '') for res in header]
        lst = [header]

        # get all the characters that match the name
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            if any(name in substring for substring in result):
                result = [res.replace('\n', '') for res in result]
                links = [data for data in row.find_all('a', href=True)]
                if index > 0:
                    try:

                        # We try to fill in all the links for the character needed
                        result[1] = links[0]['href']
                        result[4] = self.fandomSite + links[2]['href']
                        result.append(links[1]['href'])
                        result[-1] = self.fandomSite + result[-1]

                        # Create a character object
                        character = Character(result[0], result[1], result[2], result[3], result[4], result[5],
                                              result[6])
                        result = character
                    except:
                        continue

                lst.append(result)
        return lst

    def getCharacterByURL(self, url: str) -> Character:
        page = requests.get(self.charactersURL)
        soup = BeautifulSoup(page.content, "html.parser")

        # get the table with all the characters

        table = soup.find("table", class_="table")

        # get all the rows in the table
        rows = table.find_all('tr')
        lst = []
        link = ''
        # get all the characters that match the name
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            links = [data for data in row.find_all('a', href=True)]
            if len(links) > 1:
                link = self.fandomSite + links[1]['href']
            if len(links) > 1 and url == link:
                result = [res.replace('\n', '') for res in result]
                if index > 0:
                    try:

                        # We try to fill in all the links for the character needed
                        result[1] = links[0]['href']
                        result[4] = self.fandomSite + links[2]['href']
                        result.append(links[1]['href'])
                        result[-1] = self.fandomSite + result[-1]

                        # Create a character object
                        character = Character(result[0], result[1], result[2], result[3], result[4], result[5],
                                              result[6])
                        result = character
                        return result
                    except:
                        continue

    def getCharacters(self, name: str) -> str:
        """
        Returns a json format of all the characters that match the given name
        :param name: name of the character
        :return: a json format of all the characters that match the name as a string
        """
        characters = self.searchCharacter(name)

        # remove the header
        characters.pop(0)

        # convert the list to json format
        CharacterJsonFormat = jsonpickle.dumps(characters, unpicklable=False, indent=4)

        return CharacterJsonFormat

    def getCharacterInfo(self, url: str):
        """
        Gets the info of the character
        :param url: url of the character
        :return: A json format of the character info
        """
        basicInfo = self.getCharacterByURL(url)

        tables = Tables(url)
        stars = tables.Stars()
        miscs = tables.LeftTableCard()
        skill = tables.FieldBuddyStats()
        abilities = tables.Abilities(stars)
        status = tables.Status()
        jutsu = tables.Jutsu(stars)

        characterInfo = CharacterInfo(basicInfo.Index, basicInfo.Picture,
                                      basicInfo.Name, basicInfo.Rarity,
                                      basicInfo.Element, basicInfo.Type,
                                      basicInfo.CharacterURL, miscs, status, skill, abilities, jutsu)
        CharacterJsonFormat = jsonpickle.dumps(characterInfo, unpicklable=False, indent=4)

        return CharacterJsonFormat


n = NBlazingApi()

# naruto = n.getCharacters('Naruto')
# js = jsonpickle.loads(naruto)
# n.getCharacterInfo('https://naruto-blazing.fandom.com/wiki/Minato_Namikaze_%22Unfading_Courage%22_(%E2%98%855)')
x = n.getCharacterInfo('https://naruto-blazing.fandom.com/wiki/Naruto_Uzumaki_%22The_Worst_Loser%22_(%E2%98%853)')
js = jsonpickle.dumps(n)
print(js)
f = open("cev.json", 'wb')
f.write(x.encode('ascii', 'ignore'))
f.close()

# print(js)
# print()
# n.getCharacterInfo(js[0]['CharacterURL'])

# print(js)

# page = requests.get(js[0]["CharacterURL"])
# soup = BeautifulSoup(page.content, "html.parser")
# f = open("cev.json",'wb')
# f.write(soup.encode('ascii', 'ignore'))
# f.close()
