from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """Garante que apenas 1 registro exista."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():  # ty:ignore[unresolved-attribute]
            raise ValidationError(
                f"Já existe um registro de {self._meta.verbose_name}. Edite o existente."  # ty:ignore[unresolved-attribute]
            )
        return super().save(*args, **kwargs)


class TimeStampedModel(models.Model):
    """Adiciona created_at e updated_at automaticamente."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
