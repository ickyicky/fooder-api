from typing import AsyncIterator
from fastapi import HTTPException

from ..model.entry import Entry, CreateEntryPayload, UpdateEntryPayload
from ..domain.entry import Entry as DBEntry
from .base import AuthorizedController


class CreateEntry(AuthorizedController):
    async def call(self, content: CreateEntryPayload) -> Entry:
        async with self.async_session.begin() as session:
            try:
                entry = await DBEntry.create(
                    session, content.meal_id, content.product_id, content.grams
                )
                return Entry.from_orm(entry)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class UpdateEntry(AuthorizedController):
    async def call(self, entry_id: int, content: UpdateEntryPayload) -> Entry:
        async with self.async_session.begin() as session:
            entry = await DBEntry.get_by_id(session, entry_id)
            if entry is None:
                raise HTTPException(status_code=404, detail="entry not found")

            try:
                await entry.update(
                    session, content.meal_id, content.product_id, content.grams
                )
                return Entry.from_orm(entry)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class DeleteEntry(AuthorizedController):
    async def call(self, entry_id: int) -> Entry:
        async with self.async_session.begin() as session:
            entry = await DBEntry.get_by_id(session, entry_id)
            if entry is None:
                raise HTTPException(status_code=404, detail="entry not found")

            try:
                await entry.delete(session)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])
