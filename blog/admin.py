
# Register your models here.

from django.contrib import admin
from .models import Post, User
# from django.contrib.auth.admin import UserAdmin
from .models import Category,Tag,Comment

admin.site.register(User)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "slug", "published_date")
    search_fields = ['tags','author','category']
    autocomplete_fields = ['tags','category']
  
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {"slug": ["name",]}
    search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display =('name','slug')
    prepopulated_fields = {"slug": ["name",]}
    search_fields = ['name']

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)

