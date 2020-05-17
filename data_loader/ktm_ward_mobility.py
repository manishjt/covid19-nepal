import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

data = gpd.read_file("../shapefiles/nepal-map-governance/valley_wards.shp")
data_mob = pd.read_csv("../data/Entry_to_Kathmandui_valley_data.csv")

# print(data)
# print(data_mob)
gapa = []
ward = []
district = []

for _,v in data_mob.iterrows():
    point = Point(v["longitude"],v["latitude"])
    cnt = 0
    for i,vi in data.iterrows():
        result = vi["geometry"].contains(point)
        if result:
            if not cnt:
                gapa.append(vi["GaPa_NaPa"]+" "+vi["Type_GN"])
                ward.append(vi["NEW_WARD_N"])
                district.append(vi["DISTRICT"])
            else:
                print("More than one wtf")
            cnt += 1
    if not cnt:
        print("NULL")
        gapa.append("NULL")
        ward.append("NULL")
        district.append("NULL")
    
data_mob["gpnp"] = gapa
data_mob["ward"] = ward
data_mob["district"] = district
data_mob.to_csv("../data/entry_ktm_new1.csv")