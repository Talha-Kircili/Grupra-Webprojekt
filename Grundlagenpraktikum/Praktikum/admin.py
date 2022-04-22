from .models import CustomUser, Hilfesuche, Fortschritt, Versuch, Aufgabe, Wochentag
from django.contrib.messages import add_message, WARNING
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from datetime import datetime as date
from django.http import HttpResponse
from django.contrib import admin
from json import dumps


admin.site.site_header = "Grundlagenpraktikum"
admin.site.site_title = "Grundlagenpraktikum"


@admin.action(description='Deactivate Versuch')
def deactivate(modeladmin, request, queryset):
    Versuch.objects.all().update(status = False)
    Hilfesuche.objects.all().delete()
    Fortschritt.objects.all().delete()
    for user in CustomUser.objects.all():
        Fortschritt.objects.create(user=user)

@admin.action(description='Activate Versuch')
def activate(modeladmin, request, queryset):
    if len(queryset) > 1:
        return add_message(request, WARNING, 'Bitte wählen Sie nur einen Versuch aus.')
    deactivate(modeladmin, request, queryset)
    queryset.update(status = True)

@admin.action(description='Delete Logs', permissions=['add'])
def delete_logs(modeladmin, request, queryset):
    LogEntry.objects.all().delete()

class UserAdmin(UserAdmin):
    ordering = ('-is_staff', 'id')
    list_display = ('username', 'is_staff', 'last_login')
    list_filter = ('is_staff',)
    fieldsets = ((None, {'fields': ('username', 'password', 'is_staff')}),)
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2', 'is_staff')
    }),)

class AufgabeInline(admin.StackedInline):
    model = Aufgabe

class VersuchAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'document')
    fields=(('title', 'document'),)
    actions = [activate, deactivate, delete_logs]
    inlines = [AufgabeInline]
    ordering = ('id', )
    save_on_top=True

class MonitorAdmin(admin.ModelAdmin):
    list_display = ['user', 'priority', 'creation_time']
    sortable_by = ()
    ordering = ('-priority', 'creation_time')
    
    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, request, extra_context=None):
        if request.GET.get('refresh'):
            return HttpResponse(Hilfesuche.objects.all().count())

        fortschritte = Fortschritt.objects.exclude(user="admin")
        active = Versuch.objects.filter(status = True)
        progress = {}
        time = Wochentag.objects.filter(day = date.today().strftime("%A"))
        if time:
            time = time[0].time
        else:
            time = None
        if active:
            tasks = Aufgabe.objects.filter(versuch = active[0])
            for i in tasks:
                progress[i.description]=[]
                for j in fortschritte:
                    if i.description in j.progress:
                        progress[i.description].append(1)
                    else:
                        progress[i.description].append(0)
        return super().changelist_view(request, extra_context={
            "time": time,
            "progress": progress,
            "reports": Hilfesuche.objects.all().count(),
            "status": bool(Versuch.objects.filter(status = True))
        })

class WochentagAdmin(admin.ModelAdmin):
    list_display = ['day', 'time']


admin.site.unregister(Group)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Versuch, VersuchAdmin)
admin.site.register(Hilfesuche, MonitorAdmin)
admin.site.register(Wochentag, WochentagAdmin)
