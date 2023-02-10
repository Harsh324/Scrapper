import pymongo

class Database:

    def __init__(self) -> None:
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        db = self.conn['harshTripathi']
        self.collection = db['leclerc_fr1']

    def runQuery(self):
        return self.collection

    def countTotal(self):
        return self.collection.count_documents({})


def Query1(Db):
    # How many products did you scrape?
    print(Db.count_documents({}))
def Query2(Db):
    # How many products have a discount on them?
    pass

def Query3(Db):
    # 3. How many unique `brands` are present in the collection?
    pass

def Query4(Db):
    # 4. What is the count of products for each `brand`?
    Res = Db.runQuery().aggregate([
        {
            "$group": {
                "_id": "$brand",
                "count": {
                    "$sum": 1
                }
            }
        }
    ])
    


def Query5(Db):
    Db.count()
    # 5. What is the count of discounted products for each `brand`?
    pass


def Query6(Db):
    # 6. What is count of distinct `product_url` based on category `vetement-homme`?
    pass



def Query7(Db):
    # 7. How many products have `ean` in them?
    pass



def Query8(Db):
    # 8. How many products have `sale_price` greater than `original_price`?
    pass



def Query9(Db):
    # 9. How many products have `sale_price` greater than 300?
    pass


def Query10(Db):
    # 10. How many products have discount % greater than 30%?
    pass


def Query11(Db):
    # 11. How many products have a 50% discount?
    pass


def Query12(Db):
    # 12. Which `brand` in each section is selling the most number of products?
    from pymongo import MongoClient



    result = Db.aggregate([
    {
        "$group": {
            "_id": {
                "product_category": "$product_category",
                "brand": "$brand"
            },
            "count": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "count": -1
        }
    },
    {
        "$group": {
            "_id": "$_id.product_category",
            "brand": {
                "$first": "$_id.brand"
            },
            "count": {
                "$first": "$count"
            }
        }
    }
    ])
    for doc in result:
        print("Product category: " + str(doc["_id"]) + ", Brand: " + str(doc["brand"]) + ", Count: " + str(doc["count"]))


if __name__ == '__main__':

    Db = Database()

    
    print(Db.runQuery().count_documents({}))
    Query1(Db.runQuery())
    # 2. How many products have a discount on them?

    #print(Db.runQuery().count())
    # 3. How many unique `brands` are present in the collection?
    #print(Db.runQuery().distinct('brand').count())
    # 4. What is the count of products for each `brand`?
    # Res = Db.runQuery().aggregate([
    #     {
    #         "$group": {
    #             "_id": "$brand",
    #             "count": {
    #                 "$sum": 1
    #             }
    #         }
    #     }
    # ])

    # for doc in Res:
    #     print("Brand: " + str(doc["_id"]) + ", Count: " + str(doc["count"]))
  
    # 5. What is the count of discounted products for each `brand`?
    # 6. What is count of distinct `product_url` based on category `vetement-homme`?
    # 7. How many products have `ean` in them?
    # 8. How many products have `sale_price` greater than `original_price`?
    # 9. How many products have `sale_price` greater than 300?
    # 10. How many products have discount % greater than 30%?
    # 11. How many products have a 50% discount?
    # 12. Which `brand` in each section is selling the most number of products?
    Query12(Db.runQuery())

