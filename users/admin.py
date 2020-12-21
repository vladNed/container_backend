from django.contrib import admin
from users.models.user import ContainerUser
# Register your models here.


@admin.register(ContainerUser)
class ContainerUser(admin.ModelAdmin):
    fields = (
        ('first_name', 'last_name'),
        'email', 'role', 'password',
        ('is_active', 'is_staff')
    )
    list_display = ('pk', 'name', 'email', 'role', 'is_active', 'is_staff')

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
