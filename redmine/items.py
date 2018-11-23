# -*- coding: utf-8 -*-

import scrapy

class Plugin:
    name = ''
    img_src = ''
    url = ''
    author = ''
    website = ''
    repo = ''
    register_date = ''
    cur_version = ''
    compatiable_version = ''
    rating = ''
    rating_count = ''


    def __str__(self):
        return '|'.join([self.name, self.img_src, self.url, self.author, self.website,
                 self.repo, self.register_date, self.cur_version, self.compatiable_version,
                 self.rating, self.rating_count])
