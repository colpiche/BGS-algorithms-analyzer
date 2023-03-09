from algo_tester.comparator import Comparator
from PIL import Image
# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
import os


DIRECTORY: str = "outputs"


def main():
    comparator: Comparator = Comparator(DIRECTORY)
    comparator.compute_images_results()
    comparator.print_images_results()


if __name__ == "__main__":
    main()
