import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


def get_game_name(banner_title_text: str) -> str:
    """
    Get the game name from the banner title.
    Args:
        banner_title_text: The banner title. We will run a regex to get the game name.
    Returns:
        str: The game name, GOG Giveaway if not found.
    """
    result = re.search(
        r"being with us! Claim (.*?) as a token of our gratitude!",
        banner_title_text,
    )
    if result:
        return result.group(1)
    return "GOG Giveaway"




def get_free_gog_game():
    """Check if free GOG game.
    Returns:
        DiscordEmbed: Embed for the free GOG games.
    """

    request = requests.get("https://www.gog.com/")
    soup = BeautifulSoup(request.text, "html.parser")
    giveaway = soup.find("a", {"id": "giveaway"})

    # If no giveaway, return an empty list
    if giveaway is None:
        return

    # Game name
    banner_title = giveaway.find("span", class_="giveaway-banner__title")
    game_name = get_game_name(banner_title.text)

    # Game URL
    ng_href = giveaway.attrs["ng-href"]
    game_url = f"https://www.gog.com{ng_href}"

    # Game image
    image_url_class = giveaway.find("source", attrs={"srcset": True})
    image_url = image_url_class.attrs["srcset"].strip().split()
    image_url = f"https:{image_url[0]}"



    data = {
        'game_name': game_name,
        'game_url': game_url,
        'image_url': image_url,
    }
    return data


if __name__ == "__main__":
    # Remember to delete previous games if you are testing
    # It can be found in %appdata%\TheLovinator\discord_free_game_notifier
    gog_embed = get_free_gog_game()
    print(gog_embed)
    # if gog_embed:
    #     response = send_embed_webhook(gog_embed)
    #     if not response.ok:
    #         print(
    #             f"Error when checking game for GOG:\n{response.status_code} - {response.reason}: {response.text}")