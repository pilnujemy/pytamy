from django.contrib import admin
from .models import Letter, Attachment


class AttachmentInline(admin.TabularInline):
    '''
        Tabular Inline View for Attachment
    '''
    model = Attachment


class LetterAdmin(admin.ModelAdmin):
    '''
        Admin View for Letter
    '''
    list_display = ('sender', 'subject', 'incoming', 'is_send')
    list_filter = ('incoming',)
    inlines = [
        AttachmentInline,
    ]
    search_fields = ['subject']

admin.site.register(Letter, LetterAdmin)
