
from labelers.connected_component_labelers import *

import numpy as np
from pytest import fixture


@fixture
def binary_image():
    img = np.zeros((3, 3))
    img[1, 1] = 1
    yield


def test_recursive_labeler(big_binary_image):
    labeler = RecursiveConnectedComponentLabeler()
    label_img = labeler.label_components(big_binary_image)
    assert label_img.tolist() == [[-0.0, -0.0, -0.0], [-0.0, 1.0, -0.0], [-0.0, -0.0, -0.0]]


def test_union_find_labeler(binary_image):
    labeler = UnionFindConnectedComponentLabeler()
    label_img = labeler.label_components(binary_image)
    assert label_img.tolist() == [[-0.0, -0.0, -0.0], [-0.0, 1.0, -0.0], [-0.0, -0.0, -0.0]]




