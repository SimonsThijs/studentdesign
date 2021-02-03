from design.models.project import Project, Material
from design.models.user import User, BusinessUser, DesignerUser
# from design.forms.user_registration import UserRegistrationForm

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'date_joined',)
    list_filter = ('is_staff', 'is_active','is_business', 'is_designer', 'is_email_activated')
    fieldsets = (
        (None, {'fields': ('email', 'password','is_business', 'is_designer', 'is_email_activated')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(BusinessUser)
admin.site.register(DesignerUser)
admin.site.register(Project)
admin.site.register(Material)