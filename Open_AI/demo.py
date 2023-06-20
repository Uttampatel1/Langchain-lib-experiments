import os
from dotenv import load_dotenv
import requests

load_dotenv()
rapid_api_key = os.getenv("X-RapidAPI-Key")
smart_light_api_key = os.getenv("SMART_LIGHT_API_KEY")


def get_stock_news(performanceId):
    url = "https://morning-star.p.rapidapi.com/news/list"

    querystring = {"performanceId":performanceId}

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "morning-star.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    short_news_list = response.json()[:5]

    print("response:", response, " json response:", short_news_list)

    return short_news_list

get_stock_news("0P0000OQN8")