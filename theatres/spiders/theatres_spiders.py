import scrapy
from theatres.items import PlaceCover
from theatres.items import EventCover

from theatres.parseTransport import parseTransport
from theatres.getGPS import get_coordonates

class TheatreSpider(scrapy.Spider):
    name = 'theatre'

    start_urls = ['http://www.offi.fr/theatre']

    def parse(self, response):
        # follow links to threatres infos pages
        for href in response.css('#ListeTheatre a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_theater)

    #Theatre
    def parse_theater(self, response):
        events = []

        content = response.css('#content')
        #Parse telephone
        telephone = content.css('[itemprop=telephone]::text').extract_first()
        telephone = telephone.split(' ')[0]

        #GET position
        position = dict()
        address = dict()
        street = content.css('[itemprop=streetAddress]::text').extract_first()
        address['street'] = street
        address['postalCode'] = content.css('[itemprop=postalCode]::text').extract_first()
        address['city'] = content.css('[itemprop=addressLocality]::text').extract_first()
        position['address'] = address

        #GET GPS
        gps = dict()
        gps['lat'] = content.css('[itemprop=latitude]::attr(content)').extract_first()
        gps['lng'] = content.css('[itemprop=longitude]::attr(content)').extract_first()
        position['gps'] = gps

        for eventHREF in response.css('#tabs-prog .eventTitle a::attr(href)').extract():
            events.append(eventHREF)

        #GET IMAGES
        img = content.css(".imgFiche img").xpath("@src")
        imageURL = img.extract_first()

        #Yield data
        yield PlaceCover (
            name = content.css('h1 span::text').extract_first(),
            phone = telephone,
            website = content.css('[itemprop=url]::text').extract_first(),
            mtype = "theatre",
            position = position,
            description = content.css('[itemprop=description]::text').extract_first(),
            events = events,
            image_urls = [imageURL]
        )
