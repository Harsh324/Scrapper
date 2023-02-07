import scrapy
from scrap_Eleclerc.items import ScrapEleclercItem

class ScrapitSpider(scrapy.Spider):
    name = 'scrapit'
    product_page_url = ''
    product_category = ''
    headers = {

    }

    start_urls = ['https://www.e.leclerc/cat/sport-loisirs']

    def parse(self, response):
        yield scrapy.Request(
            url="https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=NAVIGATION&maxDepth=undefined",
            callback=self.parse_Sub,
            headers=self.headers
        )

    def parse_Sub(self, response):
        data = response.json() # Newer version of Scrapy come with shortcut to get JSON data
        
        #print("Size = ", len(data['children']))
        for Index in range(len(data['children'])):
            code = data['children'][Index]['code']
            self.product_category = code
            self.product_category = self.product_category.replace("NAVIGATION_", "")
            #print("Type of children dict is ", data['children'][Index].keys())
        
            # print("Id = ", data['children'][Index]['id'])
            print("Code = ", data['children'][Index]['code'])
            # print("Slug = ", data['children'][Index]['slug'])
            # print("Label = ", data['children'][Index]['label'])
            # print("Description = ", data['children'][Index]['description'])
            # print("attribute = ", data['children'][Index]['attributes'])
            # print("breadcrumb = ", data['children'][Index]['breadcrumb'])
            # print("nbproducts = ", data['children'][Index]['nbProducts'])
            # print("Type = ",type(data))
            # print(data.keys())

            headers = {

            }


            yield scrapy.Request(
                #url = f"https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_materiel-de-randonnee?pageType=NAVIGATION&maxDepth=undefined",
                url = f"https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/{code}?pageType=NAVIGATION&maxDepth=undefined",
                callback=self.parse_Sub_Sub,
                headers=self.headers
            )
        # for i,school in enumerate(data):
        #     school_code = school["itSchoolCode"]
        #     yield scrapy.Request(
        #         f"https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}",
        #         callback=self.parse_school,
        #         headers=self.headers,
        #         dont_filter=True # Many schools have the same code, same page, but listed more than once
        #     )

    def parse_Sub_Sub(self, response):
        data = response.json()
        print("*****************************************************************************************")
        print("*****************************************************************************************")

        headers = {

        }
        # print(data)
        if('children' in data.keys()):
            for Index in range(len(data['children'])):
                code = data['children'][Index]['code']
                # print("Type of children dict is ", data['children'][Index].keys())
                # print("Id = ", data['children'][Index]['id'])
                print("Code = ", data['children'][Index]['code'])
                # print("Slug = ", data['children'][Index]['slug'])
                # print("Label = ", data['children'][Index]['label'])
                # print("Description = ", data['children'][Index]['description'])
                # print("attribute = ", data['children'][Index]['attributes'])
                # print("breadcrumb = ", data['children'][Index]['breadcrumb'])
                # print("nbproducts = ", data['children'][Index]['nbProducts'])
                # print("Type = ",type(data))
                # print(data.keys())
                yield scrapy.Request(
                    
                    url = f"https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=1&categories=%7B%22code%22:%5B%22{code}%22%5D%7D",
                    callback=self.parseProductPage,
                    headers = self.headers
                )
        else:
            #print("Here trying to put some conditions")
            string = "NAVIGATION_" + self.product_category
            #print("Trying the url , ", f"https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=1&categories=%7B%22code%22:%5B%22" + "NAVIGATION_" + {self.product_category} + "%22%5D%7D")
            yield scrapy.Request(
                url = f"https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=1&categories=%7B%22code%22:%5B%22{string}%22%5D%7D",
                callback = self.parseProductPage,
                headers = self.headers

            )

    def parseProductPage(self, response):
        data = response.json()

        print("#############################################################################################")
        print("#############################################################################################")
        # print(data.keys())
        for Index in range(len(data['items'])):
            
            # print(data['items'][Index].keys())
            # print("slug = ", data['items'][Index]['slug'])
            print("sku = ", data['items'][Index]['sku'])
            sku = data['items'][Index]['sku']
            headers = {

            }
            # "https://www.e.leclerc/api/rest/live-api/product-details-by-sku/3700092677155"
            self.product_page_url = f"https://www.e.leclerc/api/rest/live-api/product-details-by-sku/{sku}"
            yield scrapy.Request(
                url = f"https://www.e.leclerc/api/rest/live-api/product-details-by-sku/{sku}",
                callback=self.parseProduct,
                headers = self.headers
            )
        


    def parseProduct(self, response):
        data = response.json()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(data.keys())
        # print(data['categories'])
        # print(data['slug'])
        # print(data['attributeGroups'][0]['attributes'][5])
        # Name =  dict_keys(['id', 'sku', 'label', 'slug', 'attributes', 'offers'])

        print("Name = ", data['label'])
        
        print("Brand = ", data['attributeGroups'][0]['attributes'][5]['value']['label'])
        print("Original_price = ", data['variants'][0]['offers'][0]['basePrice']['price']['price'])
        print("Sale_price = ", data['variants'][0]['offers'][0]['basePrice']['totalPrice']['price'])
        print("Image_url = ", data['variants'][0]['attributes'][1]['value']['url'])
        print("Product_page_url = ", self.product_page_url)
        print("Product_cateogry = ", self.product_category)
        print("Stock = ",data['variants'][0]['offers'][0]['stock'])
        print("sku = ", data['sku'])
        print("Ean = ", data['variants'][0]['attributes'][3]['value'])

        

        print(data['variants'][0].keys())
        print(data['variants'][0]['attributes'][3].keys())
        #print(data['variants'][0]['attributes'][3]['value'])
        print(data['variants'][0]['offers'][0].keys())

        print(data['variants'][0]['offers'][0]['basePrice'])


        #item = ScrapEleclercItem()





# import scrapy

# class AllSpider(scrapy.Spider):
#     name = "all"
#     start_urls = ["https://directory.ntschools.net/#/schools"]
#     headers = {
#         "Accept": "application/json",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,lb;q=0.7",
#         "Referer": "https://directory.ntschools.net/",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
#         "X-Requested-With": "Fetch",
#     }

#     def parse(self, response):
#         yield scrapy.Request(
#             url="https://directory.ntschools.net/api/System/GetAllSchools",
#             callback=self.parse_json,
#             headers=self.headers
#         )

#     def parse_json(self, response):
#         data = response.json() # Newer version of Scrapy come with shortcut to get JSON data

#         for i,school in enumerate(data):
#             school_code = school["itSchoolCode"]
#             yield scrapy.Request(
#                 f"https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}",
#                 callback=self.parse_school,
#                 headers=self.headers,
#                 dont_filter=True # Many schools have the same code, same page, but listed more than once
#             )

#     def parse_school(self, response):
#         data = response.json() # Newer version of Scrapy come with shortcut to get JSON data
#         yield {
#             "name": data["name"],
#             "telephoneNumber": data["telephoneNumber"],
#             "mail": data["mail"],
#             "physicalAddress": data["physicalAddress"]["displayAddress"],
#             "postalAddress": data["postalAddress"]["displayAddress"],
#         }
