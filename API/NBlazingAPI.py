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

    def searchAllCharactersWithName(self, name: str) -> dict:
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

        characters = lst
        CharacterJsonFormat = jsonpickle.dumps(characters, unpicklable=False, indent=4)

        return CharacterJsonFormat

    def AllCharacters(self) -> dict:
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

        characters = lst
        CharacterJsonFormat = jsonpickle.dumps(characters, unpicklable=False, indent=4)

        return CharacterJsonFormat

    def searchCharacter(self, name: str) -> Character:
        """
        Search for the character in encyclopedia with the given name
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

        # get the character that matches the name
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            if index > 0:
                result = [res.replace('\n', '') for res in result]
                links = [data for data in row.find_all('a', href=True)]
                if (name in substring for substring in links):
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

    def getCharacterInfoByName(self, name: str) -> CharacterInfo:
        """
        Gets the info of the character
        :param url: url of the character
        :return: A json format of the character info
        """
        characters = self.searchCharacter(name)
        url = characters.CharacterURL

        basicInfo = self.getCharacterByURL(url)

        tables = Tables(url)
        stars = tables.Stars()
        misc = tables.LeftTableCard()
        skill = tables.FieldBuddyStats()

        abilities = tables.Abilities(stars)
        status = tables.Status()
        jutsu = tables.Jutsu(stars)

        if stars == 5:
            sync = tables.syncSkills()
            characterInfo = CharacterInfo(basicInfo.Index, basicInfo.Picture,
                                          basicInfo.Name, basicInfo.Rarity,
                                          basicInfo.Element, basicInfo.Type,
                                          basicInfo.CharacterURL, misc, status, skill, sync, abilities, jutsu)
        else:
            characterInfo = CharacterInfo(basicInfo.Index, basicInfo.Picture,
                                          basicInfo.Name, basicInfo.Rarity,
                                          basicInfo.Element, basicInfo.Type,
                                          basicInfo.CharacterURL, misc, status, skill, '', abilities, jutsu)

        CharacterJsonFormat = jsonpickle.dumps(characterInfo, unpicklable=False, indent=4)

        return CharacterJsonFormat


n = NBlazingApi()
x = n.getCharacterInfoByName('Naruto_Uzumaki_%22The_Worst_Loser%22_(%E2%98%853)')
js = jsonpickle.loads(x)
print(js )


