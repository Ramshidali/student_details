from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel

# Create your models here.
class UserProfile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=16)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    image = VersatileImageField('Image', upload_to="student")

    class Meta:
        db_table = 'user_profile'
        verbose_name = ('User Profile')
        verbose_name_plural = ('User Profile')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)