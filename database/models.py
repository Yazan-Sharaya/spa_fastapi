"""
Declares the Mapped Classes to use with sqlalchemy ORM.
No database tables are created by default, for that, the function `ops.create_tables` needs to be explicitly called.
Both Pydantic and SQLAlchemy use the term model, in this project, ORM classes are called models and Pydantic's
validation `models` are called schemas to avoid confusion.
"""
from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

# For a list of python types to sqlalchemy datatypes visit the following link:
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation


class Base(DeclarativeBase):
    """
    The new way of defining a base in sqlalchemy, superseding `declarative_base` function.
    Note that `DeclarativeBase` can't be used directly. Refer to the documentation for more information.
    """


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    lname: Mapped[str]
    fname: Mapped[str]

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    notes: Mapped[list["Note"]] = relationship(back_populates="author", cascade="all, delete-orphan", lazy='selectin')
    # lazy=selectin is one of the ways of avoiding implicit io using asyncio with SQLAlchemy, another options is
    # to use selectinload option for each query. Either must be used, or an error occurs.

    def __repr__(self) -> str:
        return f"Person(id={self.id}, lname={self.lname}, fname={self.fname}, timestamp={self.timestamp})"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))

    author: Mapped["Person"] = relationship(back_populates="notes", lazy='selectin')

    def __repr__(self) -> str:
        return f"Note(id={self.id}, content={self.content}, timestamp={self.timestamp})"
