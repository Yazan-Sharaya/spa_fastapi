"""Main application entry point. Defines the app and adds the routers, static and template directories."""
import os
import pprint
from typing import Any
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import Response
from starlette.staticfiles import PathLike
from starlette.types import Scope
import pydantic

from api.dependencies import SessionDependency
from api.routers import notes, people
from database import ops, schemas, engine


class StaticFilesNoCache(StaticFiles):
    """
    A class the inherits from `fastapi.StaticFiles` that disables caching of static files.
    Very useful during developments, since the content of the static files (js, css, etc.) is changed often, and if
    caching is enabled, the new changes will not be reflected.
    """
    def __init__(self, *args: Any, cache_control: str = "", **kwargs: Any) -> None:
        self.cache_control = cache_control if cache_control else "max-age=0, no-cache, no-store, must-revalidate"
        super().__init__(*args, **kwargs)

    def file_response(
        self,
        full_path: PathLike,
        stat_result: os.stat_result,
        scope: Scope,
        status_code: int = 200,
    ) -> Response:
        resp = super().file_response(full_path, stat_result, scope, status_code)
        if self.cache_control:
            resp.headers.setdefault("Cache-Control", self.cache_control)
        return resp


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """A function that creates/loads the database tables at startup, and closes the database engine at shutdown."""
    # Visit https://fastapi.tiangolo.com/advanced/events/#lifespan-function for more information.
    await ops.create_tables()
    yield
    await engine.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(people.router)
app.include_router(notes.router)
app.mount("/static", StaticFilesNoCache(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDependency):
    # Validate the database result in the endpoint as suggested by
    # https://www.starlette.io/templates/#asynchronous-template-rendering
    users = await ops.read_all_users(session)
    try:
        schemas.PeopleSchema.model_validate(users)
    except pydantic.ValidationError:
        return HTTPException(500, "Could not validate the data.")
    return templates.TemplateResponse(
        name="index.html", request=request, context={
            "people": users, "request_content": pprint.pformat(dict(request.items()))})
