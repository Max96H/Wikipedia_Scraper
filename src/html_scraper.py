from bs4 import BeautifulSoup
import json
import re
import requests

class WikipediaScraper():
    def __init__(self, session):
        """
        Constructor with one parameter
        :param: a requests.Session() object put into self.session attribute
        """
        self.session = session
    
    def fetch_html(self, url: str):
        """
        Method to fetch a web page's html
        :param: string of an url
        Returns the html or an empty string if unsuccessfull
        """
        leader_wiki = ""
        try:
            #Using the opened session to scrape a wikipedia page
            leader_wiki = self.session.get(url, headers={"User-Agent": "MyDataScraperBot/1.0 BasedOnPythonRequests"})
            #Handling of errors
            match leader_wiki.status_code:
                case 404:
                    raise Exception("Could not find this url")
                case 500:
                    raise Exception("Servor problem")
        except Exception as ex:
            print(f"Something went wrong: {ex}")
        except BaseException as ex:
            print(f"Something went wrong: {ex}")
        #Whatever happens, returns a string 
        finally:
            return leader_wiki
        
    def get_first_paragraph(self, html: str):
        """
        Method to get the first paragraph of someone's biography on wikipedia
        :param: a string of a web page's html
        Returns a string of the first paragraph or 'failed' if unsuccessfull
        """
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
        #Handling of errors
        except Exception as ex:
            print("Something went wrong", ex)
        except BaseException as ex:
            print("Something went wrong", ex)
        # Whatever happens, return a string
        finally:
            return first_paragraph
    
    def clean_text(self, text: str):
        """
        Method to clean a string with re library
        :param: a string to parse
        Returns the parsed string
        """
        #List of characters to remove
        problem_chars = ["Écouterⓘ", "\\[n 3\\]", "\\[\\w\\]","\\(uitspraakⓘ\\)", "uitspraakⓘ", "ⓘ", "\\n", "\\[\\d+\\]"]
        #Removing the characters by "" 
        for char in problem_chars:
            text = re.sub(char, "", text)
        return text

    def to_json_file(self, filepath: str, leaders) -> None:
        """
        Method to create or overwrite a json file
        :param: string of the filepath
        :param: Python object to put in the file
        """
        with open(filepath, "w") as js_file:
            #Transform the python object in a json string
            js_str = json.dumps(leaders)
            js_file.write(js_str)

    def to_csv_file(self, filepath: str, leaders: dict) -> None:
        """
        Method to create or overwrite a csv file
        :param: string of the filepath
        :param: Python dictionary to put in the file
        """
        with open(filepath, "w") as csv_file:
            #Write each key on a line and the value on the following line
            for country, leads in leaders.items():
                csv_file.write(f"{country}\n")
                #Transform the list of dictionaries (the value) in strings and join them with commas
                csv_file.write(",".join(map(str, leads)) + "\n")


if __name__ == "__main__":
    #Some testing of the class and it's methods if this file is directly executed in a command line
    with requests.Session() as session:
        wiki = WikipediaScraper(session)

        html = wiki.fetch_html("https://fr.wikipedia.org/wiki/Fran%C3%A7ois_Hollande")

        fp = wiki.get_first_paragraph(html)

        print(fp)