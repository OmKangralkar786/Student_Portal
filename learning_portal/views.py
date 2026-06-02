from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os

from .models import Profile, StudyMaterial, Course
from .forms import UserRegisterForm


# ✅ File Download View (Fixed & Optimized)
def download_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    file_path = material.file.path  # Full path to file

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return HttpResponse("File not found.", status=404)


# ✅ Login View (Default Page)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ✅ User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            Profile.objects.create(user=user)  # Create linked profile
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


# ✅ Logout View
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Home Page (Dashboard)
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


# ✅ View All Courses
@login_required(login_url='login')
def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


# ✅ View Study Materials for Specific Course
@login_required(login_url='login')
def materials(request, course_id):
    materials = StudyMaterial.objects.filter(course_id=course_id)
    return render(request, 'materials.html', {'materials': materials})


# ✅ Semester-wise Courses with Study Materials
@login_required(login_url='login')
def semester_materials(request, semester_id):
    courses = Course.objects.filter(semester=semester_id)
    return render(request, 'semester_courses.html', {
        'courses': courses,
        'semester_id': semester_id
    })


# ✅ Semester-wise Courses with Descriptions
@login_required(login_url='login')
def semester_courses(request, semester_id):
    courses = Course.objects.filter(semester=semester_id)
    return render(request, 'semester_courses.html', {
        'courses': courses,
        'semester_id': semester_id
    })
@login_required(login_url='login')
def notes(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    notes = StudyMaterial.objects.filter(course=course, category='note')
    question_papers = StudyMaterial.objects.filter(course=course, category='question_paper')
    schemes = StudyMaterial.objects.filter(course=course, category='scheme')
    results = StudyMaterial.objects.filter(course=course, category='result')

    context = {
        'course': course,
        'notes': notes,
        'question_papers': question_papers,
        'schemes': schemes,
        'results': results,
    }
    return render(request, 'notes.html', context)
