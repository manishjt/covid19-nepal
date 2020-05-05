import folium
from folium import plugins
import datetime
import numpy as np

def make_folium(coordinates, data, start_date, save_file="../results/map.html", center=[27.700769,85.300140], zoom=7, tiles="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=tiles,
        attr='...',
    )
    print(len(data))
    print(len(data[0]))
    date = start_date
    features = []
    for data_single in data:
        for coordinate, coor_data in zip(coordinates, data_single):
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type':'Point', 
                    'coordinates': [coordinate[0],coordinate[1]]
                },
                'properties': {
                    'time': date.__str__(),
                    'style': {'color' : 'red'},
                    'icon': 'circle',
                    'iconstyle':{
                        'fillColor': "red",
                        'fillOpacity': 0.8,
                        'stroke': 'true',
                        'radius': coor_data
                    }
                }
            }
            features.append(feature)
        date += datetime.timedelta(days=1)
    
    print(features[0])#,features[76],features[77])
    print(len(features))
    plugins.TimestampedGeoJson(features,
                  period = 'P1D',
                  duration = 'P1D',
                  transition_time = 1000,
                  auto_play = False).add_to(m)
    

    m.save(save_file)

if __name__=="__main__":
    coordinates = [[85.300140,27.700769],[85.300140,27.800769],[85.400140,27.800769],[85.400140,27.700769]]
    data = [[5,10,15,20],[15,20,15,25],[2,4,5,1],[1,9,3,2]]
    start_date = datetime.date(year=2020, month=5, day=6)
    make_folium(coordinates,data, start_date)
