'''
Created on Feb 12, 2019

@author: daniel
'''

from ConnectedComponentLabeler import ConnectedComponentLabeler

class RecursiveConnectedComponentLabeler(ConnectedComponentLabeler):
    
    def findComponent(self, LB, label):
        MAX_ROWS = LB.shape[0]
        MAX_COLS = LB.shape[1]
        for i in range(MAX_ROWS):
            for j in range(MAX_COLS):
                if LB[i, j] == -1:
                    label = label + 1
                    self.search(LB, label, i,j)
                    
                    
    def search(self,LB, label, i, j):
        LB[i, j] = label
        neighborhood = LB[i-1:i+2, j-1:j+2]
        for n in range(neighborhood.shape[0]):
            for m in range(neighborhood.shape[1]):
                if neighborhood[n,m] == -1:
                    self.search(LB, label, i+n-1, j+m-1)
    
    def labelComponents(self, B):
        LB = -B
        label = 0
        self.findComponent(LB, label)
        return LB
        