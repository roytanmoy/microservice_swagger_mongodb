import connexion
import setting
from injector import Module, provider, Injector
from services.mongodb import MongoFactory, MongoCollection
from connexion.resolver import RestyResolver


class DatabaseModule(Module):

    @provider
    def provide_db_connection(self) -> MongoCollection:
        host = setting.MONGO['HOST']
        port = setting.MONGO['PORT']
        db = setting.MONGO['DB']
        collection = setting.MONGO['COLLECTION']
        return MongoCollection(MongoFactory(host, port), collection, db)

injector = Injector([DatabaseModule()])


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('recipe.yaml', resolver=RestyResolver('api'))
    app.run(host='0.0.0.0', port ='80')