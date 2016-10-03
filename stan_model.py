#!/usr/bin/env python
import csv
import sys
import datetime
from dateutil.parser import parse
import pickle
import numpy as np
import pystan

def get_median_percentile(fit, name='', niter=0, save=True):
    mu = fit.extract(permuted=True)['mu']
    low = np.nanpercentile(mu, 2.5, axis=0)
    high = np.nanpercentile(mu, 97.5, axis=0)
    mum = np.median(mu, axis=0)
    if save:
        pickle.dump(mum, open('mu_%s_%s.pkl' % (name, niter), 'w'))
        pickle.dump(low, open('low_%s_%s.pkl' % (name, niter), 'w'))
        pickle.dump(high, open('high_%s_%s.pkl' % (name, niter), 'w'))
    return mum, low, high

def fit_stan(stan_dat, n_chains, n_iter, fit=None, verbose=False):
    fit = pystan.stan(
            fit = fit,
            file='state_space_polls.stan',
            data=stan_dat,
            chains=n_chains,
            iter=n_iter,
            verbose= verbose,
        )

    return fit

def get_data(fname="data_polls.csv", numdays=500):
    re =  csv.reader(open(fname))
    Y_clinton, Y_trump, sigma, dates = [], [], [] ,[]
    mdate = {}
    for r in re: 
        end_date= r[1]
        if r[2] == "--": 
            r[2] = 5
        mdate[end_date] = mdate.get(end_date, []) + [[ float(r[3]), float(r[4]), float(r[2]), r[0], r[1] ] ]

    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]

    for k in date_list[::-1]:
        k = k.strftime("%Y/%m/%d")
        
        vals = mdate.get(k, [])
        vals = vals + ([[-9]*4 ]*(4-len(vals)))
        Y_clinton.append([v[0] for v in vals])
        Y_trump.append([v[1] for v in vals])
        sigma.append([v[2] for v in vals])
        dates.append(k)

    return [np.array(x) for x in [Y_clinton, Y_trump, sigma, dates]]

if __name__ == '__main__':
    
    n_iter = 1500
    n_chains= 1

    if len(sys.argv)>1:
        n_iter = int(sys.argv[1])
    if len(sys.argv)>2:
        n_chains = int(sys.argv[2])

    #getting data
    Y_clinton, Y_trump, sigma, dates = get_data()

    #fitting model
    print "Fitting Model. Num. Iterations: %s. Num. Chains:%s" % (n_iter, n_chains)

    pickle.dump(dates, open('dates.pkl', 'w'))

    fit = None
    for name, Y, prior in [('Clinton', Y_clinton, 50.0), ('Trump', Y_trump, 30.0)]: 
        stan_dat = {
                   'T': len(Y),
                   'polls': len(Y[0]),
                   'Y': Y, 
                   'initial_prior': prior,
                    'sigma': sigma,
                    }

        fit = fit_stan(stan_dat, n_chains, n_iter, fit)
        get_median_percentile(fit, name, n_iter)

