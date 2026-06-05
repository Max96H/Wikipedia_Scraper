# WIKIPEDIA COUNTRY LEADERS SCRAPER

This project is a modular Python web scraping pipeline built in 3 days. It automatically collects data on political leaders by combining a custom REST API client with a BeautifulSoup scraper that extracts summaries directly from Wikipedia pages.


## KEY FEATURES

- **Dynamic File Exporter:** Built with the native argparse library, allowing the user to select the output format directly from the terminal using dedicated parameters. It can flatten nested data structures to generate a tabular .csv spreadsheet file ready for pandas, or export a standard structured .json database.
- **API Client with Cookie Refresh:** Automatically manages session cookies and refreshes them if they expire during execution.
- **HTML Scraper:** Grabs and cleans the first biographical paragraph of a leader's Wikipedia page using BeautifulSoup and regex.
- **OOP Architecture:** Clear separation of concerns between API requests (src/api_client.py), HTML processing (src/html_scraper.py), and the main orchestration (main.py).
- **Playgrounds:** A dev/ folder where we tested our endpoints and selectors in Jupyter Notebooks before writing production code.

## PROJECT STRUCTURE

```
wikipdia-scraper/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── dev/
│   ├── max_sandbox.ipynb
│   └── siegried_sandbox.ipynb
└── src/
├── __init__.py
├── api_client.py
└── html_scraper.py
```

## HOW TO SETUP AND RUN

To set up the project locally inside a clean virtual environment, run git clone https://github.com/Max96H/Wikipedia_Scraper/tree/main and then go inside the folder using cd wikipedia-scraper.

Create your virtual environment with python3 -m venv wikipedia_scraper_env. Activate it on Windows with source wikipedia_scraper_env/Scripts/activate (or on Linux/macOS with source wikipedia_scraper_env/bin/activate). 
Once activated, install the libraries with pip install -r requirements.txt.

To run the full scraper and generate the final data file, just execute python main.py. This will create a file named leaders.json at the root of the project.

If you want to test the components separately, you can run them individually. For the API connection and cookie checks, run python src/api_client.py. For the HTML extraction logic, run python src/html_scraper.py.

## HOW THE CODE WORKS

```
def main():

    parser = argparse.ArgumentParser(description="A wiki scraper to make json/csv file")
    parser.add_argument('--file', type=str, default='json', help='The type of file to create (json|csv)')
    args = parser.parse_args()

    chose_csv = False
    file = "leaders.json"
    if args.file == "csv":
        chose_csv = True
        file = "leaders.csv"

    base_url = "https://country-leaders.onrender.com"
    country_leader_api = CountryLeadersAPI(base_url)

    countries = country_leader_api.get_countries()

    leaders_per_countries = {}
    for country in countries:
        leaders = country_leader_api.get_leaders(country)

        leaders_per_countries[country] = leaders

    with requests.Session() as session:
        wikipedia_scraper = WikipediaScraper(session)

        for country, leaders in leaders_per_countries.items():
            for i, leader in enumerate(leaders):
                html = wikipedia_scraper.fetch_html(leader["wikipedia_url"])

                leaders_per_countries[country][i]["first_paragraph"] = wikipedia_scraper.get_first_paragraph(html)


    if chose_csv:
        wikipedia_scraper.to_csv_file(file, leaders_per_countries)
        print(1)
    else:
        wikipedia_scraper.to_json_file(file, leaders_per_countries)
        print(2)



if __name__ == "__main__":
    main()
```

We split the core logic into two tracks before plugging everything together in the main file:

### The API Part (src/api_client.py)
This file contains the CountryLeadersAPI class. Its main job is to fetch raw JSON data from the server. It handles security by checking for 401 and 403 HTTP status codes. If a token expires while looping through the data, the refresh_cookie method triggers automatically to get a new one. It uses get_countries to see which countries are supported and get_leaders to fetch the list of politicians for a specific country.

### The Scraping Part (src/html_scraper.py)
This file handles the WikipediaScraper class. To avoid overloading the network, it reuses the same requests.Session object created by the main script. The get_first_paragraph method uses BeautifulSoup to search the first 10 paragraphs of the page. It looks for a bold tag () which usually contains the leader's name, meaning it found the actual introduction. The clean_text method uses regex (re.sub) to strip out annoying Wikipedia artifacts like citation brackets (e.g., [1], [n 3]), extra newlines (\n), or the speaker icon (Écouterⓘ).

### Integration (main.py)
This is the central script. It coordinates the whole pipeline: it calls the API client to map out the target countries, fetches the leaders, loops through their Wikipedia URLs, uses the scraper to append the text summary to each leader, and finally saves everything into a JSON file.

```
 {
        "id": "Q329",
        "first_name": "Nicolas",
        "last_name": "Sarkozy",
        "birth_date": "1955-01-28",
        "death_date": null,
        "place_of_birth": "Paris",
        "wikipedia_url": "https://fr.wikipedia.org/wiki/Nicolas_Sarkozy",
        "start_mandate": "2007-05-16",
        "end_mandate": "2012-05-15",
        "biography": "Nicolas Sarközy de Nagy-Bocsa, dit Nicolas Sarkozy (/ni.kɔ.la saʁ.kɔ.zi/ Écouterⓘ ; en hongrois Sárközy ou Sárközi ,,), né le 28 janvier 1955 à Paris 17e (Seine), est un homme d'État français. Il est président de la République française du 16 mai 2007 au 15 mai 2012."
    },
```

## GIT FLOW & COLLABORATION

To simulate the real-world conditions of a data engineering pipeline in a company, any direct push to the main branch was strictly prohibited.
All phases of individual exploration and prototyping were restricted to the dev directory using the files max_sandbox_notebooook.ipynb and siegried_sandbox_notebooook.ipynb. The production code was developed on the branch Sieg for the api-client and on the branch Max for the html-scraper. Each feature integration required opening a formal Pull Request (PR) on GitHub, followed by a code review and manual approval from the partner before it could be merged.
