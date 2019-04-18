from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:teacher_home')
        elif request.user.is_student:
            return redirect('students:student_home')
        elif request.user.is_admin:
            return redirect('admin:admin_home')
        else:
            return redirect('parents:parent_home')
    return render(request, 'classroom/home.html')
