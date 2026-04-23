import requests
import random
import re 
import time 
import json
from datetime import datetime
from datetime import timezone
from storage import init_db
from storage import save_case_data
from urllib.parse import unquote


# TODO: import the two functions you wrote in storage.py
# from storage import ...
def main(): 
    targets = ["KiloWatt%20Case", "Recoil%20Case"]
    #"Revolution%20Case", "Fever%20Case", "Fracture%20Case", "Gallery%20Case", "Snakebite%20Case", "Clutch%20Case", "Prisma%20Case", "Spectrum%202%20Case", "Glove%20Case", "Horizon%20Case", "Gamma%20Case", "Shadow%20Case", "Spectrum%20Case","Revolver%20Case", "Falchion%20Case", "Chrome%20Case", "Dreams%20%26%20Nightmares%20Case", "Prisma%202%20Case", "Danger%20Zone%20Case", "Chroma%203%20Case"]

    url = 'https://steamcommunity.com/market/listings/730/'
    custom_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}

    master_data = {}
    for i in range(len(targets)):

        cleaned_data = []

        random_delay = random.uniform(3.5,7.5)
        if i < len(targets) - 1: time.sleep(random_delay)

        try:
            response = requests.get(
                url+targets[i], 
                headers=custom_headers
            )
        except requests.exceptions.RequestException as e :
            print(f"An error has occcured: {e}")
        

        
        targets[i] = unquote(targets[i])

        html = response.text

        # The unified pattern
        pattern = r"var line1=(\[.*?\]);"

        # The single search execution
        match = re.search(pattern, html)

        RECENT_HOURS = 24 * 30

        if match:
            raw_string = match.group(1)
            parsed_list = json.loads(raw_string)
            recent_data = parsed_list[-RECENT_HOURS:]
            
            for item in recent_data:
                raw_date = item[0]

                clean_date = raw_date.split(':')[0]
                math_timestamp = datetime.strptime(clean_date, "%b %d %Y %H").replace(tzinfo=timezone.utc)

                price = item[1].replace(",","")

                volume = int(item[2].replace(",",""))

                cleaned_data.append([math_timestamp, price, volume])

            master_data[targets[i]] = cleaned_data
            #Acts kind of weird and says the second zero is out of bounds but the data looked good when printed so it didn't seem important
            #print(type(cleaned_data[0][0]))
        else:
            print(f"FAILED: Steam blocked {targets[i]}")




    #add saftey features to normalize data and to make sure date is not empty 
    #Storage with sqlite, clean data polars and math with numpy


    # ---------------------------------------------------------------------------
    # Persist master_data to SQLite
    # ---------------------------------------------------------------------------
    # You now have `master_data`: a dict mapping URL-encoded case names (e.g.
    # "KiloWatt%20Case") to a list of [datetime, price, volume] rows.
    #
    # Your job here:
    #   1. Call init_db() exactly once to make sure the table exists.
    #   2. For each (url_encoded_name, rows) pair in master_data:
    #        a. Convert the URL-encoded name back into a clean display name
    #           (think: urllib.parse.unquote, or a .replace on "%20").
    #        b. Call save_case_data(clean_name, rows).
    #
    # Keep it in a simple loop. No try/except yet — let errors surface so you can
    # see and learn from them.


    init_db()

    for key, value in master_data.items():
        save_case_data(key,value)

if __name__ == "__main__":
    main()










                    








