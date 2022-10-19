from rest_framework import serializers
from freelancer.account.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError(
                'A user with this email and password is not found.')
        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "email", "password", "confirm_password")

    def validate(self, data):
        if data.get("password", None) != data.get("confirm_password", None):
            raise serializers.ValidationError("Password not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create(**validated_data)
