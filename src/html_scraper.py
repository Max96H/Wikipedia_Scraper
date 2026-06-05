from bs4 import BeautifulSoup
import json
import re
import requests

class WikipediaScraper():
    def __init__(self, session):
        self.session = session
    
    def fetch_html(self, url: str):
        leader_wiki = ""
        try:
            #Using the opened session to scrape a wikipedia page
            leader_wiki = self.session.get(url, headers={"User-Agent": "MyDataScraperBot/1.0 BasedOnPythonRequests"})
            match leader_wiki.status_code:
                case 404:
                    raise Exception("Could not find this url")
                case 500:
                    raise Exception("Servor problem")
        except Exception as ex:
            print(f"Something went wrong: {ex}")
        except BaseException as ex:
            print(f"Something went wrong: {ex}")
        finally:
            return leader_wiki
        
    def get_first_paragraph(self, html: str):
        first_paragraph = "failed"
        try:
            #Loading the content (html tree) in a BeautifulSoup Object
            soup = BeautifulSoup(html.text, features="html.parser")
            #Making a list of all the paragraphs and checking there was at least one
            paragraphs = soup.find_all("p")
            if not paragraphs:
                raise Exception("Couldn't find any paragraphs.")
            #Going throug the first ten and finding the first with an emboldened part and checking if there was at least one
            for p in paragraphs[:10]:
                if p.find("b"):
                    first_paragraph = self.clean_text(str(p.text))
                    break
            if first_paragraph == "failed":
                raise Exception(f"Couldn't find a paragraph containing <bold> within : {paragraphs[:10]}")
        except Exception as ex:
            print("Something went wrong", ex)
        except BaseException as ex:
            print("Something went wrong", ex)
        # Whatever happens, return a string
        finally:
            return first_paragraph
    
    def clean_text(self, text: str):
        problem_chars = ["Écouterⓘ", "\\[n 3\\]", "\\[\\w\\]","\\(uitspraakⓘ\\)", "uitspraakⓘ", "ⓘ", "\\n", "\\[\\d+\\]"]
        for char in problem_chars:
            text = re.sub(char, "", text)
        return text

    def to_json_file(self, filepath: str, leaders) -> None:
        with open(filepath, "w") as js_file:
            js_str = json.dumps(leaders)
            js_file.write(js_str)

    def to_csv_file(self, filepath: str, leaders) -> None:
        with open(filepath, "w") as csv_file:
            for country, leads in leaders.items():
                csv_file.write(f"{country}\n")
                csv_file.write(",".join(map(str, leads)) + "\n")


if __name__ == "__main__":
    with requests.Session() as session:
        wiki = WikipediaScraper(session)

        html = wiki.fetch_html("https://fr.wikipedia.org/wiki/Fran%C3%A7ois_Hollande")

        fp = wiki.get_first_paragraph(html)

        print(fp)