import urllib2
import logging
import daemon
import os, sys
import signal
import argparse
import os.path

import time

dirpath = os.getcwd()
pidfile = dirpath + '/pidfile.txt'

url = "http://localhost:12345"

def monitoring(url, secs, error_threshold, level=logging.DEBUG):
    """Function for monitoring health of Magnificent server."""

    # Write pidfile
    write_pid_file()
    
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


def write_pid_file():
    pid = str(os.get_pid())
    if os.path.exists(pidfile):
        sys.exit(1)
    else:
        with open(pidfile, 'w') as f:
            f.write(pid)
            


def arguments_reader():

    parser = argparse.ArgumentParser(description='Run daemon for monitoring Magnificent server.')
    parser.add_argument('operation', 
        help='Operation with monitor daemon. Accepts "start" or "stop" as values.',
        choices=['start', 'stop'])
    args = parser.parse_args()
    operation = args.operation
    return operation

# Run daemon process in background
# with daemon.DaemonContext():
#     monitoring(url, 1, 0.25, logging.DEBUG)

if __name__ == "__main__":
    
    action = arguments_reader()

    if action == 'start':
        print "Starting monitor.py."
        with daemon.DaemonContext():
            monitoring(url, 1, 0.25, logging.DEBUG)
            
    if action == 'stop':
        print "Stopping monitor.py"
        if not os.path.exists(pidfile):
            sys.exit(1)
        else:
            with open(pidfile, 'r') as f:
                pid = f.readline().strip()
            os.kill(pid, signal.SIGTERM)
            os.remove(dirpath + '/pidfile.txt')
