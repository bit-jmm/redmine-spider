# -*- coding: utf-8 -*-

import scrapy

class Plugin:
    def __init__(self):
        self.name = '-'
        self.img_src = '-'
        self.url = '-'
        self.author = '-'
        self.website = '-'
        self.repo = '-'
        self.register_date = '-'
        self.cur_version = '-'
        self.compatiable_version = '-'
        self.rating = '-'
        self.rating_count = '-'
        self.wiki = '-'


    def __str__(self):
        return '|'.join([self.name, self.img_src, self.url, self.author, self.website,
                 self.repo, self.register_date, self.cur_version, self.compatiable_version,
                 self.rating, self.rating_count, self.wiki])
