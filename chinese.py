""""
I love chinese food. I can never find any on campus..
Running this program will search all the RIT dining locations and try
to find me some delicious chinese food.

@author - Reid
"""

from bs4 import BeautifulSoup
import requests

def findChineseFood() :
    base_url = "https://www.rit.edu/fa/diningservices/"

    #page_response = requests.get(base_url+"commons", timeout=5)
    #page_content = BeautifulSoup(page_response.content, "html.parser")

    #menu_items = page_content.find_all(class_="menu-items")

    #print(menu_items)
    print(analyzePages())

def analyzePages() -> str:
    base_url = "https://www.rit.edu/fa/diningservices/places-to-eat/hours"
    page_response = requests.get(base_url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    list_of_places = str(page_content.find_all(class_="hours-title"))
    #print(list_of_places)
    list_of_urls = list_of_places.split("<a")
    for link in list_of_urls[1:]:
        #print(link)
        analyzePage(_extractLinkFromText(link))
    #print(list_of_places)

def analyzePage(url) -> str:
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    menu_items = page_content.find_all(class_="menu-items")

    print(menu_items)

def _extractLinkFromText(text) -> str:
    startIndex = text.index('href="') + 5
    endIndex = text.index('\"', startIndex + 1)
    return text[startIndex + 1:endIndex]

findChineseFood()