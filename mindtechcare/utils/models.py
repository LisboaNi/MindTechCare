from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    """Gerencia apenas objetos que não estão deletados."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()  
    active_objects = ActiveManager()  

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete, marcando a data de exclusão em vez de remover do banco."""
        if not self.deleted_at:
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restaura um item deletado removendo o timestamp de exclusão."""
        if self.deleted_at:
            self.deleted_at = None
            self.save(update_fields=["deleted_at"])

    def is_deleted(self):
        """Verifica se o objeto está deletado."""
        return self.deleted_at is not None
