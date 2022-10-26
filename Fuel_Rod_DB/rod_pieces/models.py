from django.contrib.auth.models import User
from django.db import models


class RodPieceNote(models.Model):
    rod = models.ForeignKey('RodPiece', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class AnalysisTechnique(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SampleState(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RodPiece(models.Model):
    rod_id = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100)
    number = models.IntegerField()
    analysis_technique = models.ForeignKey(AnalysisTechnique, on_delete=models.CASCADE)
    sample_state = models.ForeignKey(SampleState, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='piece_user_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='piece_user_updated')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.rod_id:
            self.number = RodPiece.objects.filter(material=self.material, analysis_technique=self.analysis_technique).count() + 1
        self.rod_id = f'{self.material}-{self.analysis_technique}{self.number:02}{"-R" if self.sample_state.name == "Ready" else ""}'
        super().save()

    def __str__(self):
        return self.rod_id
