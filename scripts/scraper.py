import requests
from bs4 import BeautifulSoup
import csv
import re

urltype ='short'

# Function to scrape page information: titles, numeric value, and total pages
def scrape_page_info():
    # Base URL for the site to scrape from
    base_url = f'https://www.boerse.de/hebelzertifikate/{urltype}/Rheinmetall-Aktie/DE0007030009'

    # Send a GET request to the page
    response = requests.get(base_url)
    response.raise_for_status()  # If the response was unsuccessful, raise an HTTPError

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table head containing the headers
    table_head = soup.find('thead')

    # Extract the column headers
    titles = [th.text.strip() for th in table_head.find_all('th') if th.text.strip()]

    # Find the numeric value
    stockval_element = soup.find('div', class_='col-sm-4')
    if stockval_element:
        text_inside_div = stockval_element.text.strip()
        cleaned_text = ''.join(filter(str.isdigit, text_inside_div))
        numeric_value = float(cleaned_text) / 100  # Divide by 100 to handle the decimal point
    else:
        print("Div element not found.")
        numeric_value = None

    # Find the total number of pages
    
    response = requests.get(base_url)
    response.raise_for_status()
    content = response.text
    pattern = r'<a[^>]*?href="#"[^>]*?>(\d+)</a>'
    matches = re.findall(pattern, content)
    page_numbers = [int(num) for num in matches]
    total_pages = max(page_numbers)

    return titles, numeric_value, total_pages

# Function to scrape the table rows from a single page
def scrape_table_rows(page_number):
    # Base URL for the site to scrape from
    base_url = 'https://www.boerse.de/ajax/table.php'

    # Parameters for the POST request
    params = {
        'TYP': 'Derivate',
        'SEARCH_D[za]': '7',
        'SEARCH_D[ag]': '',
        'SEARCH_D[emittent_id]': '',
        'SEARCH_D[emittent_name]': '',
        'SEARCH_D[isin]': '',
        'SEARCH_D[diff_knock_out]': '|',
        'SEARCH_D[diff_knock_out_rel]': '',
        'SEARCH_D[diff_strike]': '',
        'SEARCH_D[diff_strike_rel]': '',
        'SEARCH_D[implied_vola]': '|',
        'SEARCH_D[leverage]': '|',
        'SEARCH_D[knock_out]': '|',
        'SEARCH_D[kurs_ask]': '',
        'SEARCH_D[kurs_bid]': '',
        'SEARCH_D[laufzeit_ende]': '2024-04-25|2099-12-31',
        'SEARCH_D[laufzeit_start]': '1900-00-00|2024-04-25',
        'SEARCH_D[produkt_name]': '',
        'SEARCH_D[strike]': '|',
        'SEARCH_D[typ]':urltype,
        'SEARCH_D[underlying_isin]': 'DE0007030009',
        'SEARCH_D[underlying_name]': '',
        'SEARCH_D[underlying_preis]': '',
        'SEARCH_D[wkn]': '',
        'SEARCH_D[page_size]': '50',
        'SEARCH_D[sort]': 'h',
        'SEARCH_D[sort_d]': 'desc',
        'SEARCH_D[spread]': '|',
        'SEARCH_D[cols]': '',
        'SEARCH_D[eq_quanto]': '',
        'K_SORT': '1',
        'LISTID': 'derivate',
        'FIELDS[0]': 'wkn',
        'FIELDS[1]': 'B',
        'FIELDS[2]': 'w',
        'FIELDS[3]': 'typ',
        'FIELDS[4]': 'b',
        'FIELDS[5]': 'a',
        'FIELDS[6]': 'k',
        'FIELDS[7]': 'h',
        'FIELDS[8]': 'e',
        'FIELDS[9]': 'u',
        'FIELDSMOBILE[0]': 'wkn',
        'FIELDSMOBILE[6]': 'k',
        'FIELDSMOBILE[7]': 'h',
        'FIELDSMOBILE[8]': 'e',
        'FIELDSMOBILE[9]': 'u',
        'BOX_ID': '0',
        'SIGN': '',
        'DUMPTIME': '7200',
        'HEADLINE': '',
        'ADPARAGRAPH': '',
        'PUSHLIST': '',
        'TS_SORT': '1',
        'TS_SORTCOL': '1',
        'TS_SORTORDER': '0',
        'TS_PAGE_SIZE': '100',
        'INIT': '',
        'PUSH_LIST_ID': 'pushList',
        'PUSH_BUTTON_ID': 'pushButton',
        'COUNTFIELDS': '10',
        'TOPFLOPLIST': '',
        'TOPFLOPHEAD': '1',
        'TOPFLOPINTERVAL': '1',
        'SHOWMEHR': '',
        'HEADID': '',
        'AKTIEN': '',
        'SEARCH_D[page]': str(page_number)
    }

    # Send a POST request to the page
    response = requests.post(base_url, data=params)
    response.raise_for_status()  # If the response was unsuccessful, raise an HTTPError

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table rows containing the data
    table_body = soup.find('tbody')

    # Extract data from each row
    rows = []
    for row in table_body.find_all('tr'):
        # Check if the row has the specified class
        if 'kurslistenwerbesatz' not in row.get('class', []):
            row_data = []
            for td in row.find_all('td'):
                # Check if the value can be converted to a float
                try:
                    row_data.append(float(td.text.strip().replace(',', '.')))
                except ValueError:
                    row_data.append(td.text.strip())
            rows.append(row_data)

    return rows

# Function to calculate Abstand, Abstand in %, and Risk/Reward for each row and write to CSV
def write_to_csv_with_calculations(filename, titles, rows, numeric_value):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        headers = titles + ['Abstand', 'Abstand in %', 'Risk/Reward']
        csv_writer.writerow(headers)  # Write headers
        for row in rows:
            # Calculate Abstand
            if row[3] == 'Call':
                abstand = numeric_value - row[9]
            else:
                abstand = row[9] - numeric_value

            # Calculate Abstand in percentage
            abstand_percentage = (abstand / numeric_value) * 100

            # Calculate Risk/Reward ratio
            hebel = row[7]
            risk_reward = abstand / hebel

            # Update row with calculated values
            row.extend([abstand, abstand_percentage, risk_reward])
            csv_writer.writerow(row)

# Main function to scrape and write data for multiple pages
def scrape_multiple_pages_and_write_to_csv(total_pages):
    titles, numeric_value, _ = scrape_page_info()
    print("Numeric Value:", numeric_value)
    filename = 'output.csv'
    for page_number in range(1, total_pages+1 ):
        # Scrape data from the current page
        rows = scrape_table_rows(page_number)
        # Write all scraped data to a CSV file with calculations
        write_to_csv_with_calculations(filename, titles, rows, numeric_value)
        print(f'Data from page {page_number} written to {filename}')

# Call the function to scrape and write data for multiple pages
_, _, total_pages = scrape_page_info()
print("Total Pages:", total_pages)
scrape_multiple_pages_and_write_to_csv(total_pages)

# wait 5 secnods
import time
time.sleep(2)
print("Done")

# execute the plot.py script

