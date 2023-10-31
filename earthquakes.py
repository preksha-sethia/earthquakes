import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    text = response.text
    dic = json.loads(text)
    return dic

def count_earthquakes(data):
    return data["metadata"]["count"]

def get_magnitude(earthquake):
    return earthquake["properties"]["mag"]  # Fix here

def year_data(earthquake):
    return datetime.datetime.fromtimestamp(earthquake["properties"]["time"] / 1000).year  # Get only the year

def earthquake_magnitudes_per_year(earthquakes):
    dict_year = {}
    for earth in earthquakes["features"]:
        year = year_data(earth)
        if year in dict_year:
            dict_year[year].append(get_magnitude(earth))
        else:
            dict_year[year] = [get_magnitude(earth)]
    return dict_year

def plot_number_per_year(earthquakes):
    dict = earthquake_magnitudes_per_year(earthquakes)
    year_list = list(dict.keys())
    year_list.sort()
    num_list = [len(dict[year]) for year in year_list]
    
    year_list = np.array(year_list)
    num_list = np.array(num_list)
    
    plt.title('Number of Earthquakes Per Year')
    plt.plot(year_list, num_list, label='Earthquakes')
    plt.legend()
    plt.xlabel('Year')
    plt.xticks(year_list, rotation=45)
    plt.ylabel('Number')
    plt.tight_layout()
    plt.show()

data = get_data()
plot_number_per_year(data)