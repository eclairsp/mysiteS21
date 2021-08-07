from django.contrib import admin
from .models import Topic, Course, Student, Order, Review


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price', 'hours', 'for_everyone')
    actions = ['add_10_to_hours']

    @admin.action(description='Add 10 hours to the Course length')
    def add_10_to_hours(self, request, queryset):
        for course in queryset:
            course.hours = course.hours + 10
            course.save()

class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status', 'order_date')]
    list_display = ('id', 'student', 'order_status', 'order_date', 'total_items', 'total_cost')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'upper_case_name', 'city')

    def upper_case_name(self, obj):
        return '{0} {1}'.format(obj.first_name.upper(), obj.last_name.upper())

    upper_case_name.short_description = 'Student Full Name'


# Register your models here.

admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
