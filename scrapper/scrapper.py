from bs4 import BeautifulSoup
import requests


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

def printStationMenus():
    print("Station Menus:\n\n")
    for i in range(len(station_names)):
        print(station_names[i] + ":")
        print(station_menus[i])
        print("\n")

def printFoodsAndIngredients():
    print("List of Foods and their Ingredients:\n\n")
    for i in range(len(food_list)):
        print(food_list[i] + ":")
        print(ingredients[i] + "\n")

url = "https://harvesttableuva.com/locations/runk-dining-hall/"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
station_elements = soup.find_all(attrs={"menu-station"})
station_names = getStationNames()
station_menus = getStationFoods()
food_list, ingredients = getFoodsAndTheirIngredients()


printStationMenus()
printFoodsAndIngredients()

# stations = soup.find_all(attrs={"class":"toggle-menu-station-data"})


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup # Set up Selenium Chrome driver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# url = "https://virginia.campusdish.com/LocationsAndMenus/ObservatoryHillDiningRoom"
# driver.get(url) # Wait for the page to load (you might need to adjust the wait time)
# driver.implicitly_wait(10) # Extract the HTML content after it's been rendered by JavaScript
# html = driver.page_source # Parse the HTML using BeautifulSoup
# soup = BeautifulSoup(html, 'html.parser') # Now you can extract the content you need from the BeautifulSoup object
# print(soup) # Remember to close the driver when you're done
# driver.quit()
