"""Modified version of https://github.com/andrewguest/slack-free-epic-games"""

import calendar
import time
from typing import Dict

import requests
from requests.utils import requote_uri

# Epic's backend API URL for the free games promotion
EPIC_API: str = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

# HTTP params for the US free games
PARAMS: Dict[str, str] = {
    "locale": "en-US",
    "country": "US",
    "allowCountries": "US",
}


def promotion_start(game) -> int:
    """Get the start date of a game's promotion.

    offer["startDate"] = "2022-04-07T15:00:00.000Z"

    Args:
        game: The game JSON.

    Returns:
        int: Returns the start date of the game's promotion.
    """
    start_date = 0

    if game["promotions"]:
        for promotion in game["promotions"]["promotionalOffers"]:
            for offer in promotion["promotionalOffers"]:
                start_date = calendar.timegm(time.strptime(offer["startDate"], "%Y-%m-%dT%H:%M:%S.%fZ"))

    # Convert to int to remove the microseconds
    start_date = int(start_date)
    return start_date


def promotion_end(game) -> int:
    """Get the end date of a game's promotion.

    offer["endDate"] = "2022-04-07T15:00:00.000Z"

    Args:
        game: The game JSON.

    Returns:
        int: Returns the end date of the game's promotion.
    """
    end_date = 0

    if game["promotions"]:
        for promotion in game["promotions"]["promotionalOffers"]:
            for offer in promotion["promotionalOffers"]:
                end_date = time.mktime(time.strptime(offer["endDate"], "%Y-%m-%dT%H:%M:%S.%fZ"))

    # Convert to int to remove the microseconds
    end_date = int(end_date)-time.timezone
    
    return end_date


def game_image(game) -> str:
    """Get an image URL for the game.

    Args:
        game (_type_): The free game to get the image of.

    Returns:
        str: Returns the image URL of the game.
    """
    # Get the game's image. Image is 2560x1440
    # TODO: Get other image if Thumbnail is not available?
    image_url = ""
    for image in game["keyImages"]:
        if image["type"] in ["DieselStoreFrontWide", "Thumbnail"]:
            image_url = image["url"]
    
    # Epic's image URL has spaces in them, so requote the URL.
    return requote_uri(image_url)


def game_url(game) -> str:
    """If you click the game name, you'll be taken to the game's page on Epic.

    Args:
        game: The game JSON

    Returns:
        str: Returns the URL of the game.
    """
    url = "https://store.epicgames.com/"
    if product_slug := game["productSlug"]:
        url = f"https://store.epicgames.com/en-US/p/{product_slug.split('/')[0]}"
    else:
        for offer in game["offerMappings"]:
            if offer["pageSlug"]:
                page_slug = offer["pageSlug"]
                url = f"https://store.epicgames.com/en-US/p/{page_slug.split('/')[0]}"


    # Epic's image URL has spaces in them, could happen here too so requote the URL.
    return requote_uri(url)


def check_promotion(game) -> bool:
    """
    Check if the game has a promotion, only free games has these.

    Args:
        game: The game JSON

    Returns:
        bool: True if game has promotion
    """
    game_name = game["title"]
    if not game["promotions"]:
        return False
    return True


def get_free_epic_games():
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
    for game in response.json()["data"]["Catalog"]["searchStore"]["elements"]:
        original_price = game["price"]["totalPrice"]["originalPrice"]
        discount = game["price"]["totalPrice"]["discount"]

        final_price = original_price - discount

        for image in game["keyImages"]:
            if image["type"] == "VaultOpened":
                if check_promotion is False:
                    continue


        # If the original_price - discount is 0, then the game is free.
        if final_price == 0 and (original_price != 0 and discount != 0):
            if check_promotion is False:
                continue
            else:
                DATA = {
                    'game': game["title"],
                    'url': game_url(game),
                    'img': game_image(game),
                    'description': game["description"] + f'\n\n End: <t:{promotion_end(game)}>'
                }
                gamelist.append(DATA)
    return gamelist

if __name__ == "__main__": 
    test1=get_free_epic_games()
    for i in test1:
        print("{}: {} ({})".format(i["game"],i["url"],i["description"]))
