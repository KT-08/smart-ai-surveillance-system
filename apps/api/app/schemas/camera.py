
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Data required to register a camera
class CameraCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    camera_code: str = Field(min_length=1, max_length=100)
    location_id: UUID
    source_url: str = Field(min_length=1, max_length=500)


# Data returned by the API
class CameraResponse(BaseModel):
    id: UUID
    name: str
    camera_code: str
    location_id: UUID
    is_active: bool
    connection_status: str
    last_seen_at: datetime | None
    last_health_check_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Data required to activate or deactivate a camera
class CameraStatusUpdate(BaseModel):
    is_active: bool
