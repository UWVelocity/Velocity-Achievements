from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from models import Achievement, Participant, Grant, Nomination, Term

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'can_nominate',)

admin.site.register(Achievement, AchievementAdmin)

class ParticipantChangeForm(UserChangeForm):
    class Meta:
        model = Participant

class ParticipantAdmin(UserAdmin):
    form = ParticipantChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')

admin.site.register(Participant, ParticipantAdmin)

class GrantAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'participant', 'granted','term',)

admin.site.register(Grant, GrantAdmin)

class NominationAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'participant', 'nominator','term',)

admin.site.register(Nomination, NominationAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ('term',)

admin.site.register(Term, TermAdmin)
