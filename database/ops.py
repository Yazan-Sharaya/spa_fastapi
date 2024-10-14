"""
Database CRUD operation on people and notes.

*Note* that timestamp field is ignored even if passed by the user when updating or creating a note, because the database
automatically sets it on creation and updating.
"""
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.schemas import PersonCreate, PersonUpdate, NoteCreate, NoteUpdate
from database.models import Base, Person, Note
from database.engine import engine


async def drop_tables() -> None:
    """Deletes the tables that exist in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables() -> None:
    """
    Creates the tables defined in the Mapped Class(es) that inherited `Base`.
    This function should be called after the declaration of the Mapped Class(es), otherwise nothing will happen.
    Note also that this function doesn't recreate tables that already exist in the database.
    """
    # Database tables should be created like this when using an async session as seen in the docs
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#running-synchronous-methods-and-functions-under-asyncio
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def read_all_users(session: AsyncSession) -> Sequence[Person]:
    return (await session.scalars(select(Person))).all()


async def read_user_by_id(session: AsyncSession, user_id: int) -> Person | None:
    return await session.scalar(select(Person).filter_by(id=user_id))


async def create_user(session: AsyncSession, person: PersonCreate) -> Person:
    user = Person(**person.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    # Refresh the instance so that it contains the generated id and relationship objects (if any)
    return user


async def update_user(session: AsyncSession, user_id: int, person: PersonUpdate) -> Person:
    user = await read_user_by_id(session, user_id)
    user.fname = person.fname
    user.lname = person.lname
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await read_user_by_id(session, user_id)
    await session.delete(user)
    await session.commit()


async def read_all_notes(session: AsyncSession) -> Sequence[Note]:
    return (await session.scalars(select(Note))).all()


async def read_note_by_id(session: AsyncSession, note_id: int) -> Note | None:
    return await session.scalar(select(Note).filter_by(id=note_id))


async def create_note(session: AsyncSession, note: NoteCreate) -> Note:
    note = Note(**note.model_dump())
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


async def update_note(session: AsyncSession, note_id: int, note: NoteUpdate) -> Note:
    existing_note = await read_note_by_id(session, note_id)
    existing_note.content = note.content
    await session.commit()
    await session.refresh(existing_note)
    return existing_note


async def delete_note(session: AsyncSession, note_id: int) -> None:
    note = await read_note_by_id(session, note_id)
    await session.delete(note)
    await session.commit()
