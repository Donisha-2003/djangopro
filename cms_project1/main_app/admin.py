from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Cro)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(Stu)
admin.site.register(Walkin)
admin.site.register(CollectionReport)
admin.site.register(WalkinReport)
admin.site.register(PendingPaymentReport)
admin.site.register(RegistrationReport)
admin.site.register(ReferenceReport)
