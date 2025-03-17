The main.py is a web scraping script designed to collect product information from the Jumia website. Here is a summary of its key components:

**Imports:** 
Various libraries are imported, including requests_cache, BeautifulSoup, sqlite3, csv, json, and threading.

**Setup:**
Creates a cached session for HTTP requests.
Ensures a directory named 'data' exists.
Classes and Functions:

**Jumia Class:** 
A data class to store product information (name, price, stars, product link).

get_response(link): Sends a GET request to the provided link and returns the response if successful.
extract_text(soup, tags, sel, value): Extracts text from HTML elements.
pipline(value): Cleans text data.
next_page(html): Determines and navigates to the next page of products.
scraper(response): Scrapes product data from the response and returns it as dictionaries and tuples.
writer_to_json(data): Writes scraped data to a JSON file.
writer_to_csv(data): Writes scraped data to a CSV file.
sql_writer(data): Writes scraped data to an SQLite database.
main(link): The main function that ties together all the above functions to scrape data from a provided URL.

**Execution:**

The script starts scraping from a specific URL (https://www.jumia.com.ng/catalog/?q=itel) and uses threading to run the scraping process.
The script collects product details such as name, price, stars, and product link, and stores the data in JSON, CSV, and SQLite formats.
