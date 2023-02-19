import requests

def discord_send(token, platform, title, url, urlimg, description=''):
    textcontent = ""
    titletext = title
    color = 0x000000
    if platform == 'Steam':
        titletext = "[Steam] " + title
        color = 0x00FF00
    if platform == 'Epic':
        titletext = "[Epic Games] " + title
        color = 0x00FFFF
    if platform == 'UE':
        titletext = "[UE Assets] " + title
        color = 0xFFFF00

    
    data = {
        "content": textcontent,
        "username": "Free bot",
        "tts": False,
        "embeds": [{
            "type": "rich",
            "title": titletext,
            "description": description,
            "color": color,
            "thumbnail": {
                "url": urlimg,
            },
            "url": url,
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }
    result = requests.post(token, json=data, headers=headers)

    if 200 <= result.status_code < 300:
        return True
    else:
        print(f"Not sent with {result.status_code}")
        print(result)
        return False


if __name__ == "__main__": 
    token = ""

    discord_send(token, 'Steam', "title", "https://cdn.discordapp.com/attachments/1028600912123531274/1071745793712726076/image.png", "https://cdn.discordapp.com/attachments/1028600912123531274/1071745793712726076/image.png", "12345")

