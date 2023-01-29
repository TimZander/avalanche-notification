from requests import request
import json
from shapely.geometry import Point, Polygon

def load_json_from_url(url, method):
    return json.loads(request(method=method,url=url).text)

def get_json_for_areaId(areaId):
    products = load_json_from_url(url = "https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all?datetime=2023-01-29T21:30:00.000Z&includeExpired=true", method="GET")
    for product in products:
        #print(product["areaId"])
        if product["areaId"] == areaId:
            #print(product)
            return product

def get_areaId_from_lat_long(lat, long):
    avalanche_forecasts = load_json_from_url(url="https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all/area?productType=avalancheforecast&datetime=2023-01-29T21:30:00.000Z&includeExpired=true", method="GET")
    #print("forecasts")
    areas = []
    for avalanche_forecast in avalanche_forecasts["features"]:
        bbox = avalanche_forecast["bbox"]
        #print(bbox)
        #if bbox[0] <= long <= bbox[2] and bbox[1] <= lat <= bbox[3]:
            #print(avalanche_forecast["id"])
            #areas.append(avalanche_forecast["id"])
        polygon_coordinates = avalanche_forecast["geometry"]["coordinates"]
        #print(polygon_coordinates)
        poly = Polygon(polygon_coordinates[0][0])
        point = Point(long, lat)
        if point.within(poly):
            print("WITHIN")
            print(avalanche_forecast["id"])
            areas.append(avalanche_forecast["id"])
    return areas

areaIds = get_areaId_from_lat_long(lat = 39.49460789109591, long = -106.04589843749999)
for areaId in areaIds:
    product = get_json_for_areaId(areaId=areaId)
    print(product["title"])