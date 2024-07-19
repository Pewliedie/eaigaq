# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from passlib.hash import pbkdf2_sha256
import time


def default_now():
    return datetime.now()


def create_barcode_value():
    return round(time.time())


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    rank = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=default_now)
    updated = models.DateTimeField(default=default_now)
    photo_data = models.TextField(null=True, blank=True)  # Поле для фотографии

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.rank})"


class FaceID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='face')
    data = models.TextField()
    created = models.DateTimeField(default=default_now)
    updated = models.DateTimeField(default=default_now)


class Case(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=default_now)
    updated = models.DateTimeField(default=default_now)


class MaterialEvidenceStatus(models.TextChoices):
    IN_STORAGE = "На хранении"
    DESTROYED = "Уничтожен"
    TAKEN = "Взят"
    ON_EXAMINATION = "На экспертизе"
    ARCHIVED = "В архиве"


class MaterialEvidence(models.Model):
    name = models.CharField(max_length=255)
    case = models.ForeignKey('Case', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=[
        ('На хранении', 'IN_STORAGE'),
        ('Уничтожен', 'DESTROYED'),
        ('Взят', 'TAKEN'),
        ('На экспертизе', 'ON_EXAMINATION'),
        ('В архиве', 'ARCHIVED')
    ])
    barcode = models.CharField(max_length=255, default=create_barcode_value)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_image = generate_qr_code(self.barcode)
            self.qr_code.save(f'{self.id}.png', qr_image, save=False)
        super().save(*args, **kwargs)


class MaterialEvidenceEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material_evidence = models.ForeignKey(MaterialEvidence, on_delete=models.CASCADE, related_name='events')
    action = models.CharField(max_length=50, choices=MaterialEvidenceStatus.choices)
    created = models.DateTimeField(default=default_now)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login = models.DateTimeField(default=default_now)
    logout = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)


class CameraType(models.TextChoices):
    FACE_ID = "Аутентификация по лицу"
    REC = "Запись видео"
    DEFAULT = "Обычная камера"


class Camera(models.Model):
    device_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=CameraType.choices)
    created = models.DateTimeField(default=default_now)
    updated = models.DateTimeField(default=default_now)
    active = models.BooleanField(default=True)


class AuditEntry(models.Model):
    object_id = models.IntegerField()
    table_name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    fields = models.TextField()
    data = models.TextField()
    created = models.DateTimeField(default=default_now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class TableModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
