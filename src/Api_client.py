import requests

class CountryLeadersAPI:

    def __init__(self, base_url="https://country-leaders.onrender.com"):
        self.base_url = base_url
        self.country_endpoint = f"{base_url}/countries"
        self.leaders_endpoint = f"{base_url}/leaders"
        self.cookies_endpoint = f"{base_url}/cookie"
        self.cookies = None
        self.refresh_cookie()

    def refresh_cookie(self):
        
        if self.cookies is None:
            try:
                response = requests.get(self.cookies_endpoint)
                self.cookies = response.cookies
            except Exception as e:
                print(f"Error getting cookies: {e}")

    def get_countries(self):
        try:
            response = requests.get(self.country_endpoint, cookies=self.cookies)
                        
            if response.status_code == 401 or response.status_code == 403:
                self.cookies = None # On réinitialise pour forcer refresh_cookie
                self.refresh_cookie()
                response = requests.get(self.country_endpoint, cookies=self.cookies)
                
            return response.json()
        except Exception as e:
            print(f"Error getting countries: {e}")
            return []

    def get_leaders(self, country):
        try:
            params = {"country": country}
            response = requests.get(self.leaders_endpoint, params=params, cookies=self.cookies)
            
            # Si le cookie a expiré au milieu de la boucle
            if response.status_code == 401 or response.status_code == 403:
                print("Token expired, refreshing cookie...")
                self.cookies = None
                self.refresh_cookie()
                response = requests.get(self.leaders_endpoint, params=params, cookies=self.cookies)
                
            return response.json()
        except Exception as e:
            print(f"Error getting leaders for {country}: {e}")
            return []


# test
if __name__ == "__main__":
    print("Testing CountryLeadersAPI...")
    client = CountryLeadersAPI()
    
    countries = client.get_countries()
    print(f"Countries found: {countries}")
    
    if countries:
        test_country = countries[0]
        print(f"Fetching leaders for: {test_country}")
        leaders = client.get_leaders(test_country)
        print(f"Successfully fetched {len(leaders)} leaders for {test_country}.")
        if leaders:
            print(f"First leader example: {leaders[0].get('first_name')} {leaders[0].get('last_name')}")