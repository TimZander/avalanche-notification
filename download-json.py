from requests import request
import json
from shapely.geometry import Point, Polygon
import datetime

url_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
#url_datetime = "2023-01-29T21:30:00.000Z"

def load_json_from_url(url, method):
    return json.loads(request(method=method,url=url).text)

def get_json_for_areaId(areaId):
    products = load_json_from_url(url = "https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all?datetime="+url_datetime+"&includeExpired=true", method="GET")
    for product in products:
        #print(product["areaId"])
        if product["areaId"] == areaId:
            #print(product)
            return product

def get_areaId_from_lat_long(lat, long):
    regional_discussions = load_json_from_url(url="https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all/area?productType=regionaldiscussion&datetime="+url_datetime+"&includeExpired=true", method="GET")
    avalanche_forecasts = load_json_from_url(url="https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all/area?productType=avalancheforecast&datetime="+url_datetime+"&includeExpired=true", method="GET")
    areas = []
    for avalanche_forecast in avalanche_forecasts["features"]:
        polygon_coordinates = avalanche_forecast["geometry"]["coordinates"]
        poly = Polygon(polygon_coordinates[0][0])
        point = Point(long, lat)
        if point.within(poly):
            areas.append(avalanche_forecast["id"])
    for regional_discussion in regional_discussions["features"]:
        polygon_coordinates = regional_discussion["geometry"]["coordinates"]
        for coordinate_set in polygon_coordinates:
            poly = Polygon(coordinate_set[0])
            point = Point(long, lat)
            if point.within(poly):
                areas.append(regional_discussion["id"])
    return areas

def print_avalancheforecast(product):
    print(product["forecaster"])
    for summary in product["avalancheSummary"]["days"]:
        print("date: " + summary["date"])
        print("summary: " + summary["content"])
    #print(product)

def print_regionaldiscussion(product):
    print(product["forecaster"])
    print(product["message"])

def print_product(product):
    print(product["title"])
    print(product["type"])
    print('Expires: ' + product["expiryDateTime"])
    if product["type"] == "avalancheforecast":
        print_avalancheforecast(product)
    if product["type"] == "regionaldiscussion":
        print_regionaldiscussion(product)

areaIds = get_areaId_from_lat_long(lat = 39.49460789109591, long = -106.04589843749999)
for areaId in areaIds:
    product = get_json_for_areaId(areaId=areaId)
    print_product(product=product)
    print()