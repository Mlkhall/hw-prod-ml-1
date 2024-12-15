from datetime import datetime
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class FeaturesMessage(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    teacher: float
    features: list[float]
    created_at: datetime = Field(default_factory=datetime.now)
    timestamp: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))


class ModelResponseMessage(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    id_source: UUID4
    teacher: float
    prediction: float
    created_at: datetime
    timestamp: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))


class MetricLogMessage(BaseModel):
    id: UUID4
    y_true: float
    y_pred: float
    absolute_error: float
