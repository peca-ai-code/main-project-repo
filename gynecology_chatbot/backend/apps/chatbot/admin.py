from django.contrib import admin
from .models import Conversation, Message, AIModelResponse

class MessageInline(admin.TabularInline):
    model = Message
    readonly_fields = ('created_at',)
    extra = 0

class AIModelResponseInline(admin.TabularInline):
    model = AIModelResponse
    readonly_fields = ('created_at',)
    extra = 0

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'user__email')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'message_type', 'created_at', 'model_name')
    list_filter = ('message_type', 'created_at', 'model_name')
    search_fields = ('content', 'conversation__title')
    inlines = [AIModelResponseInline]

@admin.register(AIModelResponse)
class AIModelResponseAdmin(admin.ModelAdmin):
    list_display = ('message', 'model_name', 'created_at')
    list_filter = ('model_name', 'created_at')
    search_fields = ('content', 'message__content')
