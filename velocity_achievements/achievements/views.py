from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django import forms
from django.forms import ModelForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Participant, Nomination

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
def nominate(request, participant_id = None):
    nomination = Nomination(nominator = request.user)
    initial = {}
    participant = Participant.objects.filter(pk = participant_id)
    if participant:
        initial['participant'] = participant.get()
    if request.method == 'POST':
        form = NominateForm(request.POST, instance = nomination, initial = initial)
        if form.is_valid():
            nomination = form.save()
            return redirect(achievements)
    else:
        form = NominateForm(instance = nomination, initial = initial)
    return render_to_response('nominate.html', {'form': form}, context_instance=RequestContext(request))
