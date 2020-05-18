import folium
from folium import plugins
import datetime
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import pyepsg
from folium import IFrame
from folium.plugins import MarkerCluster

from table_html import table_html

def polygon_to_list(polygon):
    x,y = polygon.exterior.coords.xy
    x,y = np.mean(np.array(x)), np.mean(np.array(y))
    return (y,x)

def make_folium(wards_df, data_json, save_file="../results/kathmandu.html", center=[27.700769,85.300140], zoom=11, tiles="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=tiles,
        attr='...',
    )

    width = 310
    popups, polygons = [], []

    # print(data_json)

    for _, rows in wards_df.iterrows():
        district = rows["DISTRICT"]
        palika = rows["GaPa_NaPa"] + " " + rows["Type_GN"]
        ward = rows["NEW_WARD_N"]

        polygon = polygon_to_list(rows["geometry"])
        polygons.append(polygon)

        ddgnww = rows["DDGNWW"]

        required_row = data_json.loc[(data_json["DDGNWW"]==ddgnww)]        
        return_q = required_row["Returnee.Quarantined"].values[0]
        return_nq = required_row["Returnee.Not_Quarantined"].values[0]
        return_t = return_q + return_nq

        pcr_p = required_row["PCR.Positive"].values[0]
        pcr_n = required_row["PCR.Negative"].values[0]
        pcr_t = pcr_p + pcr_n

        rdt_p = required_row["RDT.Positive"].values[0]
        rdt_n = required_row["RDT.Negative"].values[0]
        rdt_t = rdt_p + rdt_n

        iframe = folium.Popup(folium.Html(table_html(district, palika, ward, return_q, pcr_p, rdt_p, return_nq, pcr_n, rdt_n, return_t, pcr_t, rdt_t), script=True, width=width))
        # iframe = IFrame(table_html.format(district, palika, ward, return_q, return_nq, return_t, pcr_p, pcr_n, pcr_t, rdt_p, rdt_n, rdt_t), width=width, height=height)
        
        popups.append(iframe)

    h = folium.FeatureGroup(name='Tests and Returnees')
    h.add_child(MarkerCluster(locations=polygons, popups=popups))

    geojs = folium.features.GeoJson(wards_df, name = "Boundary")
    m.add_child(geojs)
    m.add_child(h)
    m.save(save_file)

if __name__=="__main__":
    wards_df = gpd.read_file("../shapefiles/nepal-map-governance/valley_wards.shp")
    with open("../shapefiles/nepal-map-governance/random_valley_data.json","r") as file:
        data_json = file.read()
    data_json = json.loads(data_json)
    data_json = pd.json_normalize(data_json["data"])
    
    make_folium(wards_df, data_json)


