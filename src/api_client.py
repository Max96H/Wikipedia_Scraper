import requests                                         # to send requests on internet

class CountryLeadersAPI:
    '''
    This is a class that manages connections to the country leaders REST API.
    It acts as the main blueprint to store endpoints, cookies, and internal session logic.
    '''

    def __init__(self, base_url="https://country-leaders.onrender.com"):  # constructor
        '''
        This is the constructor method of the class.
        It accepts an optional parameter: 'base_url' (string, with a default value).
        Inside, it automatically calls the internal 'refresh_cookie' method.
        '''
        
        self.base_url = base_url                        # store var in object
        self.country_endpoint = f"{base_url}/countries"
        self.leaders_endpoint = f"{base_url}/leaders"
        self.cookies_endpoint = f"{base_url}/cookie"
        self.cookies = None
        self.refresh_cookie()

    def refresh_cookie(self):  
        '''
        This is an internal instance method of the class.
        It takes no arguments or parameters except the default 'self'.
        It calls the external 'requests.get' method to fetch new authentication tokens.
        '''
                                                        # Check validity: only fetch a new cookie if we don't have one
        if self.cookies is None:
            try:                                        # search new cookie on server
                response = requests.get(self.cookies_endpoint, timeout=10)
                self.cookies = response.cookies
            except Exception as e:
                print(f"Error getting cookies: {e}")

    def get_countries(self):                            # fct to have the list of countries
        
        '''
        This is an instance method used to fetch supported countries.
        It takes no extra parameters except 'self'.
        It internally calls 'requests.get' and invokes the 'self.refresh_cookie' method if access is denied.
        '''
        try:
            response = requests.get(self.country_endpoint, cookies=self.cookies, timeout=10)
                        
                                                        # if access denied or cookie expired
            if response.status_code == 401 or response.status_code == 403:  
                self.cookies = None                     # reinitialize to force cookie refresh
                self.refresh_cookie()                   # refresh cookie
                response = requests.get(self.country_endpoint, cookies=self.cookies, timeout=10)
                
            return response.json()                      # return the list of countries as json         
        except Exception as e:
            print(f"Error getting countries: {e}")
            return []

    def get_leaders(self, country):                     # fct to get leaders, need of the code of country in parameter
        '''
        This is an instance method used to fetch leaders for a specific nation.
        It requires one mandatory parameter: 'country' (string representing the country code).
        It calls 'requests.get' with query arguments and can invoke 'self.refresh_cookie' if needed.
        '''
        try:
            params = {"country": country}               # create dict params to see which country we want
            response = requests.get(self.leaders_endpoint, params=params, cookies=self.cookies, timeout=10)
            
                                                        # if cookie expired in the loop
            if response.status_code == 401 or response.status_code == 403:
                print("Token expired, refreshing cookie...")
                self.cookies = None
                self.refresh_cookie()
                response = requests.get(self.leaders_endpoint, params=params, cookies=self.cookies, timeout=10)
            return response.json()
        except Exception as e:                          # convert answer in python and send it back. If network doesn't work: error and empty list
            print(f"Error getting leaders for {country}: {e}")
            return []


# test
if __name__ == "__main__":                              # run the code only if we launch the file api_client.py (ignore if in main...)
    '''
    This is the main execution block for local script testing.
    It instantiates the 'CountryLeadersAPI' class and saves the object into the 'client' variable.
    It calls the object methods 'get_countries' and 'get_leaders' using local test variables as arguments.
    '''
    print("Testing CountryLeadersAPI...")
    client = CountryLeadersAPI()                        # msg and creation of object client, so call of the constructor and search 1st cookie
    
    countries = client.get_countries()
    print(f"Countries found: {countries}")              # call method to fetch countries and print result in the terminal.
    
    if countries:                                       # if countries in list, we fetch the 1st one, we call get_leaders() to test and print how many leaders have been found: len(leaders).
        test_country = countries[2]
        print(f"Fetching leaders for: {test_country}")
        leaders = client.get_leaders(test_country)
        print(f"Successfully fetched {len(leaders)} leaders for {test_country}.")
        
        if leaders:                                       # if leaders, we take the 1st of the list and we take first and last name to validate (dict contains info)
            print(f"First leader exple: {leaders[0].get('first_name')} {leaders[0].get('last_name')}")