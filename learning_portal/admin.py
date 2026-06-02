from django.contrib import admin
from .models import Course, Profile, StudyMaterial

# Avoid duplicate registration error
admin.site.unregister(Course) if admin.site.is_registered(Course) else None
admin.site.unregister(Profile) if admin.site.is_registered(Profile) else None
admin.site.unregister(StudyMaterial) if admin.site.is_registered(StudyMaterial) else None

# Custom Admin Panel Display
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'description')  # ✅ Show description in Admin Panel
    search_fields = ('name',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Profile)
admin.site.register(StudyMaterial)
