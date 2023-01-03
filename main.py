import os
import requests

from dotenv import load_dotenv
from urllib.parse import urlparse
from urllib.parse import unquote


path = os.path.abspath(".")
directory = "images"


def download_image(url, path, params=None):
    response = requests.get(url, params, stream=True)
    response.raise_for_status()
    with open(path, "wb") as image:
        image.write(response.content)


def get_file_extension_from_url(url):
    filename = unquote(urlparse(url).path.split("/")[-1])
    return os.path.splitext(filename)[-1]


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v5/launches/"
    image_links = None
    response = requests.get(url)
    response.raise_for_status()
    for launch in response.json()[::-1]:
        if launch["links"]["flickr"]["original"]:
            image_links = launch["links"]["flickr"]["original"]
            break
    for image_number, image_link in enumerate(image_links):
        download_image(
            image_link,
            os.path.join(path, directory, f"spacex_{image_number}.jpg")
        )


def fetch_nasa_apod_images():
    url = "https://api.nasa.gov/planetary/apod"
    params = {"count": 10, "api_key": os.getenv("NASA_API_KEY")}
    response = requests.get(url, params)
    response.raise_for_status()
    for image_number, image_data in enumerate(response.json()):
        if image_data["media_type"] == "image":
            extension = get_file_extension_from_url(image_data["url"])
            download_image(
                image_data["url"],
                os.path.join(
                    path,
                    directory,
                    f"nasa_{image_number}{extension}"
                )
            )


def fetch_nasa_epic_images():
    metadata = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": os.getenv("NASA_API_KEY")}
    response = requests.get(metadata, params)
    response.raise_for_status()
    for image_number, image_data in enumerate(response.json()):
        
        download_image(
            (f"https://api.nasa.gov/EPIC/archive/natural/"
             f"{image_data['date'].split()[0].replace('-', '/')}/png/"
             f"{image_data['image']}.png"),
            os.path.join(path, directory, f"nasa_epic_{image_number}.png"),
            params
        )

def main():
    load_dotenv()
    try:
        os.makedirs(os.path.join(path, directory), exist_ok=True)
        fetch_spacex_last_launch()
        fetch_nasa_apod_images()
        fetch_nasa_epic_images()
    except FileExistsError as error:
        # directory already exist
        pass


if __name__ == "__main__":
    main()
