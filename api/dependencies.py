"""Defines the dependencies to be injected into fastapi's path operation functions."""
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession  # Used for type annotation.

from database.engine import SessionLocal


async def create_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    A dependency to create a session per request and close it after it's done, which is a best practise.
    https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks
    """
    # It's always a good idea to rollback in case of an error and to close the session after it's done, both are done
    # here implicitly.
    async with SessionLocal() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(create_async_session)]
# This is the new preferred way of annotating a dependency because it reduces unnecessary code duplication.
# For more information, see https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant
