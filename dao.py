#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient, IndexModel

class DAO:

    def __init__(self, *args, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        if len(kwargs) == 0:
            self.default_init()
        else:
            self.client = MongoClient(kwargs.get('host'), kwargs.get('port'))
            self.db = self.client[kwargs.get('db')]

    def default_init(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['dark']
        self.db['actress'].create_index('id', unique=True)
        works_index_no = IndexModel("no", unique=True)
        works_index_angels = IndexModel("angels")
        self.db['works'].create_indexes([works_index_no, works_index_angels])

    def find_actress_by_id(self, id):
        collection = self.db['actress']
        return collection.find_one({"id": id})

    def insert_actress(self, actress):
        collection = self.db['actress']
        return collection.insert_one(actress)

    def find_works_by_no(self, no):
        collection = self.db['works']
        return collection.find_one({"no": no})

    def insert_works(self, works):
        collection = self.db['works']
        return collection.insert_one(works)
