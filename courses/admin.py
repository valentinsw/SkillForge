from django.contrib import admin
from .models import Course, Lesson, Enrollment

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title","is_published","created_by","created_at")
    list_filter = ("is_published","created_at")
    search_fields = ("title","short_description","description")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]
    readonly_fields = ("created_at",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("course","title","order")
    list_editable = ("order",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user","course","joined_at")
    date_hierarchy = "joined_at"
