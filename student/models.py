from django.db import models
from main.models import BaseModel
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField
# Create your models here.

class StudentDetails(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=16, null=True, blank=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=10)
    standerd = models.CharField(max_length=10)
    email = models.EmailField()
    image = VersatileImageField('Image', upload_to="student")

    class Meta:
        db_table = 'student_details'
        verbose_name = ('Student Details')
        verbose_name_plural = ('Student Details')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class Subjects(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'student_subject'
        verbose_name = ('Subject')
        verbose_name_plural = ('Subject')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)


class StudentMark(BaseModel):
    student = models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    mark = models.CharField(max_length=3)

    class Meta:
        db_table = 'student_mark'
        verbose_name = ('Student Mark')
        verbose_name_plural = ('Student Mark')
        ordering = ('auto_id',)

    def __str__(self):
        return f"student :{self.student.name} - subject :{self.subject.name} - mark :{self.mark}"