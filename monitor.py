import urllib2
import logging
import daemon
import os

import time

dirpath = os.getcwd()

url = "http://localhost:12345"

def monitoring(url, secs, error_threshold, level=logging.DEBUG):
    """Function for monitoring health of Magnificent server."""

    # Initialize attempt counter
    counter = 0

    # Running average of past 100 attempts
    status = [0 for i in range(100)]

    # Set name and directory of logging file, prepend each log with timestamp.
    # *********************8CHANGE 'W' TO 'A' BEFORE SENDING******************
    logging.basicConfig(filename=dirpath + '/performance.log', filemode='w', 
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p:', 
        level=level)

    # Flag for server health
    healthy = True

    # Monitoring script
    while True:
        # Set frequency of checking
        time.sleep(secs)
        
        failure_rate = sum(status) / len(status)

        # Notify when first exceed error threshold
        if failure_rate > error_threshold and healthy:
                healthy = False
                logging.warning("Exceeding error threshold of {}. Current: {}".format(str(error_threshold), str(failure_rate)))
        # Notify when threshold resumed
        elif failure_rate < error_threshold and not healthy:
            healthy = True
            logging.info("Error threshold restored to normal parameters.")

        # Set status index for a given attempt
        idx = counter % 100

        # Increment counter
        counter += 1

        # Attempt to access url and log if successful
        try:
            test = urllib2.urlopen(url)
            # Reset index for attempt to 0
            status[idx] = 0
            logging.debug("Success.")
        # Log if attempt unsuccessful
        except urllib2.HTTPError as e:
            # Set index for attempt to 1
            status[idx] = 1.0 
            logging.debug("HTTPError: {}". format(str(e.code)))

# Run daemon process in background
with daemon.DaemonContext():
    monitoring(url, 1, 0.25, logging.DEBUG)