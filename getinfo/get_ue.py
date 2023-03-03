"""Modified version of https://github.com/andrewguest/slack-free-epic-games"""

from typing import Dict

import requests
from requests.utils import requote_uri

# Epic's backend API URL for the free games promotion
EPIC_API: str = "https://www.unrealengine.com/marketplace/api/assets?tag[]=4910"

# HTTP params for the US free games
PARAMS: Dict[str, str] = {
    "locale": "en-US",
    "country": "US",
    "allowCountries": "US",
}


def get_free_ue():
    """Uses an API from Epic to parse a list of free games to find this
    week's free games.

    Original source:
    https://github.com/andrewguest/slack-free-epic-games/blob/main/lambda_function.py#L18

    Returns:
        Embed containing a free Epic game.
    """
    gamelist=[]

    # Connect to the Epic API and get the free games
    response = requests.get(EPIC_API, params=PARAMS)

    # Find the free games in the response
    for game in response.json()["data"]["elements"]:
        game_name = game["title"]

        original_price = game["priceValue"]
        discount = game["discountPriceValue"]

        final_price = original_price - discount

        DATA = {
            'game': game["title"],
            'url': "https://www.unrealengine.com/marketplace/en-US/product/" + game["urlSlug"],
            'img': game["thumbnail"],
            'description': game["description"],
        }
        gamelist.append(DATA)
    return gamelist

if __name__ == "__main__": 
    test1=get_free_ue()
    for i in test1:
        print("{}: {}".format(i["game"],i["url"]))
