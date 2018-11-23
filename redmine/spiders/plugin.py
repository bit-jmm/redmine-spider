# -*- coding: utf-8 -*-
import scrapy

class PluginSpider(scrapy.Spider):
    name = 'plugin'
    start_urls = ['http://www.redmine.org/plugins?page=1/']
    f = open('plugins.csv', 'wb')
    def parse(self, response):
        plugin_count = response.css('div > h2::text').re(r'(\d+)')[0]
        print('plugin count:' + plugin_count)
        page_count= response.css('a.page::text').extract()[-1]
        print('page count: ' + page_count)
        for a in response.css('tr.plugin'):
            print('image src: ' + a.css('td.thumbnail > img::attr(src)').extract_first())
            print('plugin url: ' + a.css('td.description > p.name > a.plugin::attr(href)').extract_first())
        next_page_url = response.css('a.next::attr(href)').extract_first()
        print(next_page_url)
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)


