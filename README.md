Simple single page application
==============================

A simple single page application written in Javascript and FastAPI.


Stack
-----
* Python >= 3.10
* FastAPI (REST API)
* Pydantic V2 (Data validation + serialization)
* SQLAlchemy V2 (ORM)
* aiosqlite or any other async compatible relational database driver (Database)
* Javascript, html and css (Frontend)


Motivation
----------
The motivation behind the project is that resources for building a backend using FastAPI
and integrating SQLAlcehmy V2 and Pydantic V2 with FastAPI are scarce, and the FastAPI documentation is outdated, it
only showcases the use of Pydantic and SQLAlchemy V1.

So I decided to build this project, it directly follows the excellent 4 part tutorial series by [realpython](https://realpython.com/).
However, their choice of backend technologies is different, their app is built using Flask, SQLAlchemy V1 and
marshmallow for data serialization.


Aim
---
The aim of this repo is to demonstrate how to build the same app using SQLAlchemy V2 ORM, integrating Pydantic V2
for data validation and serialization in and out of the database and utilizing FastAPI's powers such as 
dependency injection and async path operations.

I find this stack more elegant and performant than Flask/marshmallow/SQLAlchemy V1.
Another advantage of using FastAPI is automatic OpenAPI and Swagger-UI documentation. 


This repo might interest you if you
-----------------------------------
1. Have experience in Flask and want to know more about FastAPI.
2. Want to integrate SQLAlchemy V2 elegance and powers into a FastAPI backend.
3. Confused about how Pydantic and SQLAlchemy would work together in a FastAPI project.
4. Want to know how to implement async SQLAlchemy sessions to take advantage of the asynchronous nature of FastAPI.


Resources
---------
As this is a direct port of the code from the realpython tutorial series, it's best that you give it a read if you want
to know more about how REST APIs are developed in Python and how to build the frontend.
The code in this repo is comparable to the final version of the code in part 4, albeit using a different stack.
This also means some of the shortcomings of the code and design are present here too.

1. [Part 1 - Setup](https://realpython.com/flask-connexion-rest-api/)
2. [Part 2 - Database](https://realpython.com/flask-connexion-rest-api-part-2/)
3. [Part 3 - Relationships](https://realpython.com/flask-connexion-rest-api-part-3/)
4. [Part 4 - Frontend](https://realpython.com/flask-javascript-frontend-for-rest-api/)


Documentation
-------------
This project isn't comprehensively documented since it's a port of the in depth series by realpython.
Nonetheless, each module contains docstrings that explain the purpose of the module, conventions used and some of its
functionality.
I also recommend checking the comments in the code, because they explain some of the decisions made and link to
official documentation.


License
-------
This project is licensed under the [MIT license](https://github.com/Yazan-Sharaya/spa_fastapi/blob/main/LICENSE)
