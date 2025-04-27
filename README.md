# RedBus Data Scraping 🚍

This project scrapes private and government bus details (like bus name, type, timings, price, ratings, and seat availability) from [RedBus.in](https://www.redbus.in/) using **Selenium** and **Python**.

---

## ✨ Features
- Scrapes bus information: **Bus Name**, **Bus Type**, **Departure Time**, **Duration**, **Arrival Time**, **Star Rating**, **Price**, and **Seat Availability**.
- Dynamically detects the **Route Name** from any RedBus link.
- Saves the scraped data into a **MySQL database**.
- Retrieves and displays bus information directly from the database.

---

## 🛠 Requirements
- Python 3.8 or higher
- Chrome Browser
- Chrome Driver (compatible with your Chrome version)
- MySQL Workbench

### Python Libraries
- `pandas`
- `selenium-stealth`
- `pymysql`

---

## 🚀 How to Run

1. **Download** the code.
2. **Install** the required Python packages:
   ```bash
   pip install pandas selenium-stealth pymysql



CSV file format will be:
Route Name | Bus Name | Bus Type | Departure | Duration | Arrival | Star Rating | Price | Seat Availability
Kumbakonam to Chennai | PNX Travels | AC Seater 2+2 | 08:00 AM | 5h 30m | 01:30 PM | 4.2 | INR 445 | 37 Seats available