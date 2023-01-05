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
    directory = "images"
    path = os.path.abspath(".")
    url = "https://api.spacexdata.com/v5/launches/"
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "launch_id", nargs='?',
            help="Fetch spacex images",
            type=str
    )
    args = parser.parse_args()
    os.makedirs(os.path.join(path, directory), exist_ok=True)
    try:
        if not args.launch_id:
            launch_id = get_spacex_last_launch_id(url)
            fetch_spacex_last_launch(url,
                                     os.path.join(path, directory),
                                     launch_id)
            return
        fetch_spacex_last_launch(url,
                                 os.path.join(path, directory),
                                 args.launch_id)
    except requests.exceptions.RequestException as error:
        raise error


if __name__ == "__main__":
    main()
