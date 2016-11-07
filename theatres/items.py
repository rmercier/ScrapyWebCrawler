# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TheatreCover(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    images = scrapy.Field()


class MuseumCover(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    mtype = scrapy.Field()
    position = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
