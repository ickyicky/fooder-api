from fastapi import APIRouter, Depends, Request
from ..model.preset import ListPresetsPayload, PresetDetails
from ..controller.preset import ListPresets, DeletePreset, GetPreset


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


@router.get("/{preset_id}", response_model=PresetDetails)
async def get_preset(
    request: Request,
    preset_id: int,
    controller: GetPreset = Depends(GetPreset),
):
    return await controller.call(preset_id)


@router.delete("/{preset_id}")
async def delete_preset(
    request: Request,
    preset_id: int,
    controller: DeletePreset = Depends(DeletePreset),
):
    await controller.call(preset_id)
