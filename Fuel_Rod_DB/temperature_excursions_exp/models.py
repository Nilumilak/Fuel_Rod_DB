from django.contrib.auth.models import User
from django.db import models

from fresh_inventory.models import RawRod


class TemperatureExcursionExpNote(models.Model):
    rod = models.ForeignKey('TemperatureExcursionExp', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class TemperatureExcursionExp(models.Model):
    exp_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    material = models.ForeignKey(RawRod, on_delete=models.CASCADE)
    quenched = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='temperature_exp_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='temperature_exp_user_updated')

    class Meta:
        ordering = ['exp_id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if the rod doesn't exist then creates 'number' and 'rod_id'
        if not self.exp_id:
            rods_list = TemperatureExcursionExp.objects.filter(material__material=self.material.material, quenched=self.quenched)
            # if the rod is not the first then searches for last number
            if rods_list:
                self.number = rods_list.latest('number').number + 1
            else:
                self.number = 1

            self.exp_id = f'{self.material.material}-TE{"Q" if self.quenched else ""}{self.number:02}'
        super().save()

    def __str__(self):
        return self.exp_id
