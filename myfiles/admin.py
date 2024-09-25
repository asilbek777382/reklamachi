from django.contrib import admin

from myfiles.models import *


# Register your models here.
class Adminkirish(admin.ModelAdmin):
    list_display = ['id','login','parol','user_id']

admin.site.register(kirish,Adminkirish)

class Adminset_message(admin.ModelAdmin):
    list_display = ['id','gurux_id','users_id','xolati','matn','rasm','video','url_tugmachalar','vaqt','tugash_sanasi','xabarni_qadash','songgi_xabarni_ochirish']

admin.site.register(set_message,Adminset_message)


