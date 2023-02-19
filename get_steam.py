import bs4
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"

# All
# STEAM_URL = "https://store.steampowered.com/search/?maxprice=free&specials=1"
# Games and soft
STEAM_URL = "https://store.steampowered.com/search/?maxprice=free&specials=1&category1=998%2C994"


def get_game_image(game):
    """
    Get the game ID and create image URL.

    Args:
        game: Contains information about the game.

    Returns:
        Image url for the game.
    """
    game_id = game["data-ds-appid"]
    image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"
    return image_url


def get_game_url(game):
    """
    Get the game url.

    Args:
        game: Contains information about the game.

    Returns:
        Game URL.
    """
    game_url = game["href"]
    return game_url


def get_game_name(game):
    """
    Get the game name.

    Args:
        game: Contains information about the game.

    Returns:
        The game name.
    """
    game_name_class: bs4.element.Tag = game.find("span", class_="title")
    game_name = game_name_class.text
    return game_name

def get_free_steam_games():
    """Go to the Steam store and check for free games and return them.

    Returns:
        Embed containing the free Steam games.
    """
    gamelist=[]

    request = requests.get(STEAM_URL)
    soup = BeautifulSoup(request.text, "html.parser")

    games = soup.find_all("a", class_="search_result_row")
    for game in games:
        DATA = {
            'game': get_game_name(game),
            'url': game["href"],
            'img': get_game_image(game),
            'description': "[ASF] `!addlicense ASF app/" + game["data-ds-appid"] +"`",
        }
        gamelist.append(DATA)
        # game_name: str = get_game_name(game)
        # game_url: str = get_game_url(game)
        # image_url: str = get_game_image(game)

    return gamelist

if __name__ == "__main__": 
    test1=get_free_steam_games()
    for i in test1:
        print("{}: {}".format(i["game"],i["url"]))
