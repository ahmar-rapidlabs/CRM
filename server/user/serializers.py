from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
import tempfile
from .models import User
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }
    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            role=self.validated_data.get("role")
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})
        user.set_password(password)
        user.save()
        path = tempfile.NamedTemporaryFile().name
        file = open(path, 'w', encoding='utf-8')
        file.write(f"Email: {user.email}, Password: {password}\n")
        file.close()
        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']