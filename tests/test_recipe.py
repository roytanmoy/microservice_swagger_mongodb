import unittest
from flexmock import flexmock
import uuid
from tests.fake_repo import FakeRecipesRepository
from api.recipe import Recipe

test_id = str(uuid.uuid4())

recipe = {
  "name": "veg rice",
  "prepTime": 20,
  "difficulty": 3,
  "vegetarian": True,
  "rating": []
}
updated_recipe = {
  "name": "veg fried rice",
  "prepTime": 60,
  "difficulty": 1,
  "vegetarian": False
}

class TestRecipe(unittest.TestCase):

    def setUp(self):
        repo = FakeRecipesRepository(recipe)
        self.Recipes = Recipe(repo)

    def test_create_recipe(self):
        """Test application logic for creation"""
        self.setUp()
        resp, status_code = self.Recipes.create_recipe(new_recipe = recipe)
        self.assertIn('id', resp.keys())
        self.assertEqual(201, status_code)

    def test_get_recipe(self):
        """Test application logic for fetching recipe"""
        self.setUp()
        resp1, _ = self.Recipes.create_recipe(new_recipe = recipe)
        recipe_id = resp1['id']
        resp2, status_code = self.Recipes.get_recipe(recipe_id)
        self.assertEqual(resp1['id'], resp2['id'])
        self.assertEqual(200, status_code)

    def test_update_recipe(self):
        """Test application logic for updating recipe"""
        self.setUp()
        resp1, _ = self.Recipes.create_recipe(new_recipe=recipe)
        recipe_id = resp1['id']
        _, status_code = self.Recipes.update_recipe(recipe_id, updated_recipe)
        self.assertEqual(200, status_code)
        _, status_code = self.Recipes.update_recipe(recipe_id, recipe)
        self.assertEqual(200, status_code)

        #id not found failures
        repo = flexmock()
        flexmock(repo).should_receive('find_by_id').and_return(None)
        Recipes = Recipe(repo)
        _, status_code = Recipes.update_recipe('222222', recipe)
        self.assertEqual(404, status_code)

        # failed to update
        repo = flexmock()
        flexmock(repo).should_receive('find_by_id').and_return(updated_recipe)
        flexmock(repo).should_receive('update_or_create').and_return(False)
        Recipes = Recipe(repo)
        _, status_code = Recipes.update_recipe('222222', recipe)
        self.assertEqual(500, status_code)


    def test_delete_recipe(self):
        """Test application logic for delete recipe"""
        # delete success
        self.setUp()
        resp, status_code = self.Recipes.delete_recipe('333333')
        self.assertEqual(204, status_code)

        # failed to delete
        repo = flexmock()
        flexmock(repo).should_receive('delete_one').and_return(False)
        Recipes = Recipe(repo)
        _, status_code = Recipes.delete_recipe('33333')
        self.assertEqual(404, status_code)

    def test_rate_recipe(self):
        """Test application logic for rate a recipe"""
        rating = {"rate": 5, "user": "nick de"}
        repo = flexmock()
        flexmock(repo).should_receive('add_rating').and_return(True)
        flexmock(repo).should_receive('find_by_id').and_return(recipe,False).one_by_one()
        Recipes = Recipe(repo)

        # rating update success
        _, status_code = Recipes.rate_recipe(test_id,rating)
        self.assertEqual(200, status_code)

        # user rating exists
        flexmock(repo).should_receive('find_by_id').and_return(recipe, True).one_by_one()
        _, status_code = Recipes.rate_recipe(test_id, rating)
        self.assertEqual(204, status_code)

        # failed to update rating
        flexmock(repo).should_receive('add_rating').and_return(False)
        flexmock(repo).should_receive('find_by_id').and_return(recipe, False).one_by_one()
        _, status_code = Recipes.rate_recipe(test_id, rating)
        self.assertEqual(500, status_code)




if __name__ == '__main__':
    unittest.main()