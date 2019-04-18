from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import formset_factory
from classroom.models import *
import datetime
from bootstrap_datepicker_plus import DateTimePickerInput

SCHOOLS = [('Bhartiya Vidyapeeth School', 'Bhartiya Vidyapeeth School'),('Cambridge School Indirapuram','Cambridge School Indirapuram')]
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('firstName','lastName',)

    def save(self,school):
        user = super().save(commit=False)
        user.is_teacher = True
        Teacher_number = User.objects.filter(is_teacher=True).count() + 1
        roll_no = '0'*(4 - len(str(Teacher_number))) + str(Teacher_number)
        user.school = school
        user.save()
        user_ins = User.objects.get(username = self.instance)
        self.instance.username = 'VK'+ school + 'T' + roll_no
        self.instance.save()
        user.save()
        return user

class ParentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('firstName','lastName',)

    def save(self,school):
        user = super().save(commit=False)
        user.is_parent = True
        Parent_number = User.objects.filter(is_parent=True).count() + 1
        roll_no = '0'*(4 - len(str(Parent_number))) + str(Parent_number)
        user.school = school
        user.save()
        user_ins = User.objects.get(username = self.instance)
        self.instance.username = 'VK'+ school + 'P' + roll_no
        self.instance.save()
        return user

class ParentSignUpTwo(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('child','email','phone_number','address','image',)
        widgets = {
            'chils': forms.Select(),
        }
    def __init__(self, user, *args, **kwargs):
        super(ParentSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['child'].queryset = Student.objects.filter(user__school = user.school)

    def save(self,user):
        self.fields['user'] = user
        child = self.cleaned_data['child']
        email = self.cleaned_data['email']
        image = self.cleaned_data['image']
        phone_number = self.cleaned_data['phone_number']
        address = self.cleaned_data['address']
        parent = Parent.objects.create(user=user,child=child,email=email,
            phone_number=phone_number,address=address,image=image)

class StudentSignUpTwo(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('batch','email','phone_number','dob','address','age','image',)


    def __init__(self, user, *args, **kwargs):
        super(StudentSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(school=user.school)

    def save(self,user):
        self.fields['user'] = user
        batch = self.cleaned_data['batch']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        dob = self.cleaned_data['dob']
        address = self.cleaned_data['address']
        age = self.cleaned_data['age']
        image = self.cleaned_data['image']
        student = Student.objects.create(user=user,batch=batch,email=email,
            phone_number=phone_number,dob=dob,address=address,age=age,image=image)

class TeacherSignUpTwo(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('batch','email','phone_number','image',)
        widgets = {
            'batch': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, user, *args, **kwargs):
        super(TeacherSignUpTwo, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(school=user.school)
        # self.fields["batch"].widget = forms.widgets.CheckboxSelectMultiple()

    def save(self,user):
        self.fields['user'] = user
        batches = self.cleaned_data['batch']
        email = self.cleaned_data['email']
        image = self.cleaned_data['image']
        phone_number = self.cleaned_data['phone_number']
        teacher = Teacher.objects.create(user=user,email=email,
            phone_number=phone_number,image=image)
        teacher.batch.set(batches)

class AdminSignUpForm(UserCreationForm):
    school = forms.CharField(label='select school:', widget=forms.Select(choices=SCHOOLS))
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        user.school = ''.join([ i[0] for i in self.cleaned_data['school'].split(' ')])
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    # SCHOOLS = [('school1', 'school1'), ('school2', 'school2')]
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('firstName','lastName',)

    @transaction.atomic
    def save(self,school):
        Student_number = Student.objects.all().count() + 1
        roll_no = '0'*(4 - len(str(Student_number))) + str(Student_number)
        user = super().save(commit=False)
        user.is_student = True
        user.school = school
        user.save()
        user_ins = User.objects.get(username = self.instance)
        self.instance.username = 'VK'+ school + 'S' + roll_no
        self.instance.save()
        return user

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('firstName','lastName',)

    @transaction.atomic
    def save(self, user):
        user_ins = User.objects.get(username = user)
        user_ins.firstName = self.cleaned_data['firstName']
        user_ins.lastName = self.cleaned_data['lastName']
        user_ins.save()
        return user_ins

class StudentEditFormTwo(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('batch','email','phone_number','dob','address','age','image',)

    def __init__(self, username, *args, **kwargs):
        super(StudentEditFormTwo, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(school=User.objects.get(username=username).school)

    def save(self, username):
        self.fields['user'] = User.objects.get(username=username)
        student = Student.objects.get(user__username=username)
        student.batch = self.cleaned_data['batch']
        student.email = self.cleaned_data['email']
        student.phone_number = self.cleaned_data['phone_number']
        student.dob = self.cleaned_data['dob']
        student.image = self.cleaned_data['image']
        student.address = self.cleaned_data['address']
        student.age = self.cleaned_data['age']
        student.save()

class ParentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('firstName','lastName',)

    @transaction.atomic
    def save(self, user):
        user_ins = User.objects.get(username = user)
        user_ins.firstName = self.cleaned_data['firstName']
        user_ins.lastName = self.cleaned_data['lastName']
        user_ins.save()
        return user_ins

class ParentEditFormTwo(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('child','email','phone_number','address','image',)

    def __init__(self, user, *args, **kwargs):
        super(ParentEditFormTwo, self).__init__(*args, **kwargs)
        self.fields['child'].queryset = Student.objects.filter(user__school = User.objects.get(username=user).school)

    def save(self, user):
        self.fields['user'] = User.objects.get(username=user)
        parent = Parent.objects.get(user__username=user)
        parent.child = self.cleaned_data['child']
        parent.email = self.cleaned_data['email']
        parent.image = self.cleaned_data['image']
        parent.phone_number = self.cleaned_data['phone_number']
        parent.address = self.cleaned_data['address']
        parent.save()

class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('firstName','lastName',)

    @transaction.atomic
    def save(self, user):
        user_ins = User.objects.get(username = user)
        user_ins.firstName = self.cleaned_data['firstName']
        user_ins.lastName = self.cleaned_data['lastName']
        user_ins.save()
        return user_ins

class TeacherEditFormTwo(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('batch','email','phone_number','image',)

    def __init__(self, username, *args, **kwargs):
        super(TeacherEditFormTwo, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(school=User.objects.get(username=username).school)

    def save(self, username):
        self.fields['user'] = User.objects.get(username=username)
        teacher = Teacher.objects.get(user__username=username)
        batches = self.cleaned_data['batch']
        teacher.email = self.cleaned_data['email']
        teacher.phone_number = self.cleaned_data['phone_number']
        teacher.image = self.cleaned_data['image']
        teacher.batch.set(batches)
        teacher.save()

class AttendanceForm(forms.ModelForm):
    present = forms.BooleanField(required=True, label="Check this")
    class Meta:
        model = Attendance
        fields = ('present',)

    @transaction.atomic
    def save(self,student,subject):
        try:
            attendance = Attendance.objects.get(class_date = datetime.datetime.now().strftime("%Y-%m-%d"),
                student=student,Subject=Subject.objects.get(name=subject))
#             attendance.Subject = Subject.objects.get(name=subject)
#             attendance.class_date = datetime.datetime.now().strftime("%Y-%m-%d")

            attendance.present = self.cleaned_data.get('present')
            attendance.save()
        except:
            Attendance.objects.create(student=student,
                Subject=Subject.objects.get(name=subject,school=student.user.school),class_date = datetime.datetime.now().strftime("%Y-%m-%d"),
                present=self.cleaned_data.get('present'))

class MarksCreateForm(forms.ModelForm):
    class Meta:
       model = Marks
       fields = ('Scored_marks',)
    @transaction.atomic
    def save(self,test,student):
        try:
            marks = Marks.objects.get(test=Test.objects.get(test_id=test),
                student=student)
            marks.Scored_marks = self.cleaned_data.get('Scored_marks')
            marks.save()
        except:
            Marks.objects.create(test=Test.objects.get(test_id=test),
                student=student,
                    Scored_marks=self.cleaned_data.get('Scored_marks'))

class HomeworkCreateForm(forms.ModelForm):
    deadline = forms.DateField(
    widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
)
    class Meta:
        model = Homework
        fields = ('name', 'subject','batch', 'description', 'deadline', 'file',)

    def save(self, user):
        owner = user
        school = user.school
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        name = self.cleaned_data['name']
        subject = self.cleaned_data['subject']
        description = self.cleaned_data['description']
        deadline = self.cleaned_data['deadline']
        file = self.cleaned_data['file']
        Homework.objects.create(owner=owner, school=school, issue_date=issue_date, name=name, subject=subject, description=description, deadline=deadline, file=file)

    def __init__(self, user, *args, **kwargs):
        super(HomeworkCreateForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(school = user.school)
        teacher = Teacher.objects.get(user=user)
        self.fields['batch'].queryset = teacher.batch.all()

class RemarkCreateForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('title','description',)

    @transaction.atomic
    def save(self,teacher,student_id):
        student = Student.objects.get(user__username=student_id)
        teacher = Teacher.objects.get(user=teacher)
        title = self.cleaned_data['title']
        description=self.cleaned_data['description']
        Remark.objects.create(teacher=teacher,student=student,title=title,description=description)

class RequestCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title','description',)

    @transaction.atomic
    def save(self,owner):
        school = owner.school
        owner = owner
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        Request.objects.create(school=school,owner=owner,title=title,description=description)


class TimetableCreateForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ('batch','start_time','class_duration','subject','teacher',)
        widgets = {'start_time': DateTimePickerInput(),}


    def save(self, user):
        school = user.school
        batch = self.cleaned_data['batch']
        subject = self.cleaned_data['subject']
        class_duration = self.cleaned_data['class_duration']
        teacher = self.cleaned_data['teacher']
        start_time = self.cleaned_data['start_time']
        Timetable.objects.create(school=school,batch=batch,start_time=start_time,
            class_duration=class_duration,teacher=teacher,subject=subject)

    def __init__(self, user, *args, **kwargs):
        super(TimetableCreateForm, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(school = user.school)
        self.fields['teacher'].queryset = Teacher.objects.filter(user__school = user.school)
        self.fields['subject'].queryset = Subject.objects.filter(school=user.school)

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('subject','name','Total_marks',)

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(TestCreateForm, self).__init__(*args, **kwargs)
       self.fields['subject'].queryset = Subject.objects.filter(school=user.school)