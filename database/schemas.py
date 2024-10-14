"""
Stores Pydantic schemas for the models in `models.py` that are used for data validation and (de)serialization.
Both Pydantic and SQLAlchemy use the term model, in this project, ORM classes are called models and Pydantic's
validation `models` are called schemas to avoid confusion.

There are multiple schemas for each `model (people and notes)`, each responsible for a specific operation like creation
and updating, because some field may be required for one operation but not the other.
For example, creating a person doesn't require passing an id, since it's automatically assigned by the database, but
updating a person does require it, hence the different schemas.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, RootModel


class PersonBase(BaseModel):
    lname: str
    fname: str


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    id: int
    timestamp: datetime | None = None  # This field is assigned a None by default because the user doesn't have to pass
    # it when updating a person, but they still can.


class PersonSchema(PersonBase):
    model_config = ConfigDict(from_attributes=True)
    # Refer to https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances for more information about
    # `model_config`. But basically, it allows the construction of Pydantic models from ORM (sqlalchemy) models.

    id: int
    timestamp: datetime

    notes: list["NoteSchema"]


class PeopleSchema(RootModel):
    """A schema used to validate multiple PersonSchema, so same as list[PersonSchema]."""
    root: list["PersonSchema"]


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    person_id: int


class NoteUpdate(NoteBase):
    id: int
    # Same as PersonUpdate, timestamp and person_id can be passed, but they don't have to be.
    timestamp: datetime | None = None
    person_id: int | None = None


class NoteSchema(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    person_id: int
