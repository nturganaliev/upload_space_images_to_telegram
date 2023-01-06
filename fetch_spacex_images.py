import argparse
import os
import requests

from download_image import download_image


def get_spacex_last_launch_id(url):
    response = requests.get(url)
    response.raise_for_status()
    for launch in response.json()[::-1]:
        if launch["links"]["flickr"]["original"]:
            return launch["id"]


def fetch_spacex_last_launch(url, path, launch_id, params=None):
    image_links = None
    response = requests.get(f"{url}{launch_id}")
    response.raise_for_status()
    if not response.json()["links"]["flickr"]["original"]:
        return
    image_links = response.json()["links"]["flickr"]["original"]
    for image_number, image_link in enumerate(image_links):
        download_image(
            image_link,
            os.path.join(path, f"spacex_{image_number}.jpg")
        )


def main():
    url = "https://api.spacexdata.com/v5/launches/"
    path = os.path.join(os.path.abspath("."), "images")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "launch_id", nargs='?',
            help="Fetch spacex images",
            type=str
    )
    args = parser.parse_args()
    try:
        launch_id = (
            args.launch_id if args.launch_id else get_spacex_last_launch_id(url)
        )
    except requests.exceptions.RequestException as error:
        print(error)
    try:
        if launch_id:
            fetch_spacex_last_launch(url, path, launch_id)
    except requests.exceptions.RequestException as error:
        print(error)
    print("Завершение программы")


if __name__ == "__main__":
    main()
