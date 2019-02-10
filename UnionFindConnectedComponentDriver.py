'''
Created on Feb 4, 2019

@author: daniel
'''
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

parent = []
MAXLAB = 100


def initialize():
    for _ in range(0, MAXLAB):
        parent.append(0)

def find(X, parent):
    j = int(X);
    while parent[j] != 0:
        j = parent[j]
    return j
     
          
def prior_neighbors(img, i, j):
        neighbors = []
        if i == 0:
            A = img[i, j-1:j]
        elif j == 0:
            A = img[i-1:i, j]
        else:
            A = img[i-1:i+1, j-1:j+2].flatten()[:-2]
        for i in range(A.shape[0]):
            if A[i] == 1:
                neighbors.append(i)
                
        return neighbors
    
def get_labels(LB, i, j, indices):
        if i == 0:
            labels = LB[i, j-1:j]
        elif j == 0:
            labels = LB[i-1:i+1, j:j+2].flatten()[:-1]
        else:
            labels = LB[i-1:i+1, j-1:j+2].flatten()[:-2]
        neighboring_labels = []
        for index in indices:
            neighboring_labels.append(labels[index])
        return neighboring_labels


def union(X, Y, parent):
    j = int(X);
    k = int(Y);
    while parent[j] != 0:
        j = parent[j]
    while parent[k] != 0:
        k = parent[k]
    if k != j:
        parent[k] = j

def makeLabelsContiguous(LB):
    unique_labels = np.unique(LB)
    for i, label in enumerate(unique_labels):
        LB[LB == label] = i
    return LB
        
def labelConnectedComponents(img):
    label = 1
    LB = np.zeros(img.shape)
    MAX_ROWS = img.shape[0]
    MAX_COLS = img.shape[1]
    for i in range(MAX_ROWS):
        for j in range(MAX_COLS):
            if img[i, j] == 1:
                A = prior_neighbors(img, i, j)
                if len(A) == 0:
                    M = label;
                    label = label + 1
                    if M > len(parent):
                        return LB
                else:
                    M = int(np.amin(get_labels(LB, i, j, A)))
                LB[i, j] = M
                for X in get_labels(LB, i, j, A):
                    if X != M:
                        union(M, X, parent)
    for i in range(MAX_ROWS):
        for j in range(MAX_COLS):
            if img[i, j] == 1:
                LB[i,j] = find(LB[i,j], parent)
    LB = makeLabelsContiguous(LB)
    return LB

def main():
    if len(sys.argv[1:]) == 0:
        sys.argv[1:] = ["example_img_2.txt", "example_img_3.txt", "example_img_1.txt"]
    
    initialize();

    imgs = []
    for arg in sys.argv[1:]:
        text_file = open(arg, "r")
        lines = text_file.read().split(',')
        vals = [int(line) for line in lines]
        imgs.append(np.array(vals))
        
    for img in imgs:
        
        ## assume arrays can be reshaped into squares
        s = int(math.sqrt(img.shape[0]))
        img = np.reshape(img, (s, s))
        
        labeled_img = labelConnectedComponents(img)
            
        fig = plt.figure()
        ax = fig.add_subplot(121)
        
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title("Original Image")
    
        ax = fig.add_subplot(122)
        plt.imshow(labeled_img)
        plt.axis('off')
        plt.title("Labeled Image")
        
        for (j,i),label in np.ndenumerate(labeled_img):
            ax.text(i,j,int(label),ha='center',va='center')

        plt.show()
    
if __name__== "__main__":
    main()
    exit()