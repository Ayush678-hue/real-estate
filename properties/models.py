from django.db import models
from django.conf import settings


class Property(models.Model):
    """Model representing a real estate property listing."""

    class PropertyType(models.TextChoices):
        HOUSE = 'house', 'House'
        APARTMENT = 'apartment', 'Apartment'
        CONDO = 'condo', 'Condo'
        LAND = 'land', 'Land'
        COMMERCIAL = 'commercial', 'Commercial'

    class ListingType(models.TextChoices):
        SALE = 'sale', 'For Sale'
        RENT = 'rent', 'For Rent'

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.HOUSE,
    )
    listing_type = models.CharField(
        max_length=10,
        choices=ListingType.choices,
        default=ListingType.SALE,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2)

    # Address fields
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')

    # Geo-coordinates (optional, for map integration)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # Status flags
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    # Relationships
    agent = models.ForeignKey(
        'agents.Agent',
        on_delete=models.CASCADE,
        related_name='properties',
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'properties'
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.city}, {self.state}"


class PropertyImage(models.Model):
    """Model representing an image associated with a property."""
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_images'
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'

    def __str__(self):
        return f"Image for {self.property.title}"
