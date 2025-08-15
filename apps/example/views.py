from django.http import Http404
from drf_spectacular.utils import extend_schema
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import ExampleModel
from .serializers import (
    ExampleCreateRequest,
    ExampleListResponse,
    ExampleResponse,
    ExampleUpdateRequest,
)


class ExampleViewSet(ViewSet):
    """
    ViewSet for managing example items using Pydantic validation.
    
    This demonstrates the ADR-002 pattern of using Django REST Framework
    with Pydantic models for request/response validation.
    """

    @extend_schema(
        summary="List example items",
        description="Retrieve a paginated list of example items.",
        responses={200: ExampleListResponse},
        tags=["Example Items"],
    )
    def list(self, request):
        """List all example items with pagination."""
        queryset = ExampleModel.objects.all()
        
        page_size = 20
        page = int(request.GET.get("page", 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        items = queryset[start:end]
        total_count = queryset.count()
        
        results = [ExampleResponse.from_model(item) for item in items]
        
        next_url = None
        if end < total_count:
            next_url = f"{request.build_absolute_uri()}?page={page + 1}"
        
        previous_url = None
        if page > 1:
            previous_url = f"{request.build_absolute_uri()}?page={page - 1}"
        
        response_data = ExampleListResponse(
            count=total_count,
            next=next_url,
            previous=previous_url,
            results=results,
        )
        
        return Response(response_data.model_dump())

    @extend_schema(
        summary="Create example item",
        description="Create a new example item with the provided data.",
        request=ExampleCreateRequest,
        responses={201: ExampleResponse},
        tags=["Example Items"],
    )
    def create(self, request):
        """Create a new example item."""
        try:
            validated_data = ExampleCreateRequest(**request.data)
        except ValidationError as e:
            return Response(
                {"validation_errors": e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        instance = ExampleModel.objects.create(
            name=validated_data.name,
            description=validated_data.description or "",
            is_active=validated_data.is_active,
        )
        
        response_data = ExampleResponse.from_model(instance)
        return Response(response_data.model_dump(), status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Retrieve example item",
        description="Retrieve a specific example item by ID.",
        responses={200: ExampleResponse, 404: {"description": "Item not found"}},
        tags=["Example Items"],
    )
    def retrieve(self, request, pk=None):
        """Retrieve a specific example item."""
        try:
            instance = ExampleModel.objects.get(pk=pk)
        except ExampleModel.DoesNotExist:
            raise Http404("Example item not found")
        
        response_data = ExampleResponse.from_model(instance)
        return Response(response_data.model_dump())

    @extend_schema(
        summary="Update example item",
        description="Update a specific example item with the provided data.",
        request=ExampleUpdateRequest,
        responses={200: ExampleResponse, 404: {"description": "Item not found"}},
        tags=["Example Items"],
    )
    def update(self, request, pk=None):
        """Update a specific example item."""
        try:
            instance = ExampleModel.objects.get(pk=pk)
        except ExampleModel.DoesNotExist:
            raise Http404("Example item not found")
        
        try:
            validated_data = ExampleUpdateRequest(**request.data)
        except ValidationError as e:
            return Response(
                {"validation_errors": e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if validated_data.name is not None:
            instance.name = validated_data.name
        if validated_data.description is not None:
            instance.description = validated_data.description
        if validated_data.is_active is not None:
            instance.is_active = validated_data.is_active
        
        instance.save()
        
        response_data = ExampleResponse.from_model(instance)
        return Response(response_data.model_dump())

    @extend_schema(
        summary="Delete example item",
        description="Delete a specific example item by ID.",
        responses={204: {"description": "Item deleted"}, 404: {"description": "Item not found"}},
        tags=["Example Items"],
    )
    def destroy(self, request, pk=None):
        """Delete a specific example item."""
        try:
            instance = ExampleModel.objects.get(pk=pk)
        except ExampleModel.DoesNotExist:
            raise Http404("Example item not found")
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)