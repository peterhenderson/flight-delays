#!/usr/bin/python

import optparse
import urllib
import time

# Parse command-line options
parser = optparse.OptionParser()
parser.add_option('-a', '--airport', dest='airport', default='SLC', metavar='AAA', help='retrieve data for airport AAA (default %default)')
parser.add_option('-c', '--carrier', dest='carrier', default='DL', metavar='CC', help='retrieve data for airline CC (default %default)')
parser.add_option('-b', '--begin', dest='first_day', type='int', default=1, help='first day of month to retrieve (default %default)')
parser.add_option('-e', '--end', dest='last_day', type='int', default=1, help='last day of month to retrieve (default %default)')
parser.add_option('-m', '--month', dest='month', type='int', default=1, metavar='MM', help='retrieve data for month number MM (default %default)')
parser.add_option('-l', '--lastmonth', dest='last_month', type='int', default=12, metavar='MM', help='if specified, retrives data from previously specified month until MM (default %default)')
parser.add_option('-y', '--year', dest='year', type='int', default=2010, metavar='YYYY', help='retrieve data for year YYYY (default %default)')
parser.add_option('-o', '--output', dest='output', metavar='FILE', help='save output to FILE')
parser.add_option('-f', '--format', dest='format', type='choice', choices=['csv', 'arff'], default='csv', help='output format of the data (csv or arff; default %default)')
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
}
#for day in range(options.first_day, options.last_day+1):
#    params['Day%i' % day] = day

airlines = [ 'AA', 'CO', 'DL', 'UA', 'WN' ]
airports = ['ORD', 'BOS', 'SEA', 'IAD', 'MSP', 'PWM', 'DSM', 'MEM', 'CMH', 'FYI', 'DEN']

for airport in airports:
  options.airport = airport
  params['airport1'] = airport
  for airline in airlines:
    params['airline'] = airline
    for year in range(2008, 2011):
      
      params['year1'] = str(year)
      
      for month in range(1, 13):
        params['month%i' % month] = month
        for day in range(1, 32):
          params['Day%i' % day] = str(day)
          options.output = 'data/%s/%s_%s_%i_%02i_%02i.csv' % (options.airport, options.airport, airline, year, month, day )
          print options.output
          # Request data
          dataStr = "<!DOCTYPE HTML"
          #make sure we don't get an error page from the server
          while dataStr.startswith("<!DOCTYPE HTML"):
            data = urllib.urlopen('http://www.bts.gov/xml/ontimesummarystatistics/src/dstat/OntimeSummaryDepaturesDataCSV.xml', urllib.urlencode(params))
            dataStr = data.read()
            
            #if we do get an error then we just wait a few seconds and try again
            if dataStr.startswith("<!DOCTYPE HTML"):
              print "Error. Trying again in 10 seconds...."
              time.sleep(10)
          
          with open(options.output, 'w') as output:
            output.write(dataStr)
            #print data.read()
          del params['Day%i' % day]
        del params['month%i' % month]

    
