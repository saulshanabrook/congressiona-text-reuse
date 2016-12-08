import numpy as np
from scipy.special import expit as logistic
import pandas as pd
from tqdm import tqdm_notebook, tqdm


class Gradient():
    def __init__(self, data):
        """
        `data` should be a dataframe with three columns:
            * position: 1/0 for yes/no
            * legislator: index of legislator who voted
            * vote: vote this poition is for
        """
        self.data = data

        self.n_legislators = data['legislator'].max() + 1
        self.n_votes = data['vote'].max() + 1

        self.randomly_initialize()


    def randomly_initialize(self):
        self.params = {
            "legislator_ideologies": np.random.randn(self.n_legislators),
            "vote_ideologies": np.random.randn(self.n_votes),
            "vote_biases": np.random.randn(self.n_votes),
        }


    def log_likelihood(self):
        """
        Likelihood of data, given parameters
        log prod_positions Bernouli(logistic(legislator_ideology * vote_ideology + vote_bias))
        = sum_positions log Bernouli(logistic(legislator_ideology * vote_ideology + vote_bias))
        """
        rows = self.rows()
  
        p = logistic(rows['legislator_ideology'] * rows['vote_ideology'] + rows['vote_bias'])
        
        # p if position, 1 - p if not position
        actual_p = np.where(rows['position'], p, (1 - p))
        return np.log(actual_p).sum()

    def rows(self):
        """
        return [position, legislator_ideology, vote_ideology, vote_bias]
        """
        return pd.DataFrame({
            "position": self.data['position'],
            "legislator_ideology": self.params['legislator_ideologies'][self.data['legislator']],
            "vote_ideology": self.params['vote_ideologies'][self.data['vote']],
            "vote_bias": self.params['vote_biases'][self.data['vote']],
        })

    
    def exp_(self, rows):
        return np.exp(rows['legislator_ideology'] * rows['vote_ideology'] + rows['vote_bias'])
    
    def deriv_legislator_ideology(self, wrt_legislator):
        """
        sum of rows w/ this legislator of 
            if position
                vote_ide / (exp_ + 1)
            else
                vote_ide / (exp_ + 1) - vote_ide
        
        where exp_ =
            exp{leg_ideo * vote_ideo + vote_bias}
        
        
        """

        rows = self.rows()[self.data['legislator'] == wrt_legislator]        
        return (
            rows['vote_ideology'] / (self.exp_(rows) + 1) \
            + np.where(rows['position'], 0, -rows['vote_ideology'])      
        ).sum()


    def deriv_vote_ideology(self, wrt_vote):
        rows = self.rows()[self.data['vote'] == wrt_vote]        
        return (
            rows['legislator_ideology'] / (self.exp_(rows) + 1) \
            + np.where(rows['position'], 0, -rows['legislator_ideology'])      
        ).sum()

    def deriv_vote_bias(self, wrt_vote):
        rows = self.rows()[self.data['vote'] == wrt_vote]        
        return (
            1 / (self.exp_(rows) + 1) \
            + np.where(rows['position'], 0, -1)      
        ).sum()


    def descend(self):
        alpha = 0.1
        for i in range(self.n_votes):
            self.params['vote_ideologies'][i] += alpha * self.deriv_vote_ideology(i)

        for i in range(self.n_votes):
            self.params['vote_biases'][i] += alpha * self.deriv_vote_bias(i)

        for i in range(self.n_legislators):
            self.params['legislator_ideologies'][i] += alpha * self.deriv_legislator_ideology(i)
 
    def run(self, n=10):
        for i in tqdm_notebook(list(range(n))):
            if i % 10 == 0:
                tqdm.write(str(self.log_likelihood()))
            self.descend()
