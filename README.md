# Wikipedia Country Leaders Scraper

This project is a modular web scraping pipeline written in Python. It automates data collection on national leaders by combining information from a REST API with biographical data extracted directly from Wikipedia pages.

## Key Features

- **Decoupled API Client:** Automatically handles session cookies, authentication, and token refreshes upon expiration.
- **Robust HTML Scraper:** Extracts and cleans the primary biographical paragraphs from Wikipedia using BeautifulSoup and regex.
- **Modular Architecture (OOP):** Enforces a strict separation of concerns among network communication (`src/api_client.py`), HTML parsing (`src/html_scraper.py`), and central orchestration (`main.py`).
- **Sandbox Workspaces:** Dedicated environment (`dev/`) for individual prototyping and exploratory coding before committing to production modules.

---

## 📁 Project Structure

```text
wikipedia-scraper/
├── .gitignore              # Local environment, cache, and sandbox exclusions
├── README.md               # Project documentation
├── requirements.txt        # Managed list of third-party project dependencies
├── main.py                 # Central orchestrator (Main entry point)
├── dev/
│   ├── max_sandbox.ipynb   # Playground for individual development
│   └── siegried_sandbox.ipynb   
└── src/
    ├── __init__.py         # Package initializer
    ├── api_client.py       # CountryLeadersAPI class (Requests & cookies)
    └── html_scraper.py     # WikipediaScraper class (HTML parsing & cleaning)