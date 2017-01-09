# -*- coding: utf-8 -*-
import json

import scrapy
from theatres.items import EventCover

from theatres.parseTransport import parseTransport

class ConcertEventsSpider(scrapy.Spider):
    name = 'concert_events'

    start_urls = ['http://www.offi.fr/']

    #placeName = None

    def parse(self, response):
        data_file = open('concerts.json')
        theatres = json.load(data_file)
        data_file.close()

        for t in theatres:
            placeName = t['name']

            for e in t['events']:
                request = scrapy.Request(response.urljoin(e), callback=self.parse_event)
                request.meta['item'] = placeName
                yield request

    def parse_event(self, response):
        placeName = response.meta['item']

        name = response.css('h1::text').extract_first()

        performers = ""
        for value in response.css('[itemprop=performers] [itemprop=name]::text').extract_first():
            performers += " " + value

        description = performers

        #description = response.css('.detail li:nth-child(4)::text').extract_first()

        #Details
        details = response.css('.detail')
        dateStart = ""
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
