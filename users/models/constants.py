from django.db.models import TextChoices

ROLE_TYPES = [
    ('PR', 'Processor'),
    ('SV', 'Supervisor'),
    ('AD', 'Admin'),
    ('EX', 'External')
]


class Roles(TextChoices):
    PROCESSOR = 'PR'
    SUPERVISRO = 'SV'
    ADMIN = 'AD'
    EXTERNAL = 'EX'
