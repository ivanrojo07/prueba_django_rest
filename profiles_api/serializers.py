from rest_framework import serializers
from .models import UserProfile

class HelloSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=10)


class RegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=16,min_length=6,allow_blank=False, write_only=True)
    password2 = serializers.CharField(max_length=16,min_length=6,allow_blank=False, write_only=True)
    
    class Meta:
        model=UserProfile
        fields = ['email','name', 'password1','password2']

    def validate(self,data):
        if data['password1'] and data['password2'] and data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords don´t match")
        return data

    def create(self, validated_data):
        user = UserProfile.objects.create_user(validated_data['email'],validated_data['name'],validated_data['password1'])
        return user.__dict__
