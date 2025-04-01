from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# URL of the website
URL = "https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile"

# Set up the Chrome driver
driver = webdriver.Chrome()
driver.get(URL)
driver.maximize_window()
time.sleep(5)  # Wait for the page to load

# Function to scrape bus routes
def scrape_bus_routes():
    route_elements = driver.find_elements(By.CLASS_NAME, 'route')
    bus_routes_link = [route.get_attribute('href') for route in route_elements]
    bus_routes_name = [route.text.strip() for route in route_elements]
    return bus_routes_link, bus_routes_name

# Scrape the first page
all_bus_routes_link, all_bus_routes_name = scrape_bus_routes()

# Function to scrape bus details
def scrape_bus_details(url, route_name):
    try:
        driver.get(url)
        time.sleep(5)  # Allow the page to load
        
        # Scroll down to load all bus items
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for the page to load more content
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Find bus item details
        bus_name_elements = driver.find_elements(By.CLASS_NAME, "travels.lh-24.f-bold.d-color")
        bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type.f-12.m-top-16.l-color.evBus")
        departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")
        duration_elements = driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")
        reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline")
        star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
        price_elements = driver.find_elements(By.CLASS_NAME, "fare.d-block")
        seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

        bus_details = []
        for i in range(len(bus_name_elements)):
            bus_detail = {
                "Route_Name": route_name,
                "Route_Link": url,
                "Bus_Name": bus_name_elements[i].text,
                "Bus_Type": bus_type_elements[i].text,
                "Departing_Time": departing_time_elements[i].text,
                "Duration": duration_elements[i].text,
                "Reaching_Time": reaching_time_elements[i].text,
                "Star_Rating": star_rating_elements[i].text if i < len(star_rating_elements) else '0',
                "Price": price_elements[i].text,
                "Seat_Availability": seat_availability_elements[i].text if i < len(seat_availability_elements) else '0'
            }
            bus_details.append(bus_detail)
        return bus_details

    except Exception as e:
        print(f"Error occurred while accessing {url}: {str(e)}")
        return []

# List to hold all bus details
all_bus_details = []

# Iterate over each bus route link and scrape the details
for link, name in zip(all_bus_routes_link, all_bus_routes_name):
    bus_details = scrape_bus_details(link, name)
    if bus_details:
        all_bus_details.extend(bus_details)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_bus_details)

# Save the DataFrame to a CSV file
df.to_csv('wb2.csv', index=False)

# Close the driver
driver.quit()
