from fastapi import APIRouter, Depends, Request
from ..model.preset import ListPresetsPayload
from ..controller.preset import ListPresets


router = APIRouter(tags=["preset"])


@router.get("", response_model=ListPresetsPayload)
async def list_presets(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    q: str | None = None,
    controller: ListPresets = Depends(ListPresets),
):
    return ListPresetsPayload(
        presets=[p async for p in controller.call(limit=limit, offset=offset, q=q)]
    )
