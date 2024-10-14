"""REST API endpoints that deal with note creation, deletion, reading and updating."""
from fastapi import APIRouter, HTTPException

from database import schemas, ops
from api.dependencies import SessionDependency

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[schemas.NoteSchema])
async def read_all_notes(session: SessionDependency):
    return await ops.read_all_notes(session)


@router.get("/{note_id}", response_model=schemas.NoteSchema)
async def read_note(note_id: int, session: SessionDependency):
    note = await ops.read_note_by_id(session, note_id)
    if note:
        return note
    raise HTTPException(404, f"Note with id {note_id} doesn't exist.")


@router.post("/", status_code=201, response_model=schemas.NoteSchema)
async def create_note(note: schemas.NoteCreate, session: SessionDependency):
    if await ops.read_user_by_id(session, note.person_id):
        return await ops.create_note(session, note)
    raise HTTPException(404, f"Person with {note.person_id} id was not found.")


@router.put("/{note_id}", response_model=schemas.NoteSchema)
async def update_note(note_id: int, note: schemas.NoteUpdate, session: SessionDependency):
    if await ops.read_note_by_id(session, note_id):
        note = await ops.update_note(session, note_id, note)
        return note
    raise HTTPException(404, f"Note with id {note_id} doesn't exist.")


@router.delete("/{note_id}")
async def delete_note(note_id: int, session: SessionDependency):
    note = await ops.read_note_by_id(session, note_id)
    if note:
        await ops.delete_note(session, note_id)
        return f"Note {note_id} was deleted successfully"
    raise HTTPException(404, f"Note with {note_id} id was not found.")
