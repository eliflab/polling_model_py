# Smooth poll aggregation using state-space modeling in Stan/python

This project is a replica in pyStan of the R/Stan project from Jim Savage, described on [http://andrewgelman.com/2016/08/06/state-space-poll-averaging-model/](http://andrewgelman.com/2016/08/06/state-space-poll-averaging-model/).

Stan is a probabilistic programming language for statistical inference, written in C++. 

The original idea is to estimate the unobserved preference values for the two candidates Hillary Clinton and Donald Trump.

In this Bayesian model, the value at the time t is related to the polls published on [http://www.realclearpolitics.com](realclearpolitics.com) and also to the value at time t-1.

While the Stan model is unchanged, the scraper and the code to transform and fitting data are a bit different from the original R script.

![example] (example.png)

## Usage:

The process is splitted in 3 steps:

- Get data from **realclearpolitics.com** 

    python polls.py

- Fit Stan Model **state_space_polls.stan**

    python stan_model.py <NUM-ITERATION\> <NUM-CHAINS\>

- Display Data

    python show_data.py <NUM-ITERATION\>


*polls.py* will generate the file:

* data_polls.csv

*stan_model.py* will generate the pickle files:

* mu__<NAME\>_<NUM-ITERATION\>.pkl - median of mu parameter
* high_<NAME\>_<NUM-ITERATION\>.pkl - 97.5 percentile  
* low__<NAME\>_<NUM-ITERATION\>.pkl - 2.5 percentile

## Requirements

* numpy
* pystan
* Beautiful Soup 4
* pylab
* seaborn

