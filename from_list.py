#!/usr/bin/env python
"""
Uses Selenium and Headless Chrome to scrap a list of websites.
Each web site's home is loaded and fully weighted.
Full weight = all resources that are downloaded initially by the browser to display the home page (no cache).

Developed and tested with Python 3.6
Requires Chrome and chromedriver
Requires packages listed in requirements.txt

Usage:
    chromedriver 2> /dev/null &
    python -m from_list 2018-09-15-alexa-top-sites-50.txt

where `site-list` is the path to a plain text file containing a list of websites, one per line.
"""
import re
import sys
import time

from argparse import ArgumentParser

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException

# 0. Loads list of web site addresses from file.
parser = ArgumentParser()
parser.add_argument('fname', help="Path to plain text file containing the list of websites, one per line")
args = parser.parse_args()

with open(args.fname) as f:
    # Skips empty lines and lines starting with `#` (comments).
    site_list = [l.strip() for l in f if l.strip() and '#' != l.strip()[0]]

    print(f'Loaded list of {len(site_list)} URLs:');


# 1. Configs Selenium w/ Headless Chrome.

# > See https://intoli.com/blog/running-selenium-with-headless-chrome/
options = webdriver.ChromeOptions()
options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)

# See https://sites.google.com/a/chromium.org/chromedriver/logging/performance-log
# and https://docs.seleniumhq.org/docs/04_webdriver_advanced.jsp#remotewebdriver
capbs = webdriver.DesiredCapabilities.CHROME.copy()
capbs.update({'loggingPrefs': {'performance': 'ALL'}, 'detach': False})


# 2. Crawls each website.
tot_enc_data_len = {}
tot_elapsed = 0
for url in site_list:
    # Inits the WebDriver (again).
    driver = webdriver.Remote("http://127.0.0.1:9515", capbs, options=options)
    # ^ Requires chromedriver (server) running locally (on default port).
    driver.set_page_load_timeout(10)  # Set the amount of time to wait for a page load to complete...
    driver.set_script_timeout(10)  # Set the amount of time that the to wait during an execute_async_script call...

    print(f'Loading {url}... ', end='');
    sys.stdout.flush()

    start = time.time()
    try:
        driver.get(url)
    except TimeoutException as timeout:
        print('Taking too long! Skipping after 10s waits');
        continue
    except WebDriverException as invalidurl:
        print(f'Skipping invalid URL {url}');
        # FIXME: Assumes it's an invalidurl error.
        continue

    end = time.time()
    elapsed = end - start
    tot_elapsed += elapsed

    logs = driver.execute('getLog', {'type': 'performance'})['value']


    # 3. Calculate full size of each - from Network.loadingFinished INFO logs.
    loading_finished = [l['message'] for l in logs if
                        'INFO' == l['level'] and 'Network.loadingFinished' in l['message']]
    re_encdatalen = re.compile(r'^.*encodedDataLength":(-?[0-9]+),.*$')
    enc_data_len = [int(re_encdatalen.match(m)[1]) for m in loading_finished]
    tot_enc_data_len[url] = sum(enc_data_len)

    print(f'{tot_enc_data_len[url]}B, {elapsed:.3}s')

    # Quits the driver to clear cache.
    driver.quit()
    # FIXME: Can we use driver.start_session(capabilities) with previous driver's capabilities?


# 4. Calculates average.
avg_enc_data_len = sum(tot_enc_data_len.values()) / len(tot_enc_data_len) / 10 ** 6  # MB
# avg_enc_data_len = sum(tot_enc_data_len.values()) / len(tot_enc_data_len) / 2**20  # MiB

print(f'The average web page size is {avg_enc_data_len}MB from {len(tot_enc_data_len)} processed web sites, loaded in {tot_elapsed:.3}s.')
