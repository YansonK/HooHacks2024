from bs4 import BeautifulSoup
from selenium import webdriver

def getHTML(url):
    driver = webdriver.Chrome()
    driver.get(url)  # Wait for the page to load (you might need to adjust the wait time)
    driver.implicitly_wait(10)  # Extract the HTML content after it's been rendered by JavaScript
    html = driver.page_source
    driver.quit()
    return html # Parse the HTML using BeautifulSoup


def getStationNames():
    station_names = []
    for station_element in station_elements:
        station_name_element = station_element.find("h4")
        station_name = station_name_element.get_text()
        if station_name not in station_names:
            station_names.append(station_name)
    return station_names


def getStationFoods():
    station_menus = []
    for station_element in station_elements:
        food_link_elements = station_element.find_all("li")
        station_menu = []
        for food_link_element in food_link_elements:
            food_element = food_link_element.find("a")
            food = food_element.get_text()
            station_menu.append(food)
        if station_menu not in station_menus:
            station_menus.append(station_menu)
    return station_menus


def getFoodsAndTheirIngredients():
    ingredients = []
    food_list = []
    for station_element in station_elements:
        station_data = station_element.find("div")
        foods = station_data.find_all("li")
        for food in foods:
            food_attributes = food.attrs
            food_name_element = food.find("a")
            food_name = food_name_element.get_text()
            food_ingredients = food_attributes["data-searchable"]
            ingredients.append(food_ingredients[len(food_name):len(food_ingredients)])
            food_list.append(food_name)
    return food_list, ingredients


def getOHillOrFFCStationNames(dining_hall_website):
    station_names = []
    station_elements = dining_hall_website.find_all(attrs={"class": "sc-hHOBiw flydZD StationHeaderTitle"},
                                                    recursive=True)
    for station_element in station_elements:
        station_name = station_element.get_text()
        if station_name not in station_names:
            station_names.append(station_name)
    return station_names


def getOHillOrFFCStationFoods(dining_hall_website):
    station_menus = []
    station_elements = dining_hall_website.find_all(attrs={"class":"sc-ejfMa-d flvhaP MenuStation_no-categories"},
                                                    recursive=True)
    for station_element in station_elements:
        food_link_elements = station_element.find_all(attrs={"data-testid":"product-card-header-link"}, recursive = True)
        food_title_elements = station_element.find_all(attrs={"data-testid":"product-card-header-title"}, recursive = True)
        for element in food_title_elements:
            food_link_elements.append(element)
        station_menu = []
        for food_link_element in food_link_elements:
            food = food_link_element.get_text()
            station_menu.append(food)
        if station_menu not in station_menus:
            station_menus.append(station_menu)
    return station_menus


def getOHillOrFFCFoodsAndTheirIngredients(dining_hall_website):
    ingredients = []
    food_list = []

    food_cards = dining_hall_website.find_all(attrs={"data-testid":"product-card"}, recursive = True)

    for food_card in food_cards:
        foods = food_card.find_all(attrs={"data-testid": "product-card-header-link"}, recursive=True)
        foods_unlinked = food_card.find_all(attrs={"data-testid": "product-card-header-title"},
                                                       recursive=True)
        for food in foods_unlinked:
            foods.append(food)
        food_descriptions = food_card.find_all(attrs={"data-testid": "product-card-description"},
                                                         recursive=True)
        for i in range(0, len(foods)):
            food_list.append(foods[i].get_text())
            if len(food_descriptions) > i:
                ingredients.append(food_descriptions[i].get_text())
            else:
                ingredients.append("Ingredient information is currently unavailable.")

    return food_list, ingredients


def printStationMenus(location_name):
    print(location_name + " Stations: \n")
    for i in range(len(station_names)):
        print(station_names[i] + " Menu:")
        print(station_menus[i])
        print("")


def printFoodsAndIngredients():
    print("List of Foods and their Ingredients:\n")
    for i in range(len(food_list)):
        print(food_list[i] + ":")
        print(ingredients[i] + "\n")


def scrapeDiningHallWebsite(dining_hall_url, dining_hall_name):
    global station_elements, station_names, station_menus, food_list, ingredients
    dining_hall_website = BeautifulSoup(getHTML(dining_hall_url),
                                        'html.parser')  # Now you can extract the content you need from the BeautifulSoup object
    if "Runk" in dining_hall_name:
        station_elements = dining_hall_website.find_all(attrs={"menu-station"})
        station_names = getStationNames()
        station_menus = getStationFoods()
        food_list, ingredients = getFoodsAndTheirIngredients()
    else:
        station_names = getOHillOrFFCStationNames(dining_hall_website)
        station_menus = getOHillOrFFCStationFoods(dining_hall_website)
        food_list, ingredients = getOHillOrFFCFoodsAndTheirIngredients(dining_hall_website)


uva_dine_url = "https://virginia.campusdish.com/en"
uva_dine_website = BeautifulSoup(getHTML(uva_dine_url + "/LocationsAndMenus"), 'html.parser') # Now you can extract the content you need from the BeautifulSoup object
content_wrapper = uva_dine_website.find(attrs={"locationList"})
location_list = content_wrapper.find("ul", recursive=True)
location_links = (location_list.find_all("a", recursive=True))[0:3]
location_attributes = location_links[1].attrs
location_name = location_attributes["aria-label"]
if "Runk" in location_name:
    location_web_address = "https://harvesttableuva.com/locations/runk-dining-hall/"
else:
    location_web_address = uva_dine_url + location_attributes['href']
scrapeDiningHallWebsite(location_web_address, location_name)
printStationMenus(location_name)
printFoodsAndIngredients()
