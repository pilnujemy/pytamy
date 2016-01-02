from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    '''
        Admin View for Post
    '''
    list_display = ('name', 'created', 'published', 'user')
    list_filter = ('created', 'published', 'user')
    search_fields = ['name']
admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    '''
        Admin View for Tag
    '''
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Tag, TagAdmin)
