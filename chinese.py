""""
I love chinese food. I can never find any on campus.
Running this program will search all the RIT dining locations and try
to find you some delicious chinese food. Enjoy

@author - Reid
"""

from bs4 import BeautifulSoup
import requests

def findChineseFood() :
    """"
    Finds chinese food at RIT
    """

    print("Let's find chinese food!")

    placesWithChineseFood = []

    # Store the pages we search in an array
    analyzedPages = analyzePages()

    # Analyze each page
    for store in analyzedPages:
        storeName = store[0]

        print("================")
        print("LOCATION: " + storeName)
        print("")

        # Print out menu for each location and add chinese food to list
        for menuItem in store[1:]:
            if isChineseFood(menuItem):
                # We have found chinese food!
                if storeName not in placesWithChineseFood:
                    placesWithChineseFood.append(storeName)
            print(menuItem)

    # Print out locations with chinese food
    print("PLACES WITH CHINESE FOOD: " + str(placesWithChineseFood))

def isChineseFood(menuItem) -> bool:
    return 'General Tso' in menuItem or 'Chinese' in menuItem or 'Asian' in menuItem or 'Stir Fry' in menuItem

def analyzePages() -> list:
    """
    Scrape the RIT dining page and get a list of all dining locations
    :return: list of stores(each store is a list)
    """

    base_url = "https://www.rit.edu/fa/diningservices/places-to-eat/hours"
    print("Retrieving dining locations from " + base_url)

    page_response = requests.get(base_url, timeout=2)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    list_of_places = str(page_content.find_all(class_="hours-title"))
    list_of_urls = list_of_places.split("<a")

    print("\n")
    print("Total locations found " + str(len(list_of_urls)))
    print("Successful! Analyzing the locations now.")
    print("\n\n")

    menuItems = []

    # Always use [1:] because of the way we split our string
    for page in list_of_urls[1:]:
        diningPage = _extractLinkFromText(page)
        print("Reading data from " + diningPage)
        menuItems.append(analyzePage(diningPage))
    return menuItems

def analyzePage(url) -> list:
    """
    Scrape a SINGLE RIT dining page and get a list of food
    :return: list of [store, menuItem, menuItem, etc.]
    """
    page_response = requests.get(url, timeout=2)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    # Fancy up our location name to look nice
    locationName = str(page_content.find("title"))
    locationName = _modifyForeignChars(locationName.replace("<title>", "")\
        .replace("</title>","").replace(" | Dining Services", ""))

    menu_item_string = str(page_content.find_all(class_="menu-items"))
    print("Menu items have been retrieved.")
    print("Location: " + locationName)

    raw_menu_items = menu_item_string.split('<div')

    # Return a list of [store, item, item, item]
    menuItems = [locationName]
    for itemString in raw_menu_items[1:]:
        menuItems.append(_analyzeItemFromMenuString(itemString))
    return menuItems

def _analyzeItemFromMenuString(menu_item_string) -> str:
    """
    Retrieve item name from a raw html string
    :return: Menu item name
    """
    startIndex = menu_item_string.index('-items">') + 7
    endIndex = menu_item_string.rfind("<br",)
    menuItem = menu_item_string[startIndex+1:endIndex]
    return _modifyForeignChars(menuItem)

def _modifyForeignChars(text) -> str:
    """
    Removes foreign characters from text
    :param text:
    :return:
    """
    text = text.replace("<br/>", ", ")
    text = text.replace("&amp;", "&")
    return text

def _extractLinkFromText(text) -> str:
    """
    Extract a dining link from a long html string
    :param text:
    :return:
    """
    startIndex = text.index('href="') + 5
    endIndex = text.index('\"', startIndex + 1)
    return text[startIndex + 1:endIndex]

findChineseFood()