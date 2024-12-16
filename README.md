# Google Maps Data Scraper

A robust Python-based web scraping tool designed to extract business information from Google Maps. This tool automates the process of gathering data such as business names, ratings, addresses, websites, and phone numbers for any search query.

## Video Demonstration
Project Walkthrough Video : https://youtu.be/4FFlsmhf1A8

## 📋 Features

- **Automated Scrolling**: Automatically scrolls through search results to load all available entries
- **Comprehensive Data Collection**: Extracts multiple data points for each business:
  - Business name
  - Rating and number of reviews
  - Physical address
  - Website URL
  - Phone number
- **CSV Export**: Automatically saves data to CSV files with timestamped filenames
- **Error Handling**: Robust error handling for missing data and network issues
- **Progress Feedback**: Console output to track scraping progress

## 🔧 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.6 or higher
- Firefox web browser
- Selenium WebDriver
- Firefox GeckoDriver

## 📦 Installation

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install selenium
```

3. Install Firefox GeckoDriver:
   - Download the appropriate version from [Mozilla GeckoDriver releases](https://github.com/mozilla/geckodriver/releases)
   - Add the driver to your system's PATH

## 💻 Usage

1. Run the script:
```bash
python project.py
```

2. Enter your search query when prompted:
```
Enter the search query with location at the end: restaurants in New York
```

3. The script will:
   - Open Firefox browser
   - Navigate to Google Maps
   - Scroll through results
   - Extract data from each listing
   - Save results to a CSV file

## 📄 Output

The script generates a CSV file with the following format:
- Filename pattern: `scraped_data_YYYYMMDD_HHMMSS.csv`
- Headers: Title, Rating & no. of Reviews, Address, Website, Phone
- Each row contains data for one business listing

Example output:
```csv
Title,Rating & no. of Reviews,Address,Website,Phone
Restaurant A,4.5 (500 reviews),123 Main St,www.resta.com,555-0123
Restaurant B,4.2 (300 reviews),456 Oak Ave,www.restb.com,555-0456
```

## 🧪 Testing

The project includes a comprehensive test suite using pytest. To run the tests:

```bash
python -m pytest test_project.py -v
```

Test coverage includes:
- CSV file creation and formatting
- Scroll functionality
- Data scraping accuracy
- Error handling

## ⚠️ Important Notes

1. **Browser Window**: Do not close or minimize the browser window during scraping
2. **Rate Limiting**: Be mindful of Google's rate limiting and terms of service
3. **Network Dependencies**: Requires stable internet connection
4. **Data Availability**: Some businesses may have incomplete information

## 🔍 Functions Overview

### `save_to_csv(data)`
- Saves scraped data to a CSV file with timestamp
- Handles UTF-8 encoding for special characters
- Creates consistent header structure

### `scroll_to_load_results(driver, query)`
- Implements dynamic scrolling to load all results
- Includes delay to allow content loading
- Detects when all results are loaded

### `scrape_results(driver)`
- Extracts data from each business listing
- Implements error handling for missing fields
- Manages browser automation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details

## 👥 Authors

- Devansh Dave - Initial work

## 🙏 Acknowledgments

- Selenium Documentation
- Mozilla Firefox GeckoDriver team
- Python CSV module documentation
