from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import Post, User, Category, Tags , Comments

def export_as_csv(self, request, queryset):
    
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


class PostAdmin(admin.ModelAdmin):
    list_filter = ['category', 'tags', 'author','published_date']
    list_display = ('title', 'thumbnail_image','author','published_date')
    search_fields = ['title','name']
    filter_horizontal = ('tags',)
    autocomplete_fields = ['category','author']

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['title']
    search_fields = ['name']

class TagsAdmin(admin.ModelAdmin):
    list_filter = ['title']
    search_fields = ['tags' ]

class UserAdmin(admin.ModelAdmin):
    # list_filter = ['email','gender','mobile_no','city','country','image']
    search_fields = ['name']

class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['post','email',]
    search_fields = ['name',]
    # autocomplete_fields = ('post',)

admin.site.register(Post,PostAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tags,TagsAdmin)
admin.site.register(Comments,CommentsAdmin)