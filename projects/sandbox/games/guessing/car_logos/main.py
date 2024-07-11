
from os.path import dirname, exists, join, realpath
from carlogos import CarLogos
from misc import get_headers
import traceback
import requests
import logging
import sys
import os


class Setup:

    def __init__(self) -> None:
        self._dirname = realpath(dirname(__file__))

        # Define folder directories
        # Image folder
        self.image_foldername = "img"
        self.image_folderpath = join(self._dirname, self.image_foldername)

        # Car logos sub-folder
        self.car_logos_foldername = "car_logos"
        self.car_logos_folderpath = join(self.image_folderpath, self.car_logos_foldername)

    def run(self):

        # Initialize folder structure
        os.makedirs(self.car_logos_folderpath, mode=775, exist_ok=True)

        # Download all the car pictures
        for alphabet, data in CarLogos().cars.items():

            folderpath = join(self.car_logos_folderpath, alphabet)
            os.makedirs(folderpath, mode=775, exist_ok=True)

            for car in data["cars"]:
                name = car["name"].lower()
                url = car["picture"]

                filename = f"{name}." + url.split(".")[-1]
                filepath = join(folderpath, filename)
                if exists(filepath):
                    continue

                logging.warning(f"Downloading picture {name}")
                while True:
                    try:
                        response = requests.get(url, headers=get_headers(), verify=False)
                        response.raise_for_status()
                        picture_data = response.content
                        break
                    except Exception:
                        logging.warning("Retry...")

                with open(filepath, "wb") as fh:
                    fh.write(picture_data)


def main(*, returncode: int = 0) -> int:
    try:
        setup = Setup()
        setup.run()
    except Exception:
        returncode = 1
        print(traceback.format_exc())
    finally:
        return returncode


if __name__ == "__main__":
    returncode = main()
    sys.exit(returncode)
