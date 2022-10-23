from django.contrib.auth.models import User
from django.db import models

from fresh_inventory.models import RawRod


class RodDryStorageTestNote(models.Model):
    rod = models.ForeignKey('RodDryStorageTest', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class RodDryStorageTest(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    material = models.ForeignKey(RawRod, on_delete=models.CASCADE)
    original_length = models.IntegerField()
    heating_rate = models.IntegerField()
    cooling_rate = models.IntegerField()
    max_temperature = models.IntegerField()
    heating_time = models.IntegerField()
    cooling_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_updated')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            self.number = RodDryStorageTest.objects.filter(material=self.material).count() + 1
        self.rod_id = f'{self.material.material}-DS{self.material.number:02}-R{self.number:02}'
        super().save()

    def __str__(self):
        return self.rod_id
