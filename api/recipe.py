import uuid
from datetime import datetime
from app import injector
from injector import inject
from services.mongodb import MongoCollection



class Recipe(object):

    @inject
    def __init__(self, db: MongoCollection):
        self._db = db


    def create_recipe(self, new_recipe: dict):

        recipes = self._db.find_all({'name': new_recipe['name']})
        if recipes.count() != 0:
            return ({"message": "A recipe with same name already exists"}, 409)

        # Generate a unique ID for the recipe
        new_recipe['id'] = str(uuid.uuid4())
        new_recipe['created'] = datetime.utcnow()
        new_recipe['rating'] = []

        return self._db.create_one(new_recipe), 201


    def get_recipe(self, recipe_id: str):
        recipe = self._db.find_by_id({'id': recipe_id})
        if recipe:
            return recipe, 200
        else:
            return {"message": "Recipe not found"}, 404


    def update_recipe(self, recipe_id: str, recipe):

        curr_recipe = self._db.find_by_id({'id': recipe_id})
        if not curr_recipe:
            return ({"message": "Recipe not found"}, 404)

        if recipe['name'] and curr_recipe['name'] != recipe['name']:
            return ({"message": "Recipe name modification not allowed"}, 400)

        item_to_update = {k for k in recipe if k in curr_recipe and recipe[k]!=curr_recipe[k]}
        if not item_to_update:
            return curr_recipe, 200

        if 'id' not in recipe:
            recipe['id'] = recipe_id
        recipe['updated'] = datetime.utcnow()

        exists = self._db.update_or_create({'id': recipe_id}, recipe)

        if exists:
            return self._db.find_by_id({'id': recipe_id}), 200
        else:
            return {"message": "failed to update the recipe"}, 500


    def delete_recipe(self, recipe_id: str):

        recipe = self._db.find_by_id({'id': recipe_id})
        if not recipe:
            return {"message": "Recipe not found for the given id"}, 404

        deleted = self._db.delete_one({'id': recipe_id})
        if deleted:
            return {"message": "successfull deleted the recipe"}, 200
        else:
            return {"message": "failed to delete the recipe"}, 404


    def get_recipes(self, **kwargs):

        items = {}
        if 'name' in kwargs:
            items['name'] = kwargs['name']
        if 'prepTime' in kwargs:
            items['prepTime'] = {'$lte': kwargs['prepTime']}
        if 'difficulty' in kwargs:
            items['difficulty'] = {'$lte': kwargs['difficulty']}
        if 'vegetarian' in kwargs:
            items['vegetarian'] = kwargs['vegetarian']
        if 'status' in kwargs:
            items['status'] = kwargs['status']

        recipes = self._db.find_all(items)
        if 'limit' in kwargs:
            limited_recipes = [recipe for recipe in recipes][:kwargs['limit']]
        if 'sort'in kwargs:
            limited_recipes.sort(key=lambda x: int(x['id']), reverse=kwargs['sort'] == 'desc')

        return limited_recipes


    def rate_recipe(self, recipe_id: str, rate_recipe):

        found_recipe = self._db.find_by_id({'id': recipe_id})
        if not found_recipe:
            return ({"message": "Recipe not found"}, 404)

        user = rate_recipe['user']
        rate = rate_recipe['rate']
        review ={'user': user, 'rate':rate}

        find_user = self._db.find_by_id({'id': recipe_id, 'rating.user':user})
        if find_user:
            return {"message": "Rating already provided by the user"}, 200

        updatedExisting = self._db.add_rating({'id': recipe_id}, {'rating':review})
        if updatedExisting:
            return {"message": "Successfully updated rating"}, 201
        else:
            return {"message": "Failed to update Rating"},  500



class_instance = injector.get(Recipe)