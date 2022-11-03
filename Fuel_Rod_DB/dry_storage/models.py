from django.contrib.auth.models import User
from django.db import models

from dry_storage_exp.models import DryStorageExp


class RodDryStorageTestNote(models.Model):
    rod = models.ForeignKey('RodDryStorageTest', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class RodDryStorageTest(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    raw_rod = models.ForeignKey(DryStorageExp, on_delete=models.CASCADE)
    original_length = models.FloatField()
    heating_rate = models.FloatField()
    cooling_rate = models.FloatField()
    max_temperature = models.FloatField()
    heating_time = models.FloatField()
    cooling_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_updated')

    class Meta:
        ordering = ['rod_id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            self.number = RodDryStorageTest.objects.filter(raw_rod=self.raw_rod).count() + 1
        self.rod_id = f'{self.raw_rod.exp_id}-R{self.number:02}'
        super().save()

    def __str__(self):
        return self.rod_id
