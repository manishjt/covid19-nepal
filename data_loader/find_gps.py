import pandas as pd
from geopy.geocoders import Nominatim

def find_gps_by_name(name):
    locator = Nominatim()
    try:
        location = locator.geocode(name+", Nepal")
        return(location.longitude, location.latitude)
    except:
        print("error in location", name)
        return(0,0)
    
if __name__=="__main__":
    cities = pd.read_csv("../data/cities_data.csv").set_index("index")
    print(cities)
    lat_ = []
    long_ = []
    for i in cities["Cities"].values:
        print(i)
        locator = Nominatim()
        location = locator.geocode(i+", Nepal")
        lat_.append(location.latitude)
        long_.append(location.longitude)
    cities["lat"] = lat_
    cities["long"] = long_
    cities.to_csv("../data/cities_data1.csv")