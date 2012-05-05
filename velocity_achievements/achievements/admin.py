from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from models import Achievement, Participant, Grant, Nomination, Term

admin.site.register(Achievement)

class ParticipantChangeForm(UserChangeForm):
    class Meta:
        model = Participant

class ParticipantAdmin(UserAdmin):
    form = ParticipantChangeForm

admin.site.register(Participant, ParticipantAdmin)

class GrantAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'participant', 'granted',)

admin.site.register(Grant, GrantAdmin)

class NominationAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'participant', 'nominator',)

admin.site.register(Nomination, NominationAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ('term',)

admin.site.register(Term, TermAdmin)
