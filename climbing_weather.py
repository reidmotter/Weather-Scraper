from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from datetime import date
from datetime import time
import os
import pandas as pd

# List for all the sites to scrape from
weather_page = ['https://forecast.weather.gov/MapClick.php?lat=36.220480000000066&lon=-81.68718999999999',
              'https://forecast.weather.gov/MapClick.php?lat=38.0732&lon=-81.0749',
              'https://forecast.weather.gov/MapClick.php?lat=37.7938&lon=-83.7032',
              'https://forecast.weather.gov/MapClick.php?lat=34.7101&lon=-85.2811',
              'https://forecast.weather.gov/MapClick.php?lat=36.624&lon=-81.4984',
              'https://forecast.weather.gov/MapClick.php?lat=36.7106&lon=-81.9752']


data = [] # List for tuples of weather data
c_or_p = 0 # 0 for csv format or 1 for panda format
squiggles = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
fname = str(date.today()) + '_climbing_weather.csv'

# Loops through all sites
for pg in weather_page:
    
    page = urlopen(pg) # Open pg and retrieve its html
    soup = BeautifulSoup(page, 'html.parser') # Parse the html

    # Scrape for location name and current conditions
    name_box = soup.select("#seven-day-forecast > div > h2")
    #print(name_box)
    curr_conditions = soup.select("#current_conditions-summary > p")
    loc = name_box[0].get_text().lstrip()
    cond = curr_conditions[0].get_text().lstrip()
    temp = curr_conditions[1].get_text().lstrip()
    
    # Scrape for the forecast data and descriptions
    periods = [p.get_text() for p in soup.select("#seven-day-forecast-list > li > div > .period-name")]
    short = [s.get_text() for s in soup.select("#seven-day-forecast-list > li > div > .short-desc")]
    temps = [t.get_text() for t in soup.select("#seven-day-forecast-list > li > div > .temp")]
    description = soup.find_all(class_="forecast-icon")
    desc = [d["title"] for d in description]
    
    # Combines each time period with its respective short description and temp.
    combo = set(zip(periods, short, temps))
    
    data.append((loc, cond, temp, combo, desc))

if os.path.exists(fname):
    os.remove(fname)
if c_or_p == 0:
    # Writes and formats all the scraped data into a CSV file
    with open(fname, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Location', 'Current Condition', 'Current Temperature'])
        for loc, cond, temp, combo, desc in data:
            writer.writerow([loc, cond, temp])
            for d in desc:
                writer.writerow([d]) 
            writer.writerow([squiggles, squiggles, squiggles, squiggles, squiggles,
                             squiggles, squiggles, squiggles, squiggles, squiggles,
                             squiggles, squiggles, squiggles, squiggles, squiggles,
                             squiggles, squiggles, squiggles, squiggles, squiggles,
                             squiggles, squiggles, squiggles, squiggles, squiggles,
                             squiggles, squiggles, squiggles, squiggles, squiggles,])       
        writer.writerow(['Updated as of', datetime.today()])

'''
else:
    
    locations.append(loc)
    current_temps.append(temp)
    current_conditions.append(cond)
    
    weather = pd.DataFrame({
            "Location": locations,
            "Current Temperature": current_temps,
            "Current Condition": current_conditions,
      
        })
    weather.to_csv(fname)
'''
print('done')
