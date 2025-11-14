# DragonsHoard
A Python wrapper to facilitate API requests from ComicVine.com

# How to use
You can simply call the Dragon class by giving your API key to it, as well as the resource (section) of the API you want to work with.
It uses the **requests** library to make the connection, and does not require any extra information to acquire the necessary information, although we recommend giving it some basic fields to filter for the wanted information.

See example:

```
my_dragon = Dragon(api = MY_API_KEY, resource = 'characters')
acquired_data = my_dragon.pillage(fields = 'name,id,birth,publisher')
my_dragon.hoard(acquired_data, 'characters.json')
```

Currently it works only with the json format and requires the 'id' field in the payload to format and organize the saved information.