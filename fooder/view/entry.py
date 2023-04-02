from fastapi import APIRouter, Depends, Request
from ..model.entry import Entry, CreateEntryPayload, UpdateEntryPayload
from ..controller.entry import CreateEntry, UpdateEntry, DeleteEntry


router = APIRouter(tags=["entry"])


@router.post("", response_model=Entry)
async def create_entry(
    request: Request,
    data: CreateEntryPayload,
    contoller: CreateEntry = Depends(CreateEntry),
):
    return await contoller.call(data)


@router.put("/{entry_id}", response_model=Entry)
async def update_entry(
    request: Request,
    entry_id: int,
    data: UpdateEntryPayload,
    contoller: UpdateEntry = Depends(UpdateEntry),
):
    return await contoller.call(entry_id, data)


@router.delete("/{entry_id}")
async def delete_entry(
    request: Request,
    entry_id: int,
    contoller: DeleteEntry = Depends(DeleteEntry),
):
    return await contoller.call(entry_id)
