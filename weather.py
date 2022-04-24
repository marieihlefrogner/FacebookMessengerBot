import requests
import json
import sys
import re
import datetime
import shlex

from config import WEATHER_KEY
import maps

url = "https://api.darksky.net/forecast/{}/{},{}?units=si"

def get_weather(lat, lng, forecast_time="now"):
    data = json.loads(requests.get(url.format(WEATHER_KEY, lat, lng)).text)
    summary, temperature, t = None, None, None

    if forecast_time in ["now", "today", "nå", "i dag"]:
        summary = data["currently"]["summary"]
        temperature = data["currently"]["temperature"]
        return summary, temperature
    elif forecast_time in ["tomorrow", "i morgen"]:
        weather_times = [w for w in data["hourly"]["data"]]

        for wt in weather_times:
            ts = datetime.datetime.fromtimestamp(int(wt["time"]))
            if ts.day == (datetime.date.today() + datetime.timedelta(days=1)).day:
                if ts.hour == datetime.datetime.today().hour:
                    summary = wt["summary"]
                    temperature = wt["temperature"]
                    t = str(ts)

    return summary, temperature

if __name__ == '__main__':
    if len(sys.argv) == 3:
        place = sys.argv[1]
        forecast_time = sys.argv[2]

        lat, lng = maps.get_location(place)
        summary, temperature = get_weather(lat, lng, forecast_time)

        print("Weather for {} {}:\n{}°C\n{}".format(place, forecast_time, temperature, summary))
    else:
        inp = input()
        pieces = shlex.split(inp)

        lat, lng = maps.get_location(pieces[0])
        summary, temperature = get_weather(lat, lng, pieces[1])
        print("Weather for {} {}:\n{}°C\n{}".format(pieces[0], pieces[1], temperature, summary))