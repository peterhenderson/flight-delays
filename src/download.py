#!/usr/bin/python

import optparse
import urllib

# Parse command-line options
parser = optparse.OptionParser()
parser.add_option('-a', '--airport', dest='airport', default='SLC', metavar='AAA', help='retrieve data for airport AAA (default %default)')
parser.add_option('-c', '--carrier', dest='carrier', default='DL', metavar='CC', help='retrieve data for airline CC (default %default)')
parser.add_option('-b', '--begin', dest='first_day', type='int', default=1, help='first day of month to retrieve (default %default)')
parser.add_option('-e', '--end', dest='last_day', type='int', default=1, help='last day of month to retrieve (default %default)')
parser.add_option('-m', '--month', dest='month', type='int', default=1, metavar='MM', help='retrieve data for month number MM (default %default)')
parser.add_option('-y', '--year', dest='year', type='int', default=2010, metavar='YYYY', help='retrieve data for year YYYY (default %default)')
parser.add_option('-o', '--output', dest='output', metavar='FILE', help='save output to FILE')
parser.add_option('-f', '--format', dest='format', type='choice', choices=['csv', 'arff'], default='arff', help='output format of the data (csv or arff; default %default)')
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
for day in range(options.first_day, options.last_day+1):
    params['Day%i' % day] = day

# Request data
data = urllib.urlopen('http://www.bts.gov/xml/ontimesummarystatistics/src/dstat/OntimeSummaryDepaturesDataCSV.xml', urllib.urlencode(params)).read()
if options.output:
    with open(options.output, 'w') as output:
        output.write(data)
else:
    print data
