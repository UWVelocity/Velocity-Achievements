from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from models import Achievement, Participant, Grant, Nomination

admin.site.register(Achievement)

class ParticipantChangeForm(UserChangeForm):
    class Meta:
        model = Participant

class ParticipantAdmin(UserAdmin):
    pass

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Grant)
admin.site.register(Nomination)
