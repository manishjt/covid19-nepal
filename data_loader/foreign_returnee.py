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

data = pd.read_csv("../data/entry_ktm_new1.csv")

def make_folium(data, save_file="../results/ktm_high_risk1.html", center=[27.7021,85.3343], zoom=13, tiles="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=tiles,
        attr='...',
    )

    width = 200

    # print(data_json)

    for _, rows in data.iterrows():
        district = rows["district"]
        palika = rows["gpnp"]# + " " + rows["type"]
        ward = rows["ward"]

        return_t = rows["cnt.1"]

        circle = rows["latitude"], rows["longitude"]

        if return_t<10:
            radius = 50
            color = "green"
        else:
            if return_t<30:
                radius = 100
                color = "blue"
            elif return_t<100:
                radius = 150
                color = "orange"
            else:
                radius = 200
                color = "red"
        # print(radius)

        iframe = folium.Popup(folium.Html(table_return_html(district, palika, ward, return_t, color), script=True, width=width))
        # iframe = IFrame(table_html.format(district, palika, ward, return_q, return_nq, return_t, pcr_p, pcr_n, pcr_t, rdt_p, rdt_n, rdt_t), width=width, height=height)
        folium.vector_layers.Circle(location=circle, radius=radius, color=color, fill=True, fill_color=color ,popup=iframe).add_to(m)

    m.save(save_file)

make_folium(data)