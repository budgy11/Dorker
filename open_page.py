#!/usr/bin/env python3
import time

from invisible_playwright import InvisiblePlaywright

with InvisiblePlaywright() as browser:
    page = browser.new_page()
    page.goto("https://antcpt.com/score_detector/",)
    time.sleep(10)

