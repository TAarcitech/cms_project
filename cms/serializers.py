from rest_framework import serializers
from .models import User, Content
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'first_name', 'last_name', 'role',
            'phone', 'pincode'
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value) or not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain both upper and lower case characters.")
        return value

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pincode must be 6 digits.")
        return value

    def create(self, validated_data):
        # Auto generate username if not provided
        if not validated_data.get('username'):
            import uuid
            validated_data['username'] = f"user_{uuid.uuid4().hex[:8]}"
        return User.objects.create_user(**validated_data)

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at']

    def validate_title(self, value):
        if len(value) > 30:
            raise serializers.ValidationError("Title must be <= 30 characters.")
        return value

    def validate_body(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("Body must be <= 300 characters.")
        return value
    
    def validate(self, data):
        request = self.context.get('request')
        author = request.user if request else None
        title = data.get('title')

        # Check for duplicates only on create (not update)
        if self.instance is None and Content.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError("You have already created content with this title.")
        
        return data