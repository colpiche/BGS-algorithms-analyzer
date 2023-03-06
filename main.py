from algo_tester.comparator import Comparator
from PIL import Image
# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
import os


DIRECTORY: str = "outputs"


def main():
    comparator: Comparator = Comparator(DIRECTORY)
    comparator.compute_images_results()

    # ONLY FOR TESTING TO FIND THE BUG WHERE VALUES ARE SWITCHED BETWEEN DICTIONNARIES
    IMAGE1: str = "GroundTruth_MovedObject_985.BMP"
    IMAGE2: str = "SigmaDelta_MovedObject_986.png"
    image1 = Image.open(os.path.join(DIRECTORY, IMAGE1))
    image2 = Image.open(os.path.join(DIRECTORY, IMAGE2))
    result = comparator.compare_images(image1, image2)
    print(f'result from method : {result}')
    # print(f'fn = {result["fn"]}, fp = {result["fp"]}')


if __name__ == "__main__":
    main()
