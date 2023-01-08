import time
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances


class Recommender:
    def __init__(self, strategy='user'):
        self.strategy = strategy
        self.u_similarity = np.NaN
        
    def fit(self, matrix):
        " * ** YOUR CODE HERE ** * "
        self.user_item_matrix = matrix

        if self.strategy == 'user':
            # User - User based collaborative filtering
            start_time = time.time()

            self.pred = pd.DataFrame() #self.pred should contain your prediction metrix.


            time_taken = time.time() - start_time
            print('User Model in {} seconds'.format(time_taken))

            return self


        elif self.strategy == 'item':
            # Item - Item based collaborative filtering
            start_time = time.time()

            self.pred = pd.DataFrame() #self.pred should contain your prediction metrix.

            time_taken = time.time() - start_time
            print('Item Model in {} seconds'.format(time_taken))

            return self

    def recommend_items(self, id, k=5):
        " * ** YOUR CODE HERE ** * "
        if self.strategy == 'user':

            pass

        elif self.strategy == 'item':

            pass