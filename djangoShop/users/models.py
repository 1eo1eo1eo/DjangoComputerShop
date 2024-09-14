from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_images",
        blank=True,
        null=True,
        verbose_name="Avatar",
    )

    class Meta:
        db_table: str = "Users"
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self) -> str:
        return self.username
