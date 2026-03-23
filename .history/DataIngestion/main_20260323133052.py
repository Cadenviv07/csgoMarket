import requests
import random
import re 
import time 
import json
import calendar
from datetime import datetime

targets = ["KiloWatt%20Case", "Recoil%20Case"]
#"Revolution%20Case", "Fever%20Case", "Fracture%20Case", "Gallery%20Case", "Snakebite%20Case", "Clutch%20Case", "Prisma%20Case", "Spectrum%202%20Case", "Glove%20Case", "Horizon%20Case", "Gamma%20Case", "Shadow%20Case", "Spectrum%20Case","Revolver%20Case", "Falchion%20Case", "Chrome%20Case", "Dreams%20%26%20Nightmares%20Case", "Prisma%202%20Case", "Danger%20Zone%20Case", "Chroma%203%20Case"]

url = 'https://steamcommunity.com/market/listings/730/'
custom_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}

master_data = {}
for i in range(len(targets)):

    cleaned_data = [[]]

    response = requests.get(url+targets[i], custom_headers)
    random_delay = random.uniform(3.5,7.5)
    time.sleep(random_delay)

    html = response.text

    # The unified pattern
    pattern = r"var line1=(\[.*?\]);"

    # The single search execution
    match = re.search(pattern, html)

    if match:
        raw_string = match.group(1)
        parsed_list = json.loads(raw_string)
        recent_data = parsed_list[-720:]
        
        for item in recent_data:
            raw_date = item[0]

            clean_date = raw_date.split(':')[0]
            math_timestamp = datetime.strptime(clean_date, "%b %d %Y %H")

            price = item[1]

            volume = int(item[2])

            cleaned_data.append([math_timestamp, price, volume])

        master_data[targets[i]] = cleaned_data
        #Acts kind of weird and says the second zero is out of bounds but the data looked good when printed so it didn't seem important
        #print(type(cleaned_data[0][0]))
    else:
        print(f"FAILED: Steam blocked {targets[i]}")




#add saftey features to normalize data and to make sure date is not empty 
#Storage with sqlite, clean data polars and math with numpy









                   








