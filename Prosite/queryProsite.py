import scrapy

class prositeSpider(scrapy.Spider):
   name = 'prosite-spider'
   prosite_url = 'prosite.expasy.org'
   start_urls = [prosite_url]

   def parse(self, response):
       data = {
           'SEARCH': pc #put prosite code
       }
       yield scrapy.FormRequest(url=self.prosite_url, formdata=data, callback=self.parse_results)
   def parse_data(self, response): 

            

