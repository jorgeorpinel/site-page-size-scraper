#!/usr/bin/env python

"""
Uses Selenium and Headless Chrome to scrap a list of websites.
Each website is crawled and all pages are weighted (their full size is measured).
Full size = all resources that have to be downloaded except cached content from previous pages in the same site.

Tested with Python 3.
Required packages listed in requirements.txt

Usage:
    python -m from_list site-list

where `site-list` is the path to a plain text file containing a list of websites, one per line.
"""

from argparse import ArgumentParser

from selenium import webdriver


# 0. Loads list of sites from file.
parser = ArgumentParser()
parser.add_argument('fname', help="Path to plain text file containing the list of websites, one per line")
args = parser.parse_args()

with open(args.fname) as f:
    site_list = [l.strip() for l in f]

# 1. Inits Selenium w/ Headless Chrome.
# > See https://intoli.com/blog/running-selenium-with-headless-chrome/

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options)

# TODO: 2. Crawls each website.

# TODO: 3. Calculate full size of each page.

# TODO: 4. Calculates averages.

driver.quit()
