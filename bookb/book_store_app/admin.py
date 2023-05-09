from django.contrib import admin
from book_store_app.models import *



class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publisher', 'price')

    search_fields = ['title', 'author', 'genre', 'publisher', 'price']




class BBComponentsAdmin(admin.ModelAdmin):

    list_display = ('key', 'description')
    search_fields = ['key']
    

class BBRolesAdmin(admin.ModelAdmin):

    list_display = ('key', 'description',)
    search_fields = ['key']

class BBUserRolesAdmin(admin.ModelAdmin):

    list_display = ('fk_user', 'fk_role')
    search_fields = ['fk_user']

class BBRolesComponentsAdmin(admin.ModelAdmin):

    list_display = ('fk_role', 'fk_component')
    search_fields = ['fk_role']


admin.site.register(Books, BooksAdmin)
admin.site.register(BBComponents, BBComponentsAdmin)
admin.site.register(BBRoles, BBRolesAdmin)
admin.site.register(BBUserRoles, BBUserRolesAdmin)
admin.site.register(BBRolesComponents, BBRolesComponentsAdmin)