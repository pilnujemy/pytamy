from django.contrib import admin
from .models import Letter, Attachment, OutgoingLetter, IncomingLetter


class AttachmentInline(admin.TabularInline):
    '''
        Tabular Inline View for Attachment
    '''
    model = Attachment


class LetterAdmin(admin.ModelAdmin):
    '''
        Admin View for Letter
    '''
    list_display = ['subject', 'case', 'created', 'modified']
    inlines = [
        AttachmentInline,
    ]
    search_fields = ['subject']

admin.site.register(Letter, LetterAdmin)


class OutgoingLetterAdmin(LetterAdmin):
    list_display = LetterAdmin.list_display + ['email']

admin.site.register(OutgoingLetter, LetterAdmin)


class IncomingLetterAdmin(LetterAdmin):
    list_display = LetterAdmin.list_display + ['email']

admin.site.register(IncomingLetter, LetterAdmin)
