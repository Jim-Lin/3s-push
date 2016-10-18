#!/usr/bin/python
# -*- coding: utf-8 -*-

from etl import ETL

if __name__ == "__main__":
    etl = ETL()
    new_works = etl.get_new_works()
