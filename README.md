# Magnificent Monitor

## Installation

 1. Install Python
 2. `pip install -r requirements.txt`
 3. `python server.py`
 4. Okay, now you're running Magnificent!
 5. Visit http://localhost:12345 in a web browser or something.
 6. It should throw a verbose error, or return "Magnificent!".
 7. `python monitor.py start`
 5. Okay, now you're running Magnificent Monitor!
 6. Open performance.log to see the status of the server.
 7. Too many logs? Edit the arguments on line 112 of monitor.py to meet your preferences.
 - **url**: url of server being monitored
 - **secs**: interval for monitoring server
 - **error_threshold**: acceptable failure rate for server *(Magnificent's is 25%)*
 - **level**: minimum level of severity to store in log file *(Options by level of severity: DEBUG, INFO, WARNING, ERROR, CRITICAL)*
 8. Done monitoring Magnificent server? Run `python monitor.py stop` to end the program.