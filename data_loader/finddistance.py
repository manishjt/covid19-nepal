import requests, json

url = 'http://router.project-osrm.org/route/v1/driving/'

def find_distance(g1,g2):

    try:
        response = requests.get(url+g1+";"+g2)
        return json.loads(response.content)['routes'][0]['distance']*0.001
    except:
        return -1

if __name__=="__main__":
    lat1, long1 = 27.012541, 84.877998 #birjung
    lat2, long2 = 27.699894, 83.465996 #butwal

    g1, g2 = str(long1) + "," + str(lat1), str(long2) + "," + str(lat2)
    print(find_distance(g1,g2))