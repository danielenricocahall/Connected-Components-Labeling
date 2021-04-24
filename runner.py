import math
import argparse
import matplotlib.pyplot as plt
import numpy as np
from labelers.connected_component_labelers import ConnectedComponentLabeler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--labeler", help="Labeler type", type=str, default="union")
    parser.add_argument('images', nargs='*')
    args = parser.parse_args()

    if not args.images:
        images = ["test_data/example_img_1.txt", "test_data/example_img_2.txt", "test_data/example_img_3.txt"]
    else:
        images = args.images

    imgs = []
    for arg in images:
        text_file = open(arg, "r")
        lines = text_file.read().split(',')
        vals = [int(line) for line in lines]
        imgs.append(np.array(vals))

    for img in imgs:
        labeler = ConnectedComponentLabeler.get_labeler(args.labeler)

        s = int(math.sqrt(img.shape[0]))
        img = np.reshape(img, (s, s))

        labeled_img = labeler.label_components(img)

        fig = plt.figure()
        ax = fig.add_subplot(121)

        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title("Original Image")

        ax = fig.add_subplot(122)
        plt.imshow(labeled_img)
        plt.axis('off')
        plt.title("Labeled Image")

        for (j, i), label in np.ndenumerate(labeled_img):
            ax.text(i, j, int(label), ha='center', va='center')

        plt.show()
        del labeler


if __name__ == "__main__":
    main()
    exit()
