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
    url = "https://api.nasa.gov/planetary/apod"
    path = os.path.join(os.path.abspath("."), "images")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "count", nargs='?',
            help="Number of images to be downloaded",
            default=3,
            type=int
    )
    args = parser.parse_args()
    params = {"count": args.count, "api_key": os.getenv("NASA_API_KEY")}
    try:
        fetch_nasa_apod_images(url, path, params)
    except requests.exceptions.RequestException as error:
        print(error)
    print("Завершение программы")


if __name__ == "__main__":
    main()
