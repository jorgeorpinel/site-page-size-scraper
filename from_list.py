#!/usr/bin/env python
"""
Uses Selenium and Headless Chrome to scrap a list of websites.
Each website is crawled and all pages are weighted (their full size is measured).
Full size = all resources that have to be downloaded except cached content from previous pages in the same site.

Tested with Python 3.
Required packages listed in requirements.txt

Usage:
    chromedriver
    python -m from_list 2018-09-15-alexa-top-sites-10.txt

where `site-list` is the path to a plain text file containing a list of websites, one per line.
"""
import re

from argparse import ArgumentParser

from selenium import webdriver


# 0. Loads list of web site addresses from file.
parser = ArgumentParser()
parser.add_argument('fname', help="Path to plain text file containing the list of websites, one per line")
args = parser.parse_args()

# # From https://stackoverflow.com/a/5494315/761963
# re_3986_enhanced = re.compile(r"""
#         # Parse and capture RFC-3986 Generic URI components. See https://tools.ietf.org/html/rfc3986#appendix-B
#         ^
#         (?:  (?P<scheme>    [^:/?#\s]+):// )?   # Optional scheme
#         (?:(?P<authority>  [^/?#\s]*)  )?       # Optional authority
#              (?P<path>        [^?#\s]*)         # Required path
#         (?:\?(?P<query>        [^#\s]*)  )?     # Optional query
#         (?:\#(?P<fragment>      [^\s]*)  )?     # Optional fragment
#         $
#         """, re.MULTILINE | re.VERBOSE)

with open(args.fname) as f:
    # Skips empty lines and lines starting with `#` (comments).
    # site_list = [re_3986_enhanced.match(l.strip())[2] for l in f if l.strip() and '#' != l.strip()[0]]
    site_list = [l.strip() for l in f if l.strip() and '#' != l.strip()[0]]


# 1. Inits Selenium w/ Headless Chrome.

# > See https://intoli.com/blog/running-selenium-with-headless-chrome/
options = webdriver.ChromeOptions()
options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)

# See https://sites.google.com/a/chromium.org/chromedriver/logging/performance-log
# and https://docs.seleniumhq.org/docs/04_webdriver_advanced.jsp#remotewebdriver
capbs = webdriver.DesiredCapabilities.CHROME.copy()
capbs.update({'loggingPrefs': {'performance': 'ALL'}, 'detach': False})
driver = webdriver.Remote("http://127.0.0.1:9515", capbs, options=options)
# ^ Requires chromedriver (server) running locally (on default port).

# TODO: driver.set_page_load_timeout(10)  # Sets the amount of time to wait for a page load to complete before throwing an error
# OR: driver.implicitly_wait(15)  # Sets a sticky timeout to implicitly wait to find element or complete command.

# Enables DevTools Network panel.  # Unnecessary given loggingPrefs above.
# driver.execute_cdp_cmd('Network.enable', {})


# TODO: 2. Crawls each website.
tot_enc_data_len = {}
for url in site_list:
    print(f'Loading {url}...')

    driver.get(url)
    logs = driver.execute('getLog', {'type': 'performance'})['value']


    # TODO: 3. Calculate full size of each - from Network.loadingFinished INFO logs.
    loading_finished = [l['message'] for l in logs if 'INFO' == l['level'] and 'Network.loadingFinished' in l['message']]
    re_encdatalen = re.compile(r'^.*encodedDataLength":(-?[0-9]+),.*$')
    enc_data_len = [int(re_encdatalen.match(m)[1]) for m in loading_finished]
    tot_enc_data_len[url] = sum(enc_data_len)

    # Answer stackoverflow.com/questions/51581676
    # See stackoverflow.com/a/1611406/761963
    # and stackoverflow.com/a/39321151/761963 ):

    # Restarts driver to clear cache.
    driver.quit()
    driver = webdriver.Remote("http://127.0.0.1:9515", capbs, options=options)
    # FIXME: Can we use driver.start_session(capabilities) with previous driver's capabilities?
    # TODO: driver.implicitly_wait(15)  # Sets a sticky timeout to implicitly wait to find element or complete command.


# TODO: 4. Calculates average.
avg_enc_data_len = sum(tot_enc_data_len.values()) / len(tot_enc_data_len) / 10**6  # MB
# avg_enc_data_len = sum(tot_enc_data_len.values()) / len(tot_enc_data_len) / 2**20  # MiB

print(f'The average web page size is {avg_enc_data_len} MB')

driver.quit()
