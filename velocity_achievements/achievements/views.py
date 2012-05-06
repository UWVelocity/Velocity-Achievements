from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django import forms
from django.forms import ModelForm
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from models import Participant, Nomination, Achievement, Grant, Term
import itertools
import operator
from collections import namedtuple

def achievements(request):
    current_term = Term.current_term_key()
    active = Participant.objects.filter(is_active=True)
    with_awards = active.filter(grant__term_id=current_term
            ).annotate(num_grants=Count('grant'), time=Max('grant__granted')
                    ).order_by('-num_grants', '-time')
    without_awards = active.exclude(grant__term_id=current_term)
    hide_nominate_link = request.REQUEST.get('hide_nominate_links', False)
    return render_to_response('achievements.html',
            {'participants': itertools.chain(with_awards, without_awards),
                'show_nominate_link': not hide_nominate_link},
            context_instance=RequestContext(request))

class NominatePersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NominatePersonForm, self).__init__(*args, **kwargs)
        this_term = Term.current_term_key()
        term_grants = Grant.objects.filter(\
                participant = self.instance.participant,\
                term = this_term)
        term_user_nominations = Nomination.objects.filter(\
                nominator = self.instance.nominator,
                participant = self.instance.participant,
                term = this_term)
        self.fields['achievement'] = forms.ModelChoiceField(\
                queryset = Achievement.objects.filter(\
                    can_nominate=True).exclude(\
                    grant__in = term_grants).exclude(\
                    nomination__in = term_user_nominations))

    class Meta:
        model = Nomination
        exclude = ('nominator', 'participant', 'term')
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

NominationTuple = namedtuple('NominationTuple', ('participant','achievement'))

def nominations_list(request):
    granted = operator.methodcaller('granted')
    def nomination_tuple(nomination):
        return NominationTuple(nomination.participant, nomination.achievement)
    def size_item((nomination, lst)):
        nomination = dict(nomination.__dict__)
        nomination['count'] = sum(1 for _ in lst)
        return nomination
    nominations = Nomination.objects.active()\
            .order_by('participant','achievement')
    with_counts = itertools.imap(size_item,
            itertools.groupby(itertools.ifilterfalse(granted, nominations),
                key=nomination_tuple))
    with_counts = sorted(with_counts, key = lambda n:n['count'], reverse=True)
    return render(request, 'nominations_list.html', {'nominations':with_counts})
