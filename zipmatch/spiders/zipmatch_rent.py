# -*- coding: utf-8 -*-
import re
import json

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor


class ZipmatchRentSpider(Spider):
    name = 'zipmatch_rent'
    allowed_domains = ['zipmatch.com']
    # NOTE: limit in the url query could be changed to display everything in one page
    # For demo purposes, we used the default limit (45) to simulate pagination
    # This scraper will get all condo for rent listings located at Metro Manila
    listing_url = 'https://www.zipmatch.com/rent/condominium/metro-manila?p={}&limit=45&v=u&bedrooms=0&bathrooms=1'
    
    def start_requests(self):
        page_number = 1
        yield Request(self.listing_url.format(page_number),
                      meta={'page_number': page_number})

    def parse(self, response):
        links = LinkExtractor(allow='/listings').extract_links(response)
        for link in links:  # crawl each listing
            yield response.follow(link, callback=self.handle_unit_response)
        
        page_number = response.meta.get('page_number')     
        if links:  # if list is not empty, go to next page
            yield Request(self.listing_url.format(page_number + 1),
                          meta={'page_number': page_number + 1})

    def handle_unit_response(self, response):
        def parse_unit_details(response):
            unit_details = {}
            unit_details_div = response.xpath(
                '//div[h3[text()="Unit Details"]]/following-sibling::div')

            tables = unit_details_div.xpath('.//table')            
            for table in tables:
                keys = [x.strip() for x in table.xpath('.//th/text()[1]').getall()]
                values = [x.strip() for x in table.xpath('.//td/text()[1]').getall()]
                unit_details.update(dict(zip(keys, values)))

            return unit_details
                
        title = response.xpath('.//h1[@class="title"]/text()').get().strip()
        image_links = response.xpath('.//div[@class="fotorama"]/img/@src').getall()
        description = response.xpath('//p[@itemprop="description"]/text()').getall()
        description = '|'.join([x.strip() for x in description])
        address = ', '.join(response.xpath(
            '//div[@itemprop="address"]/span/text()').getall())
        latitude = response.xpath('.//meta[@itemprop="latitude"]/@content').get()
        longitude = response.xpath('.//meta[@itemprop="latitude"]/@content').get()
        
        yield {
            'title': title,
            'description': description,
            'link': response.url,
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'image_links': image_links,
            **parse_unit_details(response)
        }
