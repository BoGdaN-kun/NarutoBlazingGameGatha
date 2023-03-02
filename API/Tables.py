import lxml
import requests
from bs4 import BeautifulSoup
from lxml import html

from API.Utils import clearWord


class Tables:
    def __init__(self, url):
        self.url = url

    def LeftTableCard(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        tables = soup.find("div", class_="lefttablecard")
        # dom = etree.HTML(str(soup))
        # print(dom.xpath('/html/body/div[4]/div[3]/div[3]/main/div[3]/div[2]/div[1]/div/div[1]/table[2]'))
        # page = requests.get(url)
        # tree = lxml.html.fromstring(page.content)
        # table = tree.xpath('//div[text()="lefttablecard"]')

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
        Range = lst[1][0]
        Luck = lst[1][1]
        Cost = lst[1][2]

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
        print(FieldSkill)
        print(BuddySkill)

        # Print the text content of each table
        # for table in soup_tables:
        #     print(table.get_text())

    def FieldBuddyStats(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Convert the BeautifulSoup object to an lxml tree
        tree = html.fromstring(str(soup))

        # Use an XPath expression to select all table elements on the page
        tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[4]/tbody')

        # Convert each table element back to a BeautifulSoup object
        soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]

        soup_table = soup_table[0].find_all('tr')
        lst = []
        for i in soup_table:
            res = [clearWord(res.get_text(separator=' ', strip=True)) for res in i]
            new_list = [item for item in res if item != '']
            lst.append(new_list)

        listOfSkills = []
        for i in range(len(lst)):
            if i!=0:
                listOfSkills.append((lst[i][1],lst[i][2]))

        print(listOfSkills)


x = Tables(url='https://naruto-blazing.fandom.com/wiki/Naruto_Uzumaki_%22The_Worst_Loser%22_(%E2%98%853)')
x.FieldBuddyStats()

#
# page = requests.get(self.url)
# soup = BeautifulSoup(page.content, 'html.parser')
#
# # Convert the BeautifulSoup object to an lxml tree
# tree = html.fromstring(str(soup))
#
# # Use an XPath expression to select all table elements on the page
# tables = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[4]/tbody')
#
# # Convert each table element back to a BeautifulSoup object
# soup_table = [BeautifulSoup(html.tostring(table), 'html.parser') for table in tables]
#
# soup_table = soup_table[0].find_all('td')
# lst = []
# for i in soup_table:
#     res = [clearWord(res.text) for res in i if res.text != '' and res.text != '\n']
#     lst.append(res)
# filtered_list = [my_list for my_list in lst if my_list]
# print(filtered_list)
# # Print the text content of each table
# # for table in soup_tables:
# #     print(table.get_text())
