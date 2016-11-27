import requests
from bs4 import BeautifulSoup
import os
from definitions import ROOT_DIR
from shutil import copyfile


def download_sprite(pokemon):
    """
    Saves a sprite of a pokemon to sprites/{pokename}.png
    """
    pokemon = pokemon.lower()
    url = "http://pokemondb.net/sprites/" + pokemon
    url = url.replace("é", "e")
    url = url.replace("'", "")
    url = url.replace("mime jr.", "mime-jr")
    url = url.replace("♂", "-m")
    url = url.replace("♀", "-f")
    url = url.replace("mr. mime", "mr-mime")

    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")

    image_urls = [element["data-original"] for element in soup.find_all("img")]
    best_url = ""

    # trying to get omega ruby image
    for url in image_urls:
        if "omega-ruby" in url:
            best_url = url
            break

    # trying to get any image
    if not best_url:
        for url in image_urls:
            if pokemon in url:
                best_url = url
                break

    if not best_url:
        copyfile(os.path.join(ROOT_DIR, "sprites", "default.png"), os.path.join(ROOT_DIR, "sprites", pokemon+".png"))
        print("error with: " + url)
        return
    else:
        path = os.path.join(ROOT_DIR, "sprites", pokemon + ".png")
        image = requests.get(best_url)
        open(path, "wb").write(image.content)
        print("Saved sprite to " + path)

if __name__ == "__main__":
    download_sprite("mew")