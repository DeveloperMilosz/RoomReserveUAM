from pydantic import BaseModel

class BuildingNameIn(BaseModel):
    pl: str
    en: str


class RoomDataIn(BaseModel):
    id: int
    number: str
    building_id: int
    building_name: BuildingNameIn
