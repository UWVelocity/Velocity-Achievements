from models import Participant
from emailauth.backends import EmailBackend

class ParticipantBackend(EmailBackend):
    object_class = Participant
