© 2018 Dev Spotlight, All Rights Reserved  
Author: Jorge Orpinel Perez @jorgeorpinel

# Website Page Size Scraper

Python script that uses Selenium and Headless Chrome to determine the average page size among a list of websites.
This will include [transferSize](https://www.w3.org/TR/resource-timing-2/#dom-performanceresourcetiming-transfersize) AND any other content loaded dynamically to display the home page of each site.

## Installation

This tool was developed and ran with Python 3.6.5 on macOS 10.13

> Further versions should continue to work.

### External dependencies

- [Chrome](https://www.google.com/chrome/) 68+ installed
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver) in the OS path - chromedriver 2.42 used

### Required Python package
> See requirements.txt

- Python language bindings for **Selenium WebDriver** – [selenium](https://seleniumhq.github.io/selenium/docs/api/py/api.html) 3.14 used

To install, we will use [virtualenv](https://virtualenv.pypa.io/en/stable/):
```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
> Virtualenv installs [pip](https://pip.pypa.io/) automatically.

## Usage

Save a list of websites (one per line) in a plain text file. Included in [2018-09-15-alexa-top-sites-10.txt](2018-09-15-alexa-top-sites-50.txt) is a sample list of 50 top sites from Alexa (Sep 2018).  
Make sure the script is executable by your user:
```sh
chmod u+x from_list.py
```
You may now run it:
```sh
chromedriver 2> /dev/null &  # Implies --remote-debugging-port=9515. Runs in background.
./from_list.py 2018-09-15-alexa-top-sites-50.txt
```
> See the file docstring in from_list.py for further info.

Don't forget to stop chromedriver after running the Python script e.g.:
```sh
fg  # To bering chromedriver tot he background
^C  # Ctrl + C
```
