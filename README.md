
# Expense Tracker API

A simple REST API created using Spring Boot and MySql.

## Run Locally

Clone the project

```bash
  git clone 
```

Go to the project directory

```bash
  cd expense-tracker-api
```

Create a database

```bash
  CREATE DATABASE database_name
```

The app will start running at http://localhost:9182


## Swagger - API Documentation
- [UI format](http://localhost:9182/docs)

Cilck [here](https://swagger.io/) to know more about Swagger

## Explore REST APIs
  
### User Authentication

| Method        | URL           | Description   | Return          |      
| ------------- |---------------| ------------- | --------------- |
| POST          | api/signup    | Sign-up       | JSON Web Token  |
| POST          | api/login     | Login         | JSON Web Token  |               

### Categories

| Method        | URL                        | Description   | Return          |      
| --- |----------------------------| --- | --- |
| GET | api/categories/            | Get all categories | Array of JSON objects |
| GET | api/categories/{id}        | Get a category by id | Single JSON object |            
| POST | api/categories/create      | Create a new category | Created JSON object |
| PUT | api/categories/update/{id} | Update an existing category | Updated JSON object |
| DELETE | api/categories/delete/{id} | Delete a category | Success message |

### Transactions

| Method        |         URL        | Description   | Return          |      
| --- | --- | --- | --- |
| GET | api/categories/{cid}/transactions/ | Get all transactions of "cid" category | Array of JSON objects |
| GET | api/categories/{cid}/transactions/{tid} | Get a single transaction by "tid" of category "cid" | Single JSON object |            
| POST | api/categories/{cid}/transactions/ | Insert a new transaction for the category "cid" | Created JSON object |
| PUT | api/categories/{cid}/transactions/{tid} | Update an existing transaction | Updated JSON object |
| DELETE | api/categories/{cid}/transactions/{tid} | Delete a transaction | Success message |

> **_NOTE:_**  
The endpoints of "Categories" and "Transactions" are restricted. To access those endpoints, use the token which is generated after logging-in as the value of the Bearer in the Authorization header as follows:  
**"Authorization: login-token"**

## Sample Request Body

### User - Register
```bash
  {
    "firstName": "Thomas",
    "lastName": "Shelby",
    "email": "shelby@gmail.com",
    "password": "test123"
  }
```
### User - Login
```bash
  {
    "email": "shelby@gmail.com",
    "password": ""  --> password must be encoded with base64 and add the first three letters at first
  }
```
