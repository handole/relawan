from rest_framework import serializers
from django.contrib.auth.models import User
from post.models import Korcam, Relawan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class RelawanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relawan
        fields = ("__all__")

class KorcamSerializer(serializers.ModelSerializer):
    relawan = RelawanSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Korcam
        fields = ("__all__")