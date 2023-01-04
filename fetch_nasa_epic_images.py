import os
import requests

from dotenv import load_dotenv
from download_image import download_image
from get_file_extension_from_url import get_file_extension_from_url


def fetch_nasa_epic_images(url, path, params):
    response = requests.get(url, params)
    response.raise_for_status()
    for image_number, image_data in enumerate(response.json()):
        download_image(
            (f"https://api.nasa.gov/EPIC/archive/natural/"
             f"{image_data['date'].split()[0].replace('-', '/')}/png/"
             f"{image_data['image']}.png"),
            os.path.join(path, f"nasa_epic_{image_number}.png"),
            params
        )

def main():
    load_dotenv()
    directory = "images"
    path = os.path.abspath(".")
    params = {"api_key": os.getenv("NASA_API_KEY")}
    url = "https://api.nasa.gov/EPIC/api/natural"
    try:
        os.makedirs(os.path.join(path, directory), exist_ok=True)
        fetch_nasa_epic_images(url, os.path.join(path, directory), params)
    except FileExistsError as error:
        # directory already exist
        pass


if __name__ == "__main__":
    main()
