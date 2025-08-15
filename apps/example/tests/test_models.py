from django.test import TestCase

from ..models import ExampleModel


class ExampleModelTest(TestCase):
    """Test cases for ExampleModel."""

    def setUp(self):
        """Set up test data."""
        self.example = ExampleModel.objects.create(
            name="Test Example",
            description="This is a test example",
            is_active=True,
        )

    def test_string_representation(self):
        """Test the string representation of ExampleModel."""
        self.assertEqual(str(self.example), "Test Example")

    def test_model_fields(self):
        """Test that model fields are set correctly."""
        self.assertEqual(self.example.name, "Test Example")
        self.assertEqual(self.example.description, "This is a test example")
        self.assertTrue(self.example.is_active)
        self.assertIsNotNone(self.example.created_at)
        self.assertIsNotNone(self.example.updated_at)

    def test_model_ordering(self):
        """Test that models are ordered by creation date descending."""
        example2 = ExampleModel.objects.create(
            name="Test Example 2",
            description="This is another test example",
            is_active=True,
        )
        
        examples = list(ExampleModel.objects.all())
        self.assertEqual(examples[0], example2)  # Most recent first
        self.assertEqual(examples[1], self.example)

    def test_verbose_names(self):
        """Test model verbose names."""
        self.assertEqual(ExampleModel._meta.verbose_name, "Example Item")
        self.assertEqual(ExampleModel._meta.verbose_name_plural, "Example Items")