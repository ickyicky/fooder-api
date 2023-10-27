from typing import AsyncIterator, Optional
from fastapi import HTTPException

from ..model.preset import Preset, PresetDetails
from ..domain.preset import Preset as DBPreset
from .base import AuthorizedController


class ListPresets(AuthorizedController):
    async def call(
        self, limit: int, offset: int, q: Optional[str]
    ) -> AsyncIterator[Preset]:
        async with self.async_session() as session:
            async for preset in DBPreset.list_all(
                session, user_id=self.user.id, limit=limit, offset=offset, q=q
            ):
                yield Preset.from_orm(preset)


class GetPreset(AuthorizedController):
    async def call(self, id: int) -> PresetDetails:
        async with self.async_session() as session:
            preset = await DBPreset.get(session, self.user.id, id)

            if preset is not None:
                return PresetDetails.from_orm(preset)

            raise HTTPException(status_code=404, detail="preset not found")


class DeletePreset(AuthorizedController):
    async def call(
        self,
        id: int,
    ) -> AsyncIterator[Preset]:
        async with self.async_session.begin() as session:
            preset = await DBPreset.get(session, self.user.id, id)

            if preset is None:
                raise HTTPException(status_code=404, detail="preset not found")

            await preset.delete(session)
