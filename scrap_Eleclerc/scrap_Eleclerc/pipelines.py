# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class ScrapEleclercPipeline:

    def __init__(self) -> None:
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        '''Database name'''
        db = self.conn['harshTripathi']

        '''collections name'''
        self.collection = db['leclerc_fr']

    def process_item(self, item, spider):
        '''item container is inserted to the mongodb database'''
        self.collection.insert_one(dict(item))
        return item
