from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('author', 'Author'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)  # ✅ enforce email uniqueness
    username = models.CharField(max_length=150, unique=True)  # ✅ enforce username uniqueness

    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'role', 'phone', 'pincode']

    def __str__(self):
        return f"{self.username} ({self.role})"



class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=150, blank=True)
    categories = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'author')  # ✅ Prevent same user from adding same title twice

    def __str__(self):
        return f"{self.title} by {self.author.username}"
