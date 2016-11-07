import scrapy
from theatres.items import TheatreCover
from theatres.parseTransport import parseTransport
from theatres.getGPS import get_coordonates


class TheatreSpider(scrapy.Spider):
    name = 'theatre'

    start_urls = ['http://www.offi.fr/theatre']

    def parse(self, response):
        # follow links to threatres infos pages
        for href in response.css('#ListeTheatre a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_theater)

    #Theatre
    def parse_theater(self, response):

        events = []

        #Get events
        for eventData in response.css('#tabs-prog .oneRes'):
            event = dict()
            event['name'] = eventData.css('[itemprop=name]::text').extract_first()
            event['description'] = eventData.css('[itemprop=description]::text').extract_first()

            #Details
            details = eventData.css('.detail ')
            startDate = details.css('[itemprop=startDate]')
            endDate = details.css('[itemprop=endDate]')

            event['dateStart'] = startDate.css('meta::attr(content)').extract_first()
            event['dateEnd'] = startDate.css('meta::attr(content)').extract_first()
            events.append(event)


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
        position['gps'] = get_coordonates(street)

        #Yield data
        yield {
            'name': content.css('[itemprop=name]::text').extract_first(),
            'phone': telephone,
            'website': content.css('[itemprop=url]::text').extract_first(),
            'type': "theatre",
            'position': position,
            'description': content.css('[itemprop=description]::text').extract_first(),
            'events': events
        }
