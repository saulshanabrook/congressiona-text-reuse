import numpy as np
from scipy.special import expit as logistic
import pandas as pd
from tqdm import tqdm_notebook, tqdm
from scipy.stats import norm


class Gradient():
    def __init__(self, data):
        """
        `data` should be a dataframe with three columns:
            * position: 1/0 for yes/no
            * legislator: index of legislator who voted
            * vote: vote this poition is for
        """

        #
        self.position, self.legislator, self.vote = data.as_matrix(columns=["position", "legislator", "vote"]).T

        self.n_legislators = self.legislator.max() + 1
        self.n_votes = self.vote.max() + 1
        self.params = {
            "legislator_ideologies": np.random.randn(self.n_legislators),
            "vote_ideologies": np.random.randn(self.n_votes),
            "vote_biases": np.random.randn(self.n_votes),
        }

        self.legislator_mask = self.compute_mask(self.legislator)
        self.vote_mask = self.compute_mask(self.vote)


    def compute_rows(self):
        """
        Updates current values of latent parameters for each row of the data.
        """,
        self.legislator_ideology = self.params['legislator_ideologies'][self.legislator]
        self.vote_ideology = self.params['vote_ideologies'][self.vote]
        self.vote_bias = self.params['vote_biases'][self.vote]


    def compute_mask(self, column):
        """
        Returns a list of masks for a column. It returns a list, each index is the column
        value and each value is a array mask (1s and 0s) for when that index is in the column.

        We can iterate through this to select rows for each vote/legislator.
        """
        return [(column == i) for i in range(column.max() + 1)]


    def log_likelihood(self):
        """
        Likelihood of data, given parameters
        log prod_positions Bernouli(logistic(legislator_ideology * vote_ideology + vote_bias))
        = sum_positions log Bernouli(logistic(legislator_ideology * vote_ideology + vote_bias))
        """
        p = logistic(self.legislator_ideology * self.vote_ideology + self.vote_bias)
        
        # p if position, 1 - p if not position
        actual_p = np.where(self.position, p, (1 - p))
        return np.log(actual_p).sum()

    def descend(self):
        alpha = 0.001

        self.compute_rows()
        exp = np.exp(self.legislator_ideology * self.vote_ideology + self.vote_bias)
        exp_div = 1 / (exp + 1)
        position_neg = np.where(self.position, 0, -1)  

        deriv_legislator_ideology = self.vote_ideology * exp_div + position_neg * self.vote_ideology

        deriv_vote_ideology = self.legislator_ideology * exp_div + position_neg * self.legislator_ideology
        deriv_vote_bias = exp_div + position_neg

        for (i, mask) in enumerate(self.vote_mask):
            self.params['vote_ideologies'][i] += alpha * deriv_vote_ideology[mask].sum()
            self.params['vote_biases'][i] += alpha * deriv_vote_bias[mask].sum()

        for (i, mask) in enumerate(self.legislator_mask):
            self.params['legislator_ideologies'][i] += alpha *  deriv_legislator_ideology[mask].sum()
 
    def run(self, n=10):
        self.compute_rows()
        for i in tqdm_notebook(list(range(n))):
            if i % 1 == 0:
                tqdm.write(str(self.log_likelihood()))
            self.descend()
