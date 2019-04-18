from rest_framework import serializers
from .models import Subject, Batch, Student, User, Parent, Teacher, Homework, Attendance, Notification, Timetable, Marks, Test, Remark, Request
from django.http import JsonResponse
from django.db import models
from django.forms.models import model_to_dict
from django.conf.urls import url



class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ("__all__")

class BatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Batch
        fields = ("__all__")

class HomeworkSerializer(serializers.ModelSerializer):
    sub_name=serializers.SerializerMethodField()
    def get_sub_name(self,item):
        print("kya sub",item.subject)
        return item.subject.name

    color=serializers.SerializerMethodField()
    def get_color(self,item):
        print("kya ayayayayay",item.subject.color)
        return item.subject.color

    owner_name=serializers.SerializerMethodField()
    def get_owner_name(self,item):
        print("kya ayayayayay",item.owner)
        return str(item.owner)

    batch_name=serializers.SerializerMethodField()
    def get_batch_name(self,item):
        print("kya ayayayayay",item.batch)
        return str(item.batch)

    class Meta:
        model = Homework
        fields = ('school','batch_name','owner','owner_name','subject','sub_name','name','issue_date','deadline','color','description','file','name','id')

class StudentAttendanceSerializer(serializers.ModelSerializer):
    total_absent=serializers.SerializerMethodField()
    total_present=serializers.SerializerMethodField()
    total_classes=serializers.SerializerMethodField()
    student_name=serializers.SerializerMethodField()

    def get_total_classes(self,item):
        # for i in Student.objects.all():
        #     return str(Attendance.objects.filter(student=item.student.pk).count())
        return str(item.student_today.filter(present=True).count()+item.student_today.filter(present=False).count())

    def get_total_present(self,item):
        return str(item.student_today.filter(present=True).count())


    def get_total_absent(self,item):
            return str(item.student_today.filter(present=False).count())


    def get_student_name(self,item):
        return str(item.user.firstName)

    class Meta:
        model = Student
        fields = ('total_absent','total_present','total_classes','student_name')



class StudentSerializer(serializers.HyperlinkedModelSerializer):
    status=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    parent_name=serializers.SerializerMethodField()
    #child_name=serializers.SerializerMethodField()
    #user.id
    #parent login then show child name

    def get_name(self,item):
        request = self.context.get("request")
        return (request.user.firstName+" "+request.user.lastName)

    batch_name=serializers.SerializerMethodField()
    def get_batch_name(self,item):
        print("kya ayayayayay",item.batch)
        return str(item.batch)  
    
    def get_parent_name(self,item):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if request.user.is_student:
                print(item.parent_set)
                return list(item.parent_set.all().values('user__firstName'))
        
    def get_status(self,item):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if request.user.is_student:
                return "Student"
            if request.user.is_parent:
                return "Parent"
            if request.user.is_teacher:
                return "Teacher"

    class Meta:
        model = Student
        fields = ("parent_name",'status','name','batch_name','dob','age','address','email','phone_number','image')

class ParentSerializer(serializers.HyperlinkedModelSerializer):
    status=serializers.SerializerMethodField()
    def get_status(self,item):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if request.user.is_student:
                return "Student"
            if request.user.is_parent:
                return "Parent"
            if request.user.is_teacher:
                return "Teacher"

    
    child_name=serializers.SerializerMethodField()
    def get_child_name(self,item):
        print("kya ayayayayay",item.child)
        return str(item.child)

    name=serializers.SerializerMethodField()
    def get_name(self,item):
        print("kya ayayayayay",item.user.firstName)
        return str(item.user.firstName+" "+item.user.lastName)

    class Meta:
        model = Parent
        fields = ('status','name','child_name','email','phone_number','address','image')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    status=serializers.SerializerMethodField()
    def get_status(self,item):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if request.user.is_student:
                return "Student"
            if request.user.is_parent:
                return "Parent"
            if request.user.is_teacher:
                return "Teacher"

    name=serializers.SerializerMethodField()
    def get_name(self,item):
        print("kya ayayayayay",item.user.firstName)
        return str(item.user.firstName+" "+item.user.lastName)
    
    #batch_name=serializers.SerializerMethodField()
    #def get_batch_name(self,item):
        #print("kya ayayayayay",item.batch)
        #return str(item.batch)  

    class Meta:
        model = Teacher
        fields = ('status','name','batch','email','phone_number','image')


class TimetableSerializer(serializers.ModelSerializer):
    teacher_name=serializers.SerializerMethodField()
    def get_teacher_name(self,item):
        print("kya ayayayayay",item.teacher)
        return str(item.teacher)

    batch_name=serializers.SerializerMethodField()
    def get_batch_name(self,item):
        print("kya ayayayayay",item.batch)
        return str(item.batch)
    
    sub_name=serializers.SerializerMethodField()
    def get_sub_name(self,item):
        print("kya sub",item.subject)
        return str(item.subject)

    class Meta:
        model = Timetable
        fields = ('school','teacher','teacher_name','batch','batch_name','start_time','class_duration','subject','sub_name')

class TestSerializer(serializers.ModelSerializer):
    owner_username=serializers.SerializerMethodField()
    def get_owner_username(self,item):
        print("kya ayayayayay",item.owner)
        return str(item.owner)
    
    test_name=serializers.SerializerMethodField()
    def get_test_name(self,item):
        print("kya test",item.name)
        return str(item.name)

    class Meta:
        model = Test
        fields = ('owner','owner_username','test_id','test_name','subject','name','Total_marks')

class RemarkSerializer(serializers.ModelSerializer):
    student_name=serializers.SerializerMethodField()
    def get_student_name(self,item):
        print("kya sub",item.student)
        return str(item.student)
    teacher_name=serializers.SerializerMethodField()
    def get_teacher_name(self,item):
        print("kya sub",item.teacher)
        return str(item.teacher)

    pro_image=serializers.SerializerMethodField()
    def get_pro_image(self,item):
        print("kya sub",type(item.teacher.image))
        return str(item.teacher.image)

    class Meta:
        model = Remark
        fields = ('id','student_name','teacher_name','pro_image','title','description','teacher','student')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")


class NotifSerializer(serializers.ModelSerializer):
    owner_username=serializers.SerializerMethodField()
    def get_owner_username(self,item):
        print("kya ayayayayay",item.owner)
        return str(item.owner)

    class Meta:
        model = Notification
        fields = ('school','issue_date','owner','owner_username','name','description','file')




class RequestSerializer(serializers.ModelSerializer):

    owner_username=serializers.SerializerMethodField()
    def get_owner_username(self,item):
        print("kya ayayayayay",item.owner)
        return str(item.owner)

    class Meta:
        model = Request
        fields = ('school','owner_username','owner','title','description','noted')

class MarksSerializer(serializers.ModelSerializer):

    total_marks=serializers.SerializerMethodField()
    def get_total_marks(self,item):
        print("kya ayayayayay",item.test.Total_marks)
        return item.test.Total_marks

    subject=serializers.SerializerMethodField()
    def get_subject(self,item):
        print("kya ayayayayay",type(item.test.subject))
        return str(item.test.subject)

    color=serializers.SerializerMethodField()
    def get_color(self,item):
        print("kya color",item.test.subject.color)
        return item.test.subject.color    

    student_name=serializers.SerializerMethodField()
    def get_student_name(self,item):
        print("kya ayayayayay",type(item.student))
        return str(item.student)

    test_name=serializers.SerializerMethodField()
    def get_test_name(self,item):
        print("kya ayayayayay",(item.test.name))
        return str(item.test.name)


    class Meta:
        model = Marks
        fields = ('id','test','test_name','color','student','student_name','subject','Scored_marks','total_marks')



