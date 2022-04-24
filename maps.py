import requests
import json

from config import GOOGLE_MAPS_KEY

maps_url = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address=".format(GOOGLE_MAPS_KEY)

def get_location(place):
    data = json.loads(requests.get(maps_url + place).text)
    status = data["status"]

    if(status == "OK"):
        return data["results"][0]["geometry"]["location"]["lat"], data["results"][0]["geometry"]["location"]["lng"]
    else:
        return None, None

if __name__ == "__main__":
    print(get_location("oslo"))
