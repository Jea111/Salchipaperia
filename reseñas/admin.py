from django.contrib import admin
from . models import ReseñaSite
# Register your models here.

class reseñaAdmin(admin.ModelAdmin):
    fields = ['email','message']
    list_display = ['email','message','create_at']
    list_filter = ['email','message','create_at']
    search_fields  = ['email','message','create_at']
admin.site.register(ReseñaSite,reseñaAdmin)