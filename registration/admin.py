from django.contrib import admin

from .models import BlacklistedAccessToken, MyUser

admin.site.register(MyUser)
admin.site.register(BlacklistedAccessToken)
