import pprint
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
    print("Totall number of products:", Db.count_documents({}))



def Query2(Db):
    # How many products have a discount on them?
    discounted_count = Db.count_documents({"sale_price": {"$lt": "original_price"}})

    print("Number of discounted products: ", discounted_count)
    

def Query3(Db):
    # 3. How many unique `brands` are present in the collection?
    
    unique = len(Db.distinct("brand"))

    print("Total Unique brands:" + str(unique))


def Query4(Db):
    # 4. What is the count of products for each `brand`?
    Count = Db.aggregate
    ([
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    pprint.pprint(list(Count))
    


def Query5(Db):
    # 5. What is the count of discounted products for each `brand`?
    pipeline = [
    {
        "$match": {
            "sale_price": { "$lt": "$original_price" }
        }
    },
    {
        "$group": {
            "_id": "$brand",
            "discounted_products_count": { "$sum": 1 }
        }
    }
    ]

    discounted_products_count_by_brand = list(Db.aggregate(pipeline))

# Print the result
    for brand in discounted_products_count_by_brand:
        print(f"Brand: {brand['_id']}, Discounted Products Count: {brand['discounted_products_count']}")




def Query6(Db):
    # 6. What is count of distinct `product_url` based on category `vetement-homme`?
    result = Db.aggregate([
        {
            "$match": {"product_category": "Vêtements Homme"}
        },
        {
            "$group": {
                "_id": "$product_page_url",
                "count": { "$sum": 1 }
            }
        },
        {
            "$group": {
                "_id": None,
                "total": { "$sum": 1 }
            }
        }
    ])

    # Get the count from the result
    count = list(result)[0]["total"]

# Print the count
    print("The number of distinct product_page_url in the vetement-homme category is:", count)



def Query7(Db):
    # 7. How many products have `ean` in them?
    ean_products = Db.count_documents({"ean": {"$exists": True, "$ne": None}})

    print("Products with EAN: " + str(ean_products))
    



def Query8(Db):
    # 8. How many products have `sale_price` greater than `original_price`?
    count = Db.count_documents({"$expr": {"$gt": ["$sale_price", "$original_price"]}})

    print("Number of products with sale_price greater than original_price:", count)




def Query9(Db):
    # 9. How many products have `sale_price` greater than 300?
    product_count = Db.count_documents({"sale_price": {"$gt": 300}})

    print("Product count: " + str(product_count))
    


def Query10(Db):
    # 10. How many products have discount % greater than 30%?
    pass


def Query11(Db):
    # 11. How many products have a 50% discount?
    discounted_products = Db.count_documents({"sale_price": {"$lt": {"$multiply": ["$original_price", 0.5]}}})

    print("Number of products with a 50% discount:", discounted_products)
    
    


def Query12(Db):
    # 12. Which `brand` in each section is selling the most number of products?
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

    Query1(Db.runQuery())
    Query2(Db.runQuery())
    Query3(Db.runQuery())
    Query4(Db.runQuery())
    Query5(Db.runQuery())
    Query6(Db.runQuery())
    Query7(Db.runQuery())
    Query8(Db.runQuery())
    Query9(Db.runQuery())
    Query10(Db.runQuery())
    Query11(Db.runQuery())
    Query12(Db.runQuery())

