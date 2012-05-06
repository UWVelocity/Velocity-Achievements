from django.core.mail import EmailMessage
from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string
from optparse import make_option
from achievements.models import Grant, Participant, Term
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
        grants = Grant.objects.filter(granted__gte = datetime.datetime.now() - delta,
                term_id=Term.current_term_key())\
                .order_by('achievement').select_related('achievement','participant')
        if not grants:
            self.stdout.write("No activity to summarize. Not sending anything\n")
            return 0
        self.stdout.write("Going to summarize %d days of activity (%d events)\n" %
                (delta.days, len(grants)))
        achievement_data = [{
            'achievement': g.achievement,
            'participant': g.participant
            } for g in grants]
        message_body = render_to_string("email_update.txt", {
                'days': delta.days,
                'grants': achievement_data
            })
        for email in Participant.objects.filter(is_active=True)\
                .values_list('email', flat=True):
            email = EmailMessage('Velocity the Game Updates',
                    message_body, 'GLaDOS@velocitythegame.com', [email])
            email.send()

