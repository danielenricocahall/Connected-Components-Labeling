'''
Created on Jan 31, 2019

@author: DCahall
'''
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

    
def labelConnectedComponents(B):
    LB = -B
    label = 0
    findComponent(LB, label)
    return LB

def findComponent(LB, label):
    MAX_ROWS = LB.shape[0]
    MAX_COLS = LB.shape[1]
    for i in range(MAX_ROWS):
        for j in range(MAX_COLS):
            if LB[i, j] == -1:
                label = label + 1
                search(LB, label, i,j)
                
                
def search(LB, label, i, j):
    LB[i, j] = label
    neighborhood = LB[i-1:i+2, j-1:j+2]
    for n in range(neighborhood.shape[0]):
        for m in range(neighborhood.shape[1]):
            if neighborhood[n,m] == -1:
                search(LB, label, i+n-1, j+m-1)
    

def main():
    if len(sys.argv[1:]) == 0:
        sys.argv[1:] = ["example_img.txt", "example_img_2.txt"]
        
    imgs = []
    for arg in sys.argv[1:]:
        text_file = open(arg, "r")
        lines = text_file.read().split(',')
        vals = [int(line) for line in lines]
        imgs.append(np.array(vals))
        
    for img in imgs:
        s = int(math.sqrt(img.shape[0]))
        img = np.reshape(img, (s, s))
        
        labeled_img = labelConnectedComponents(img)
        
        plt.subplot(1,2,1)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title("Original Image")
    
        plt.subplot(1,2,2)
        plt.imshow(labeled_img)
        plt.axis('off')
        plt.title("Labeled Image")

        plt.show()
    
if __name__== "__main__":
    main()
    exit()