import unittest
from pymongo import MongoClient
import setting
from services.mongodb import MongoFactory, MongoCollection
import uuid


id1 = str(uuid.uuid4())
recipe1 = {
  "id": id1,
  "name": "crispy potato finger chips",
  "prepTime": 9,
  "difficulty": 2,
  "vegetarian": True,
  "rating": []
}
id2 = str(uuid.uuid4())
recipe2 = {
  "id": id2,
  "name": "veg fried rice",
  "prepTime": 20,
  "difficulty": 3,
  "vegetarian": True,
  "rating": []
}
id3 = str(uuid.uuid4())
recipe3 = {
  "id": id3,
  "name": "butter chicken",
  "prepTime": 40,
  "difficulty": 1,
  "vegetarian": False,
  "rating": []
}

class TestMongoCollection(unittest.TestCase):

    def setUp(self):
        """Setup connection with test db and initialize the repository"""
        host = setting.MONGO['HOST']
        port = setting.MONGO['PORT']
        db = setting.MONGO['DB']
        collection = setting.MONGO['COLLECTION']

        self.client = MongoClient(host, port)
        self.client.drop_database(db)

        self.repository = MongoCollection(MongoFactory(host, port), collection, db)


    def test_insert_recipe(self):
        """Test that the repository can create Recipes"""
        created_recipes = self.repository.create_one(recipe1)
        recipe_id = created_recipes['id']
        self.assertEqual(recipe_id, recipe1['id'])


    def test_retrieve_recipe(self):
        """Test that the repository can retrieve Recipes"""
        self.repository.create_one(recipe2)
        retrieved = self.repository.find_by_id({'id': recipe2['id']})
        self.assertEqual(retrieved['id'], recipe2['id'])
        self.assertEqual(retrieved['name'], recipe2['name'])
        self.assertEqual(retrieved['prepTime'], recipe2['prepTime'])
        self.assertEqual(retrieved['difficulty'], recipe2['difficulty'])
        self.assertEqual(retrieved['vegetarian'], recipe2['vegetarian'])


    def test_delete_recipe(self):
        """Test that the repository can delete Recipes"""
        self.repository.create_one(recipe3)
        self.repository.delete_one({'id': recipe3['id']})
        retrieved = self.repository.find_by_id({'id': recipe3['id']})

        self.assertFalse(retrieved)



    def tearDown(self):
        """Close connection to the test db"""
        self.client.close()


if __name__ == '__main__':
    unittest.main()