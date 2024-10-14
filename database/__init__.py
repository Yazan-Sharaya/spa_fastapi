"""
The database package. it contains four modules which are as follows:
- engine.py: Defines the global SQLAlchemy database engine, sessionmaker `Session` factory and database settings.
- models.py: Contains the People and Notes ORM mapped classes or `models`.
- schemas.py: Pydantic's `models` are located here, but they are called `schemas` to avoid confusion
  with SQLAlchemy's `models` defined in `models.py`.
- ops.py: CRUD operations on notes and people.

Before calling any API endpoints, database tables must be created/read by calling `create_tables` function in `ops.py`.
"""
