from pydantic import BaseModel
from typing import List
from .preset_entry import PresetEntry


class Preset(BaseModel):
    """Preset."""

    id: int
    name: str
    calories: float
    protein: float
    carb: float
    fat: float
    fiber: float

    class Config:
        from_attributes = True


class PresetDetails(Preset):
    """PresetDetails."""

    entries: List[PresetEntry]


class ListPresetsPayload(BaseModel):
    """ListPresetsPayload."""

    presets: List[Preset]
