import requests
import json

LIB_NAME = "Dragon's Hoard"
VERSION = "0.0.12"

class Dragon():
    """This class manages the API requests and saves the received data
    into pre-defined files.
    Takes the API KEY needed to access the url and the target resource;
    see https://comicvine.gamespot.com/api/documentation for options."""
    def __init__(self, api:str, resource:str = '', format:str = 'json'):
        ## Class constants
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
            }

        ## Class variables
        self.api_key = api
        self.format = format
        self.url = 'https://comicvine.gamespot.com/api/' + resource.lower() + '/'
        self.acquired_results = 0
        self.total_results = 100
        self.offset = 0
        self.my_hoard = {} # where we will save the formatted requested data

    def melt_gold(self, data:list) -> dict:
        """Turns the list received from results into a dictionary
        with key:value pairs that can be more easily saved and loaded from
        the json files."""
        return {str(entry['id']):entry for entry in data}
    
    def take_flight(self, file:str):
        """Called to set the initial offset to correspond to the amount of entries in a given file.
        Sets to 0 if no file found."""
        try:
            with open(file, mode='r') as f:
                data = json.load(file)
                self.offset = len(data)
        except FileNotFoundError:
            self.offset = 0

    def hoard(self, fmt_data:dict, save_target:str):
        """Saves acquired data into a chosen file.
        First tries to load json info from file if it exists to update,
        then dumps."""
        # try opening file to verify it already exixts
        try:
            with open(save_target, mode='r') as file:
                print(f'File "{save_target}" found. Loading data...')
                saved_data = json.load(file)
        # if it doesn't exist, create new and save formatted data
        except FileNotFoundError:
            print(f'File "{save_target}" not found. Creating new one...')
            with open(save_target, mode='w') as file:
                json.dump(fmt_data, file, indent=2, sort_keys=True)
        # if it exists and we acquired the data, update and save
        else:
            saved_data.update(fmt_data)
            with open(save_target, mode='w') as file:
                json.dump(saved_data, file, indent=2, sort_keys=True)
        finally:
            print('Data saved.')

    def pillage(self,
                offset:int = -1,
                fields:str = '',
                url:str = 'https://comicvine.gamespot.com/api/') -> dict:
        """Connects to the url with the given payload and acquires data.
        Returns a dictionary containing that info that can be easily saved in
        a json file."""

        if offset != -1:
            self.offset = offset

        # If the 'fields' argument was received, check to see if contains 'id'.
        # If not, add to it so the class can work
        if fields != '' and 'id' not in fields:
            fields += ',id'

        payload = {
            'api_key': self.api_key,
            'format': self.format,
            'offset': str(self.offset),
            'field_list': fields,
        }

        self.acquired_results = offset # in case we are starting somewhere
        re = requests.get(url=self.url, params=payload, headers=self.header)
        re.raise_for_status()
        delta = re.elapsed
        raw_data = re.json()
        print(f'Time to acquire data: {delta}')

        self.total_results = raw_data['number_of_total_results'] # grab the number of results from the API before discarding
        raw_data = raw_data.pop('results') # remove header and get results
        self.my_hoard = self.melt_gold(raw_data) # format data
        self.offset += len(self.my_hoard)
        return self.my_hoard # return to sender
    
    def is_done(self, target:int = -1) -> bool:
        """Returns False if there amount of acquired data entries is smaller
        than the total results or the target, if one was given.
        Returns True if it has acquired as many entries as there are results."""
        if target <= 0:
            target = self.total_results
        if self.offset >= target:
            return True
        return False