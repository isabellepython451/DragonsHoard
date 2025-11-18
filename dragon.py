import requests, json
from egg import Egg

LIB_NAME = "Dragon's Hoard"
VERSION = "0.0.14"


class Dragon:
    """This class manages the API requests and saves the received data
    into pre-defined files.
    Takes the API KEY needed to access the url and the target resource;
    see https://comicvine.gamespot.com/api/documentation for options."""

    def __init__(self, api: str, file:str, resource, format: str = 'json'):
        ## Class constants
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
        }
        self.comicvine_endpoint = 'https://comicvine.gamespot.com/api/'
        self.valid_resources = [
            'character',
            'characters',
            'chat',
            'chats',
            'concept',
            'concepts',
            'episode',
            'episodes',
            'issue',
            'issues',
            'location',
            'locations',
            'movie',
            'movies',
            'object',
            'objects',
            'origin',
            'origins',
            'person',
            'people',
            'power',
            'powers',
            'promo',
            'promos',
            'publisher',
            'publishers',
            'series',
            'series_list',
            'search',
            'story_arc',
            'story_arcs',
            'team',
            'teams',
            'types',
            'video',
            'videos',
            'video_type',
            'video_types',
            'video_category',
            'video_categories',
            'volume',
            'volumes'
            ]

        ## Class variables
        self.api_key = api
        self.format = format
        self.save_target = file
        self.total_results = 100
        self.my_hoard = {}  # where we will save the formatted requested data

        # Create an egg and save in a list
        self.egg = Egg(file, resource, format)
        self.offset = self.egg.get_offset()

        # list containing valid paths and their fields and checking if valid value was given
        self.resource = resource
        self._validate_resource()
        self.url = f'{self.comicvine_endpoint}{self.resource}/'

    def _melt_gold(self, data: list) -> dict:
        """Turns the list received from results into a dictionary
        with key:value pairs that can be more easily saved and loaded from
        the json files."""
        return {str(entry['id']): entry for entry in data}

    def _validate_resource(self) -> None:
        if self.resource in self.valid_resources:
            return None
        else:
            print(f'Invalid resource given ("{self.resource}");\nUsing fallback instead ("characters").')
            self.resource = 'characters'

    def _hoard(self):
        """Saves acquired data into a chosen file."""
        if self.egg.empty:
            with open(self.save_target, mode='w') as file:
                json.dump(self.my_hoard, file, indent=2, sort_keys=True)
                self.egg.empty = False
        else:
            with open(self.save_target, mode='r') as file:
                saved_data = json.load(file)
            with open(self.save_target, mode='w') as file:
                saved_data.update(self.my_hoard)
                json.dump(saved_data, file, indent=2, sort_keys=True)
        print('Data saved.')

    def pillage(self,
                offset: int = -1,
                fields: str = '') -> None:
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
            'offset': self.offset,
            'field_list': fields,
        }

        re = requests.get(url=self.url, params=payload, headers=self.header)
        re.raise_for_status()
        delta = re.elapsed
        raw_data = re.json()
        print(f'Time to acquire data: {delta}')

        self.total_results = raw_data['number_of_total_results']  # grab the number of results from the API before discarding
        raw_data = raw_data.pop('results')  # remove header and get results
        self.my_hoard = self._melt_gold(raw_data)  # format data for json file
        self.offset += len(self.my_hoard)
        self._hoard() # save to file
    
    def is_done(self, target: int = -1) -> bool:
        """Returns False if the amount of acquired data entries is smaller
        than the total results or the target, if one was given.
        Returns True if it has acquired as many entries as there are results."""
        if target <= 0:
            target = self.total_results
        if self.offset >= target:
            return True
        return False