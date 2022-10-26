from django.contrib.auth.models import User
from django.db import models

from fresh_inventory.models import RawRod


class DryStorageExpNote(models.Model):
    rod = models.ForeignKey('DryStorageExp', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class DryStorageExp(models.Model):
    exp_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    material = models.ForeignKey(RawRod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_exp_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_exp_user_updated')

    class Meta:
        ordering = ['exp_id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.exp_id:
            self.number = DryStorageExp.objects.filter(material__material=self.material.material).count() + 1
        self.exp_id = f'{self.material.material}-DS{self.number:02}'
        super().save()

    def __str__(self):
        return self.exp_id
