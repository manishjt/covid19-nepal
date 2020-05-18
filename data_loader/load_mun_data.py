import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def find_centroid(data):
    long_ = []
    lat_ = []
    for i in data:
        long_.append(i.centroid.x)
        lat_.append(i.centroid.y)
    return(long_,lat_)

data = gpd.read_file("../shapefiles/nepal-map-governance/NEPAL_GAPANAPA_WGS.shp")

# data.plot()
# plt.savefig("Nepal_gapanapa.png")
palika = pd.DataFrame(data["PALIKA"])
palika["District"] = data["DISTRICT"]
palika["Province"] = data["PROVINCE"]
palika["Full_Name"] = data["PALIKA"] + ", " + data["DISTRICT"]
palika["Longitude"], palika["Latitude"] = find_centroid(data["geometry"])

print(palika)

palika.to_csv("../data/Palika_data.csv")