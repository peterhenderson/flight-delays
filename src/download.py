#!/usr/bin/python

import optparse
import urllib

# Parse command-line options
parser = optparse.OptionParser()
parser.add_option('-a', '--airport', dest='airport', default='SLC', metavar='AAA', help='retrieve data for airport AAA')
parser.add_option('-c', '--carrier', dest='carrier', default='DL', metavar='CC', help='retrieve data for airline CC')
parser.add_option('-m', '--month', dest='month', type='int', default=1, metavar='MM', help='retrieve data for month number MM')
parser.add_option('-y', '--year', dest='year', type='int', default=2010, metavar='YYYY', help='retrieve data for year YYYY')
parser.add_option('-o', '--output', dest='output', metavar='FILE', help='save ARFF output to FILE')
(options, args) = parser.parse_args()

# Construct POST data
params = {
    'sdtime': 'Scheduled departure time',
    'adtime': 'Actual departure time',
    'setime': 'Scheduled elapsed time',
    'aetime': 'Actual elapsed time',
    'ddtime': 'Departure delay',
    'wotime': 'Wheels-off time',
    'totime': 'Taxi-out time',
    'delay': 'Cause of Delay',
    'airport1': options.airport,
    'airline': options.carrier,
    'month%i' % options.month: options.month,
    'year1': options.year
}
for day in range(1, 32):
    params['Day%i' % day] = day

# Request data
print urllib.urlopen('http://www.bts.gov/xml/ontimesummarystatistics/src/dstat/OntimeSummaryDepaturesDataCSV.xml', urllib.urlencode(params)).read()
