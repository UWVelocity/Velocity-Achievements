from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django import forms
from django.forms import ModelForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from models import Participant, Nomination, Achievement, Term
import itertools

def achievements(request):
    current_term = Term.current_term_key()
    active = Participant.objects.filter(is_active=True)
    with_awards = active.filter(grant__term_id=current_term
            ).annotate(num_grants=Count('grant'), time=Max('grant__granted')
                    ).order_by('-num_grants', '-time')
    without_awards = active.exclude(grant__term_id=current_term)
    return render_to_response('achievements.html',
            {'participants': itertools.chain(with_awards, without_awards)},
            context_instance=RequestContext(request))

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
def nominate(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id, is_active=True)
    nomination = Nomination(nominator = request.user, participant=participant)
    if request.method == 'POST':
        form = NominatePersonForm(request.POST, instance = nomination)
        if form.is_valid():
            nomination = form.save()
            return redirect(achievements)
    else:
        form = NominatePersonForm(instance = nomination)
    return render_to_response('nominate.html', {'form': form, 'participant': participant}, context_instance=RequestContext(request))
