from bs4 import BeautifulSoup
from selenium import webdriver

class DiningHallScraper:
    def __init__(self, dining_hall_url = "", dining_hall_name = ""):
        self.dining_hall_url = dining_hall_url
        self.dining_hall_name = dining_hall_name
        self.station_elements = []
        self.station_names = []
        self.station_menus = []
        self.food_list = []
        self.ingredients = []

    def getHTML(self, url):
        """
        Retrieves the HTML content of a web page using Selenium.

        Args:
            url (str): The URL of the web page to retrieve.

        Returns:
            str: The HTML content of the web page.

        """
        driver = webdriver.Chrome()
        driver.get(url)  # Wait for the page to load (you might need to adjust the wait time)
        driver.implicitly_wait(10)  # Extract the HTML content after it's been rendered by JavaScript
        html = driver.page_source
        driver.quit()
        return html

    def getRunkStationNames(self):
        """
        Retrieves the names of the stations from the station elements.

        Returns:
            A list of station names.
        """
        station_names = []
        for station_element in self.station_elements:
            station_name_element = station_element.find("h4")
            station_name = station_name_element.get_text()
            if station_name not in station_names:
                station_names.append(station_name)
        return station_names

    def getRunkStationFoods(self):
        """
        Retrieves the food menus for each station at Runk Dining Hall.

        Returns:
        station_menus (list): A list of lists containing the food menus for each station.
        """
        station_menus = []
        for station_element in self.station_elements:
            food_link_elements = station_element.find_all("li")
            station_menu = []
            for food_link_element in food_link_elements:
                food_element = food_link_element.find("a")
                food = food_element.get_text()
                station_menu.append(food)
            if station_menu not in station_menus:
                station_menus.append(station_menu)
        return station_menus

    def getRunkFoodsAndTheirIngredients(self):
        """
        Retrieves a list of food names and their corresponding ingredients from the station elements.

        Returns:
            food_list (list): A list of food names.
            ingredients (list): A list of ingredients corresponding to each food name.
        """
        ingredients = []
        food_list = []
        for station_element in self.station_elements:
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

    def getOHillOrFFCStationNames(self, dining_hall_website):
        station_names = []
        station_elements = dining_hall_website.find_all(attrs={"class": "sc-hHOBiw flydZD StationHeaderTitle"},
                                                        recursive=True)
        for station_element in station_elements:
            station_name = station_element.get_text()
            if station_name not in station_names:
                station_names.append(station_name)
        return station_names

    def getOHillOrFFCStationFoods(self, dining_hall_website):
        station_menus = []
        station_elements = dining_hall_website.find_all(attrs={"class": "sc-ejfMa-d flvhaP MenuStation_no-categories"},
                                                        recursive=True)
        for station_element in station_elements:
            food_link_elements = station_element.find_all(attrs={"data-testid": "product-card-header-link"},
                                                          recursive=True)
            food_title_elements = station_element.find_all(attrs={"data-testid": "product-card-header-title"},
                                                           recursive=True)
            for element in food_title_elements:
                food_link_elements.append(element)
            station_menu = []
            for food_link_element in food_link_elements:
                food = food_link_element.get_text()
                station_menu.append(food)
            if station_menu not in station_menus:
                station_menus.append(station_menu)
        return station_menus

    def getOHillOrFFCFoodsAndTheirIngredients(self, dining_hall_website):
        ingredients = []
        food_list = []

        food_cards = dining_hall_website.find_all(attrs={"data-testid": "product-card"}, recursive=True)

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

    def printStationMenus(self):
        print(self.dining_hall_name + " Stations: \n")
        for i in range(len(self.station_names)):
            print(self.station_names[i] + " Menu:")
            print(self.station_menus[i])
            print("")

    def printFoodsAndIngredients(self):
        print("List of Foods and their Ingredients:\n")
        for i in range(len(self.food_list)):
            print(self.food_list[i] + ":")
            print(self.ingredients[i] + "\n")

    def scrapeDiningHallWebsite(self):
        dining_hall_website = BeautifulSoup(self.getHTML(self.dining_hall_url),
                                            'html.parser')  # Now you can extract the content you need from the BeautifulSoup object
        if "Runk" in self.dining_hall_name:
            self.station_elements = dining_hall_website.find_all(attrs={"menu-station"})
            self.station_names = self.getRunkStationNames()
            self.station_menus = self.getRunkStationFoods()
            self.food_list, self.ingredients = self.getRunkFoodsAndTheirIngredients()
        else:
            self.station_names = self.getOHillOrFFCStationNames(dining_hall_website)
            self.station_menus = self.getOHillOrFFCStationFoods(dining_hall_website)
            self.food_list, self.ingredients = self.getOHillOrFFCFoodsAndTheirIngredients(dining_hall_website)

    def get_station_menu_pairings(self):
        station_menu_pairings = {}
        for i in range(len(self.station_names)):
            station_menu_pairings[self.station_names[i]] = self.station_menus[i]
        return station_menu_pairings

    def get_ingredients_for_menu(self, menu_option):
        ingredients = []
        for i in range(len(self.food_list)):
            if self.food_list[i] == menu_option:
                ingredients.append(self.ingredients[i])
        return ingredients
    
    def get_scraped_dining_location(index):
        #index: 0=ohill 1=ffc 2=runk
        uva_dine_url = "https://virginia.campusdish.com/en"
        uva_dine_website = BeautifulSoup(DiningHallScraper().getHTML(uva_dine_url + "/LocationsAndMenus"), 'html.parser')
        content_wrapper = uva_dine_website.find(attrs={"locationList"})
        location_list = content_wrapper.find("ul", recursive=True)
        location_links = (location_list.find_all("a", recursive=True))[0:3]
        location_attributes = location_links[index].attrs
        location_name = location_attributes["aria-label"]
        if "Runk" in location_name:
            location_web_address = "https://harvesttableuva.com/locations/runk-dining-hall/"
        else:
            location_web_address = uva_dine_url + location_attributes['href']

        return DiningHallScraper(location_web_address, location_name)




scraper = DiningHallScraper().get_scraped_dining_location(0)
scraper.scrapeDiningHallWebsite()
scraper.printStationMenus()
scraper.printFoodsAndIngredients()
station_menu_pairings = scraper.get_station_menu_pairings()
ingredients_for_menu = scraper.get_ingredients_for_menu("Cheeseburger Mac & Cheese Bowl")

print(station_menu_pairings)
print(ingredients_for_menu)
