from abc import ABC, abstractmethod

import numpy as np


class ConnectedComponentLabeler(ABC):

    @abstractmethod
    def label_components(self, B):
        pass


class RecursiveConnectedComponentLabeler(ConnectedComponentLabeler):

    def find_components(self, label_img, label):
        max_rows, max_cols = label_img.shape
        for i in range(max_rows):
            for j in range(max_cols):
                if label_img[i, j] == -1:
                    label = label + 1
                    self.search(label_img, label, i, j)

    def search(self, label_img, label, i, j):
        label_img[i, j] = label
        neighborhood = label_img[i - 1:i + 2, j - 1:j + 2]
        for n in range(neighborhood.shape[0]):
            for m in range(neighborhood.shape[1]):
                if neighborhood[n, m] == -1:
                    self.search(label_img, label, i + n - 1, j + m - 1)

    def label_components(self, binary_img):
        label_img = -binary_img
        label = 0
        self.find_components(label_img, label)
        return label_img


def prior_neighbors(img, i, j):
    neighbors = []
    if i == 0:
        A = img[i, j - 1:j]
    elif j == 0:
        A = img[i - 1:i, j]
    else:
        A = img[i - 1:i + 1, j - 1:j + 2].flatten()[:-2]
    for i in range(A.shape[0]):
        if A[i] == 1:
            neighbors.append(i)
    return neighbors


def get_labels(label_img, i, j, indices):
    if i == 0:
        labels = label_img[i, j - 1:j]
    elif j == 0:
        labels = label_img[i - 1:i + 1, j:j + 2].flatten()[:-1]
    else:
        labels = label_img[i - 1:i + 1, j - 1:j + 2].flatten()[:-2]
    neighboring_labels = []
    for index in indices:
        neighboring_labels.append(labels[index])
    return neighboring_labels


class UnionFindConnectedComponentLabeler(ConnectedComponentLabeler):

    def __init__(self):
        self.parent = []
        for _ in range(0, 100):
            self.parent.append(0)
        self.num_labels = 0

    def union(self, X, Y):
        j = int(X)
        k = int(Y)
        while self.parent[j] != 0:
            j = self.parent[j]
        while self.parent[k] != 0:
            k = self.parent[k]
        if k != j:
            self.parent[k] = j

    def find(self, X):
        j = int(X)
        while self.parent[j] != 0:
            j = self.parent[j]
        return j

    def label_components(self, binary_image):
        label = 1
        label_image = np.zeros(binary_image.shape)
        max_rows, max_cols = binary_image.shape
        for i in range(max_rows):
            for j in range(max_cols):
                if binary_image[i, j] == 1:
                    A = prior_neighbors(binary_image, i, j)
                    if len(A) == 0:
                        m = label;
                        label = label + 1
                    else:
                        m = int(np.amin(get_labels(label_image, i, j, A)))
                    label_image[i, j] = m
                    for label in get_labels(label_image, i, j, A):
                        if label != m:
                            self.union(m, label)
        for i in range(max_rows):
            for j in range(max_cols):
                if binary_image[i, j] == 1:
                    label_image[i, j] = self.find(label_image[i, j])
        return label_image
