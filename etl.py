#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import re

class ETL:

    def check_new_arrive(self):
        count = 0
        url = "http://www.dmm.co.jp/mono/dvd/-/calendar/=/day=31/"
        r = requests.get(url)
        soup = bs(r.text)
        
        cal = soup.find("table", {"id": "monocal"})
        work_list = cal.find_all("tr")
        if len(work_list) == 0:
            return

        for work in work_list:
            actress_tag  = work.find("td", {"class": "info-01"})
            if actress_tag is None or actress_tag.text == "----":
                continue

            actress = actress_tag.find("a")
            if actress is None:
                continue

            title_tag  = work.find("td", {"class": "title-monocal"})
            title = title_tag.find("a")
            title_name = title.text
            pattern = re.compile(ur"(^(【数量限定】|【DMM限定】|【アウトレット】)|（ブルーレイディスク）$)", re.UNICODE)
            match = re.search(pattern, title_name)
            if match:
                continue

            # check_work(title)
            
            title_url = "http://www.dmm.co.jp" + title.get("href")

            detail = self.get_detail(title_url)
            if detail is None:
                continue

            print actress.text + " " + title_name + " " + title_url

            count += 1

        print count

    def check_actress(self, tag):
        url = tag.get("href")
        pattern = re.compile("/mono/dvd/-/list/=/article=actress/id=(.*)/")
        match = pattern.search(url)
        id = match.group(1)

        return

    def check_work(self, tag):
        url = tag.get("href")
        pattern = re.compile("/mono/dvd/-/detail/=/cid=(.*)/")
        match = pattern.search(url)
        cid = match.group(1)
        print cid

        return

    def get_detail(self, url):
        r = requests.get(url)
        soup = bs(r.text)
        
        sample = soup.find("div", {"class": "tx10 pd-3 lh4"})
        if sample is None:
            return
        
        # No Image
        a_tag = sample.find("a")
        if a_tag is None:
            return

        performer = soup.find("span", {"id": "performer"})
        performer_a_tag = performer.find_all("a")
        for i in xrange(len(performer_a_tag)):
            actress = performer_a_tag[i]
            print actress
            self.check_actress(actress)

        return
