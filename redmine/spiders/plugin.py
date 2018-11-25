# -*- coding: utf-8 -*-
import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf8')
import scrapy
from redmine.items import Plugin

class PluginSpider(scrapy.Spider):
    name = 'plugin'
    start_urls = ['http://www.redmine.org/plugins?page=1/']
    home_url = 'http://www.redmine.org'
    plugins = []
    f = open('plugins.txt', 'wb')

    def parse_plugin(self, response):
        p = Plugin()
        try:
            p.name = (' ').join(response.css('div#content > h2::text').extract_first().split(' ')[2:]).strip()
        except Exception, e:
            print '\nname error:'
            print e
        try:
            p.img_src = self.home_url + response.css('td > img.plugin_thumbnail::attr(src)').extract_first()
        except Exception, e:
            print '\nno image:'
            print e
        p.url = response.url
        try:
            p.author = response.css('a.user::text').extract_first().strip()
        except Exception, e:
            print '\nauthor error:'
            print e
        try:
            p.website = response.css('td > a::text')[1].extract().strip()
        except Exception, e:
            print '\nno website:'
            print e
        try:
            p.repo = response.css('td > a::text')[2].extract().strip()
        except Exception, e:
            print '\nno repo site:'
            print e
        try:
            p.register_date = response.css('tr > td::text')[2].extract().strip()
        except Exception, e:
            print '\nregister date error:'
            print e
        try:
            p.cur_version = response.css('tr > td::text')[3].extract().strip()
        except Exception, e:
            print '\ncurrent version error:'
            print e
        try:
            p.compatiable_version = response.css('tr > td::text')[4].extract().strip()
        except Exception, e:
            print '\ncompatiable version error:'
            print e
        try:
            p.rating = response.css('tr > td > span.rating-count > span::attr(title)').extract_first().strip()
            if not p.rating:
                p.rating = '-'
        except Exception, e:
            print '\nrating error:'
            print e
        try:
            p.rating_count = response.css('tr > td > span.rating-count > a::text').re('(\w+)')[0]
            if not p.rating_count:
                p.rating_count = '-'
        except Exception, e:
            try:
                p.rating_count = response.css('tr > td > span.rating-count::text').re('(\w+)')[0]
                if not p.rating_count:
                    p.rating_count = '-'
            except Exception, e1:
                print '\nno rating count'
                print e1
        try:
            p.wiki = '.'.join([st.replace('\n','.') for st in response.css('div.wiki::text').extract() if len(st.strip()) > 0])
            if not p.wiki:
                p.wiki = '-'
        except Exception, e:
            print '\nwiki:'
            print e
        self.f.write(str(p)+'\n')

    def parse(self, response):
        #plugin_count = response.css('div > h2::text').re(r'(\d+)')[0]
        #print('plugin count:' + plugin_count)
        #page_count= response.css('a.page::text').extract()[-1]
        #print('page count: ' + page_count)
        for a in response.css('tr.plugin'):
            plugin_url = a.css('td.description > p.name > a.plugin::attr(href)').extract_first()
            yield response.follow(plugin_url, callback=self.parse_plugin)
            #print('image src: ' + a.css('td.thumbnail > img::attr(src)').extract_first())
        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def __del__(self):
        self.f.close()
