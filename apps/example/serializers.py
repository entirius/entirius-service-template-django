from typing import List, Optional

from pydantic import BaseModel, Field
from rest_framework import serializers

from .models import ExampleModel


class ExampleCreateRequest(BaseModel):
    """Pydantic model for creating example items."""

    name: str = Field(..., min_length=1, max_length=255, description="Name of the item")
    description: Optional[str] = Field(
        None, description="Optional description of the item"
    )
    is_active: bool = Field(True, description="Whether the item should be active")


class ExampleUpdateRequest(BaseModel):
    """Pydantic model for updating example items."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Name of the item"
    )
    description: Optional[str] = Field(
        None, description="Optional description of the item"
    )
    is_active: Optional[bool] = Field(
        None, description="Whether the item should be active"
    )


class ExampleResponse(BaseModel):
    """Pydantic model for example item responses."""

    id: int = Field(..., description="Unique identifier of the item")
    name: str = Field(..., description="Name of the item")
    description: str = Field(..., description="Description of the item")
    is_active: bool = Field(..., description="Whether the item is active")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    @classmethod
    def from_model(cls, instance: ExampleModel) -> "ExampleResponse":
        """Convert Django model instance to Pydantic response."""
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description or "",
            is_active=instance.is_active,
            created_at=instance.created_at.isoformat(),
            updated_at=instance.updated_at.isoformat(),
        )


class ExampleListResponse(BaseModel):
    """Pydantic model for paginated example item list responses."""

    count: int = Field(..., description="Total number of items")
    next: Optional[str] = Field(None, description="Next page URL")
    previous: Optional[str] = Field(None, description="Previous page URL")
    results: List[ExampleResponse] = Field(..., description="List of example items")


class ExampleModelSerializer(serializers.ModelSerializer):
    """DRF serializer for ExampleModel (fallback for non-Pydantic use cases)."""

    class Meta:
        model = ExampleModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")