# auth_app/serializers.py

from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
