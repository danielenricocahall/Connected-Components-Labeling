import matplotlib.pyplot as plt
import math
import sys
from labelers.connected_component_labelers import *


def main():
    if len(sys.argv[1:]) == 0:
        sys.argv[1:] = ["Data/example_img_1.txt", "Data/example_img_2.txt", "Data/example_img_3.txt"]

    imgs = []
    for arg in sys.argv[1:]:
        text_file = open(arg, "r")
        lines = text_file.read().split(',')
        vals = [int(line) for line in lines]
        imgs.append(np.array(vals))

    for img in imgs:
        labeler = RecursiveConnectedComponentLabeler()

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
