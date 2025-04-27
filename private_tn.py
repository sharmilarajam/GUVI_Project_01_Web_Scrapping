from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs, unquote
from selenium_stealth import stealth

# Put your RedBus search or route URL here
URL = "https://www.redbus.in/bus-tickets/thanjavur-to-chennai?fromCityName=Thanjavur&fromCityId=66007&srcCountry=IND&toCityName=Chennai&toCityId=123&destCountry=null&onward=26-Apr-2025&opId=0&busType=Any"

def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Apply stealth
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def load_page(driver, url):
    driver.get(url)
    time.sleep(5)

def get_route_info_from_url(url):
    """Extracts route name either from the URL path or query parameters."""
    parsed = urlparse(url)
    if "bus-tickets" in parsed.path:
        path = parsed.path.strip("/").split("/")[-1]
        if "to" in path:
            parts = path.split("-to-")
            from_city = parts[0].replace("-", " ").title()
            to_city = parts[1].replace("-", " ").title()
            route_name = f"{from_city} to {to_city}"
        else:
            route_name = "Unknown Route"
    else:
        # Get from query params
        query = parse_qs(parsed.query)
        from_city = unquote(query.get("fromCityName", ["Unknown"])[0])
        to_city = unquote(query.get("toCityName", ["Unknown"])[0])
        from_city = from_city.split(",")[0].strip()
        to_city = to_city.split(",")[0].strip()
        route_name = f"{from_city} to {to_city}"

    return route_name, url

def scrape_bus_details(driver, route_name, route_link):
    try:
        # Scroll to load more buses
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        bus_name_elements = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
        bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type")
        departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time")
        duration_elements = driver.find_elements(By.CLASS_NAME, "dur")
        reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time")
        star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
        price_elements = driver.find_elements(By.CLASS_NAME, "fare")
        seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

        print(f"Found {len(bus_name_elements)} buses")

        bus_data = []
        for i in range(len(bus_name_elements)):
            data = [
                route_name,
                route_link,
                bus_name_elements[i].text if i < len(bus_name_elements) else "N/A",
                bus_type_elements[i].text if i < len(bus_type_elements) else "N/A",
                departing_time_elements[i].text if i < len(departing_time_elements) else "N/A",
                duration_elements[i].text if i < len(duration_elements) else "N/A",
                reaching_time_elements[i].text if i < len(reaching_time_elements) else "N/A",
                star_rating_elements[i].text if i < len(star_rating_elements) else "N/A",
                f"INR {price_elements[i].text}" if i < len(price_elements) else "N/A",
                seat_availability_elements[i].text if i < len(seat_availability_elements) else "N/A"
            ]
            bus_data.append(data)
            print(data)  # Optional: print each row

        return bus_data

    except Exception as e:
        print(f"Error while scraping: {e}")
        return []

def scrape_redbus():
    driver = initialize_driver()
    bus_details = []
    try:
        load_page(driver, URL)
        route_name, route_link = get_route_info_from_url(URL)
        bus_details = scrape_bus_details(driver, route_name, route_link)
    finally:
        driver.quit()
    return bus_details

# Run scraping
bus_data = scrape_redbus()

# Save as CSV
if bus_data:
    df = pd.DataFrame(bus_data, columns=[
        "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
        "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
    ])
    df.to_csv("thanjavur_chennai.csv", index=False)
    print("Scraping complete. Data saved to redbus_scraped_data.csv.")
else:
    print(" No data scraped. Please check the page or selectors.")
