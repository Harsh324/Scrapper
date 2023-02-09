import math
import scrapy
from scrap_Eleclerc.items import ScrapEleclercItem

class ScrapitSpider(scrapy.Spider):

    '''name of the spider bot'''
    name = 'scrapit'

    '''This is the global variable used to generate the product page url'''
    product_page_url = 'https://www.e.leclerc/'

    '''This is the list of url that we need to traverse'''
    start_urls = ['https://www.e.leclerc/cat/sport-loisirs', 'https://www.e.leclerc/cat/vetements']


    def parse(self, response):
        """
        # Function Description : 
            This callback Function will parse the urls listed in the start_urls list,
            this will in turn call a function to the subcategory page depending on the url.

        # Function Parameters : 
                # Self : 
                        The self parameter is a reference to the current instance of the class,
                        and is used to access variables that belongs to the class.

                # response:
                        Object for crawling the websites

        """

        '''Traversing the URL in the start_urls list'''
        for URL in self.start_urls:
            if(URL == 'https://www.e.leclerc/cat/sport-loisirs'):
                yield scrapy.Request(
                url = "https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=NAVIGATION&maxDepth=undefined",
                callback=self.parse_Sub,
            )
            else:
                yield scrapy.Request(
                    url = "https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_vetements?pageType=NAVIGATION&maxDepth=undefined",
                    callback=self.parse_Sub,
                )

    def parse_Sub(self, response):

        """
        # Function Description : 
            This callback function is being called by the parse function, the page contains the list of all products,
            in that page.

        # Function Parameters : 
                # Self : 
                        The self parameter is a reference to the current instance of the class,
                        and is used to access variables that belongs to the class.


                # response:
            
        """

        data = response.json()
        child = data['children']

        for Index in range(len(child)):
            code = child[Index]['code']
            category = child[Index]['label']
            total_prod = math.ceil(child[Index]['nbProducts'] // 90)

            for page in range(1, total_prod + 1):
                yield scrapy.Request(
                url = f"https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page={page}&categories=%7B%22code%22:%5B%22{code}%22%5D%7D",
                callback=self.parseProductPage,
                meta = {"category": category}
            )


    def parseProductPage(self, response):
        """
        # Function Description : 
            This callback function is being called by the parse function, the page contains the list of all products,
            in that page.

        # Function Parameters : 
                # Self : 
                        The self parameter is a reference to the current instance of the class,
                        and is used to access variables that belongs to the class.


                # response:
            
        """

        data = response.json()
        items = data['items']

        for Index in range(len(items)):
            sku = items[Index]['sku']
            yield scrapy.Request(
                url = f"https://www.e.leclerc/api/rest/live-api/product-details-by-sku/{sku}",
                callback=self.parseProduct,
                meta = {"category" : response.meta.get("category")}
            )
        


    def parseProduct(self, response):
        """
        # Function Description : 
            This callback function is being called by the parse function, the page contains the list of all products,
            in that page.

        # Function Parameters : 
                # Self : 
                        The self parameter is a reference to the current instance of the class,
                        and is used to access variables that belongs to the class.


                # response:
            
        """

        data = response.json()

        '''Item container imported from itme.py file'''
        item = ScrapEleclercItem()

        '''Name is stored here'''
        item['name'] = data['label']

        variant = data['variants']


        '''Brand name is stored here'''
        for Ind in range(len(data['attributeGroups'][0]['attributes'])):
            if('code' in data['attributeGroups'][0]['attributes'][Ind].keys() and data['attributeGroups'][0]['attributes'][Ind]['code'] == "marque"):
                item['brand'] = data['attributeGroups'][0]['attributes'][Ind]['value']['label']
                break

        
        '''original_price and sale_price calculation'''
        for Ind in range(len(variant)):
            if(len(variant[Ind]['offers']) > 0):
                item['original_price'] = variant[Ind]['offers'][0]['basePrice']['price']['price']
                item['sale_price'] = variant[Ind]['offers'][0]['basePrice']['totalPrice']['price']
                break


        item['image_url'] = ""
        '''Image stored here, more than one images are concatenated using ; identifier'''
        for Ind in range(len(variant[0]['attributes'])):
            if('code' in variant[0]['attributes'][Ind].keys() and variant[0]['attributes'][Ind]['code'] =='ean'):
                item['ean'] = variant[0]['attributes'][Ind]['value']

            elif('type' in variant[0]['attributes'][Ind].keys() and variant[0]['attributes'][Ind]['type'] == 'image'):
                if(item['image_url'] == ""):
                    item['image_url'] = variant[0]['attributes'][Ind]['value']['url']
                else:
                    item['image_url'] = item['image_url'] + ";" + variant[0]['attributes'][Ind]['value']['url']


        '''Product page url is calculated from here'''
        item['product_page_url'] = self.product_page_url + "/fp/" + data['slug'] + "-" + data['sku']
        

        '''Product category is added here'''
        item['product_category'] = response.meta.get("category")


        '''Addition of stock is done here'''
        for Ind1 in range(len(variant)):
            if(len(variant[Ind1]['offers']) > 0):
                for Ind in range(len(variant[Ind1]['offers'][0]['additionalFields'])):
                    if('code' in variant[Ind1]['offers'][0]['additionalFields'][Ind].keys()):
                        if(variant[Ind1]['offers'][0]['additionalFields'][Ind]['code'] == 'availability-status'):
                            if(variant[Ind1]['offers'][0]['additionalFields'][Ind]['value'] == 'in-stock'):
                                item['stock'] = True
                            else:
                                item['stock'] = False
                            break


        '''sku of the item is stored from here'''
        item['sku'] = data['sku']
        yield item