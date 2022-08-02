from django.db import models
from django.utils import timezone


from softskillspace.utils.models import TimeBasedModel

# Create your models here.

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

class Career(TimeBasedModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    deadline = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Candidateinfo(TimeBasedModel):
    jobtitle = models.ForeignKey(Career, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    phonenumber = models.IntegerField(default=+234-811022172)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    resumee = models.CharField(max_length=100)
    coverletter = models.TextField()

    def __str__(self):
        return str(self.lastname) + " " + str(self.firstname) + " as " + str(self.jobtitle)
