# coding: utf-8
import logging
import connexion
from flask_testing import TestCase
import unittest
import json
from pymongo import MongoClient
import setting
from services.mongodb import MongoFactory, MongoCollection

config = json.loads(open('./sample_data.json').read())



recipe = {
      "name": "Corn Pizaa with Coke",
      "prepTime": 23,
      "difficulty": 2,
      "vegetarian": False
      }
rating = {
    "rate": 5,
    "user": "Dev Martin"
    }

headers={'Authorization': 'Basic ' + '123'}



class BaseTestCase(TestCase):

    def setUp(self):
        """Setup connection with test db and initialize the repository"""
        host = setting.MONGO['HOST']
        port = setting.MONGO['PORT']
        db = setting.MONGO['DB']
        collection = setting.MONGO['COLLECTION']
        client = MongoClient(host, port)
        client.drop_database(db)
        self.repo = MongoCollection(MongoFactory(host, port), collection, db)
        self.recipe1 = self.repo.create_one(config['recipe1'])
        self.recipe2 = self.repo.create_one(config['recipe2'])
        self.recipe3 = self.repo.create_one(config['recipe3'])

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.add_api('recipe.yaml')
        return app.app


class TestIntegration(BaseTestCase):
    """ Recipe integration test stubs """

    def test_add_recipes(self):
        """
        Test case for add_recipe
        """
        response = self.client.open('/v1.0/recipes',
                                    method='POST',
                                    headers = headers,
                                    data=json.dumps(recipe),
                                    content_type='application/json')

        self.assertEqual(201, response.status_code)
        resp =json.loads(response.data)
        self.assertEqual(resp['name'], recipe['name'])
        self.assertEqual(resp['difficulty'], recipe['difficulty'])
        self.assertEqual(resp['prepTime'], recipe['prepTime'])
        self.assertEqual(resp['vegetarian'], recipe['vegetarian'])


    def test_get_recipe_by_id(self):
        """
        Test case for get a recipe1 by id
        """
        recipe_id = self.recipe1['id']
        response = self.client.open(
            '/v1.0/recipes/{}'.format(recipe_id),
            method='GET')

        self.assert200(response)
        resp = json.loads(response.data)
        self.assertEqual(resp, self.recipe1)


    def test_delete_recipe(self):
        """
        Test case for delete a recipe3
        """
        recipe_id = self.recipe3['id']
        response = self.client.open(
            '/v1.0/recipes/{}'.format(recipe_id),
            headers=headers,
            method='DELETE')
        self.assert200(response)

        resp = json.loads(response.data)
        self.assertIsNone(self.repo.find_by_id({'id':recipe_id}))


    def test_update_recipe(self):
        """
        Test case for updating a recipe2
        """
        recipe_id = self.recipe2['id']
        recipe['name'] = self.recipe2['name']
        response = self.client.open(
            '/v1.0/recipes/{}'.format(recipe_id),
            data=json.dumps(recipe),
            content_type='application/json',
            headers=headers,
            method='PUT')

        self.assertEqual(200, response.status_code)
        resp = json.loads(response.data)
        self.assertEqual(resp['name'], self.recipe2['name'])
        self.assertEqual(resp['difficulty'], recipe['difficulty'])
        self.assertEqual(resp['prepTime'], recipe['prepTime'])
        self.assertEqual(resp['vegetarian'], recipe['vegetarian'])


    def test_rating_recipe(self):
        """
        Test case for rating a recipe2
        """
        recipe_id = self.recipe2['id']
        response = self.client.open(
            '/v1.0/recipes/{}/rating'.format(recipe_id),
            data=json.dumps(rating),
            content_type='application/json',
            method='POST')

        self.assertEqual(201, response.status_code)
        resp = json.loads(response.data)
        retrieved = self.repo.find_by_id({'id': recipe_id})
        data = [item for item in retrieved['rating'] if item['user']==rating['user']]

        self.assertEqual(rating,data[0])





if __name__ == '__main__':
    unittest.main()