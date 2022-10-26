from django.contrib.auth.models import User
from django.db import models


class RodTemperatureTestNote(models.Model):
    rod = models.ForeignKey('RodTemperatureTest', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class RodTemperatureTest(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    exp_id = models.CharField(max_length=100)
    original_length = models.IntegerField()
    power = models.IntegerField()
    max_temperature = models.IntegerField()
    heating_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='temperature_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='temperature_user_updated')

    class Meta:
        ordering = ['rod_id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            self.number = RodTemperatureTest.objects.filter(exp_id=self.exp_id).count() + 1
        self.rod_id = f'{self.exp_id}-R{self.number:02}'
        super().save()

    def __str__(self):
        return self.rod_id
