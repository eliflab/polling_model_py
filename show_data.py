#!/usr/bin/env python
from stan_model import get_data
import os.path
import sys
import pickle

try:
    import seaborn as sns
    plt = sns.plt
except:
    import pylab as plt

def get_points(Y):
    pout = []
    for i, pts in enumerate(Y.tolist()):
        for pt in pts:
            if pt > 0:
                pout.append([i, pt])
    X= [x[0] for x in pout]
    Y= [x[1] for x in pout]
    return X, Y


if __name__ == '__main__':
    Y_clinton, Y_trump, sigma, dates = get_data()
    Xc, Yc = get_points(Y_clinton)
    Xt, Yt = get_points(Y_trump)

    plt.scatter(Xc, Yc, color="blue", alpha=0.6, label="Polls Clinton", marker="x") 
    plt.scatter(Xt, Yt, color="red", alpha=0.6, label="Polls Trump", marker="x") 

    n_iter = 1500 

    if len(sys.argv)>1:
        n_iter = int(sys.argv[1])

    #TODO check prfile existence
    for name, color in [('Clinton', 'blue'), ('Trump', 'red')]:

        if not os.path.isfile('mu_%s_%s.pkl' % (name, n_iter)):
            print "Data files are missing! Try to run: python stan_model.py %s before." % name 

        mum = pickle.load(open('mu_%s_%s.pkl' % (name, n_iter)))
        low = pickle.load(open('low_%s_%s.pkl' % (name, n_iter)))
        high = pickle.load(open('high_%s_%s.pkl' % (name, n_iter)))
        years = [i for i,_ in enumerate(mum)]
        plt.plot(years, mum, color=color, label=name)
        plt.fill_between(years, low, high, alpha=0.3, color='gray')
    
    dates = pickle.load(open('dates.pkl'))
    plt.legend()
    plt.xticks(years[::20], dates[::20], rotation=70)
    plt.show()
