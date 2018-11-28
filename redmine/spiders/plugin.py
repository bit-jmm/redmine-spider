# -*- coding: utf-8 -*-
import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf8')
import scrapy
import codecs
import traceback
from redmine.items import Plugin

class PluginSpider(scrapy.Spider):
    name = 'plugin'
    start_urls = ['http://www.redmine.org/plugins?page=1/']
    home_url = 'http://www.redmine.org'
    plugins = []
    f = codecs.open('plugins.txt','w','utf-8')

    def parse_plugin(self, response):
        p = Plugin()
        try:
            p.name = (' ').join(response.css('div#content > h2::text').extract_first().split(' ')[2:]).strip()
        except:
            print('\nname error:')
        try:
            p.img_src = self.home_url + response.css('td > img.plugin_thumbnail::attr(src)').extract_first()
        except:
            print('\nno image:')
        p.url = response.url
        j = 0
        try:
            p.author = response.xpath("//table//tr[1]/td[2]/a/text()").extract_first().strip()
        except:
            #traceback.print_exc()
            print('\nno author:')
        try:
            p.website = response.xpath('//table//tr[2]/td[1]/a/text()').extract_first().strip()
        except:
            print('\nno website:')
        try:
            p.repo = response.xpath('//table//tr[3]/td[1]/a/text()').extract_first().strip()
        except:
            print('\nno repo site:')
        try:
            p.register_date = response.xpath('//table//tr[4]/td[1]/text()').extract_first().strip()
        except:
            print('\nregister date error:')
        try:
            p.cur_version = response.xpath('//table//tr[5]/td[1]/text()').extract_first().strip()
        except:
            print('\ncurrent version error:')
        try:
            p.compatiable_version = response.xpath('//table//tr[6]/td[1]/text()').extract_first().strip()
        except:
            print('\ncompatiable version error:')
        try:
            p.rating = response.css('tr > td > span.rating-count > span::attr(title)').extract_first().strip()
            if not p.rating:
                p.rating = '-'
        except:
            print('\nrating error:')
        try:
            p.rating_count = response.css('tr > td > span.rating-count > a::text').re('(\w+)')[0]
            if not p.rating_count:
                p.rating_count = '-'
        except:
            try:
                p.rating_count = response.css('tr > td > span.rating-count::text').re('(\w+)')[0]
                if not p.rating_count:
                    p.rating_count = '-'
            except:
                print('\nno rating count')
        try:
            p.wiki = '.'.join([st.replace('\n','.') for st in response.xpath("//div[@class='wiki']//text()").extract() if len(st.strip()) > 0])
            if not p.wiki:
                p.wiki = '-'
        except:
            print('\nwiki:')
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
