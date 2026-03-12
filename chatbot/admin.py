from django.contrib import admin
from .models import FAQ, Navigation, AttachmentOpportunity, ChatLog


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("keywords", "answer")
    search_fields = ("keywords",)


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ("place", "description")
    search_fields = ("place", "keywords")


@admin.register(AttachmentOpportunity)
class AttachmentOpportunityAdmin(admin.ModelAdmin):
    list_display = ("degree_programme", "company_name", "location", "contact")
    search_fields = ("degree_programme", "company_name")


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "response_type", "created_at")
    search_fields = ("message",)
