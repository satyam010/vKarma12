from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..decorators import admin_required
from ..forms import AdminSignUpForm,TimetableCreateForm
from ..models import *
from django.core import serializers
import datetime

class NotificationView(ListView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'classroom/admin/notifications.html'
    
    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        print(notification)
        return {'notification':notification}

class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Admin.objects.create(user=user)
        login(self.request, user)
        return redirect('admin:admin_home')

@method_decorator([login_required, admin_required], name='dispatch')
class AdminHomeView(ListView):
    model = User
    template_name = 'classroom/admin/admin_home.html'
    # context_object_name = 'users_normal'
    paginate_by = 50



    def get_context_data(self, **kwargs):
        context = super(AdminHomeView, self).get_context_data(**kwargs)
        p = Paginator(User.objects.filter(school=self.request.user.school,is_admin=False),self.paginate_by)
        context['users_normal'] = p.page(context['page_obj'].number)
        users = User.objects.filter(school=self.request.user.school,is_admin=False)
        j_arr = []
        Students = Student.objects.filter(user__school=self.request.user.school)
        Teachers = Teacher.objects.filter(user__school=self.request.user.school)
        Parents = Parent.objects.filter(user__school=self.request.user.school)
        paginator = Paginator(users, 50)
        for user in users:
            j_arr.append(user.firstName + ' ' + user.lastName)
        users_json = serializers.serialize('json', users)
        notifs = Notification.objects.filter(school=self.request.user.school).order_by('-issue_date')[:5]
        requests = Request.objects.filter(school=self.request.user.school)[:10]
        x = {'users':users_json ,'j_arr':j_arr,'parents':Parents,'students':Students,
        'teachers':Teachers,'notifs':notifs,'requests':requests,'page_range':paginator.page_range,'max_page':paginator.num_pages}
        
        return {**context,**x}

@method_decorator([login_required, admin_required], name='dispatch')
class NotificationCreateView(CreateView):
    model = Notification
    fields = ('name', 'description', 'file', )
    template_name = 'classroom/admin/notification_add_form.html'

    def form_valid(self, form):
        notification = form.save(commit=False)
        notification.owner = self.request.user
        notification.issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        notification.school = self.request.user.school
        notification.save()
        messages.success(self.request, 'The notification was created successfully!')
        return redirect('admin:admin_home')

@method_decorator([login_required, admin_required], name='dispatch')
class BatchCreateView(CreateView):
    model = Batch
    fields = ('name',)
    template_name = 'classroom/admin/batch_create_form.html'

    def form_valid(self, form):
        batch = form.save(commit=False)
        batch.school = self.request.user.school
        batch.save()
        messages.success(self.request, 'The batch %s was created Succesfully !'%batch.name)
        return redirect('admin:admin_home')

@method_decorator([login_required, admin_required], name='dispatch')
class UsersCreateView(ListView):
    model = User
    # fields = ('user', )
    template_name = 'classroom/registration/signup.html'

@method_decorator([login_required, admin_required], name='dispatch')
class SubjectCreateView(CreateView):
    model = Subject
    fields = ('name', 'color', )
    template_name = 'classroom/admin/subject_add_form.html'

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.school = self.request.user.school
        subject.save()
        messages.success(self.request, 'Subject created successfully!')
        return redirect('admin:admin_home')

def EditView(request, user_id):
    username = User.objects.get(pk=user_id)
    student = Student.objects.get(pk=user_id)
    batches = Batch.objects.all()
    return HttpResponse(username)


@login_required
@admin_required
def TimetableCreateView(request):
    if request.method == "POST":
        form = TimetableCreateForm(request.user,request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Schedule created successfully!')
            return redirect('admin:timetable')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = TimetableCreateForm(request.user)
    return render(request, 'classroom/admin/timetable_create.html', {
        'form': form
    })
@method_decorator([login_required], name='dispatch')
class TimetableListView(ListView):
    model = Timetable
    template_name = 'classroom/admin/timetable.html'

    def get_context_data(self,**kwargs):
        timetable = Timetable.objects.all()
        return {'timetable':timetable,'user':self.request.user}

@method_decorator([login_required,admin_required], name='dispatch')
class SubjectListView(ListView):
    model = Subject
    template_name = 'classroom/admin/subjects.html'

    def get_context_data(self,**kwargs):
        subjects = Subject.objects.filter(school=self.request.user.school)
        return {'subjects' : subjects}

@method_decorator([login_required,admin_required], name='dispatch')
class BatchListView(ListView):
    model = Batch
    template_name = 'classroom/admin/batches.html'

    def get_context_data(self,**kwargs):
        Batches = Batch.objects.filter(school=self.request.user.school)
        query_object = {}
        for batch in Batches:
            query_object[batch] = Student.objects.filter(batch=batch).count()  
        return {'query_object' : query_object}

@method_decorator([login_required,admin_required], name='dispatch')
class RequestView(ListView):
    model = Request
    context_object_name = 'requests'
    template_name = 'classroom/admin/requests_list.html'

    def get_context_data(self,**kwargs):
        requests = Request.objects.filter(school=self.request.user.school)
        return {'requests':requests}