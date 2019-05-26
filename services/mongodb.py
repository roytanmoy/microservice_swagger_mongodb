from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class MongoFactory(object):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create(self) -> MongoClient:
        return MongoClient(
            host=self.host,
            port=self.port
        )


class MongoCollection(object):

    def __init__(self, mongo_factory: MongoFactory, recipe: str, db_name: str):
        self.mongo_factory = mongo_factory
        self.recipe_collection = recipe
        self.db_name = db_name
        self.instance = None


    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.mongo_factory.create()
            self.instance[self.db_name][self.recipe_collection].create_index('id', unique=True)

        return self.instance[self.db_name]


    def create_one(self, obj: dict) -> dict:
        db = self.connection()

        while True:
            collection = db[self.recipe_collection]
            try:
                collection.insert_one(obj)
                obj.pop('_id', None)  # _id is not serializable!!!!
            except DuplicateKeyError:
                continue
            break

        return obj


    def find_by_id(self, query: dict) -> list:
        db = self.connection()
        collection = self.recipe_collection

        return self.connection()[collection].find_one(query, {'_id': False})


    def update_or_create(self, query, object) -> bool:
        db = self.connection()
        collection = self.recipe_collection
        update_result = self.connection()[collection].replace_one(query, object, upsert=True)

        return update_result.matched_count == 1


    def delete_one(self, query) -> bool:
        db = self.connection()
        collection = self.recipe_collection
        deleted_result = self.connection()[collection].delete_one(query)
        return deleted_result.deleted_count == 1


    def get_count(self, query=None) -> list:

        db = self.connection()
        collection = self.recipe_collection
        count = db[collection].count_documents(query if query is not None else {})

        return count


    def find_all(self, query=None) -> list:
        db = self.connection()
        collection = self.recipe_collection
        recipes = db[collection].find(query if query is not None else {}, {'_id': False})

        return recipes


    def find_by_tags(self, tags: list) -> list:
        db = self.connection()
        collection = self.recipe_collection
        recipes_with_tags = self.connection()[collection].find(
            {
            'tags.name': {'$in': tags, '$exists': True}
            },
            {'_id': False}
        )

        if recipes_with_tags.count() <= 0:
            return []
        return [recipe for recipe in recipes_with_tags]


    def add_rating(self, query, object) -> bool:
        db = self.connection()
        collection = self.recipe_collection
        update_result = self.connection()[collection].update_one(query, {'$push': object})

        return update_result.modified_count == 1


