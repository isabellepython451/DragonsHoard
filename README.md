# DragonsHoard
A Python wrapper to facilitate API requests from ComicVine.com

# How to use
You can simply call the Dragon class by giving your API key to it, as well as the resource (section) of the API you want to work with.
It uses the **requests** library to make the connection, and does not require any extra information to acquire the necessary information, although we recommend giving it some basic fields to filter for the wanted information.

See example:

```
dragon_pal = Dragon(api = MY_API_KEY, file = MY_FILE, resource = 'characters')
custom_fields = 'name,aliases,gender,count_of_issue_appearances,publisher,origin,real_name,birth,id'
while not dragon_pal.is_done():
    dragon_pal.pillage(fields=custom_fields)
    print('waiting 10 seconds...')
    time.sleep(10)
print('done')
```

Currently it works only with the json format and requires the 'id' field in the payload to format and organize the saved information.