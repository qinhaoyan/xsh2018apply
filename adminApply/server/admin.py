from django.contrib import admin
from server.models import Students,Asp,BUInformation,Admins,Queue
# Register your models here.

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['name','tel','stu_id','asp']
    search_fields = ['tel']

class AspAdmin(admin.ModelAdmin):
    list_display = ['name','tel','stu_id','BU','applyStatus']
    search_fields = ['tel']



admin.site.register(Admins)
admin.site.register(Students,StudentsAdmin)
admin.site.register(Asp,AspAdmin)
admin.site.register(BUInformation)
admin.site.register(Queue)