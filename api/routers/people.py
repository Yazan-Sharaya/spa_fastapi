"""REST API endpoints that deal with people creation, deletion, reading and updating."""
from fastapi import APIRouter, HTTPException

from database import schemas, ops
from api.dependencies import SessionDependency

router = APIRouter(prefix="/people", tags=["people"])


@router.get("/", response_model=schemas.PeopleSchema)
async def read_all_people(session: SessionDependency):
    return await ops.read_all_users(session)


@router.get("/{person_id}", response_model=schemas.PersonSchema)
async def read_one_person(person_id: int, session: SessionDependency):
    user = await ops.read_user_by_id(session, person_id)
    if user:
        return user
    raise HTTPException(404, f"Person with {person_id} ID was not found.")


@router.post("/", status_code=201, response_model=schemas.PersonSchema)
async def create_person(person: schemas.PersonCreate, session: SessionDependency):
    return await ops.create_user(session, person)


@router.put("/{person_id}", response_model=schemas.PersonSchema)
async def update_person(person_id: int, person: schemas.PersonUpdate, session: SessionDependency):
    if await ops.read_user_by_id(session, person_id):
        return await ops.update_user(session, person_id, person)
    raise HTTPException(404, f"Person with {person_id} ID was not found.")


@router.delete("/{person_id}")
async def delete_person(person_id: int, session: SessionDependency):
    if await ops.read_user_by_id(session, person_id):
        await ops.delete_user(session, person_id)
        return f"{person_id} was deleted successfully"
    raise HTTPException(404, f"Person with {person_id} ID was not found.")
