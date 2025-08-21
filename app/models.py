from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


# Persistent models (stored in database)
class Aoi(SQLModel, table=True):
    __tablename__ = "aois"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    geojson: Dict[str, Any] = Field(sa_column=Column(JSON))
    kps_code: str = Field(max_length=50, unique=True)
    meta: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Observation(SQLModel, table=True):
    __tablename__ = "observations"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    kps_id: str = Field(max_length=100, unique=True)
    observed_at: datetime
    lat: Decimal = Field(decimal_places=8, max_digits=12)
    lng: Decimal = Field(decimal_places=8, max_digits=12)
    finding_type: str = Field(max_length=100)
    notes: str = Field(default="", max_length=2000)
    photo_url: Optional[str] = Field(default=None, max_length=500)
    source: str = Field(max_length=100)
    created_by: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schemas (for validation, forms, API requests/responses)
class AoiCreate(SQLModel, table=False):
    name: str = Field(max_length=255)
    geojson: Dict[str, Any]
    kps_code: str = Field(max_length=50)
    meta: Dict[str, Any] = Field(default={})


class AoiUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None, max_length=255)
    geojson: Optional[Dict[str, Any]] = Field(default=None)
    meta: Optional[Dict[str, Any]] = Field(default=None)


class AoiResponse(SQLModel, table=False):
    id: int
    name: str
    geojson: Dict[str, Any]
    kps_code: str
    meta: Dict[str, Any]
    created_at: str  # ISO format string for JSON serialization


class ObservationCreate(SQLModel, table=False):
    kps_id: str = Field(max_length=100)
    observed_at: datetime
    lat: Decimal = Field(decimal_places=8, max_digits=12)
    lng: Decimal = Field(decimal_places=8, max_digits=12)
    finding_type: str = Field(max_length=100)
    notes: str = Field(default="", max_length=2000)
    photo_url: Optional[str] = Field(default=None, max_length=500)
    source: str = Field(max_length=100)
    created_by: str = Field(max_length=255)


class ObservationUpdate(SQLModel, table=False):
    observed_at: Optional[datetime] = Field(default=None)
    lat: Optional[Decimal] = Field(default=None, decimal_places=8, max_digits=12)
    lng: Optional[Decimal] = Field(default=None, decimal_places=8, max_digits=12)
    finding_type: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = Field(default=None, max_length=2000)
    photo_url: Optional[str] = Field(default=None, max_length=500)
    source: Optional[str] = Field(default=None, max_length=100)


class ObservationResponse(SQLModel, table=False):
    id: int
    kps_id: str
    observed_at: str  # ISO format string for JSON serialization
    lat: Decimal
    lng: Decimal
    finding_type: str
    notes: str
    photo_url: Optional[str]
    source: str
    created_by: str
    created_at: str  # ISO format string for JSON serialization


class ObservationFilter(SQLModel, table=False):
    finding_type: Optional[str] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    created_by: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
