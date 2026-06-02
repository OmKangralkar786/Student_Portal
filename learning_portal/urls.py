from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),            # Login page (default)
    path('home/', views.home, name='home'),               # Dashboard/home page
    path('register/', views.register, name='register'),   # User registration
    path('logout/', views.logout_view, name='logout'),    # Logout

    path('courses/', views.courses, name='courses'),      # All courses page
    path('materials/<int:course_id>/', views.materials, name='materials'),  # Materials for specific course
     path('notes/<int:course_id>/', views.notes, name='notes'),
    path('semester/<int:semester_id>/', views.semester_courses, name='semester_courses'),  # Semester-wise courses
    path('download/<int:material_id>/', views.download_material, name='download_material'), # ✅ Corrected Download URL
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
