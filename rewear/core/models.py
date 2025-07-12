# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# --- Model 1: The Custom User ---
# We extend Django's built-in User to add our points system.
class User(AbstractUser):
    points = models.IntegerField(default=50) # Users start with 50 points


# --- Model 2: The Clothing Item ---
# This represents every piece of clothing on the platform.
class ClothingItem(models.Model):
    # Define choices for dropdown menus to keep data consistent
    CATEGORY_CHOICES = (
        ('Tops', 'Tops'),
        ('Bottoms', 'Bottoms'),
        ('Dresses', 'Dresses'),
        ('Outerwear', 'Outerwear'),
        ('Accessories', 'Accessories'),
    )
    CONDITION_CHOICES = (
        ('New', 'New with Tags'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('swapped', 'Swapped'),
        ('sold', 'Sold'),

    )

    # --- Fields for the ClothingItem table ---
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items') # Link to the user who owns it
    title = models.CharField(max_length=200) # The item's title, e.g., "Vintage Denim Jacket"
    description = models.TextField() # A longer description
    image = models.ImageField(upload_to='clothing_images/') # The item's photo

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES) # Dropdown for category
    size = models.CharField(max_length=20) # e.g., "M", "UK 10", "32W"
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES) # Dropdown for condition

    points_value = models.IntegerField(default=10) # How many points this item is worth
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available') # Is it available or swapped?
    is_approved = models.BooleanField(default=False) # Admin must approve items before they go live
    
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set the creation date

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


# --- Model 3: The Swap Request ---
# This tracks a request from one user to swap for an item.
class SwapRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    # --- Fields for the SwapRequest table ---
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests') # Link to the user making the request
    item_requested = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='requests') # Link to the item they want
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for '{self.item_requested.title}' from {self.requester.username}"