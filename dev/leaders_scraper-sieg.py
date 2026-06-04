import json
import re
import requests                             
from bs4 import BeautifulSoup

ROOT_URL = "https://country-leaders.onrender.com"

def get_cookie():
    cookie_url = f"{ROOT_URL}/cookie"
    response = requests.get(cookie_url)
    return response.cookies


def get_first_paragraph(wikipedia_url, session):
    
    headers = {"User-Agent": "SiegriedSandbox (siegca@hotmail.com)"}
    try:
        html_content = session.get(wikipedia_url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html_content, "html.parser")

        for p in soup.find_all("p"):
            if p.find("b") and len(p.get_text().strip()) > 40:
                text = p.get_text()
                # clean the text
                text = re.sub(r"\[.*?\]", "", text)
                text = re.sub(r"\(\s*([;,.\s]*)\s*\)", "", text)
                return re.sub(r"\s+", " ", text).strip()
    except Exception as e:
        print(f"Error scraping {wikipedia_url}: {e}")

    return "Biography unavailable."


def get_leaders():
    cookie = get_cookie()
    countries_req = requests.get(f"{ROOT_URL}/countries", cookies=cookie)
    countries = countries_req.json()

    leaders_data = []

    with requests.Session() as wiki_session:
        for country in countries:
            req = requests.get(f"{ROOT_URL}/leaders", params={"country": country}, cookies=cookie,)

            if req.status_code in [401, 403]:
                print(f"Cookies expired while fetching {country}; refreshing token")
                cookie = get_cookie()
                req = requests.get(f"{ROOT_URL}/leaders", params={"country": country}, cookies=cookie,)

            leaders = req.json()
            for leader in leaders:
                if isinstance(leader, dict) and leader.get("wikipedia_url"):
                    wiki_url = leader["wikipedia_url"]
                    print(f"Scraping: {leader.get('first_name')} {leader.get('last_name')}")
                    leader["biography"] = get_first_paragraph(
                        wiki_url, wiki_session)
                    leaders_data.append(leader)

    return leaders_data


def save(leaders_per_country):
                                                # save the final structure directly to disk
    with open("leaders.json", "w", encoding="utf-8") as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)
    print("Data saved to leaders-sieg.json")

#test
if __name__ == "__main__":
    print("Starting Country Leaders Scraping")
    all_leaders = get_leaders()
    save(all_leaders)
    print("Finished successfully!")