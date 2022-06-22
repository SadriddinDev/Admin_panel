from django.urls import path
from . import views
try: 
    from django.contrib.contenttypes.models import ContentType
    models_name = [m.name for m in ContentType.objects.filter(app_label='edu_app')]
except: models_name = []


urlpatterns = [
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),
    path('courses/', views.courses, name="courses"),
    path('index/', views.index, name="index"),
    path('teachers/', views.teachers, name="teachers"),

    # my admin
    path('logout/', views.logout, name="logout"),
    path('admin/', views.loginAdmin, name="login_admin"),
    path('admin/main/', views.mainAdmin, name="main_admin"),
    path('admin/main/bolim_qoshish', views.bolim_qoshish, name="bolim_qoshish"),

    # models
    path('admin/main/main_image/', views.main_image, name="main_image"),
    path('admin/main/teacher/', views.teacher, name="teacher"),
    path('admin/main/course/', views.course, name="course"),
    path('admin/main/learning_material/', views.learning_material, name="learning_material"),
    path('admin/main/message/', views.message, name="message"),
    path('admin/main/who_we_are/', views.who_we_are, name="who_we_are"),
    path('admin/main/new/', views.new, name="new"),
    path('admin/main/comment/', views.comment, name="comment"),

    # change_data
    path('admin/main/bolim_qoshish/<int:id>/', views.bolim_qoshish_change_data, name="bolim_qoshish_change_data"),
    path('admin/main/main_image/<int:id>/', views.main_image_change_data, name="main_image_change_data"),
    path('admin/main/teacher/<int:id>/', views.teacher_change_data, name='teacher_change_data'),
    path('admin/main/course/<int:id>/', views.course_change_data, name="course_change_data"),
    path('admin/main/learning_material/<int:id>/', views.learning_material_change_data, name="learning_material_change_data"),
    path('admin/main/message/<int:id>/', views.message_change_data, name="message_change_data"),
    path('admin/main/who_we_are/<int:id>/', views.who_we_are_change_data, name="who_we_are_change_data"),
    path('admin/main/new/<int:id>/', views.new_change_data, name="new_change_data"),
    path('admin/main/comment/<int:id>/', views.comment_change_data, name="comment_change_data"),

    # create data
    path('admin/main/bolim_qoshish/new/', views.bolim_qoshish_new_data, name="bolim_qoshish_new_data"),
    path('admin/main/main_image/new/', views.main_image_new_data, name="main_image_new_data"),
    path('admin/main/teacher/new/', views.teacher_new_data, name='teacher_new_data'),
    path('admin/main/course/new/', views.course_new_data, name="course_new_data"),
    path('admin/main/learning_material/new/', views.learning_material_new_data, name="learning_material_new_data"),
    path('admin/main/message/new/', views.message_new_data, name="message_new_data"),
    path('admin/main/who_we_are/new/', views.who_we_are_new_data, name="who_we_are_new_data"),
    path('admin/main/new/new/', views.new_new_data, name="new_new_data"),
    path('admin/main/comment/new/', views.comment_new_data, name="comment_new_data"),

]
