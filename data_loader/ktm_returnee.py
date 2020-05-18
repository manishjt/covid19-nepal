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

from table_html import table_return_html

def polygon_to_list(polygon):
    x,y = polygon.exterior.coords.xy
    x,y = np.mean(np.array(x)), np.mean(np.array(y))
    return (y,x)

data = gpd.read_file("../shapefiles/ktm_ward_retunees_ncell1/ktm_ward_retunees_ncell1.shp")

def make_folium(data, save_file="../results/kathmandu_returnee.html", center=[27.7021,85.3343], zoom=13, tiles="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=tiles,
        attr='...',
    )

    width = 200

    # print(data_json)

    for _, rows in data.iterrows():
        district = rows["DISTRICT"]
        palika = rows["GPNP_Name"]
        ward = rows["ward"]

        circle = polygon_to_list(rows["geometry"])

        return_t = int(rows["Sum_cnt1"])

        if return_t<100:
            radius = 50
            color = "green"
        else:
            radius = return_t/2
            if return_t<500:
                color = "blue"
            elif return_t<1000:
                color = "orange"
            else:
                color = "red"
        # print(radius)

        iframe = folium.Popup(folium.Html(table_return_html(district, palika, ward, return_t, color), script=True, width=width))
        # iframe = IFrame(table_html.format(district, palika, ward, return_q, return_nq, return_t, pcr_p, pcr_n, pcr_t, rdt_p, rdt_n, rdt_t), width=width, height=height)
        folium.vector_layers.Circle(location=circle, radius=radius, color=color, fill=True, fill_color=color ,popup=iframe).add_to(m)

    m.save(save_file)

make_folium(data)