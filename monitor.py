import urllib2
import logging
import daemon
import os

import time

dirpath = os.getcwd()

url = "http://localhost:12345"

def monitoring(url, secs, error_threshold, level=logging.DEBUG):
    counter = 0

    status = [0 for i in range(100)]

    # logging.basicConfig(filename='/var/log/performance.log', level=logging.DEBUG)
    logging.basicConfig(filename=dirpath + '/performance.log', filemode='w', 
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p:', 
        level=level)
    # logging.basicConfig(level=level)

    healthy = True

    while True:
        time.sleep(secs)
        
        failure_rate = sum(status) / len(status)

        if failure_rate > error_threshold and healthy:
                healthy = False
                logging.warning("Exceeding error threshold of {}. Current: {}".format(str(error_threshold), str(failure_rate)))
        elif failure_rate < error_threshold and not healthy:
            healthy = True
            logging.info("Error threshold restored to normal parameters.")

        idx = counter % 100
        counter += 1

        try:
            test = urllib2.urlopen(url)
            status[idx] = 0
            logging.debug("Success.")

        except urllib2.HTTPError as e:
            status[idx] = 1.0 
            logging.debug("HTTPError: {}". format(str(e.code)))

with daemon.DaemonContext():
    monitoring(url, 1, 0.25, logging.DEBUG)
# monitoring(url, 1, 0.25)