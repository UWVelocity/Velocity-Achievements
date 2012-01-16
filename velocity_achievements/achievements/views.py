from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django import forms
from django.forms import ModelForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from models import Participant, Nomination, Achievement

def achievements(request):
    participants = Participant.objects.annotate(num_grants=Count('grant')).order_by('-num_grants')
    return render_to_response('achievements.html', {'participants': participants}, context_instance=RequestContext(request))

class NominateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NominateForm, self).__init__(*args, **kwargs)
        if self.instance.nominator:
            self.fields['participant'] = forms.ModelChoiceField(queryset = Participant.objects.exclude(id = self.instance.nominator_id))
    class Meta:
        model = Nomination
        exclude = ('nominator',)
        widgets = {
                'achievement': forms.RadioSelect()
                }

@login_required
def nominate(request):
    nomination = Nomination(nominator = request.user)
    if request.method == 'POST':
        form = NominateForm(request.POST, instance = nomination)
        if form.is_valid():
            nomination = form.save()
            return redirect(achievements)
    else:
        form = NominateForm(instance = nomination)
    return render_to_response('nominate.html', {'form': form}, context_instance=RequestContext(request))

class NominatePersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NominatePersonForm, self).__init__(*args, **kwargs)
        self.fields['achievement'] = forms.ModelChoiceField(\
                queryset = Achievement.objects.exclude(\
                    grant__participant = self.instance.participant).exclude(\
                    nomination__nominator = self.instance.nominator, \
                    nomination__participant = self.instance.participant))

    class Meta:
        model = Nomination
        exclude = ('nominator', 'participant')
        widgets = {
                'achievement': forms.RadioSelect()
                }

@login_required
def nominate_person(request, participant_id):
    nomination = Nomination(nominator = request.user, participant = get_object_or_404(Participant, pk=participant_id))
    if request.method == 'POST':
        form = NominatePersonForm(request.POST, instance = nomination)
        if form.is_valid():
            nomination = form.save()
            return redirect(achievements)
    else:
        form = NominatePersonForm(instance = nomination)
    return render_to_response('nominate_person.html', {'form': form, 'participant_id': participant_id}, context_instance=RequestContext(request))
