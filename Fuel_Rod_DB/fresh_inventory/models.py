from django.db import models
from django.contrib.auth.models import User


class RawRodNote(models.Model):
    rod = models.ForeignKey('RawRod', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Material(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RawRod(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_updated')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            count = RawRod.objects.filter(material=self.material).count() + 1
            self.rod_id = f'{self.material}-{count:02}'
        super().save()

    def __str__(self):
        return self.rod_id
