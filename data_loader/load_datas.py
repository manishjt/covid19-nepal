import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from finddistance import find_distance
from find_gps import find_gps_by_name

service_type = "district"

if service_type == "palika":
    palika = pd.read_csv("../data/Palika_data.csv")
    dist_list = palika['Full_Name'].values
    # headq_list = dist_data['Headquarter'].values

    # long_list = []
    # lat_list = []
    # for i in headq_list:
    #     print(i)
    #     long_, lat_ = find_gps_by_name(i)
    #     long_list.append(long_)
    #     lat_list.append(lat_)
    # dist_data["longitude"] = long_list
    # dist_data["latitude"] = lat_list

    # dist_data.to_csv("dist_data.csv")

    dist_mat = pd.DataFrame(dist_list, columns=["Full_Name"]).set_index("Full_Name")
    count = 0
    for i in dist_list:
        print("calculating for ",i)
        temp = []
        long1 = palika.loc[palika['Full_Name']==i]['Longitude'].values[0]
        lat1 = palika.loc[palika['Full_Name']==i]['Latitude'].values[0]
        for j in dist_list:
            if i == j:
                temp.append(0)
            else:
                long2 = palika.loc[palika['Full_Name']==j]['Longitude'].values[0]
                lat2 = palika.loc[palika['Full_Name']==j]['Latitude'].values[0]
                d = find_distance(str(long1)+","+ str(lat1), str(long2)+","+ str(lat2))
                if d<0:
                    print(i, "to ", j)
                    print("error in this part")
                    temp.append(-1)
                else:
                    temp.append(d)
        dist_mat[i] = temp
        count += 1
    print(dist_mat)
    dist_mat.to_csv("../data/dist_matrix_napagapa.csv")
    print("done")

    # print(districts)

elif service_type == "district":
    palika = pd.read_csv("../data/dist_data.csv")
    dist_list = palika['Districts'].values
    # headq_list = dist_data['Headquarter'].values

    # long_list = []
    # lat_list = []
    # for i in headq_list:
    #     print(i)
    #     long_, lat_ = find_gps_by_name(i)
    #     long_list.append(long_)
    #     lat_list.append(lat_)
    # dist_data["longitude"] = long_list
    # dist_data["latitude"] = lat_list

    # dist_data.to_csv("dist_data.csv")

    dist_mat = pd.DataFrame(dist_list, columns=["Districts"]).set_index("Districts")
    count = 0
    for i in dist_list:
        print("calculating for ",i)
        temp = []
        long1 = palika.loc[palika['Districts']==i]['longitude'].values[0]
        lat1 = palika.loc[palika['Districts']==i]['latitude'].values[0]
        for j in dist_list:
            if i == j:
                temp.append(0)
            else:
                long2 = palika.loc[palika['Districts']==j]['longitude'].values[0]
                lat2 = palika.loc[palika['Districts']==j]['latitude'].values[0]
                d = find_distance(str(long1)+","+ str(lat1), str(long2)+","+ str(lat2))
                if d<0:
                    print(i, "to ", j)
                    print("error in this part")
                    temp.append(-1)
                else:
                    temp.append(d)
        dist_mat[i] = temp
        count += 1
    print(dist_mat)
    dist_mat.to_csv("../data/dist_matrix.csv")
    print("done")

    # print(districts)
