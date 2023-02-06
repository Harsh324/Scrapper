import scrapy


class ScrapitSpider(scrapy.Spider):
    name = 'scrapit'

    headers = {

    }

    start_urls = ['https://www.e.leclerc/cat/sport-loisirs']
    "https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=2&categories=%7B%22code%22:%5B%22NAVIGATION_bon-plan-velo%22%5D%7D"

    def parse(self, response):
        yield scrapy.Request(
            url="https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=NAVIGATION&maxDepth=undefined",
            callback=self.parse_Sub,
            headers=self.headers
        )

    def parse_Sub(self, response):
        data = response.json() # Newer version of Scrapy come with shortcut to get JSON data
        code = data['children'][0]['code']
        print("Type of children dict is ", data['children'][0].keys())
        print("Id = ", data['children'][0]['id'])
        print("Code = ", data['children'][0]['code'])
        print("Slug = ", data['children'][0]['slug'])
        print("Label = ", data['children'][0]['label'])
        print("Description = ", data['children'][0]['description'])
        print("attribute = ", data['children'][0]['attributes'])
        print("breadcrumb = ", data['children'][0]['breadcrumb'])
        print("nbproducts = ", data['children'][0]['nbProducts'])
        print("Type = ",type(data))
        print(data.keys())

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
        print("************************")
        print("************************")
        print("************************")

        headers = {

        }
        # print(data)
        if('children' in data.keys()):
            print("Type of children dict is ", data['children'][0].keys())
            print("Id = ", data['children'][0]['id'])
            print("Code = ", data['children'][0]['code'])
            print("Slug = ", data['children'][0]['slug'])
            print("Label = ", data['children'][0]['label'])
            print("Description = ", data['children'][0]['description'])
            print("attribute = ", data['children'][0]['attributes'])
            print("breadcrumb = ", data['children'][0]['breadcrumb'])
            print("nbproducts = ", data['children'][0]['nbProducts'])
            print("Type = ",type(data))
            print(data.keys())
            yield scrapy.Request(
                url = f"https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=1&categories=%7B%22code%22:%5B%22NAVIGATION_bon-plan-velo%22%5D%7D",
                callback=self.parseProductPage,
                headers = self.headers
            )
        else:
            print("Here trying to put some conditions")

    def parseProductPage(self, response):
        data = response.json()

        print("#################")
        print("#################")
        print("#################")

        print(data.keys())
        print(data['items'][0].keys())


    def parseProduct(self, response):
        data = response.json





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
