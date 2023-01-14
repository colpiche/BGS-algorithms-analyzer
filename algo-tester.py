from PIL import Image

FILE: str = "outputs/GroundTruth_Bootstrap_299.BMP"
IMAGE1: str = "outputs/GroundTruth_Bootstrap_299.BMP"
IMAGE2: str = "outputs/T2FMRF_UV_Bootstrap_300.png"

raw = Image.open(FILE)
im = raw.convert(mode="L")

image1 = Image.open(IMAGE1)
image2 = Image.open(IMAGE2)

# print(len(list(im.getdata())))



def compare_images(ground_truth, processed_image) -> list[int]:
    if not (ground_truth.size == processed_image.size):
        print("Please provide 2 images with same size")
        return []
    
    if not (ground_truth.mode == "L"):
        ground_truth = ground_truth.convert(mode="L")
    
    if not (processed_image.mode == "L"):
        processed_image = processed_image.convert(mode="L")
    
    ground_truth_list: list[int] = list(ground_truth.getdata())
    processed_image_list: list[int] = list(processed_image.getdata())

    tn: int = 0
    tp: int = 0
    fn: int = 0
    fp: int = 0

    for pixel in ground_truth_list:
        if ground_truth_list[pixel] == 0 and processed_image_list[pixel] == 0:
            # True Negative
            tn += 1
        elif (not ground_truth_list[pixel] == 0) and (not processed_image_list[pixel] == 0):
            # True Positive
            tp += 1
        elif (not ground_truth_list[pixel] == 0) and processed_image_list[pixel] == 0:
            # False Negative
            fn += 1
        elif ground_truth_list[pixel] == 0 and (not processed_image_list[pixel] == 0):
            # False Positive
            fp += 1

    return [tn, tp, fn, fp]


def get_accuracy(input: list[int]) -> float:
    if not (len(input) == 4):
        print("Please provide a 4 elements list")
    
    return (input[0] + input[1]) / sum(input)


errors: list[int] = compare_images(image1, image2)
print("Results : ", errors)
print("Accuracy : ", get_accuracy(errors))