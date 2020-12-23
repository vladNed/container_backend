from django.contrib import admin
from projects.models import Project, ProjectUser
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'days_left')


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    pass
