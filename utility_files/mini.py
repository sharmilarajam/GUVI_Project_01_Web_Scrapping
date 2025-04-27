from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Use Selenium Stealth
from selenium_stealth import stealth

# Change this URL to your required route
URL = "https://www.redbus.in/search?fromCityName=Theni&fromCityId=599&srcCountry=IND&toCityName=CMBT,%20Chennai,%20Chennai&toCityId=66065&destCountry=IND&onward=26-Apr-2025&opId=0&busType=Any"
def initialize_driver():
    """Initialize Chrome WebDriver with stealth mode."""
    options = webdriver.ChromeOptions()
    # Uncomment below line if you want to see the browser while scraping
    # options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)

    # Apply stealth mode to prevent detection
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
    """Load the webpage and wait for it to fully render."""
    driver.get(url)
    time.sleep(5)  # Give time for JavaScript content to load

def scrape_bus_details(driver, route_name, route_link):
    """Scrape private bus details from RedBus."""
    try:
        # Scroll down multiple times to load all buses
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        print("Page Title:", driver.title)

        # Locate bus details (Ensure these class names are up-to-date!)
        bus_name_elements = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
        bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type")
        departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time")
        duration_elements = driver.find_elements(By.CLASS_NAME, "dur")
        reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time")
        star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']") # Add star rating
        price_elements = driver.find_elements(By.CLASS_NAME, "fare")
        seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]") # Add seat availability

        print(f"Found {len(bus_name_elements)} buses")  # Debugging print

        bus_details = []
        for i in range(len(bus_name_elements)):
            bus_detail = {
                "Route_Name": route_name,  # Add route name
                "Route_Link": route_link,  # Add route link
                "Bus_Name": bus_name_elements[i].text if i < len(bus_name_elements) else "N/A",
                "Bus_Type": bus_type_elements[i].text if i < len(bus_type_elements) else "N/A",
                "Departing_Time": departing_time_elements[i].text if i < len(departing_time_elements) else "N/A",
                "Duration": duration_elements[i].text if i < len(duration_elements) else "N/A",
                "Reaching_Time": reaching_time_elements[i].text if i < len(reaching_time_elements) else "N/A",
                "Star_Rating": star_rating_elements[i].text if i < len(star_rating_elements) else "N/A",
                "Price": price_elements[i].text if i < len(price_elements) else "N/A",
                "Seat_Availability": seat_availability_elements[i].text if i < len(seat_availability_elements) else "N/A",
            }
            print(bus_detail)  # Debugging print
            bus_details.append(bus_detail)

        return bus_details

    except Exception as e:
        print(f"Error scraping bus details: {e}")
        return []

def scrape_all_pages():
    """Scrape private bus details from multiple pages if available."""
    all_bus_details = []
    
    driver = initialize_driver()
    try:
        load_page(driver, URL)
        for page in range(1, 4):  # Modify based on available pages
            print(f"Scraping page {page}...")
            
            # Get the route name and link
            route_name = " "  # Update this to dynamically get the route name
            route_link = URL  # Link to the current route (or modify as needed)
            
            bus_details = scrape_bus_details(driver, route_name, route_link)
            if bus_details:
                all_bus_details.extend(bus_details)

            # Try clicking the "Next Page" button
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@class='next']"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)
            except Exception as e:
                print("No more pages available or error in pagination:", e)
                break  

    except Exception as e:
        print(f"Error scraping pages: {e}")
    finally:
        driver.quit()

    return all_bus_details

# Run scraping
bus_data = scrape_all_pages()

# Convert data to DataFrame and save to CSV
if bus_data:
    df = pd.DataFrame(bus_data)
    df.to_csv("theni.csv", index=False)
    print("Scraping complete. Data saved to Private_Buses.csv.")
else:
    print("No data collected. Check the website structure or elements.")
