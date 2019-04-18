from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import parent_required, admin_required
from ..forms import ParentSignUpForm,ParentSignUpTwo, ParentEditForm, ParentEditFormTwo,RequestCreateForm

from ..models import Student, User, Parent,Timetable,Marks,Subject,Request,Notification

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def change_password(request):
    notification = Notification.objects.filter(school=request.user.school)[:5]
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('parents:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'classroom/change_password.html', {
        'form': form, 'notification':notification
    })

@login_required
@admin_required
def ParentSignUpView(request):
    school = request.user.school
    if request.method == 'POST':
        main_form = ParentSignUpForm(request.POST)
        secondary_form = ParentSignUpTwo(request.user,request.POST,request.FILES)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save(school)
            secondary_form.save(user)
            return redirect('admin:admin_home')
    else:
        main_form = ParentSignUpForm()
        secondary_form = ParentSignUpTwo(request.user)
    return render(request, 'classroom/registration/parent_register.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })

@login_required
@admin_required
def ParentEditView(request,username):
    if request.method == 'POST':
        edit_form = ParentEditForm(request.POST)
        edit_form_two = ParentEditFormTwo(username, request.POST,request.FILES)
        if edit_form.is_valid() and edit_form_two.is_valid():
            user = edit_form.save(username)
            edit_form_two.save(username)
            return redirect('admin:admin_home')
    else:
        edit_form = ParentEditForm()
        edit_form_two = ParentEditFormTwo(request.user)
    return render(request, 'classroom/registration/parent_edit.html', {
        'edit_form': edit_form,
        'edit_form_two': edit_form_two
    })

@method_decorator([login_required, parent_required], name='dispatch')
class ParentHomeView(ListView):
    model = Parent
    # ordering = ('name', )
    context_object_name = 'parent'
    template_name = 'classroom/parents/parent_home.html'

    def get_context_data(self,**kwargs):
        parent = Parent.objects.filter(pk=self.request.user)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        user = self.request.user
        return {'parent':parent, 'user': user, 'notification':notification}


@method_decorator([login_required], name='dispatch')
class TimetableListView(ListView):
    model = Timetable
    template_name = 'classroom/parents/timetable.html'

    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=request.user.school)[:5]
        parent = Parent.objects.get(user=self.request.user)
        student = Student.objects.get(user=parent__child__user)
        timetable = Timetable.objects.filter(batch=student.batch)
        return {'timetable':timetable,'user':self.request.user, 'notification':notification}


class ProfileView(ListView):
    model = Parent
    context_object_name = 'parent'
    template_name = 'classroom/parents/child_profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        parent = Parent.objects.filter(user=user)
        notification = Notification.objects.filter(school=user.school)[:5]
        return {'parent': parent, 'user': user, 'notification':notification}

class ProfileView1(ListView):
    model = Parent
    context_object_name = 'parent'
    template_name = 'classroom/parents/parent_profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        parent = Parent.objects.filter(user=user)
        notification = Notification.objects.filter(school=user.school)[:5]
        return {'parent': parent, 'user': user, 'notification':notification}


class MarksView(ListView):
    model = Marks
    context_object_name = 'marks'
    template_name = 'classroom/parents/child_marks.html'

    def get_context_data(self, **kwargs):
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'notification':notification}


def selectAttendanceSubject(request):
    Subjects = Subject.objects.all();
    notification = Notification.objects.filter(school=request.user.school)[:5]
    print(Subjects)
    return render(request,'classroom/parents/select-subject.html',{
        'subjects':Subjects, 'notification':notification
        })

@method_decorator([login_required], name='dispatch')
class RequestView(ListView):
    model = Request
    context_object_name = 'requests'
    template_name = 'classroom/parents/requests_list.html'

    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        requests = Request.objects.filter(owner=self.request.user)

        return {'requests':requests, 'notification':notification}

@method_decorator([login_required], name='dispatch')
class NotificationView(ListView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'classroom/parents/parent_notification.html'
    
    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school)

        return {'notification':notification}

@login_required
def RequestCreateView(request):
    if request.method == 'POST':
        form = RequestCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('parents:requests')
    else:
        form = RequestCreateForm()
    return render(request, 'classroom/parents/request_create.html', {
        'form':form,'user':request.user
    })