# -*- coding: utf-8 -*-
import os
import csv
import sqlite3
from collections import OrderedDict

class DictCsv(object):

    def __init__(self, filename, codec = 'utf-8'):
        self._filename = filename
        self._codec = codec
        self._heads = []
        self._content = {}
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self._filename):
            return False
        with open(self._filename, 'r', encoding=self._codec) as fp:
            reader = csv.reader(fp)
            count = 0
            for row in reader:
                if count == 0:
                    self._heads = row
                else:
                    word = row[0].lower()
                    self._content[word] = row
                count += 1
        return True

    def query(self, word):
        if not self._heads:
            return None
        word = word.lower()
        if word not in self._content:
            return None
        row = self._content[word]
        obj = OrderedDict()
        for i in range(len(self._heads)):
            obj[self._heads[i]] = row[i]
        return obj

class StarDict(object):

    def __init__(self, filename):
        self._filename = filename
        self._conn = None
        if filename:
            self._conn = sqlite3.connect(filename)

    def query(self, word):
        if not self._conn:
            return None
        c = self._conn.cursor()
        word = word.lower()
        c.execute('select * from stardict where word = ?', (word,))
        record = c.fetchone()
        if record is None:
            return None
        obj = OrderedDict()
        fields = ['word', 'sw', 'phonetic', 'definition', 'translation', 
                 'pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 'exchange', 
                 'detail', 'audio']
        for i in range(len(fields)):
            obj[fields[i]] = record[i]
        return obj

    def close(self):
        if self._conn:
            self._conn.close()