---
name: scrape
description: "Web scraping and data acquisition from websites, APIs, and online sources. Use for extracting structured data from web pages, handling pagination, managing rate limits, and storing scraped data."
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Glob
  - WebFetch
  - Bash(python *)
  - Bash(pip install *)
  - Bash(playwright *)
hooks:
  PostToolUse:
    - matcher: "*"
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Web Scraping & Data Acquisition

Systematic approach to extracting data from websites, APIs, and online sources. Covers ethics, techniques, and best practices.

## Ethics & Legal Considerations

**Before scraping ANY website:**

1. **Check robots.txt**: `https://example.com/robots.txt`
2. **Read Terms of Service**: Many sites prohibit scraping
3. **Check for APIs**: Official API is always preferred
4. **Respect rate limits**: Don't overload servers
5. **Identify yourself**: Use descriptive User-Agent
6. **Store responsibly**: Consider data privacy laws (GDPR, etc.)

```python
# Check robots.txt
import urllib.robotparser

def can_scrape(url, user_agent='*'):
    """Check if scraping is allowed by robots.txt."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    return rp.can_fetch(user_agent, url)

# Usage
if can_scrape('https://example.com/data'):
    print("Scraping allowed")
else:
    print("Check robots.txt - scraping may not be allowed")
```

---

## Quick Start: Requests + BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

# Fetch page
headers = {'User-Agent': 'DataCollector/1.0 (contact@example.com)'}
response = requests.get('https://example.com', headers=headers)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements
title = soup.find('h1').text
links = [a['href'] for a in soup.find_all('a', href=True)]
tables = soup.find_all('table')
```

---

## Method 1: Static HTML Scraping

### Basic Pattern

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class StaticScraper:
    def __init__(self, base_url, rate_limit=1.0):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DataCollector/1.0 (research purposes)',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def fetch(self, url):
        """Fetch page with rate limiting."""
        time.sleep(self.rate_limit)
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def extract_table(self, soup, table_index=0):
        """Extract table to DataFrame."""
        tables = soup.find_all('table')
        if table_index < len(tables):
            return pd.read_html(str(tables[table_index]))[0]
        return None

    def extract_list(self, soup, selector):
        """Extract list items."""
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]

# Usage
scraper = StaticScraper('https://example.com')
soup = scraper.fetch('https://example.com/data')
df = scraper.extract_table(soup)
```

### CSS Selectors

```python
# Common selectors
soup.select('div.class-name')          # Class
soup.select('div#id-name')             # ID
soup.select('div[data-id="123"]')      # Attribute
soup.select('table > tbody > tr')      # Child combinator
soup.select('div.parent span.child')   # Descendant
soup.select('h2 + p')                  # Adjacent sibling
soup.select('li:nth-child(2)')         # Position

# Extract text and attributes
elements = soup.select('a.link')
for el in elements:
    text = el.get_text(strip=True)
    href = el.get('href')
    data_id = el.get('data-id')
```

### Handling Pagination

```python
def scrape_paginated(base_url, page_param='page', max_pages=10):
    """Scrape multiple pages."""
    all_data = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}?{page_param}={page}"
        soup = scraper.fetch(url)

        # Extract data from this page
        items = soup.select('.item')
        if not items:
            break  # No more data

        for item in items:
            all_data.append({
                'title': item.select_one('.title').text.strip(),
                'price': item.select_one('.price').text.strip(),
                'link': item.select_one('a')['href']
            })

        print(f"Page {page}: {len(items)} items")

    return pd.DataFrame(all_data)
```

---

## Method 2: JavaScript-Rendered Pages (Playwright)

For sites that load content via JavaScript:

```python
from playwright.sync_api import sync_playwright
import pandas as pd

class DynamicScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self

    def __exit__(self, *args):
        self.browser.close()
        self.playwright.stop()

    def fetch(self, url, wait_for=None, timeout=30000):
        """Navigate and wait for content."""
        self.page.goto(url, timeout=timeout)
        if wait_for:
            self.page.wait_for_selector(wait_for, timeout=timeout)
        return self.page.content()

    def click_and_wait(self, selector, wait_for=None):
        """Click element and wait."""
        self.page.click(selector)
        if wait_for:
            self.page.wait_for_selector(wait_for)
        return self.page.content()

    def scroll_to_bottom(self, pause=1.0):
        """Scroll to load lazy content."""
        prev_height = 0
        while True:
            self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            self.page.wait_for_timeout(int(pause * 1000))
            new_height = self.page.evaluate('document.body.scrollHeight')
            if new_height == prev_height:
                break
            prev_height = new_height

    def screenshot(self, path):
        """Take screenshot for debugging."""
        self.page.screenshot(path=path)

# Usage
with DynamicScraper(headless=True) as scraper:
    html = scraper.fetch('https://example.com/spa', wait_for='.data-loaded')
    soup = BeautifulSoup(html, 'html.parser')
    # Extract data from soup
```

### Handling Infinite Scroll

```python
with DynamicScraper() as scraper:
    scraper.fetch('https://example.com/feed')

    all_items = []
    for i in range(10):  # Max 10 scroll iterations
        # Extract current items
        soup = BeautifulSoup(scraper.page.content(), 'html.parser')
        items = soup.select('.feed-item')
        all_items.extend([item.text for item in items])

        # Scroll and wait for new content
        scraper.scroll_to_bottom(pause=2.0)

        # Check if new items loaded
        new_soup = BeautifulSoup(scraper.page.content(), 'html.parser')
        if len(new_soup.select('.feed-item')) == len(items):
            break  # No new items

    print(f"Collected {len(all_items)} items")
```

---

## Method 3: APIs

### REST APIs

```python
import requests

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
        self.session.headers['Content-Type'] = 'application/json'

    def get(self, endpoint, params=None):
        """GET request."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        """POST request."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def paginate(self, endpoint, page_size=100, max_pages=None):
        """Paginate through results."""
        all_results = []
        page = 1

        while True:
            params = {'page': page, 'per_page': page_size}
            data = self.get(endpoint, params)

            if not data.get('results'):
                break

            all_results.extend(data['results'])
            page += 1

            if max_pages and page > max_pages:
                break

        return all_results

# Usage
api = APIClient('https://api.example.com/v1', api_key='your-key')
data = api.get('users', params={'status': 'active'})
all_data = api.paginate('products', page_size=50)
```

### Handling Rate Limits

```python
import time
from functools import wraps

def rate_limited(max_per_second):
    """Decorator to rate limit function calls."""
    min_interval = 1.0 / max_per_second
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@rate_limited(2)  # Max 2 calls per second
def fetch_data(url):
    return requests.get(url).json()
```

### Retry Logic

```python
import time
from requests.exceptions import RequestException

def retry_request(func, max_retries=3, backoff=2):
    """Retry with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait = backoff ** attempt
            print(f"Retry {attempt + 1}/{max_retries} in {wait}s: {e}")
            time.sleep(wait)

# Usage
data = retry_request(lambda: requests.get(url).json())
```

---

## Data Extraction Patterns

### Tables to DataFrame

```python
import pandas as pd

# Method 1: pd.read_html (automatic)
tables = pd.read_html('https://example.com/table-page')
df = tables[0]  # First table

# Method 2: Manual extraction
def extract_table_manual(soup, table_selector):
    table = soup.select_one(table_selector)
    headers = [th.text.strip() for th in table.select('thead th')]
    rows = []
    for tr in table.select('tbody tr'):
        row = [td.text.strip() for td in tr.select('td')]
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)
```

### Lists and Cards

```python
def extract_cards(soup, card_selector, field_map):
    """
    Extract data from repeated card elements.

    field_map: {'output_field': 'css_selector'}
    """
    data = []
    for card in soup.select(card_selector):
        item = {}
        for field, selector in field_map.items():
            el = card.select_one(selector)
            item[field] = el.text.strip() if el else None
        data.append(item)
    return pd.DataFrame(data)

# Usage
field_map = {
    'title': 'h3.title',
    'price': '.price',
    'rating': '.rating span',
    'url': 'a.link::attr(href)'
}
df = extract_cards(soup, '.product-card', field_map)
```

### Nested Data

```python
def extract_nested(soup):
    """Extract hierarchical data."""
    categories = []

    for cat in soup.select('.category'):
        category = {
            'name': cat.select_one('.cat-name').text.strip(),
            'items': []
        }

        for item in cat.select('.item'):
            category['items'].append({
                'name': item.select_one('.item-name').text.strip(),
                'value': item.select_one('.item-value').text.strip()
            })

        categories.append(category)

    return categories
```

---

## Data Cleaning

```python
import re
import pandas as pd

def clean_scraped_data(df):
    """Clean common scraping artifacts."""
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == 'object':
            # Remove extra whitespace
            df[col] = df[col].str.strip()
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)

            # Remove newlines
            df[col] = df[col].str.replace(r'[\n\r\t]', ' ', regex=True)

    return df

def parse_price(price_str):
    """Parse price string to float."""
    if pd.isna(price_str):
        return None
    # Remove currency symbols and commas
    clean = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(clean)
    except:
        return None

def parse_number(num_str):
    """Parse number with K/M suffixes."""
    if pd.isna(num_str):
        return None
    num_str = str(num_str).upper().strip()
    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    for suffix, mult in multipliers.items():
        if suffix in num_str:
            num_str = num_str.replace(suffix, '')
            try:
                return float(num_str) * mult
            except:
                return None
    try:
        return float(re.sub(r'[^\d.]', '', num_str))
    except:
        return None
```

---

## Storage

### To CSV/Excel

```python
# Incremental save (append mode)
def save_batch(data, filepath, mode='a'):
    df = pd.DataFrame(data)
    header = not os.path.exists(filepath) if mode == 'a' else True
    df.to_csv(filepath, mode=mode, header=header, index=False)
```

### To SQLite

```python
import sqlite3

def save_to_sqlite(df, db_path, table_name, if_exists='append'):
    """Save DataFrame to SQLite."""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()

def load_from_sqlite(db_path, query):
    """Load data from SQLite."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

### To JSON (with progress tracking)

```python
import json

class IncrementalJSONWriter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.items = []

    def add(self, item):
        self.items.append(item)
        if len(self.items) >= 100:  # Batch size
            self.flush()

    def flush(self):
        if not self.items:
            return
        # Append to file
        mode = 'a' if os.path.exists(self.filepath) else 'w'
        with open(self.filepath, mode) as f:
            for item in self.items:
                f.write(json.dumps(item) + '\n')
        self.items = []

    def close(self):
        self.flush()
```

---

## Complete Example: E-commerce Scraper

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class EcommerceScraper:
    def __init__(self, base_url, rate_limit=1.0):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ProductResearchBot/1.0'
        })

    def fetch(self, url):
        time.sleep(self.rate_limit)
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def parse_product(self, product_el):
        """Parse single product element."""
        return {
            'name': product_el.select_one('.product-name').text.strip(),
            'price': self.parse_price(product_el.select_one('.price')),
            'rating': self.parse_rating(product_el.select_one('.rating')),
            'reviews': self.parse_number(product_el.select_one('.review-count')),
            'url': product_el.select_one('a.product-link')['href']
        }

    def parse_price(self, el):
        if not el:
            return None
        text = el.text.strip()
        match = re.search(r'[\d,.]+', text)
        return float(match.group().replace(',', '')) if match else None

    def parse_rating(self, el):
        if not el:
            return None
        text = el.text.strip()
        match = re.search(r'[\d.]+', text)
        return float(match.group()) if match else None

    def parse_number(self, el):
        if not el:
            return None
        text = el.text.strip()
        match = re.search(r'[\d,]+', text)
        return int(match.group().replace(',', '')) if match else None

    def scrape_category(self, category_url, max_pages=10):
        """Scrape all products from a category."""
        products = []
        page = 1

        while page <= max_pages:
            url = f"{category_url}?page={page}"
            print(f"Scraping page {page}...")

            try:
                soup = self.fetch(url)
                product_els = soup.select('.product-card')

                if not product_els:
                    break

                for el in product_els:
                    try:
                        product = self.parse_product(el)
                        products.append(product)
                    except Exception as e:
                        print(f"Error parsing product: {e}")

                page += 1

            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

        return pd.DataFrame(products)

# Usage
# scraper = EcommerceScraper('https://example-store.com')
# df = scraper.scrape_category('https://example-store.com/electronics')
# df.to_csv('products.csv', index=False)
```

---

## Tips

1. **Start small**: Test on 1-2 pages before scaling
2. **Save progress**: Write to disk incrementally for long scrapes
3. **Handle errors gracefully**: Log and continue, don't crash
4. **Monitor for changes**: Websites change - your scraper will break
5. **Use caching**: Don't re-fetch pages you already have
6. **Be respectful**: Scrape during off-peak hours when possible
7. **Document your selectors**: Comment why you chose each one
