from django.db import models


class ExampleModel(models.Model):
    """
    Example model to demonstrate Django model patterns.
    Replace this with your actual business logic models.
    """

    name = models.CharField(max_length=255, help_text="Name of the example item")
    description = models.TextField(
        blank=True, help_text="Optional description of the example item"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this example item is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Example Item"
        verbose_name_plural = "Example Items"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name