from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import ExampleModel


class ExampleViewSetTest(TestCase):
    """Test cases for ExampleViewSet."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        
        self.example1 = ExampleModel.objects.create(
            name="Test Example 1",
            description="First test example",
            is_active=True,
        )
        self.example2 = ExampleModel.objects.create(
            name="Test Example 2",
            description="Second test example",
            is_active=False,
        )

    def test_list_examples(self):
        """Test listing example items."""
        url = reverse("example-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_example(self):
        """Test creating a new example item."""
        url = reverse("example-list")
        data = {
            "name": "New Test Example",
            "description": "A newly created test example",
            "is_active": True,
        }
        
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Test Example")
        self.assertEqual(response.data["description"], "A newly created test example")
        self.assertTrue(response.data["is_active"])
        
        self.assertEqual(ExampleModel.objects.count(), 3)

    def test_create_example_validation_error(self):
        """Test creating example with invalid data."""
        url = reverse("example-list")
        data = {
            "name": "",  # Invalid: empty name
            "description": "Test description",
            "is_active": True,
        }
        
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("validation_errors", response.data)

    def test_retrieve_example(self):
        """Test retrieving a specific example item."""
        url = reverse("example-detail", kwargs={"pk": self.example1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.example1.pk)
        self.assertEqual(response.data["name"], "Test Example 1")

    def test_retrieve_nonexistent_example(self):
        """Test retrieving a non-existent example item."""
        url = reverse("example-detail", kwargs={"pk": 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_example(self):
        """Test updating an example item."""
        url = reverse("example-detail", kwargs={"pk": self.example1.pk})
        data = {
            "name": "Updated Test Example",
            "description": "Updated description",
        }
        
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Test Example")
        self.assertEqual(response.data["description"], "Updated description")
        
        self.example1.refresh_from_db()
        self.assertEqual(self.example1.name, "Updated Test Example")

    def test_partial_update_example(self):
        """Test partially updating an example item."""
        url = reverse("example-detail", kwargs={"pk": self.example1.pk})
        data = {"name": "Partially Updated"}
        
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated")
        self.assertEqual(response.data["description"], "First test example")  # Unchanged

    def test_delete_example(self):
        """Test deleting an example item."""
        url = reverse("example-detail", kwargs={"pk": self.example1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExampleModel.objects.count(), 1)
        self.assertFalse(
            ExampleModel.objects.filter(pk=self.example1.pk).exists()
        )

    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected."""
        self.client.logout()
        url = reverse("example-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)