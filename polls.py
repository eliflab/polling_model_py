#!/usr/bin/env python
from bs4 import BeautifulSoup
from dateutil.parser import parse
import csv
from urllib2 import urlopen

def get_dates(dates, year):
    fr, to = dates.split(" - ")
    return [ parse("%s/%s" %(year, x)).strftime("%Y/%m/%d") for x in [fr, to] ]

if __name__ == '__main__':
    url = "http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html#polls"
    html = urlopen(url).read()
    da = open('rcp.html', 'w').write(html)
    soup = BeautifulSoup(html)
    tables = soup.find('div', {'id': 'polling-data-full'}).find_all('table')
    wri = csv.writer(open('data_polls.csv', 'w'))
    year = 2016
    out = []
    for atable in tables:
        for tr in atable.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 0:
                out.append([tr.get('data-id')] + [x.text for x in tds])

    for tds in out:  
        did, name, dates, sample, moe, clinton, trump, spread = tds
        mo = int(dates.split("- ")[0].split("/")[0])

        #HACK In the dates is not present the year. We must infer the change. 
        if mo == 12 and year == 2016:
            year = 2015
        dates = get_dates(dates, year)
        row = dates + [moe, clinton, trump]
        wri.writerow(row)
