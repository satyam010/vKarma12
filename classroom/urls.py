from django.urls import include, path

from .views import classroom, students, teachers, parents, adminV
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('subjects', students.SubjectView)
router.register('batches', students.BatchView)
router.register('students', students.StudentView)
router.register('parents', students.ParentView)
router.register('teachers', students.TeacherView)
router.register('notifications', students.NotifView)
router.register('homeworks', students.HomeworkView)
router.register('tests', students.TestView)
router.register('marks', students.MarkView)
router.register('timetable', students.TimetableView)
router.register('remarks', students.RemarkView)
router.register('requests', students.ReqView)
router.register('attendance', students.StudentAttendance)
# router.register('getcurrentuser', students.GetCurrentLoginUser)

urlpatterns = [
    path('', classroom.home, name='home'),
    path('api/', include(router.urls)),
    path('api/getcurrentuser/',students.GetCurrentLoginUser.as_view()),
    path('students/', include(([
        path('', students.StudentHomeView.as_view(), name='student_home'),
        path('notifications/', students.NotificationView.as_view(), name='notifications'),
        path('marks/', students.MarksView.as_view(), name='marks'),
        path('select-subject', students.selectAttendanceSubject, name='select_subject'),
        path('attendance/<subject>/', students.AttendanceView, name='attendance'),
        path('password-change/',students.change_password,name='change_password'),
        path('student_edit/<username>', students.StudentEditView, name='student_edit'),
        path('remark/', teachers.RemarkView.as_view(), name='teacher_remark'),
        path('request/', students.RequestView.as_view(), name='requests'),
        path('request/create/', students.RequestCreateView, name='request_create'),
        path('profile/', students.ProfileView.as_view(), name='profile'),
        path('timetable/',students.TimetableListView.as_view(),name='timetable'),
        path('attendance/pie/<subject>', students.PieChartView, name='pie'),
        path('attendance/scatter/<subject>', students.ScatterPlotView, name='scatter'),
        path('marks/chart/<marks>', students.MarksPlot, name='chart'),
        path('topper/select-subject/', students.TopperMarksView.as_view(), name='topper'),
        path('topper/comparison/<subject>', students.SelectTestView, name='comparison'),
        path('topper/compare/<subject>/<test>/', students.ComparisonView, name='compare'),

    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('remark/', teachers.RemarkView.as_view(), name='teacher_remark'),
        path('remark/create/', teachers.RemarkBatchSelect, name='remark_batch'),
        path('remark/create/<batch>/', teachers.RemarkStudentSelect, name='remark_student'),
        path('remark/create/<batch>/<student_id>', teachers.RemarkCreateView, name='remark_create'),
        path('request/', teachers.RequestView.as_view(), name='requests'),
        path('request/create', teachers.RequestCreateView, name='request_create'),
        path('timetable/',teachers.TimetableListView.as_view(),name='timetable'),
        path('', teachers.TeacherHomeView.as_view(), name='teacher_home'),
        path('homework/add/', teachers.QuizCreateView, name='homework_add'),
        path('notifications/', teachers.NotificationView.as_view(), name='notifications'),
        path('tests/', teachers.TestListView.as_view(), name='tests'),
        path('tests/create-test', teachers.TestCreateView.as_view(), name='create_test'),
        path('tests/<test>/', teachers.selectMarksBatch, name='marks_batches'),
        path('tests/<test>/<batch>/', teachers.StudentsListView, name='marks_list'),
        path('attendance/select-batch', teachers.selectAttendanceBatch, name='attendance-select'),
        path('attendance/<batch>/', teachers.selectAttendanceSubject, name='attendance-subject'),
        path('attendance/<batch>/<subject>/', teachers.AttendanceCreateView, name='attendance'),
        path('password-change/',teachers.change_password,name='change_password'),
        path('teacher_edit/<username>/', teachers.TeacherEditView, name='teacher_edit'),
        path('profile/', teachers.ProfileView.as_view(), name='profile'),
    ], 'classroom'), namespace='teachers')),

    path('parents/', include(([
        path('', parents.ParentHomeView.as_view(), name='parent_home'),
        path('password-change/',parents.change_password,name='change_password'),
        path('parent_edit/<username>/',parents.ParentEditView, name='parent_edit'),
        path('request/', parents.RequestView.as_view(), name='requests'),
        path('request/create', parents.RequestCreateView, name='request_create'),
        path('remark/', teachers.RemarkView.as_view(), name='teacher_remark'),
        path('profile/', parents.ProfileView.as_view(), name='profile'),
        path('profile1/', parents.ProfileView1.as_view(), name='profile1'),
        path('marks/', parents.MarksView.as_view(), name='marks'),
        path('select-subject', parents.selectAttendanceSubject, name='select_subject'),
        path('password-change/',parents.change_password,name='change_password'),
        path('notifications/', parents.NotificationView.as_view(), name='notifications'),
        path('timetable/',students.TimetableListView.as_view(),name='timetable'),

    ], 'classroom'), namespace='parents')),
    path('admin/', include(([
        path('', adminV.AdminHomeView.as_view(), name='admin_home'),
        path('notification/add/', adminV.NotificationCreateView.as_view(), name='notification_add'),
        path('batches/add/', adminV.BatchCreateView.as_view(), name='batch_create'),
        path('users_add/', adminV.UsersCreateView.as_view(), name='users_add'),
        path('subject_add/', adminV.SubjectCreateView.as_view(), name='subject_add'),
        path('edit/<int:user_id>', adminV.EditView, name='edit'),
        path('request/', adminV.RequestView.as_view(), name='requests'),
        path('timetable/',adminV.TimetableListView.as_view(),name='timetable'),
        path('timetable/create/',adminV.TimetableCreateView,name='timetable_create'),
        path('notifications/', adminV.NotificationView.as_view(), name='notifications'),
        path('subjects/',adminV.SubjectListView.as_view(),name='subjects'),
        path('batches',adminV.BatchListView.as_view(),name='batches')

    ], 'classroom'), namespace='admin')),
]
