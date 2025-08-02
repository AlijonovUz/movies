from django.contrib import admin

from .models import BlacklistedAccessToken, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at')
    list_display_links = ('id', 'subject')
    search_fields = ('id', 'subject')
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(BlacklistedAccessToken)