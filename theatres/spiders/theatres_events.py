# -*- coding: utf-8 -*-
import json

import scrapy
from theatres.items import EventCover

from theatres.parseTransport import parseTransport

class TheatreEventsSpider(scrapy.Spider):
    name = 'theatre_events'

    start_urls = ['http://www.offi.fr/']

    #placeName = None

    def parse(self, response):
        #events = []

        data_file = open('theatres.json')
        theatres = json.load(data_file)
        data_file.close()

        for t in theatres:
            placeName = t['name']

            for e in t['events']:
                #yield scrapy.Request(response.urljoin(e), callback=self.parse_event)
                request = scrapy.Request(response.urljoin(e), callback=self.parse_event)
                request.meta['item']  = placeName
                yield request

    #for href in response.css('#ListeTheatre a::attr(href)').extract():
    #    yield scrapy.Request(response.urljoin(href), callback=self.parse_theater)

    #def parse_theater(self, response):
    #    self.placeName = response.css('h1 span::text').extract_first()
    #    for eventHREF in response.css('#tabs-prog .eventTitle a::attr(href)').extract():
    #        yield scrapy.Request(response.urljoin(eventHREF), callback=self.parse_event)

    def parse_event(self, response):
        placeName = response.meta['item']

        name = response.css('h1::text').extract_first()
        description = response.css('[itemprop=description]::text').extract_first()

        #Details
        details = response.css('.detail')
        startDate = details.css('[itemprop=startDate]')
        dateStart = startDate.css('meta::attr(content)').extract_first()

        endDate = details.css('[itemprop=endDate]')

        if (endDate != None):
            dateEnd = endDate.css('meta::attr(content)').extract_first()
        else:
            dateEnd = ""

        img = response.css(".imgFiche img").xpath("@src")
        imageURL = img.extract_first()

        #Yield data
        yield EventCover (
            placeName = placeName,
            name = name,
            description = description,
            dateStart = dateStart,
            dateEnd = dateEnd,
            image_urls = [imageURL]
        )
