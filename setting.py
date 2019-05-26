from os import environ

MONGO = {
    'HOST': environ.get('MONGO_HOST'),
    'PORT': int(environ.get('MONGO_PORT', '27017')),
    'DB': environ.get('MONGO_DB', 'recipes'),
    'COLLECTION': environ.get('MONGO_COLLECTION', 'recipe'),
    'TEST_DB': environ.get('MONGO_TEST_DB', 'recipes_test'),
}