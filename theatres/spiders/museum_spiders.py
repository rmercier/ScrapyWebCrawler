import scrapy
from theatres.items import MuseumCover


class MuseumSpider(scrapy.Spider):
    name = 'museum'

    start_urls = ['http://www.offi.fr/expositions-musees/']

    def parse(self, response):
        # follow links to threatres infos pages
        for href in response.css('#ListeMusee a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_museum)

    #Theatre
    def parse_museum(self, response):



        content = response.css('#content')

        #Parse telephone
        telephone = content.css('[itemprop=telephone]::text').extract_first()
        telephone = telephone.split(' ')[0]


        position = dict()
        address = dict()
        address['street'] = content.css('[itemprop=streetAddress]::text').extract_first()
        address['postalCode'] = content.css('[itemprop=postalCode]::text').extract_first()
        address['city'] = content.css('[itemprop=addressLocality]::text').extract_first()

        latitude = content.css('[itemprop=latitude]')
        longitude = content.css('[itemprop=longitude]')

        latitude = latitude.css('meta::attr(content)').extract_first()
        longitude = longitude.css('meta::attr(content)').extract_first()


        gps = {'lat': latitude, 'lng': longitude}
        position['address'] = address
        position['gps'] = gps


        #Museum data
        website = content.css('[itemprop=url]')

        img = content.css(".imgFiche img").xpath("@src")
        imageURL = img.extract_first()


        yield MuseumCover(
        	name = content.css('[itemprop=name]::text').extract_first(),
        	phone = telephone,
            website = website.css('a::attr(href)').extract_first(),
            mtype = "museum",
            position = position,
            description = content.css('[itemprop=description]::text').extract_first(),
        	image_urls=[imageURL]
            )
