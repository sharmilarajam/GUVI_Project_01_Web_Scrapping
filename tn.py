from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# URL of the website
URL = "https://www.redbus.in/online-booking/tnstc"

def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def load_page(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

# Function to scrape bus routes
def scrape_bus_routes(driver):
    route_elements = driver.find_elements(By.CLASS_NAME, 'route')
    bus_routes_link = [route.get_attribute('href') for route in route_elements if route.get_attribute('href')]
    bus_routes_name = [route.text.strip() for route in route_elements if route.text.strip()]
    return bus_routes_link, bus_routes_name

# Function to scrape bus details
def scrape_bus_details(driver, url, route_name):
    try:
        driver.get(url)
        time.sleep(5)  # Allow the page to load
        
        # Click the "View Buses" button if it exists
        try:
            view_buses_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "button"))
            )
            driver.execute_script("arguments[0].click();", view_buses_button)
            time.sleep(5)  # Wait for buses to load
            
            # Scroll down to load all bus items
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for the page to load more content

            # Find bus item details
            bus_name_elements = driver.find_elements(By.CLASS_NAME, "travels")
            bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type")
            departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time")
            duration_elements = driver.find_elements(By.CLASS_NAME, "dur")
            reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time")
            star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec']")
            price_elements = driver.find_elements(By.CLASS_NAME, "fare")

            seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

            bus_details = []
            for i in range(len(bus_name_elements)):
                bus_detail = {
                    "Route_Name": route_name,
                    "Route_Link": url,
                    "Bus_Name": bus_name_elements[i].text if i < len(bus_name_elements) else "N/A",
                    "Bus_Type": bus_type_elements[i].text if i < len(bus_type_elements) else "N/A",
                    "Departing_Time": departing_time_elements[i].text if i < len(departing_time_elements) else "N/A",
                    "Duration": duration_elements[i].text if i < len(duration_elements) else "N/A",
                    "Reaching_Time": reaching_time_elements[i].text if i < len(reaching_time_elements) else "N/A",
                    "Star_Rating": star_rating_elements[i].text if i < len(star_rating_elements) else "0",
                    "Price": price_elements[i].text if i < len(price_elements) else "N/A",
                    "Seat_Availability": seat_availability_elements[i].text if i < len(seat_availability_elements) else "0"
                }
                bus_details.append(bus_detail)
            return bus_details
        
        except Exception as e:
            print(f"Error occurred while scraping bus details for {url}: {str(e)}")
            return []

    except Exception as e:
        print(f"Error occurred while accessing {url}: {str(e)}")
        return []

# List to hold all bus details
all_bus_details = []

# Function to scrape all pages
def scrape_all_pages():
    driver = initialize_driver()
    for page in range(1, 4):  # Scrape 3 pages
        try:
            load_page(driver, URL)
            
            if page > 1:
                try:
                    pagination_tab = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'DC_117_pageTabs') and text()='{page}']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", pagination_tab)
                    time.sleep(2)  # Allow smooth scrolling
                    driver.execute_script("arguments[0].click();", pagination_tab)
                    time.sleep(5)  # Wait for the page to load
                except Exception as e:
                    print(f"Error clicking pagination {page}: {str(e)}")

            all_bus_routes_link, all_bus_routes_name = scrape_bus_routes(driver)
            
            for link, name in zip(all_bus_routes_link, all_bus_routes_name):
                bus_details = scrape_bus_details(driver, link, name)
                if bus_details:
                    all_bus_details.extend(bus_details)

        except Exception as e:
            print(f"Error occurred while accessing page {page}: {str(e)}")

    driver.quit()  # Close the browser after all scraping is done

# Scrape routes and details from all pages
scrape_all_pages()

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_bus_details)

# Save the DataFrame to a CSV file
df.to_csv('tn.csv', index=False)

print("Scraping completed successfully!")
