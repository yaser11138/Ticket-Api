from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])

    password = serializers.CharField(max_length=20, write_only=True, required=True)
    password_conformation = serializers.CharField(max_length=20, write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password", "password_conformation", "email")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def validate(self, data):
        password = data["password"]
        password_conformation = data["password_conformation"]
        if password != password_conformation:
            raise serializers.ValidationError("password and password_conformation aren't same")
        return data

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user
