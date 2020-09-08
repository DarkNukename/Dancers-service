from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class Dancers(BaseModel):
    first_name = models.TextField()
    last_name = models.TextField()
    patronymic = models.TextField()
    gender = models.CharField(max_length=1)
    couple_uuid = models.UUIDField(null=True)
    club = models.UUIDField(null=True)
    age_group = models.TextField()
    rank = models.CharField(max_length=1, default='E')
    trainer_rank = models.TextField(default='Нет')
    referee_rank = models.TextField(default='Нет')

    class Meta:
        db_table = 'dancers'


class Couples(BaseModel):
    male = models.UUIDField()
    female = models.UUIDField()

    class Meta:
        db_table = 'couples'
