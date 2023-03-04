from copy import deepcopy

import lxml
import requests
from bs4 import BeautifulSoup
from lxml import html

from API.Utils import clearWord, countStars


class Tables:
    def __init__(self, url):
        self.url = url

    def LeftTableCard(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        tables = soup.find("div", class_="lefttablecard")

        tabless = tables.find_all('table')
        rows = tabless[0].find_all('tr')
        image_link = [data for data in rows[0].find_all('a', href=True)]
        image_link = image_link[0]['href']

        tabless = tables.find_all('table')
        rows = tabless[1].find_all('tr')
        lst = []
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            result = [clearWord(res) for res in result]
            lst.append(result)
        # TODO make a format for the time string
        japaneseReleaseDate = lst[2][0]
        globalReleaseDate = lst[2][1]
        dictJson = {
            "releaseDate": {"japaneseReleaseDate": japaneseReleaseDate, "globalReleaseDate": globalReleaseDate},
            "imageLink": image_link
        }
        return dictJson

    def RightTableCard(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find("div", class_="righttablecard")
        tabless = tables.find_all('table')
        rows = tabless[2].find_all('tr')
        lst = []
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            result = [clearWord(res) for res in result]
            lst.append(result)

        lst = []
        Range = lst[1][0]
        Luck = lst[1][1]
        Cost = lst[1][2]
        lst.append(Range)
        lst.append(Luck)
        lst.append(Cost)

        return lst

    def BasicInfo(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find("div", class_="righttablecard")
        tabless = tables.find_all('table')
        rows = tabless[1].find_all('tr')
        lst = []
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            result = [res.replace('\n', '') for res in result]  # strange that clearword doesnt work here
            lst.append(result)

        number = lst[1][0]
        element = lst[1][1]
        rarity = lst[1][2]
        maxLevel = lst[1][3]

        rightTableCard = self.RightTableCard()
        dictJson = {
            "Index": number,
            "Element": element,
            "Rarity": rarity,
            "MaxLevel": maxLevel,
            "Range": rightTableCard[0],
            "Luck": rightTableCard[1],
            "Cost": rightTableCard[2]
        }
        return dictJson

    def FieldBuddyStats(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Convert the BeautifulSoup object to an lxml tree
        tree = html.fromstring(str(soup))

        # Use an XPath expression to select all table elements on the page
        tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody')

        # Convert each table element back to a BeautifulSoup object
        soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]

        soup_table = soup_table[0].find_all('td')
        lst = []
        for i in soup_table:
            res = [clearWord(res.text) for res in i]
            lst.append(res)
        FieldSkill = lst[0][0]
        BuddySkill = lst[1][0]
        dictJson = {
            "FieldSkill": FieldSkill,
            "BuddySkill": BuddySkill
        }
        return dictJson

    def Stars(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find("div", class_="righttablecard")
        tabless = tables.find_all('table')
        rows = tabless[1].find_all('tr')
        lst = []
        for index, row in enumerate(rows):
            result = [data.text for data in row.find_all('td')]
            result = [clearWord(res) for res in result]
            lst.append(result)
        rarity = lst[1][2]
        return countStars(rarity)

    def Abilities(self, stars):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Convert the BeautifulSoup object to a lxml tree
        tree = html.fromstring(str(soup))

        # Use an XPath expression to select all table elements on the page
        if stars == 3 or stars == 4:
            tables = tree.xpath(f'//*[@id="mw-content-text"]/div[1]/table[4]/tbody')
        else:
            tables = tree.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody')
        # Convert each table element back to a BeautifulSoup object
        soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]

        soup_table = soup_table[0].find_all('tr')
        lst = []
        for i in soup_table:
            res = [clearWord(res.get_text(separator=' ', strip=True)) for res in i]
            new_list = [item for item in res if item != '']
            lst.append(new_list)

        # listOfSkills = []
        # skill = {
        #
        # }
        # for i in range(len(lst)):
        #     if i != 0:
        #         listOfSkills.append((lst[i][1], lst[i][2]))
        listOfSkills = []
        skill = {
            "Skill": 0,
            "Description": 0
        }
        for i in range(len(lst)):
            if i != 0:
                skill["Skill"] = lst[i][1]
                skill["Description"] = lst[i][2]
                listOfSkills.append(deepcopy(skill))

        return listOfSkills

    def Status(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Convert the BeautifulSoup object to an lxml tree
        tree = html.fromstring(str(soup))

        # Use an XPath expression to select all table elements on the page
        tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody')

        # Convert each table element back to a BeautifulSoup object
        soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]

        soup_table = soup_table[0].find_all('tr')
        lst = []
        for i in soup_table:
            res = [clearWord(res.get_text(separator=' ', strip=True)) for res in i]
            new_list = [item for item in res if item != '']
            lst.append(new_list)
        stats = []
        mini_stats = {
            "Stat": 0,
            "Base": 0,
            "Max": 0,
            "+Value": 0,
            "+Abilities": 0
        }
        dictJson = {
            "Missions": 0,
            "Ninja World Ultimate Showdown": 0
        }
        for i in range(len(lst)):
            if i == 3 or i == 4:
                for index, key in enumerate(mini_stats):
                    mini_stats[key] = lst[i][index]
                stats.append(deepcopy(mini_stats))

        dictJson["Missions"] = stats
        stats.clear()
        for i in range(len(lst)):
            if i in [6, 7, 8]:
                for index, key in enumerate(mini_stats):
                    mini_stats[key] = lst[i][index]
                stats.append(deepcopy(mini_stats))
        dictJson["Ninja World Ultimate Showdown"] = stats
        return dictJson

    def Jutsu(self, stars):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Convert the BeautifulSoup object to an lxml tree
        tree = html.fromstring(str(soup))

        # Use an XPath expression to select all table elements on the page
        if stars == 3 or stars == 4:
            tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[5]/tbody')
        else:
            tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[6]/tbody')
        # Convert each table element back to a BeautifulSoup object
        soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]

        soup_table = soup_table[0].find_all('tr')
        lst = []
        for i in soup_table:
            res = [clearWord(res.get_text(separator=' ', strip=True)) for res in i]
            new_list = [item for item in res if item != '']
            lst.append(new_list)
        ninjutsuName = lst[0][0]
        ninjutsuName = ninjutsuName.split(":")
        ninjutsuName = ninjutsuName[1]

        chakra = lst[1][2]
        chakra = chakra.split(": ")
        chakra = chakra[1]

        mini_stats = {
            "Jutsu": 0,
            "HitCount": 0,
            "Shape": 0,
            "Range": 0,
            "Position": 0
        }
        description = {
            "Name": ninjutsuName,
            "Description": lst[1][1],
            "Chakra": chakra
        }

        dictJson = {
            "Ninjutsu": description,
            "JutsuData": mini_stats
        }

        if stars == 3 or stars == 4:
            for i in range(len(lst)):
                if i == 3 or i == 4:
                    for index, key in enumerate(mini_stats):
                        mini_stats[key] = lst[i][index]
        else:
            for i in range(len(lst)):
                if i == 5:
                    for index, key in enumerate(mini_stats):
                        mini_stats[key] = lst[i][index]
        dictJson["JutsuData"] = mini_stats
        return dictJson


x = Tables(url='https://naruto-blazing.fandom.com/wiki/Naruto_Uzumaki_%22The_Worst_Loser%22_(%E2%98%853)')
# x = Tables(url='https://naruto-blazing.fandom.com/wiki/Naruto_Uzumaki_%22Unshakeable_Will%22_(%E2%98%856)')
# x = Tables(url='https://naruto-blazing.fandom.com/wiki/Hashirama_Senju_%22Long-Held_Dream%22_(%E2%98%856)_(Blazing_Awakened)')
# x = Tables(url='https://naruto-blazing.fandom.com/wiki/Minato_Namikaze_%22Unfading_Courage%22_(%E2%98%855)')
print(x.Status())
