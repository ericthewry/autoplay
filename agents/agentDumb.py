import random as rand

class AgentDumb:

	def __init__(self, initial_epsilon, training_cycles):
		pass

	def take_action(self, game_text):
		if rand.random() < 0.5:
			return 'n'
		else:
			return 's'

	def update(self, reward, new_game_text):
		return

