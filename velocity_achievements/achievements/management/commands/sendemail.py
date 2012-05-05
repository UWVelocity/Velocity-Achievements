from django.core.mail import EmailMessage
from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string
from optparse import make_option
from achievements.models import Grant, Participant
import datetime

class Command(NoArgsCommand):
    help = 'Sends an email to participants summarizing recent activity.'
    option_list = NoArgsCommand.option_list + (
        make_option('--days',
            action='store',
            dest='days',
            default=7,
            type="int",
            help='How many days the email should cover. Defaults to %default.'),
        )

    def handle_noargs(self, **options):
        delta = datetime.timedelta(options['days'])
        grants = Grant.objects.filter(granted__gte = datetime.datetime.now() - delta)\
                .order_by('achievement').select_related('achievement','participant')
        self.stdout.write("Going to summarize %d days of activity (%d events)\n" %
                (delta.days, len(grants)))
        achievement_data = [{
            'achievement': g.achievement,
            'participant': g.participant
            } for g in grants]
        message_body = render_to_string("email_update.txt", {
                'grants': achievement_data
            })
        email = EmailMessage('Velocity the Game Updates', 
                message_body, 'GLaDOS@velocitythegame.com', [], 
                Participant.objects.filter(is_active=True).values_list(
                    'email', flat=True),)
        email.send()

