from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=200)
    semester = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Semester {self.semester})"

class StudyMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('note', 'Note'),
        ('question_paper', 'Question Paper'),
        ('scheme', 'Scheme & Application'),
        ('result', 'Result'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    

    def __str__(self):
        return self.title
