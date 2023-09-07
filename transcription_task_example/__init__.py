from otree.api import *
import random
import csv
import jellyfish


doc = """
Practice Tasks
"""


class C(BaseConstants):
    NAME_IN_URL = 'practice_tasks'
    PLAYERS_PER_GROUP = None
    # Set number of rounds to required number of tasks * 5 since participants may attempt to simply click next
    # without solving the task in the hope that doing so often enough will exit them out
    NUM_ROUNDS = 100

    # Load transcription keys for greek letter task
    with open('transcription_keys.csv') as key_file:
        transcription_key = list(csv.DictReader(key_file))


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):

    for p in subsession.get_players():
        participant = p.participant

        if subsession.round_number == 1:
            # set decided_to_continue to True to indicate participant has not quit study when starting this app
            participant.decided_to_continue = True
            # set initial number of attempted transcription tasks to zero
            participant.num_transcriptions_attempted = 0
            # shuffle tasks and assign shuffled list to participant
            shuffled_tasks = random.sample(C.transcription_key, len(C.transcription_key))
            participant.shuffled_tasks = shuffled_tasks
            # initiate task for the first round
            print('initial call of set_transcription_task')
            set_transcription_task(p)


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    is_correct = models.BooleanField(initial=0)
    num_attempts = models.IntegerField(initial=0)
    current_tran_key = models.CharField()
    current_tran_path = models.CharField()
    tran_submitted_answer = models.CharField()
    continuation_choice = models.CharField()



# PLAYER METHODS
def check_correct(player):
    player.is_correct = jellyfish.levenshtein_distance(player.current_tran_key, player.tran_submitted_answer) < 7


def set_transcription_task(player):
    participant = player.participant
    print('hello ' + str(participant.num_transcriptions_attempted))
    print('hello again' + str(participant.shuffled_tasks[1]))
    new_task = participant.shuffled_tasks[participant.num_transcriptions_attempted]
    player.current_tran_key = new_task['answer_key']
    player.current_tran_path = new_task['file']




# PAGES
class transcription_task(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # pass the data from input_radiosequence in number/_init_.py
        player.participant.collected_responses = int(player.input_radiosequence[0])
        

    def is_displayed(player):
        bool_required_round = player.round_number <= int(player.participant.collected_responses[0])
        bool_round_incomplete = player.is_correct is False
        bool_quit_study = player.participant.decided_to_continue is False
        return bool_required_round and bool_round_incomplete and not bool_quit_study


    form_model = 'player'
    form_fields = ['tran_submitted_answer', 'continuation_choice']

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        # update transcription tasks based on current count of participant.num_transcriptions_attempted before new page
        print('call set_transcription_task before loading page')
        set_transcription_task(player)
        return {
            'image_path': 'transcription_pics/{}'.format(player.current_tran_path),
            'current_attempts': player.num_attempts % 3,
            'sample_task': participant.shuffled_tasks[participant.num_transcriptions_attempted]
        }

    @staticmethod
    def js_vars(player):
        session = player.session
        return dict(
            failure_fee=session.config['incomplete_fee']
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.continuation_choice == "Quit":
            participant.decided_to_continue = False
            participant.quit_during_practice = True
        else:
            player.participant.num_transcriptions_attempted += 1
            participant.quit_during_practice = False
            check_correct(player)

    def error_message(player, values):

        correct = jellyfish.levenshtein_distance(values['tran_submitted_answer'], player.current_tran_key)<7

        if values['continuation_choice'] == 'Proceed':
            player.num_attempts += 1

            if not correct:
                # check if participant completed three attempts for the same task and a new task needs to be assigned
                if player.num_attempts % 3 == 0:
                    player.participant.num_transcriptions_attempted += 1
                    set_transcription_task(player)
                    return "This is incorrect. Below is a new practice transcription. " \
                           "\n Please reach out to CTESS-workrewardstudy@caltech.edu " \
                           "if you have any questions about the transcription task and we will be happy to assist."
                # create error message
                elif player.num_attempts <= 3:
                    return "This is incorrect, please try again."
                else:
                    return "This is incorrect, please try again. \nPlease reach out to CTESS-workrewardstudy@caltech.edu" \
                           "if you have any questions about the transcription task and we will be happy to assist."




page_sequence = [transcription_task]
