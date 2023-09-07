from otree.api import *
import json
import random
import numpy as np
import time

doc = """
number of greek trans experiment
"""

class Constants(BaseConstants):
    name_in_url = 'number'
    players_per_group = None
    num_rounds = 1

 
class Player(BasePlayer):
    input_radiosequence = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],
        widget=widgets.RadioSelectHorizontal
        )

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



# PAGES
class Questions(Page):
    form_model = 'player'
    form_fields = ['input_radiosequence']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            player.participant.collected_responses = [player.input_radiosequence]
        else:
            player.participant.collected_responses.append(player.input_radiosequence)



page_sequence = [Questions,]
