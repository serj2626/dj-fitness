from django.contrib import admin

from .models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin View for User)'''

    list_display = ('email', 'is_verified', 'phone',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    '''Admin View for EmailVerification)'''

    list_display = ('user', 'token', 'created_at', 'expiration', )
    readonly_fields = ('created_at', )
