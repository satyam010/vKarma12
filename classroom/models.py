

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    firstName = models.CharField(max_length = 30)
    lastName = models.CharField(max_length = 30)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    school = models.CharField(max_length=50)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default=None)
    def __str__(self):
        return self.user.school + '_admin'

class Subject(models.Model):
    school = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Batch(models.Model):
    name = models.CharField(max_length=30,unique=True)
    school = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject)
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default=None)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10,null=True)
    dob = models.DateField(blank=True, null=True,help_text="Enter in the following format : YYYY-MM-DD")
    address = models.TextField(max_length=150,null=True)
    age = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='profile_pictures',default='student_image.png', blank=True)
    def __str__(self):
        return self.user.firstName + ' ' + self.user.lastName

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default=None)
    child = models.ForeignKey(Student,on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10,null=True)
    address = models.TextField(max_length=150,null=True)
    image = models.ImageField(upload_to='profile_pictures', default='student_image.png',blank=True)

    def __str__(self):
        return self.user.firstName + ' ' + self.user.lastName

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default=None)
    batch = models.ManyToManyField(Batch)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10,null=True)
    image = models.ImageField(upload_to='profile_pictures',default='student_image.png', blank=True)
    def __str__(self):
        return self.user.firstName + ' ' +self.user.lastName


class Homework(models.Model):
    school = models.CharField(max_length=50,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework')
    name = models.CharField(max_length=255)
    issue_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True,help_text="Enter in the following format : YYYY-MM-DD")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homework')
    description = models.TextField(max_length=500)
    batch=models.ForeignKey(Batch, on_delete=models.CASCADE,null=True)
    file = models.FileField(upload_to='homework_files', null=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    school = models.CharField(max_length=50,null=True)
    issue_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    file = models.FileField(upload_to='notification_files', blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)
    class_date = models.DateField(blank=True, null=True)
    student = models.ForeignKey(Student, related_name='student_today',on_delete=models.CASCADE,null=True)
    present = models.NullBooleanField(default=False)
    def __str__(self):
        return str(self.class_date) + '_' + str(self.student.user.username) + '_' + str(self.Subject.name)

class Test(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    test_id = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject')
    name = models.CharField(max_length=52)
    Total_marks = models.IntegerField()

    def __str__(self):
        return self.name

class Marks(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Scored_marks = models.IntegerField(default=0,null=True)
    def __str__(self):
        return self.student.user.firstName + '_' + str(self.test.test_id)

class Timetable(models.Model):
    school = models.CharField(max_length=50,null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)
    start_time = models.DateTimeField(blank=True, null=True,help_text="Enter in the following format : YYYY-MM-DD")
    class_duration = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)


class Remark(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=256)


class Request(models.Model):
    school = models.CharField(max_length=50)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=256)
    noted = models.BooleanField(default=False)

    def __str__(self):
        return self.title