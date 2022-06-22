from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from .models import Comment, Course, LearningMaterial, MainImage, Message, New, Teacher, WhoWeAre, BolimQoshish
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.paginator import Paginator
try:
    from django.contrib.contenttypes.models import ContentType
except:
    pass


def about(request):

    context = {
        'bolim_qoshish': BolimQoshish.objects.all(),
        'active': 'about',
        'main_images': MainImage.objects.all(),
    }
    return render(request, 'about.html', context)


def blog(request):

    context = {
        'bolim_qoshish': BolimQoshish.objects.all(),
        'active': 'blog',
        'main_images': MainImage.objects.all(),
    }
    return render(request, 'blog.html', context)


def courses(request):

    context = {
        'bolim_qoshish': BolimQoshish.objects.all(),
        'active': 'courses',
        'main_images': MainImage.objects.all(),
    }
    return render(request, 'courses.html', context)


def index(request):

    try:
        news = New.objects.all().order_by('-date')[:3]
    except:
        try:
            news = New.objects.all().order_by('-date')
        except:
            news = None
    try:
        materials = LearningMaterial.objects.all().order_by('-date')
    except:
        materials = None
    try:
        courses = Course.objects.all().order_by('-date')[:8]
    except:
        try:
            courses = Course.objects.all().order_by('-date')
        except:
            courses = None
    try:
        teachers = Teacher.objects.all().order_by('-date')[:9]
    except:
        try:
            teachers = Teacher.objects.all().order_by('-date')
        except:
            teachers = None
    context = {
        'bolim_qoshish': BolimQoshish.objects.all(),
        'active': 'index',
        'main_images': MainImage.objects.all(),
        "news": news,
        "materials": materials,
        "courses": courses,
        "teachers": teachers,
    }
    return render(request, 'index.html', context)


def teachers(request):

    context = {
        'bolim_qoshish': BolimQoshish.objects.all(),
        'active': 'teachers',
        'main_images': MainImage.objects.all(),
    }
    return render(request, 'teachers.html', context)

# Admin

def bolim_qoshish(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('bolim_qoshish')
        BolimQoshish.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('bolim_qoshish')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in BolimQoshish._meta.fields]
    count = 10
    pages = Paginator(BolimQoshish.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'bolim_qoshish')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/bolim_qoshish.html', context=context)



def bolim_qoshish_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = BolimQoshish.objects.get(id=id)
            BolimQoshish.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('bolim_qoshish')
        else:
            try:
                print(request.POST.get('bolim_qoshish'))
                new_data = BolimQoshish.objects.get(id=id)
                new_data.bolim_nomi = request.POST.get('bolim_nomi')
                new_data.url_manzil = request.POST.get('url_manzil')
                new_data.save()

                messages.success(
                    request, f"{BolimQoshish.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('bolim_qoshish')
            except:
                messages.error(
                    request, f"{BolimQoshish.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in BolimQoshish._meta.fields]
    data = BolimQoshish.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'bolim_qoshish',
        'right_url': [('Dashboard', 'main_admin'), ('Bolim qoshish', 'bolim_qoshish'), (f'{BolimQoshish.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/bolim_qoshish_data.html', context=context)



def bolim_qoshish_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = BolimQoshish.objects.create(bolim_nomi=request.POST.get('bolim_nomi'), url_manzil=request.POST.get(
                'url_manzil'))
            messages.success(
                request, f"{new_data.bolim_nomi} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('bolim_qoshish_new_data')
            else:
                return redirect('bolim_qoshish')
        except:
            messages.error(
                request, f"{request.POST.get('bolim_nomi')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('bolim_qoshish')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'bolim_qoshish',
        'right_url': [('Dashboard', 'main_admin'), ('Bolim qoshish', 'bolim_qoshish'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/bolim_qoshish_data.html', context=context)


def logout(request):
    auth_logout(request)
    return redirect('login_admin')

def loginAdmin(request):
    if request.user.is_authenticated:
        return redirect("main_admin")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Muvaffaqiyatli kirish!')
            return redirect('main_admin')
        else:
            messages.error(request, 'Muvaffaqiyatsiz kirish!')
            return redirect('login_admin')
    return render(request, 'login.html')



def mainAdmin(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    messages.success(request, 'Dashboardda hush kelibsiz!')
    context = {
        "models_name": models_name,
        'right_url': [('Dashboard', 'main_admin')],

    }
    return render(request, 'users/list.html', context=context)

# Comment



def comment(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('comment')
        Comment.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('comment')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Comment._meta.fields]
    count = 10
    pages = Paginator(Comment.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'comment')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/comment.html', context=context)



def comment_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = Comment.objects.get(id=id)
            Comment.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('comment')
        else:
            try:
                new_data = Comment.objects.get(id=id)
                new_data.news_id = New.objects.get(id=request.POST.get('news_id'))
                new_data.text = request.POST.get('text')
                new_data.user = request.POST.get('user')
                new_data.save()

                messages.success(
                    request, f"{Comment.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('comment')
            except:
                messages.error(
                    request, f"{Comment.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Comment._meta.fields]
    data = Comment.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'comment',
        'right_url': [('Dashboard', 'main_admin'), ('Comment', 'comment'), (f'{Comment.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
        'another_data': New.objects.all().order_by('-date'),
    }
    return render(request, 'users/datas/comment_data.html', context=context)



def comment_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = Comment.objects.create(news_id=New.objects.get(id=request.POST.get(
                'news_id')), text=request.POST.get('text'), user=request.POST.get('user'))
            messages.success(
                request, f"{new_data.news_id.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('comment_new_data')
            else:
                return redirect('comment')
        except:
            messages.error(
                request, f"{New.objects.get(id=request.POST.get('news_id')).name} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('comment')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'comment',
        'right_url': [('Dashboard', 'main_admin'), ('Comment', 'comment'), ("Yangi ma'lumot", request.resolver_match.url_name)],
        'another_data': New.objects.all().order_by('-date'),

    }
    return render(request, 'users/datas/comment_data.html', context=context)

# Course



def course(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('course')
        Course.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('course')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Course._meta.fields]
    count = 10
    pages = Paginator(Course.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'course')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/course.html', context=context)



def course_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = Course.objects.get(id=id)
            Course.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('course')
        else:
            try:
                new_data = Course.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.description = request.POST.get('description')
                new_data.image = request.FILES['image'] if request.POST.get('image') != '' else new_data.image
                new_data.teachers = Teacher.objects.get(
                    id=request.POST.get('teachers'))
                new_data.save()

                messages.success(
                    request, f"{Course.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('course')
            except:
                messages.error(
                    request, f"{Course.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Course._meta.fields]
    data = Course.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'course',
        'right_url': [('Dashboard', 'main_admin'), ('Course', 'course'), (f'{Course.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
        'another_data': Teacher.objects.all().order_by('-date'),
    }
    return render(request, 'users/datas/course_data.html', context=context)



def course_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = Course.objects.create(name=request.POST.get('name'), description=request.POST.get(
                'description'), image=request.FILES['image'], teachers=Teacher.objects.get(id=request.POST.get('teachers')), )
            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('course_new_data')
            else:
                return redirect('course')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('course')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'course',
        'right_url': [('Dashboard', 'main_admin'), ('Course', 'course'), ("Yangi ma'lumot", request.resolver_match.url_name)],
        'another_data': Teacher.objects.all().order_by('-date'),

    }
    return render(request, 'users/datas/course_data.html', context=context)

# Learning_material



def learning_material(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('learning_material')
        LearningMaterial.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('learning_material')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in LearningMaterial._meta.fields]
    count = 10
    pages = Paginator(LearningMaterial.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'learning_material')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/learning_material.html', context=context)



def learning_material_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = LearningMaterial.objects.get(id=id)
            LearningMaterial.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('learning_material')
        else:
            try:
                new_data = LearningMaterial.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.description = request.POST.get('description')
                new_data.image = request.FILES['image'] if request.POST.get('image') != '' else new_data.image
                new_data.viewed = int(request.POST.get('viewed'))
                new_data.save()

                messages.success(
                    request, f"{LearningMaterial.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('learning_material')
            except:
                messages.error(
                    request, f"{LearningMaterial.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in LearningMaterial._meta.fields]
    data = LearningMaterial.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'learning_material',
        'right_url': [('Dashboard', 'main_admin'), ('Learning Material', 'learning_material'), (f'{LearningMaterial.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/learning_material_data.html', context=context)



def learning_material_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = LearningMaterial.objects.create(name=request.POST.get('name'), description=request.POST.get(
                'description'), image=request.FILES['image'], viewed=int(request.POST.get('viewed')))
            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('learning_material_new_data')
            else:
                return redirect('learning_material')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('learning_material')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'learning_material',
        'right_url': [('Dashboard', 'main_admin'), ('Learning Material', 'learning_material'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/learning_material_data.html', context=context)

# Main_image



def main_image(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('main_image')
        MainImage.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('main_image')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in MainImage._meta.fields]
    count = 10
    pages = Paginator(MainImage.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'main_image')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/main_image.html', context=context)



def main_image_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = MainImage.objects.get(id=id)
            MainImage.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('main_image')
        else:
            try:
                new_data = MainImage.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.image = request.FILES['image'] if request.POST.get('image') != '' else new_data.image
                new_data.save()

                messages.success(
                    request, f"{MainImage.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('main_image')
            except:
                messages.error(
                    request, f"{MainImage.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in MainImage._meta.fields]
    data = MainImage.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'main_image',
        'right_url': [('Dashboard', 'main_admin'), ('Main image', 'main_image'), (f'{MainImage.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/main_image_data.html', context=context)



def main_image_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = MainImage.objects.create(
                name=request.POST.get('name'), image=request.FILES['image'])
            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('main_image_new_data')
            else:
                return redirect('main_image')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('main_image')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'main_image',
        'right_url': [('Dashboard', 'main_admin'), ('Main image', 'main_image'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/main_image_data.html', context=context)

# Message



def message(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('message')
        Message.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('message')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Message._meta.fields]
    count = 10
    pages = Paginator(Message.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'message')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/message.html', context=context)



def message_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = Message.objects.get(id=id)
            Message.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('message')
        else:
            try:
                new_data = Message.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.email = request.POST.get('email')
                new_data.adress = request.POST.get('adress')
                new_data.user = request.POST.get('user')
                new_data.tell = request.POST.get('tell')
                new_data.save()

                messages.success(
                    request, f"{Message.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('message')
            except:
                messages.error(
                    request, f"{Message.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Message._meta.fields]
    data = Message.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'message',
        'right_url': [('Dashboard', 'main_admin'), ('Message', 'message'), (f'{Message.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/message_data.html', context=context)



def message_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = Message.objects.create(name=request.POST.get('name'), email=request.POST.get(
                'email'), adress=request.POST.get('adress'), user=request.POST.get('user'), tell=request.POST.get('tell'))
            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('message_new_data')
            else:
                return redirect('message')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('message')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'message',
        'right_url': [('Dashboard', 'main_admin'), ('Message', 'message'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/message_data.html', context=context)

# New



def new(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('new')
        New.objects.filter(id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('new')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in New._meta.fields]
    count = 10
    pages = Paginator(New.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'new')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/new.html', context=context)



def new_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = New.objects.get(id=id)
            New.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('new')
        else:
            try:
                new_data = New.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.text = request.POST.get('text')
                new_data.image = request.FILES['image'] if request.POST.get('image') != '' else new_data.image
                new_data.views = int(request.POST.get('views'))
                new_data.save()

                messages.success(
                    request, f"{New.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('new')
            except:
                messages.error(
                    request, f"{New.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in New._meta.fields]
    data = New.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'new',
        'right_url': [('Dashboard', 'main_admin'), ('New', 'new'), (f'{New.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/new_data.html', context=context)



def new_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = New.objects.create(
                name=request.POST.get('name'),
                text=request.POST.get('text'),
                image=request.FILES['image'],
                views=int(request.POST.get('views'))
            )

            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('new_new_data')
            else:
                return redirect('new')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('new')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'new',
        'right_url': [('Dashboard', 'main_admin'), ('New', 'new'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/new_data.html', context=context)

# Teacher



def teacher(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('teacher')
        Teacher.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('teacher')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Teacher._meta.fields]
    count = 10
    pages = Paginator(Teacher.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'teacher')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/teacher.html', context=context)



def teacher_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = Teacher.objects.get(id=id)
            Teacher.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('teacher')
        else:
            try:
                new_data = Teacher.objects.get(id=id)
                new_data.name = request.POST.get('name')
                new_data.family_name = request.POST.get('family_name')
                new_data.description = request.POST.get('description')
                new_data.image = request.FILES['image'] if request.POST.get('image') != '' else new_data.image
                new_data.birth_day = request.POST.get('birth_day')
                new_data.tell = request.POST.get('tell')
                new_data.save()

                messages.success(
                    request, f"{Teacher.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('teacher')
            except:
                messages.error(
                    request, f"{Teacher.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in Teacher._meta.fields]
    data = Teacher.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'teacher',
        'right_url': [('Dashboard', 'main_admin'), ('Teacher', 'teacher'), (f'{Teacher.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/teacher_data.html', context=context)



def teacher_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = Teacher.objects.create(name=request.POST.get('name'), family_name=request.POST.get('family_name'), description=request.POST.get(
                'description'), image=request.FILES['image'], birth_day=request.POST.get('birth_day'), tell=request.POST.get('tell'))
            messages.success(
                request, f"{new_data.name} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('teacher_new_data')
            else:
                return redirect('teacher')
        except:
            messages.error(
                request, f"{request.POST.get('name')} ma'lumotlari jadvalga qo'shilmadi!")
            return redirect('teacher')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'teacher',
        'right_url': [('Dashboard', 'main_admin'), ('Teacher', 'teacher'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/teacher_data.html', context=context)

# Who we are



def who_we_are(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if request.POST.getlist('_checkbox') == []:
            messages.error(request, "Ma'lumot tanlanmagan!")
            return redirect('who_we_are')
        WhoWeAre.objects.filter(
            id__in=request.POST.getlist('_checkbox')).delete()
        messages.success(request, f"Ma'lumotlar muvaffaqiyatli o'chirildi!")
        return redirect('who_we_are')
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in WhoWeAre._meta.fields]
    count = 10
    pages = Paginator(WhoWeAre.objects.all().order_by('-date'), count)
    page_number = request.GET.get('page')
    try:
        f = count*int(page_number)-count
    except:
        f = 0
    context = {
        "dashboard_models_name": models_name,
        'current_url': request.resolver_match.url_name,
        'right_url': [('Dashboard', 'main_admin'), (request.resolver_match.url_name.capitalize(), 'who_we_are')],
        'current_field_names': current_field_names,
        'page_obj': pages.get_page(page_number),
        'count': f,
    }
    return render(request, 'users/models/who_we_are.html', context=context)



def who_we_are_change_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        if 'delete' in request.POST:
            datum = WhoWeAre.objects.get(id=id)
            WhoWeAre.objects.get(id=id).delete()
            messages.success(request, f"{ datum } jadvaldan o'chirildi!")
            return redirect('who_we_are')
        else:
            try:
                new_data = WhoWeAre.objects.get(id=id)
                new_data.text = request.POST.get('text')
                new_data.save()

                messages.success(
                    request, f"{WhoWeAre.objects.get(id=id)} ma'lumotlari muvaffaqiyatli o'zgardi!")
                return redirect('who_we_are')
            except:
                messages.error(
                    request, f"{WhoWeAre.objects.get(id=id)} ning ma'lumotlarini o'zgarishda xatolik. Qayta urining! ")
    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    current_field_names = [f.name for f in WhoWeAre._meta.fields]
    data = WhoWeAre.objects.get(id=id)
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'who_we_are',
        'right_url': [('Dashboard', 'main_admin'), ('Who We Are', 'who_we_are'), (f'{WhoWeAre.objects.get(id=id)}', request.resolver_match.url_name, id)],
        'data': data,
        'current_field_names': current_field_names,
    }
    return render(request, 'users/datas/who_we_are_data.html', context=context)



def who_we_are_new_data(request):
    if request.user.is_authenticated == False:
        return redirect('login_admin')
    if request.method == 'POST':
        try:
            new_data = WhoWeAre.objects.create(text=request.POST.get('text'))
            messages.success(
                request, f"{new_data} ma'lumotlari muvaffaqiyatli qo'shildi!")
            if 'save_again' in request.POST:
                return redirect('who_we_are_new_data')
            else:
                return redirect('who_we_are')
        except:
            messages.error(request, "Yangi ma'lumot jadvalga qo'shilmadi!")
            return redirect('who_we_are')

    try:
        models_name = [m.name.replace(
            ' ', '_') for m in ContentType.objects.filter(app_label='edu_app')]
    except:
        models_name = []
    context = {
        "dashboard_models_name": models_name,
        'current_url': 'who_we_are',
        'right_url': [('Dashboard', 'main_admin'), ('Who We Are', 'who_we_are'), ("Yangi ma'lumot", request.resolver_match.url_name)],
    }
    return render(request, 'users/datas/who_we_are_data.html', context=context)
