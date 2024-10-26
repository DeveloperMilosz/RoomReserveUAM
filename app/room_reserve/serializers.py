from pydantic import BaseModel
from datetime import datetime
"""
class BuildingNameIn(BaseModel):
    pl: str
    en: str


class RoomDataIn(BaseModel):
    id: int
    number: str
    building_id: int
    building_name: BuildingNameIn """


class MeetingNameIn(BaseModel):
    pl: str
    en: str

class MeetingDataIn(BaseModel):
    start_time: datetime
    end_time: datetime
    name: MeetingNameIn

