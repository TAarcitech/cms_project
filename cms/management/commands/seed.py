from django.core.management.base import BaseCommand
from cms.models import User, Content
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        # ✅ Check if user with this email already exists
        if not User.objects.filter(username='admin').exists() and not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Admin@123',
                role='admin',
                phone='9999999999',
                pincode='123456'
            )
            self.stdout.write(self.style.SUCCESS("Created admin user"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists."))

        # Create 5 authors
        for i in range(1, 6):
            username = f"user{i}"
            email = f"user{i}@example.com"
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="Password@123",
                    role='author',
                    phone=f"99999{i:05}",
                    pincode="500001"
                )
                self.stdout.write(self.style.SUCCESS(f"Created author: {username}"))

                # Add 2 posts per author
                for j in range(1, 3):
                    Content.objects.create(
                        author=user,
                        title=f"Post {j} by {username}",
                        body=f"This is a sample post {j} by {username}.",
                        summary=f"Summary {j}",
                        categories=random.choice(['Tech', 'News', 'Sports']),
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added content {j} for {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User or email already exists: {username}"))

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete."))
