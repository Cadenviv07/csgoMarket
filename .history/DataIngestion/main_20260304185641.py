import requests
import random
import re 
import time 
import json
import calendar

targets = ["KiloWatt%20Case", "Recoil%20Case", "Revolution%20Case", "Fever%20Case", "Fracture%20Case", "Gallery%20Case", "Snakebite%20Case", "Clutch%20Case", "Prisma%20Case", "Spectrum%202%20Case", "Glove%20Case", "Horizon%20Case", "Gamma%20Case", "Shadow%20Case", "Spectrum%20Case","Revolver%20Case", "Falchion%20Case", "Chrome%20Case", "Dreams%20%26%20Nightmares%20Case", "Prisma%202%20Case", "Danger%20Zone%20Case", "Chroma%203%20Case"]

url = 'https://steamcommunity.com/market/listings/730/'
custom_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}

for i in range(len(targets)):
    response = request.get(url+targets[i], custom_headers)
    random_int = random.randint(1,10)
    time.sleep(random_int)

    html = response.text

    match = re.search("var line1", html)
    if match:
        found_text = match.group()
        #fix the capturing 
        lazy_Pattern = r".;?"
        JData = re.match(lazy_Pattern, found_text)
        Data = json.loads(JData)
        
        r = calendar.monthrange()
        r = r*24
        r = len(Data) - r
        cleanedData = []
        #["Mar 04 2026 20: +0",3.003,"970"] fix date, convert volume to int
        for i in range(r):








