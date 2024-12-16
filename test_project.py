import os
import csv
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock
from project import save_to_csv, scroll_to_load_results, scrape_results
from selenium.webdriver.common.keys import Keys
import pytest

def test_scroll_to_load_results():
    driver = MagicMock()
    div_sidebar = MagicMock()
    driver.find_element.return_value = div_sidebar

    scroll_to_load_results(driver, "test query")

    assert div_sidebar.send_keys.call_count == 2

def test_scrape_results():
    driver = MagicMock()
    element_results = [MagicMock() for _ in range(10)]
    driver.find_elements.return_value = element_results

    scrape_results(driver)

    assert driver.execute_script.call_count == 10
    assert driver.find_element.call_count >= 5
    driver.quit.assert_called_once()

import csv
from unittest.mock import patch, mock_open
from datetime import datetime

def test_save_to_csv():
    data = [
        ["Title 1", "4.5 (100 reviews)", "123 Main St, Anytown USA", "www.example.com", "555-1234"],
        ["Title 2", "3.8 (75 reviews)", "456 Oak Rd, Othertown USA", "www.otherexample.com", "555-5678"]
    ]
    fixed_time = datetime(2023, 1, 1, 12, 0, 0)

    with patch("builtins.open", mock_open()) as mock_file:
        with patch("project.datetime") as mock_datetime:
            mock_datetime.now.return_value = fixed_time

            with patch("csv.writer") as mock_csv_writer:
                save_to_csv(data)

                mock_file.assert_called_with("scraped_data_20230101_120000.csv", mode="w", newline='', encoding="utf-8")

                # Check that writerow and writerows were called correctly
                handle = mock_file()
                mock_csv_writer.return_value.writerow.assert_any_call(["Title", "Rating & no. of Reviews", "Address", "Website", "Phone"])
                mock_csv_writer.return_value.writerows.assert_called_with(data)

test_save_to_csv()
