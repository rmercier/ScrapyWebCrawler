import scrapy
from theatres.items import PlaceCover
from theatres.items import EventCover

from theatres.parseTransport import parseTransport

class ConcertSpider(scrapy.Spider):
    name = 'concert'

    start_urls = ['http://www.offi.fr/concerts/salles-de-concert-paris.html']

    def parse(self, response):
        # follow links to threatres infos pages
        for href in response.css('#content table tr td:first-of-type a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_concert)

    #Theatre
    def parse_concert(self, response):
        events = []

        content = response.css('#content .detailSummary_full')
        #Parse telephone
        telephone = content.css('[itemprop=telephone]::text').extract_first()
        if telephone == None:
            telephone = ""
        else:
            telephone = telephone.split(' ')[0]

        #GET position
        position = dict()
        address = dict()
        address['street'] = content.css('[itemprop=streetAddress]::text').extract_first()
        address['postalCode'] = content.css('[itemprop=postalCode]::text').extract_first()
        address['city'] = content.css('[itemprop=addressLocality]::text').extract_first()
        position['address'] = address

        #GET GPS
        gps = dict()
        gps['lat'] = content.css('[itemprop=latitude]::attr(content)').extract_first()
        gps['lng'] = content.css('[itemprop=longitude]::attr(content)').extract_first()
        position['gps'] = gps

        for eventHREF in response.css('.tabsLieu-concerts .eventTitle a::attr(href)').extract():
            events.append(eventHREF)

        #GET IMAGES
        img = content.css(".imgFiche img").xpath("@src")
        imageURL = img.extract_first()

        #Yield data
        yield PlaceCover (
            name = content.css('h1 span::text').extract_first(),
            phone = telephone,
            website = content.css('[itemprop=url]::text').extract_first(),
            mtype = "concert",
            position = position,
            description = content.css('[itemprop=description] p::text').extract_first(),
            events = events,
            image_urls = [imageURL]
        )
