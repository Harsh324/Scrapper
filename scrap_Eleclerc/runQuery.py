import pymongo

class Database:

    def __init__(self) -> None:
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        db = self.conn['scrap']
        self.collection = db['scrap_db4']

    def runQuery(self, query):
        return self.collection.find(query)

    def countTotal(self):
        return self.collection.count_documents({})


if __name__ == '__main__':

    Db = Database()

    # How many products did you scrape?
    print(Db.countTotal())
    # 2. How many products have a discount on them?
    query = {"original_price": {"＄ne" : "sale_price"}}
    print(Db.runQuery(query).count())
    # 3. How many unique `brands` are present in the collection?
    # 4. What is the count of products for each `brand`?
    # 5. What is the count of discounted products for each `brand`?
    # 6. What is count of distinct `product_url` based on category `vetement-homme`?
    # 7. How many products have `ean` in them?
    # 8. How many products have `sale_price` greater than `original_price`?
    # 9. How many products have `sale_price` greater than 300?
    # 10. How many products have discount % greater than 30%?
    # 11. How many products have a 50% discount?
    # 12. Which `brand` in each section is selling the most number of products?

