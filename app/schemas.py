from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RideStartResponse(BaseModel):
    id: int
    start_time: datetime

class RideEndRequest(BaseModel):
    ride_id: int

class RideDetail(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    duration_minutes: Optional[float] = None   # 仅当已结束时计算
    cost: Optional[float] = None               # 仅当已结束时计算

class RideCostResponse(BaseModel):
    ride_id: int
    cost: float

class ErrorResponse(BaseModel):
    detail: str