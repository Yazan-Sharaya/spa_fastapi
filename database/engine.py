"""
Creates a global sqlalchemy engine that should be the only one used by this package, as stated in the documentation
https://docs.sqlalchemy.org/en/20/core/connections.html#basic-usage.

To specify the database url, you should set the DATABASE_URL environment variable. If not set, a sqlite
database located at database/sqlite_db/database.sqlite is used, useful when testing.
**Note** you must use an async driver, like aiosqlite for sqlite or asyncpg for postgresql.

Another environment variable is SQL_ECHO, which controls sqlaclhemy's engine logging. If set to True, all statements are
logged. Default is False.
"""
import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

DATABASE_URL = os.environ.get("DATABASE_URL", None)
if not DATABASE_URL:
    database_path = Path(__file__).parent.absolute() / "sqlite_db/database.sqlite"
    # Explicitly create the directory that'll house the database since the database engine (pysqlite in this case) can't
    # create intermediate directories.
    if not os.path.exists(database_path.parent):
        os.mkdir(database_path.parent)
    DATABASE_URL = f"sqlite+aiosqlite:///{database_path}"  # The three slashes are intentional.

ECHO = os.environ.get("SQL_ECHO", "False")
if ECHO not in ("True", "False"):
    raise ValueError("SQL_ECHO environment variable can only be True or False.")
ECHO = True if ECHO == "True" else False

engine = create_async_engine(DATABASE_URL, pool_size=10, poolclass=AsyncAdaptedQueuePool)
SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
# Create AsyncSession(s) with expire_on_commit set to False as recommended by the docs
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks
