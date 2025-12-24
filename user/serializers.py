from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User model uchun serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'telefon', 'email', 'ism', 'familiya', 'rasm', 'yaratilgan_vaqt']
        read_only_fields = ['id', 'yaratilgan_vaqt', 'username']


class UserCreateSerializer(serializers.ModelSerializer):
    """Yangi user yaratish uchun serializer"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['telefon', 'email', 'ism', 'familiya', 'password', 'rasm']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['telefon'],  # username sifatida telefon ishlatiladi
            telefon=validated_data['telefon'],
            email=validated_data['email'],
            ism=validated_data['ism'],
            familiya=validated_data['familiya'],
            password=validated_data['password']
        )
        if 'rasm' in validated_data:
            user.rasm = validated_data['rasm']
            user.save()
        return user
