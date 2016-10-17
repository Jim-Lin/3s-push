#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import re
from dao import DAO

class ETL:

    def __init__(self):
        self.dao = DAO()

    def check_new_arrive(self):
        count = 0
        url = "http://www.dmm.co.jp/mono/dvd/-/calendar/=/day=31-31/"
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

            title_tag  = work.find("td", {"class": "title-monocal"})
            title = title_tag.find("a")
            title_name = title.text
            pattern = re.compile(ur"(^(【数量限定】|【DMM限定】|【アウトレット】)|（ブルーレイディスク）$)", re.UNICODE)
            match = re.search(pattern, title_name)
            if match:
                continue

            title_url = "http://www.dmm.co.jp" + title.get("href")
            self.check_work(title_url)

            count += 1

        print count

    def get_actress_id(self, tag):
        url = tag.get("href")
        pattern = re.compile("/mono/dvd/-/list/=/article=actress/id=(.*)/")
        match = pattern.search(url)
        id = match.group(1)
        actress = self.dao.find_actress_by_id(id)
        if actress is None:
            data = {'id': id, 'name': tag.text, 'url': "http://www.dmm.co.jp" + url}
            self.dao.insert_actress(data)

        return id

    def check_work(self, url):
        r = requests.get(url)
        soup = bs(r.text)
        
        sample = soup.find("div", {"class": "tx10 pd-3 lh4"})
        if sample is None:
            return
        
        # No Image
        a_tag = sample.find("a")
        if a_tag is None:
            return

        pattern = re.compile("/mono/dvd/-/detail/=/cid=(.*)/")
        match = pattern.search(url)
        cid = match.group(1)
        work = self.dao.find_work_by_no(cid)
        if work is not None:
            return

        performer = soup.find("span", {"id": "performer"})
        performer_a_tag = performer.find_all("a")
        actresses = list()
        for i in xrange(len(performer_a_tag)):
            actress = performer_a_tag[i]
            actresses.append(self.get_actress_id(actress))

        title = soup.find("h1", {"id": "title"})
        data = {'angels': actresses, 'no': cid, 'title': title.text, 'url': url, 'cover_url': a_tag.get('href')}
        self.dao.insert_work(data)

        return
