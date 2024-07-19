# core/serializers.py

from rest_framework import serializers
from .models import User, Session
from .models import AuditEntry
from .models import Camera
from .models import Case
from .models import MaterialEvidence, MaterialEvidenceStatus


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'rank', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            rank=validated_data['rank']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.rank = validated_data.get('rank', instance.rank)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['user', 'login', 'logout']


class AuditEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEntry
        fields = ['object_id', 'table_name', 'class_name', 'action', 'fields', 'data', 'created']


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id']


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['device_id', 'name', 'type', 'created', 'updated', 'active']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['name', 'description', 'investigator', 'active', 'created', 'updated']


class MaterialEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialEvidence
        fields = ['name', 'case', 'created_by', 'description', 'status', 'barcode', 'created', 'updated']
