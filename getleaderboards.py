#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""newgetleaderboards.py
"""
import sys
import os
import json
import requests
import collections
import pandas as pd
from r6api import R6Api, GET

pages = []
errors = []

r6 = R6Api()

# r = r6.leaderboards.casual.GET(params={'page': 1})

def get_all_pages(leaderboard):
    pages = []
    errors = []

    page = r6.leaderboards[leaderboard].GET(params={'page': 1})
    pages.append(page)
    
    total_pages = page['meta']['total_pages']
    next_page = page['meta']['next_page']

    for i in xrange(next_page, total_pages+1):
        if i % 10 == 0 or i == total_pages:
            print "{} => {} of {}".format(leaderboard, i, total_pages)
        try:
            page = r6.leaderboards[leaderboard].GET(params={'page': i})
            pages.append(page)
        except Exception, err:
            page = None
            errors.append(err[1])
    return pages, errors



for leaderboard in ('casual', 'ranked', 'general'):
    print "*"*80
    print leaderboard.upper()
    print "*"*80
    pages, errors = get_all_pages(leaderboard)

    success_file = "data/{}-success-002.json".format(leaderboard)
    write_json_to_file(pages, success_file)

    error_file = "data/{}-errors-002.txt".format(leaderboard)
    write_text_to_file(errors, error_file)
    
