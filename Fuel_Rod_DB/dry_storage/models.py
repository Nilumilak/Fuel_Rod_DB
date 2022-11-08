from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from dry_storage_exp.models import DryStorageExp
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
    previous_length = models.FloatField(blank=True, null=True)
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
        # if the rod updates then changes the length of the original rod (RawRod)
        if self.previous_length:
            original_rod = self.raw_rod.material
            original_rod.length -= ((self.original_length or 0) - self.previous_length)
            original_rod.save()

        # if the rod doesn't exist then creates 'number' and 'rod_id'
        if not self.rod_id:
            rods_list = RodDryStorageTest.objects.filter(raw_rod=self.raw_rod)
            # if the rod is not the first then searches for last number
            if rods_list:
                self.number = rods_list.latest('number').number + 1
            else:
                self.number = 1

            self.rod_id = f'{self.raw_rod.exp_id}-R{self.number:02}'

        # if it is the first assign of the original_length
        if self.original_length and not self.previous_length:
            original_rod = self.raw_rod.material
            original_rod.length -= self.original_length
            original_rod.save()

        self.previous_length = self.original_length
        super().save()

    def __str__(self):
        return self.rod_id


@receiver(post_delete, sender=RodDryStorageTest)
def dry_storage_delete(sender, instance, using, **kwargs):
    # if the rod deletes then changes the length of the original rod (RawRod)
    if instance.original_length:
        original_rod = instance.raw_rod.material
        original_rod.length += instance.original_length
        original_rod.save()
    RodPiece.objects.filter(material=instance).delete()
