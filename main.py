from src.api_client import CountryLeadersAPI
from src.html_scraper import WikipediaScraper
import requests

def main():
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

    js_file = "leaders.json"
    csv_file = "leaders.csv"

    wikipedia_scraper.to_json_file(js_file, leaders_per_countries)
    wikipedia_scraper.to_csv_file(csv_file, leaders_per_countries)



if __name__ == "__main__":
    main()