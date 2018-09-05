# Website Page Size Scraper

Python script that uses Selenium and Headless Chrome to determine the average page size among a list of websites.

## Installation

This tool uses Python 3.

### External dependency

- Requres [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (`chromedriver` exec) in the system path - 2.41 used at the time of writing

### Required Python package
> See requirements.txt

- Python language bindings for **Selenium WebDriver** (selenium==3.14 used at the time of writing)

Having [pip](https://pip.pypa.io/), install it with
```sh
pip install -r requirements.txt
```

## Usage

Save a list of websites (one per line) in a plain text file e.g. site-list and make sure the script is executable by you:
```sh
chmod u+x from_list.py
```
You may now run it:
```sh
./from_list.py site-list
```
> See the file docstring in from_list.py for further info.
