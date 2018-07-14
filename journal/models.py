from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Kid(models.Model):
    photo = models.CharField(max_length=64)  # fixme -> ImageField()
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    grade = models.SmallIntegerField()
    is_studying = models.BooleanField(default=False)

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': self.photo,
            'birthday': self.birthday.isoformat(),
            'grade': self.grade,
            'isStudying': self.is_studying
        }


class Journal(models.Model):
    kid = ForeignKey(Kid, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    direction = models.CharField(choices=(
        ('IN', 'Took to nursery'),
        ('OUT', 'took from nursery')
    ), max_length=3)
    relative = models.CharField(choices=(
        ('M', 'Mother'),
        ('F', 'Father')
    ), max_length=1)

    @property
    def json(self):
        return {
            'id': self.id,
            'kid': self.kid.id,
            'timestamp': self.timestamp,
            'direction': self.direction,
            'relative': self.relative
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.direction == 'IN':
            self.kid.is_studying = True
            self.kid.save()
        elif self.direction == 'OUT':
            self.kid.is_studying = False
            self.kid.save()

        super().save()
