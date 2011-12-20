from django.db.models import Count
from django.shortcuts import render_to_response
from models import Participant

def achievements(request):
    participants = Participant.objects.annotate(num_grants=Count('grant')).filter(num_grants__gt = 0).order_by('-num_grants')
    return render_to_response('achievements.html', {'participants': participants})
