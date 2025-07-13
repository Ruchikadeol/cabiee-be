from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email is already registered. Please use a different email."
            )
        ])
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, validated_data):

        email = validated_data.get("email")
        password = validated_data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        
        return validated_data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        try:           
            user=User.objects.get(email=email)
            if not user.check_password(password):
                raise ValidationError("Invalid credentials")

            validated_data["user"] = user
            return validated_data
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")

    def to_representation(self,instance):
        user=instance.get('user')
        return{"id":user.id,'email':instance.get('email'),'role':user.role}
