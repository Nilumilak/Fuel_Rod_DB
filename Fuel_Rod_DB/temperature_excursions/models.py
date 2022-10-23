from django.contrib.auth.models import User
from django.db import models

from fresh_inventory.models import RawRod


class RodTemperatureTestNote(models.Model):
    rod = models.ForeignKey('RodTemperatureTest', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class RodTemperatureTest(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    material = models.ForeignKey(RawRod, on_delete=models.CASCADE)
    original_length = models.IntegerField()
    power = models.IntegerField()
    max_temperature = models.IntegerField()
    heating_time = models.IntegerField()
    quenched = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_user_updated')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            self.number = RodTemperatureTest.objects.filter(material=self.material).count() + 1
        self.rod_id = f'{self.material.material}-TE{"Q" if self.quenched else ""}{self.material.number:02}-R{self.number:02}'
        super().save()

    def __str__(self):
        return self.rod_id
