import urllib2
import logging
import daemon
import os
import sys
import signal
import argparse
import os.path
import time

dirpath = os.getcwd()
pidfile = dirpath + '/pidfile.txt'
url = "http://localhost:12345"


def write_pid_file():
    """ Write process id (pid) to file."""

    # Get pid
    pid = str(os.getpid())

    # Exit program if pidfile already exists
    if os.path.exists(pidfile):
        sys.exit(1)
    # Otherwise, write a pid to pidfile
    else:
        with open(pidfile, 'w') as f:
            f.write(pid)


def monitoring(url, secs, error_threshold, level=logging.DEBUG):
    """Function for monitoring health of Magnificent server."""

    # Write pid file for monitoring process
    write_pid_file()

    # Initialize attempt counter
    counter = 0

    # Running average of past 100 attempts
    status = [0 for i in range(100)]

    # Set name and directory of logging file, prepend each log with timestamp.
    logging.basicConfig(filename=dirpath + '/performance.log', filemode='a',
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p:',
                        level=level)

    # Flag for server health
    healthy = True

    # Monitoring script
    while True:
        # Set interval for checking server in seconds
        time.sleep(secs)

        failure_rate = sum(status) / len(status)

        # Notify when server health first exceeds error threshold
        if failure_rate > error_threshold and healthy:
            healthy = False
            # **Version 2.0: Find way to send this log as Slack notification**
            logging.warning("Exceeding error threshold of {}. Current: {}".format(
                str(error_threshold), str(failure_rate)))
        # Notify when server health returns to normal parameters
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
        # If HTTPError execption encountered, log error
        except urllib2.HTTPError as e:
            # Set index for attempt to 1
            status[idx] = 1.0
            logging.debug("HTTPError: {}". format(str(e.code)))


def error_threshold_logic(is_healthy, failure_rate, error_threshold):
    """Logic for testing error threshold."""

    # Notify when server health first exceeds error threshold
    if failure_rate > error_threshold and is_healthy:
        is_healthy = False
    # Notify when server health returns to normal parameters
    elif failure_rate < error_threshold and not is_healthy:
        is_healthy = True

    return is_healthy


def arguments_reader():
    """ Use argparse to allow for monitor to run based on command 
            line arguments.
    """

    parser = argparse.ArgumentParser(
        description='Run daemon for monitoring Magnificent server.')
    parser.add_argument('operation',
                        help='Operation with monitor daemon. Accepts "start" or "stop" as values.',
                        choices=['start', 'stop'])
    args = parser.parse_args()
    operation = args.operation
    return operation


###############################################################################

if __name__ == "__main__":

    # Read option for argparse
    action = arguments_reader()

    # Run monitoring daemon if action if running "python monitor.py start"
    if action == 'start':
        with daemon.DaemonContext():
            monitoring(url, 1, 0.25, logging.DEBUG)

    # Terminate monitoring daemon if action is "python monitor.py stop"
    elif action == 'stop':
        if not os.path.exists(pidfile):
            sys.exit(1)
        else:
            with open(pidfile, 'r') as f:
                pid = f.readline().strip()
            os.kill(int(pid), signal.SIGTERM)
            os.remove(dirpath + '/pidfile.txt')
