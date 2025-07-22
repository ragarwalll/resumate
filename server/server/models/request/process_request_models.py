"""Process request model schema"""

from typing import Optional
from pydantic import BaseModel, Field


class ProcessRequestModel(BaseModel):
    """Process request model schema."""

    user_id: str = Field(..., min_length=1)
    description: Optional[str] = None
    tags: Optional[list[str]] = []
