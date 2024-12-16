from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import csv
from datetime import datetime


def main():
    query = input("Enter the search query with location at the end: ").replace(" ", "+")
    print("While Scrapping Do not close/minimize the browser window.")
    time.sleep(5)

    # Setting up web driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.get(f"https://www.google.com/maps/search/{query}")

    query = query.replace("+", " ")

    # function to scroll the results page to load all the results
    scroll_to_load_results(driver, query)

    scrape_results(driver)

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

def scrape_results(driver):
    # now scrapping of all the results will be done after waiting for 10 seconds to load the webpage
    time.sleep(10)
    elem_results = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')
    i = 0
    data = []

    for result in elem_results:
        i += 1
        if i % 5 == 0:
            driver.implicitly_wait(3)
        try:
            query_result = result.find_element(By.CSS_SELECTOR, 'a')

            driver.execute_script("arguments[0].scrollIntoView(true);", query_result)
            query_result.click()
            time.sleep(5)

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

    save_to_csv(data)

    driver.quit()


if __name__ == "__main__":
    main()
