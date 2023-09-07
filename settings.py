from os import environ

SESSION_CONFIGS = [
    dict(
        name='transcription_task',
        display_name='Transcription Task',
        app_sequence=['number',
                    'transcription_task_example'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    # set participation fee and reduced fee for partial completion
    participation_fee=15.00,
    incomplete_fee=5.00,
    doc=""
)

PARTICIPANT_FIELDS = ['shuffled_tasks',
                      'num_transcriptions_attempted',
                      'decided_to_continue',
                      'quit_during_practice',
                      'collected_responses'] 
SESSION_FIELDS = []


# create ROOMS which can assign to participants or lab computers, which stay constant across sessions
ROOMS = [
    dict(
        name='transcription_task',
        display_name='Transcription Task Room',
        # change the “guest list” for the room in _rooms/participant.txt file
        # It should contain one participant label per line. 
        participant_label_file='_rooms/participant.txt',   
        use_secure_urls=True
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9224097873932'
