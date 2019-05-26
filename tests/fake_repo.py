"""
recipes = {
    "name": "veg fried rice",
    "prepTime": 20,
    "difficulty": 3,
    "vegetarian": True,
    "rating": []
}
"""
class FakeRecipesRepository(object):
    def __init__(self,recipes):
        self.recipes = recipes

    def find_by_id(self, recipe_id):
        self.recipes['id'] = recipe_id['id']
        return self.recipes

    def find_all(self, query, sort, page, page_size):
        return [r for r in self.recipes.values() if r.name == query.name]

    def create_one(self, recipe):
        return self.recipes

    def update_or_create(self, query, object):
        return self.recipes

    def delete_one(self, recipe_id):
        return True

    def add_rating(self, query, object):
        self.recipes['rating'].append(object)
        self.recipes['id'] = query
        return self.recipes

