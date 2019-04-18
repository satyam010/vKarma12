from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from classroom.views import classroom, students, teachers, parents, adminV
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('', include('classroom.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/student/', students.StudentSignUpView, name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView, name='teacher_signup'),
    path('accounts/signup/parent/', parents.ParentSignUpView, name='parent_signup'),
    path('accounts/signup/admin/', adminV.AdminSignUpView.as_view(), name='signup'),
    #path('api/token/', TokenObtainPairView.as_view()),
    #path('api/token/refresh/', TokenRefreshView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
