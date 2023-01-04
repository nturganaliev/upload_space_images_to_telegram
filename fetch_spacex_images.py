import argparse
import os
import requests

from download_image import download_image


def fetch_spacex_last_launch(url, path, launch_id=None, params=None):
    image_links = None

    if not launch_id:
        response = requests.get(url)
        response.raise_for_status()
        for launch in response.json()[::-1]:
            if launch["links"]["flickr"]["original"]:
                image_links = launch["links"]["flickr"]["original"]
                break
    else:
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
    try:
        os.makedirs(os.path.join(path, directory), exist_ok=True)
        if not args.launch_id:
            fetch_spacex_last_launch(url, os.path.join(path, directory))
            return
        fetch_spacex_last_launch(url,
                                 os.path.join(path, directory),
                                 args.launch_id)
    except FileExistsError as error:
        # directory already exist
        pass


if __name__ == "__main__":
    main()
