import argparse
import os
import requests

from dotenv import load_dotenv
from download_image import download_image
from get_file_extension_from_url import get_file_extension_from_url


def fetch_nasa_apod_images(url, path, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    for image_number, image_data in enumerate(response.json()):
        if image_data["media_type"] == "image":
            extension = get_file_extension_from_url(image_data["url"])
            download_image(
                image_data["url"],
                os.path.join(
                    path,
                    f"nasa_{image_number}{extension}"
                )
            )


def main():
    load_dotenv()
    directory = "images"
    path = os.path.abspath(".")
    url = "https://api.nasa.gov/planetary/apod"
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "count", nargs='?',
            help="Number of images to be downloaded",
            type=str
    )
    args = parser.parse_args()
    count = 3 if not args.count else args.count
    params = {"count": count, "api_key": os.getenv("NASA_API_KEY")}
    try:
        os.makedirs(os.path.join(path, directory), exist_ok=True)
        fetch_nasa_apod_images(url, os.path.join(path, directory), params)
    except FileExistsError as error:
        # directory already exist
        pass


if __name__ == "__main__":
    main()
