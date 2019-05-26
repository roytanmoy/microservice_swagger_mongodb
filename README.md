
# Recipe App

The purpose of this app is to demonstrate of building a recipe app and allow the user to search and rate the recipes.
This is not for a production grade application and should not be used as such.


## Overview

- API version: 1.0.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.RustClientCodegen

This app support the below tasks -  
● List, create, read, update, and delete Recipes.   
● Search recipes.  
● Rate recipes.  


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework.
    Easy to use pythonic web framework and it comes with the very  basic minimum required stuff to get a web app up and running as fast as possible. It is my best choice for the API demo whereas it's not recommonded for a production grade application (Django preferable).
    
* [Swagger](https://swagger.io/) -  RESTful Web services.
    Swagger id preferable because for easy API design, testing, debugging, documenting. It's easy to visualize and interact with the API’s resources without having any of the implementation logic in place. The swagger framewokr is easy to understand and thus helps for a better maintaince.
    
* [Connexion](https://connexion.readthedocs.io/en/latest/index.html) - Auto Mapping of OpenAPI endpoints to python function.
    Because, I used the Swagger, Connexion is the good choice to simplify the development process as well as reduce misinterpretation about what an API is going to look like. It allows to write http requests specifications, then maps the endpoints to the Python functions.  

* [Flask-Injector](https://pypi.org/project/Flask-Injector/) -  Dependency-injection framework for Python.
    Dependency Injection is a nice way to inject the dependencies for methods/classes. Flask-Injector is completely integrated on Flask. With this tool using the decorator @inject I can have the service I need, for instance, MongoDB.
    
* [MongoDB](https://github.com/mongodb/mongo) - Document Oriented NoSQL database.
    Mongodb is easier to use and has quick turnaround and need less resources as well as easy maintaince. However, obvious and better choice is the Elasticksearch for a production grade service for it's easy to use search queries and better performance in a distributed cluster setup. Secondly, the popularly available ELK stack is a plus point for service which needs to serve extensive search queries. Although, it comes with cost (hardware and maintaince prospective). There is a better approch to have a mix of dual database cluster with a primary database and the ES as the secindary mainly to serve the search operations..a happy.js framework can be fronted them to bind and choosing the storage based on the http request type.

* [PyMongo](https://github.com/mongodb/mongo-python-driver/) - DB Connector


### Instruction for Setup Installation

To start the app, from terminal execute 
```
setup_assist.sh start
```
To stop the app, from terminal execute  
`setup_assist.sh stop`

This will start the web service at 127.0.0.1 on port 8080.  

To verify the service  
`setup_assist.sh status`



### Accessing the Service
To access the service, use below cli from a terminal  -
```
curl -i http://localhost:8080/v1.0/recipes
curl -i -X POST -H "Authorization: Basic 123" -H "Content-Type: application/json" -d "{\"name\": \"mutton soup\", \"prepTime\": 23, \"difficulty\": 2, \"vegetarian\": false}" http://localhost:8080/v1.0/recipes
```

to get the authentication token:
```
Request:

POST http://192.168.99.100:8080/auth

{
	"username": "admin",
	"password": "123"
}
```

## Running the tests
To Update

### Unit Test

```
test_recipe.py
```
### Repository Test

```
test_storage.py
```


### Integration Test

```
test_integration.py
```



## Documentation for API Endpoints

##### Recipes

| Name | Method | URL | Protected |
| --- | --- | --- | --- |
| List | `GET` | `/recipes` | ✘ |
| List | `GET` | `/recipes?p={p}` | ✘ |
| Create | `POST` | `/recipes` | ✓ |
| Get | `GET` | `/recipes/{id}` | ✘ |
| Update | `PUT/PATCH` | `/recipes/{id}` | ✓ |
| Delete | `DELETE` | `/recipes/{id}` | ✓ |
| Rate | `Post` | `/recipes/{id}/rating` | ✘ |
| Search | `GET` | `/recipes?name={name}` | ✘ |
| Search | `GET` | `/recipes?difficulty={difficulty}` | ✘ |
| Search | `GET` | `/recipes?page=1&gt=716&lt=819&maxpagesize=100&vegetarian=true&difficultygt=1` | ✘ |

 

### `POST /recipes`: Add a New Recipe `Protected`

#### Request

The aruments are defined by **JSON data** in the HTTP request.

| Field           | Type        | Description                                                  | Description |
| --------------- | ----------- | ------------------------------------------------------------ | ----------- |
| `name`          | **string**  | `Mandatory` An empty string value is consider not set.       |             |
| `prepTime`  | **integer** | The value must be **greater than or equal to** `1` or it causes `500 internal server error` response |             |
| `difficulty`    | **integer** | The value must be **greater than or equal to** `1` and **less than or equal to** `3` or it causes `500 internal server error` response |             |
| `vegetarian` | **boolean** | `Mandatory` An invalid **boolean** value causes `400 bad request` response. |             |


The following JSON data is an example of a HTTP request body from the API endpoints.

  ```json
{
  "name": "Bread and Butter",
  "prepTime": 23,
  "difficulty": 2,
  "vegetarian": false
}
  ```
  
#### Response `RECIPE JSON`

The HTTP response body contains the data of the recipe that is just added.

The following JSON data is an example of a HTTP response body from the API endpoints.

  ```json
 {
    "created": "2019-02-15T04:00:44.194887Z",
    "difficulty": 2,
    "id": "bc17b2e1-1bf8-4fda-a124-a51802972786",
    "name": " m",
    "prepTime": 23,
    "rating": [],
    "vegetarian": false
}
  ```
### `GET /recipes/{id}`: Get an Existent Recipe

#### Request

The argument of the recipe ID is defined by the **URL parameter**.

| Type        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| **integer** | If there is no recipe that has an ID matching the value of the argument, it responses with `404 not found`. |

#### Response `RECIPE JSON`

The HTTP response body contains the data of the specified recipe.

### `PUT /recipes/{id}`: Modify an Existent Recipe `Protected`

#### Request

The argument of the recipe ID is defined by the **URL parameter**.

| Type        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| **integer** | If there is no recipe that has an ID matching the value of the argument, it responses with `404 not found`. |

The aruments for updating the recipe are defined by the **JSON data** in the HTTP request body.

| Field           | Type        | Description                                                  |
| --------------- | ----------- | ------------------------------------------------------------ |
| `name`          | **string**  | An empty string value causes `500 internal server error` response. |
| `prepare_time`  | **integer** | The value must be **greater than or equal to** `1` or it causes `500 internal server error` response. |
| `difficulty`    | **integer** | The value must be **greater than or equal to** `1` and **less than or equal to** 3 or it causes `500 internal server error` response. |
| `is_vegetarian` | **boolean** | An invalid **boolean** value causes `400 bad request` response. |

#### Response `RECIPE JSON`

The HTTP response body contains the data of the recipe that is just modified.

### `DELETE /recipes/{id}`: Delete an Existent Recipe `Protected`

#### Request

The argument of the recipe ID is defined by the **URL parameter**.

| Type        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| **integer** | If there is no recipe that has an ID matching the value of the argument, it responses with `404 not found`. |

#### Response `RECIPE JSON`

Http code for No Content

### `POST /recipes/{id}/rating`: Rate an Existent Recipe

#### Request

The argument of the recipe ID is defined by the **URL parameter**.

| Type        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| **integer** | If there is no recipe that has an ID matching the value of the argument, it responses with `404 not found`. |

The arument of rating the recipe is defined by **JSON data** in the HTTP request.

| Field    | Type        | Description                                                  |
| -------- | ----------- | ------------------------------------------------------------ |
| `rating` | **integer** | `Mandatory` The value must be **greater than or equal to** `1` and **less than or equal to** `5`. |

#### Response `RECIPE JSON`

The HTTP response body contains the data of the recipe that is just rated.




## Changes

### Commit on Feb 15 
    - docker changes to align with port requirment of 8080
    - changes in mongo count_documents method to support version alpine-mongo:3.2.3
  
### Commit on Feb 15 
    - added basic security
    - added many fixes for db and endpoint functions
    - added fixes for swagger endpoints

### Commit on Feb 14 

    - added test lib and helper files
    - added unit test
    - added db test
    - added integration test

### commit on Feb 9 

    - First Commit  




### Improvements
a.) Add a dedicated IAM(keystone underlying) microservices for authorization and authentication.  
b.) Introduce a GW API layer for handling client facing requests and responses.  
c.) Replace Mongo with/introduce additional elasticsearch db for better and easy serving of search queries.  
d.) For multiple microservices framework, need a message broker(RabbitMQ or Kafka) to be implmented.  
e.) It's required to handle the logs generated by the services (integrate a ELK stack).  

---
