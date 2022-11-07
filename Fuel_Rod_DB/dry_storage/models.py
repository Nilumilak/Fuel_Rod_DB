from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models.signals import post_delete
from django.dispatch import receiver

from dry_storage_exp.models import DryStorageExp
from fresh_inventory.models import RawRod
from rod_pieces.models import RodPiece


class RodDryStorageTestNote(models.Model):
    rod = models.ForeignKey('RodDryStorageTest', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class RodDryStorageTest(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    raw_rod = models.ForeignKey(DryStorageExp, on_delete=models.CASCADE)
    original_length = models.FloatField(blank=True, null=True)
    heating_rate = models.FloatField(blank=True, null=True)
    cooling_rate = models.FloatField(blank=True, null=True)
    max_temperature = models.FloatField(blank=True, null=True)
    heating_time = models.FloatField(blank=True, null=True)
    cooling_time = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dry_storage_user_updated')

    class Meta:
        ordering = ['rod_id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            rods_list = list(RodDryStorageTest.objects.filter(raw_rod=self.raw_rod))
            if rods_list:
                self.number = rods_list[-1].number + 1
            else:
                self.number = 1
            self.rod_id = f'{self.raw_rod.exp_id}-R{self.number:02}'
        super().save()

    def delete(self, using=None, keep_parents=False):
        super().delete()

    def __str__(self):
        return self.rod_id


@receiver(post_delete, sender=RodDryStorageTest)
def dry_storage_delete(sender, instance, using, **kwargs):
    if instance.original_length:
        RawRod.objects.filter(material=instance.raw_rod.material.material).update(length=F('length') + instance.original_length)
    RodPiece.objects.filter(material=instance).delete()
