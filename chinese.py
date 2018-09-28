""""
I love chinese food. I can never find any on campus..
Running this program will search all the RIT dining locations and try
to find me some delicious chinese food.

@author - Reid
9/28/18
"""

from bs4 import BeautifulSoup
import requests

def findChineseFood() :
    print("Let's find chinese food!")
    #print(analyzePages())
    placesWithChineseFood = []
    analyzedPages = analyzePages()
    for store in analyzedPages:
        print("================")
        print("LOCATION: " + store[0])
        print("")
        for menuItem in store[1:]:
            if(_analyzeForChineseFood(menuItem)):
                placesWithChineseFood.append(store[0])
            print(menuItem)
    print("HAS CHINESE FOOD: " + str(placesWithChineseFood))


def analyzePages() -> list:
    """
    Scrape the RIT dining page and get a list of all dining locations
    :return:
    """

    base_url = "https://www.rit.edu/fa/diningservices/places-to-eat/hours"
    print("Retrieving dining locations from " + base_url)

    page_response = requests.get(base_url, timeout=2)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    list_of_places = str(page_content.find_all(class_="hours-title"))
    list_of_urls = list_of_places.split("<a")

    print("Successful! Analyzing the locations now.")

    menuItems = []
    for page in list_of_urls[1:]:
        diningPage = _extractLinkFromText(page)
        print("Checking " + diningPage)
        menuItems.append(analyzePage(diningPage))
    return menuItems

def analyzePage(url) -> list:
    """
    Scrape a SINGLE RIT dining page and get a list of food
    :param url:
    """
    page_response = requests.get(url, timeout=2)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    locationName = str(page_content.find("title"))
    locationName = _modifyForeignChars(locationName.replace("<title>", "")\
        .replace("</title>","").replace(" | Dining Services", ""))

    print("Menu items have been retrieved.")
    menu_item_string = str(page_content.find_all(class_="menu-items"))
    raw_menu_items = menu_item_string.split('<div')

    menuItems = [locationName]
    print(menuItems)
    for itemString in raw_menu_items[1:]:
        menuItems.append(_analyzeItemFromMenuString(itemString))
    return menuItems

def _analyzeItemFromMenuString(menu_item_string) -> str:
    startIndex = menu_item_string.index('-items">') + 7
    endIndex = menu_item_string.rfind("<br",)
    menuItem = menu_item_string[startIndex+1:endIndex]
    return _modifyForeignChars(menuItem)

def _modifyForeignChars(text) -> str:
    text = text.replace("<br/>", ", ")
    text = text.replace("&amp;", "&")
    return text

def _extractLinkFromText(text) -> str:
    """
    Extract a dining link from a long string list
    :param text:
    :return:
    """
    startIndex = text.index('href="') + 5
    endIndex = text.index('\"', startIndex + 1)
    return text[startIndex + 1:endIndex]

def _analyzeForChineseFood(menuItem) -> bool:
    return 'Chinese' in menuItem

findChineseFood()