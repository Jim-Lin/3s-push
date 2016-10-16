#!/usr/bin/python
# -*- coding: utf-8 -*-

from etl import ETL

if __name__ == "__main__":
    etl = ETL()
    etl.check_new_arrive()
