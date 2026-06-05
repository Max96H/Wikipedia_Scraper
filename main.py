from src.api_client import CountryLeadersAPI
from src.html_scraper import WikipediaScraper
import argparse
import requests

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