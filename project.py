from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import csv
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'crimson',
    'database': 'google_maps_data'
}

def create_database_and_table():
    try:
        # First connect without database to create it if it doesn't exist
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        
        # Create a new table with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        table_name = f"places_{timestamp}"
        

        cursor.execute(f"""
            CREATE TABLE {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                rating VARCHAR(100),
                address TEXT,
                website VARCHAR(255),
                phone VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                search_query VARCHAR(255)
            )
        """)
        
        conn.commit()
        return table_name
    except Error as e:
        print(f"Error creating database/table: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def save_to_mysql(data, search_query):
    try:
        table_name = create_database_and_table()
        if not table_name:
            print("Failed to set up database. Falling back to CSV...")
            save_to_csv(data)
            return

        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Insert data with search query
        insert_query = f"""
            INSERT INTO {table_name} 
            (title, rating, address, website, phone, search_query)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Add search query to each row
        data_with_query = [row + [search_query] for row in data]
        cursor.executemany(insert_query, data_with_query)
        conn.commit()
        print(f"Successfully saved {len(data)} records to MySQL database table: {table_name}")
        
    except Error as e:
        print(f"Error saving to MySQL: {e}")
        print("Falling back to CSV...")
        save_to_csv(data)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


def main():
    storage_choice = input("Choose storage method (1 for CSV, 2 for MySQL): ").strip()
    query = input("Enter the search query with location at the end: ").replace(" ", "+")
    print("While Scrapping Do not close/minimize the browser window.")
    time.sleep(1)

    # Setting up web driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.get(f"https://www.google.com/maps/search/{query}")

    query = query.replace("+", " ")

    # function to scroll the results page to load all the results
    scroll_to_load_results(driver, query)

    scrape_results(driver, storage_choice, query)

def save_to_csv(data):


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    filename = f"scraped_data_{timestamp}.csv"

    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Rating & no. of Reviews", "Address", "Website", "Phone"])
        writer.writerows(data)

    print(f"Data saved to {filename}")

def scroll_to_load_results(driver, query):
    time.sleep(5)
    # Scroll to load all results
    divSideBar = driver.find_element(By.CSS_SELECTOR, f"div[aria-label='Results for {query}']")
    keepScrolling=True
    while(keepScrolling):
        divSideBar.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        divSideBar.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        html =driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
        if(html.find("You've reached the end of the list.")!=-1):
            keepScrolling=False

def scrape_results(driver, storage_choice, search_query):
    # now scrapping of all the results will be done after waiting for 10 seconds to load the webpage
    time.sleep(5)
    elem_results = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')
    data = []

    for result in elem_results:
        try:
            query_result = result.find_element(By.CSS_SELECTOR, 'a')

            driver.execute_script("arguments[0].scrollIntoView(true);", query_result)
            query_result.click()
            time.sleep(1)

            # Extract information
            try:
                title = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob').text
            except:
                title = "N/A"

            try:
                rating = driver.find_element(By.CSS_SELECTOR, 'div.F7nice ').text
            except:
                rating = "N/A"

            try:
                address = driver.find_element(By.CSS_SELECTOR, 'div.Io6YTe.fontBodyMedium.kR99db.fdkmkc ').text
            except:
                address = "N/A"

            try:
                website = driver.find_element(By.CSS_SELECTOR, 'div.rogA2c.ITvuef').text
            except:
                website = "N/A"

            try:
                phone = driver.find_element("css selector", 'button[data-item-id^="phone"] .Io6YTe').text
            except:
                phone = "N/A"

            data.append([title, rating, address, website, phone])

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    if storage_choice == '2':
        save_to_mysql(data, search_query)
    else:
        save_to_csv(data)

    driver.quit()


if __name__ == "__main__":
    main()
