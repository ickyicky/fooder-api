from typing import AsyncIterator, Optional

from ..model.preset import Preset
from ..domain.preset import Preset as DBPreset
from .base import AuthorizedController


class ListPresets(AuthorizedController):
    async def call(
        self, limit: int, offset: int, q: Optional[str]
    ) -> AsyncIterator[Preset]:
        async with self.async_session() as session:
            async for preset in DBPreset.list_all(
                session, limit=limit, offset=offset, q=q
            ):
                yield Preset.from_orm(preset)
