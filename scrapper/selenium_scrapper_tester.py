from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome()
url = "https://virginia.campusdish.com/LocationsAndMenus/ObservatoryHillDiningRoom"
driver.get(url) # Wait for the page to load (you might need to adjust the wait time)
driver.implicitly_wait(10) # Extract the HTML content after it's been rendered by JavaScript
html = driver.page_source # Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser') # Now you can extract the content you need from the BeautifulSoup object
print(soup) # Remember to close the driver when you're done
driver.quit()