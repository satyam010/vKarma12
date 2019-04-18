from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..decorators import teacher_required, admin_required
from ..forms import TeacherSignUpForm,TeacherSignUpTwo,AttendanceForm,MarksCreateForm,HomeworkCreateForm,TeacherEditForm, TeacherEditFormTwo,RemarkCreateForm,RequestCreateForm,TestCreateForm
from ..models import User, Student, Homework, Notification, Marks, Subject, Attendance,Teacher,Batch,Marks,Test,Remark,Request,Timetable
from django.forms import formset_factory
@login_required
def change_password(request):
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('teachers:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'classroom/teachers/change_password.html', {
        'form': form, 'notification':notification
    })

@login_required
@admin_required
def TeacherSignUpView(request):
    school = request.user.school
    if request.method == 'POST':
        main_form = TeacherSignUpForm(request.POST)
        secondary_form = TeacherSignUpTwo(request.user,request.POST,request.FILES)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save(school)
            secondary_form.save(user)
            return redirect('admin:admin_home')
    else:
        main_form = TeacherSignUpForm()
        secondary_form = TeacherSignUpTwo(request.user)
    return render(request, 'classroom/registration/teacher_register.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })

@login_required
@admin_required
def TeacherEditView(request,username):
    if request.method == 'POST':
        edit_form = TeacherEditForm(request.POST)
        edit_form_two = TeacherEditFormTwo(username, request.POST,request.FILES)
        if edit_form.is_valid() and edit_form_two.is_valid():
            user = edit_form.save(username)
            edit_form_two.save(username)
            return redirect('admin:admin_home')
    else:
        edit_form = TeacherEditForm()
        edit_form_two = TeacherEditFormTwo(request.user)
    return render(request, 'classroom/registration/parent_edit.html', {
        'edit_form': edit_form,
        'edit_form_two': edit_form_two
    })

class ProfileView(ListView):
    model = Teacher
    context_object_name = 'teacher'
    template_name = 'classroom/teachers/teacher_profile.html'

    def get_context_data(self, **kwargs):
        notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
        user = self.request.user
        teacher = Teacher.objects.filter(user=user)
        return {'teacher': teacher, 'user': user, 'notification':notification}

@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherHomeView(ListView):
    model = Homework
    # ordering = ('name', )
    context_object_name = 'homework'
    template_name = 'classroom/teachers/teacher_home.html'

    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        homework = Homework.objects.filter(owner=self.request.user)
        user = self.request.user
        return {'homework':homework, 'user': user, 'notification':notification}

class ProfileView(ListView):
    model = Teacher
    context_object_name = 'teacher'
    template_name = 'classroom/teachers/teacher_profile.html'

    def get_context_data(self, **kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        user = self.request.user
        teacher = Teacher.objects.filter(user=user)
        return {'teacher': teacher, 'user': user, 'notification':notification}

@login_required
@teacher_required
def QuizCreateView(request):
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    if request.method == 'POST':
        form = HomeworkCreateForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return redirect('teachers:teacher_home')
    else:
        form = HomeworkCreateForm(request.user)
    return render(request, 'classroom/teachers/quiz_add_form.html', {
        'form':form, 'notification':notification
    })

@login_required
@teacher_required
def AttendanceCreateView(request,batch,subject):
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    students = Student.objects.filter(batch__name=batch)
    AttendanceFormset = formset_factory(AttendanceForm,extra=students.count())
    present = Attendance.objects.filter(class_date=datetime.datetime.now().strftime("%Y-%m-%d")
        ,student__batch__name=batch,present=True,Subject__name=subject)
    present_students = [a.student for a in present]
    students_query = {}
    present_list = [False]*students.count()
    for student in students:
        students_query[student] = False
    for student in present_students:
        students_query[student] = True
    for i,student in enumerate(students):
        if students_query[student] == True:
            present_list[i] = True

    if request.method == 'POST':
        formset = AttendanceFormset(request.POST)
        if formset.is_valid():
            for i,form in enumerate(formset):
                form.save(students[i],subject)
            return redirect('teachers:attendance',batch=batch,subject=subject)
    else:
        formset = AttendanceFormset()

    return render(request, 'classroom/teachers/mark-attendance.html', {
        'students' : zip(students,present_list,formset),'batch':batch,'subject':subject,
        'form':formset, 'notification':notification
    })


@login_required
@teacher_required
def selectAttendanceBatch(request):
    teacher = Teacher.objects.filter(user = request.user)[0]
    batches = teacher.batch.all()
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    context_object = {}
    for batch in batches:
        students_in_batch = Student.objects.filter(batch=batch).count()
        context_object[batch] = students_in_batch
    return render(request, 'classroom/teachers/attendance_batches.html', {
        'batches' : context_object, 'notification':notification
    })

def selectAttendanceSubject(request,batch):
    Subjects = Subject.objects.filter(school=request.user.school);
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]

    return render(request,'classroom/teachers/select-subject.html',{
        'subjects':Subjects,'batch':batch, 'notification':notification
        })



class NotificationView(ListView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'classroom/teachers/teacher_notification.html'
    
    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:15]
        return {'notification':notification}

@method_decorator([login_required, teacher_required], name='dispatch')
class TestCreateView(CreateView):
    form_class = TestCreateForm
    
    template_name = 'classroom/teachers/marks/create_test.html'

    def form_valid(self, form):
        test = form.save(commit=False)
        test.owner = self.request.user
        test.test_id = Test.objects.all().count() + 1
        test.save()
        messages.success(self.request, 'Test awarded successfully!')
        return redirect('teachers:tests')

    def get_form_kwargs(self):
        kwargs = super(TestCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

@method_decorator([login_required, teacher_required], name='dispatch')
class TestListView(ListView):
    model = Test
    # ordering = ('name', )
    context_object_name = 'tests'
    template_name = 'classroom/teachers/marks/tests.html'

    def get_context_data(self,**kwargs):
        tests = Test.objects.filter(owner=self.request.user)
        return {'tests':tests}


@login_required
@teacher_required
def StudentsListView(request,test,batch):
    students = Student.objects.filter(batch__name=batch)
    marks = Marks.objects.filter(test__test_id=test,student__batch__name=batch)
    marks = [[mark.student,mark.Scored_marks] for mark in marks]
    students = Student.objects.filter(batch__name=batch)
    MarksFormset = formset_factory(MarksCreateForm,extra=students.count())
    students_query = {}
    marks_list = [0]*students.count()

    for student in students:
        students_query[student] = 0
    for obj in marks:
        students_query[obj[0]] = obj[1]
    for i,student in enumerate(students):
        marks_list[i] = students_query[student]

    if request.method == 'POST':
        formset = MarksFormset(request.POST)
        if formset.is_valid():
            for i,form in enumerate(formset):
                form.save(test,students[i])
            return redirect('teachers:marks_list',test=test,batch=batch)
    else:
        formset = MarksFormset()

    return render(request, 'classroom/teachers/marks/marks_list.html', {
        'students_query' : zip(students,marks_list,formset),
        'batch':batch,'test':test,'form':formset
})

@login_required
@teacher_required
def selectMarksBatch(request,test):
    teacher = Teacher.objects.filter(user = request.user)[0]
    batches = teacher.batch.all()
    context_object = {}
    for batch in batches:
        context_object[batch] = Student.objects.filter(batch=batch).count()
    return render(request, 'classroom/teachers/marks/marks_batches.html', {
        'batches' : context_object,'test':test
    })




@method_decorator([login_required], name='dispatch')
class RemarkView(ListView):
    model = Remark
    context_object_name = 'remarks'
    template_name = 'classroom/teachers/remark/remarks_list.html'

    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        if(self.request.user.is_teacher):
            remarks = Remark.objects.filter(teacher__user=self.request.user)
        elif(self.request.user.is_student):
            remarks = Remark.objects.filter(student__user=self.request.user)
        if(self.request.user.is_parent):
            parent_child = Parent.objects.get(child__user=self.request.user)
            remarks = Remark.objects.filter(student__user=parent_child)
        return {'remarks':remarks,'user':self.request.user,'notification':notification}

@login_required
@teacher_required
def RemarkCreateView(request,batch,student_id):
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    if request.method == 'POST':
        form = RemarkCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user,student_id)
            return redirect('teachers:remark_batch')
    else:
        form = RemarkCreateForm()
    return render(request, 'classroom/teachers/remark/remark_create.html', {
        'form': form,'batch':batch,'student_id':student_id,'notification':notification
    })

@login_required
@teacher_required
def RemarkBatchSelect(request):
    batches = Teacher.objects.get(user=request.user).batch.all()
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    context_object = {}
    for batch in batches:
        students_in_batch = Student.objects.filter(batch=batch).count()
        context_object[batch] = students_in_batch
    return render(request, 'classroom/teachers/remark/remark_batches.html', {
        'batches' : context_object,'notification':notification
    })

@login_required
@teacher_required
def RemarkStudentSelect(request,batch):
    notification = Notification.objects.filter(school=request.user.school).order_by('-issue_date')[:5]
    students = Student.objects.filter(batch__name=batch)
    return render(request, 'classroom/teachers/remark/remark_student.html', {
        'students' : students,'batch':batch,'notification':notification
    })

@login_required
def RequestCreateView(request):
    if request.method == 'POST':
        form = RequestCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('teachers:requests')
    else:
        form = RequestCreateForm()
    return render(request, 'classroom/teachers/request_create.html', {
        'form':form,'user':request.user
    })



@method_decorator([login_required], name='dispatch')
class RequestView(ListView):
    model = Request
    context_object_name = 'requests'
    template_name = 'classroom/teachers/requests_list.html'

    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        requests = Request.objects.filter(owner=self.request.user)
        return {'requests':requests,'notification':notification}


@method_decorator([login_required], name='dispatch')
class TimetableListView(ListView):
    model = Timetable
    template_name = 'classroom/teachers/timetable.html'

    def get_context_data(self,**kwargs):
        timetable = Timetable.objects.filter(teacher__user=self.request.user)
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        return {'timetable':timetable,'user':self.request.user,'notification':notification}