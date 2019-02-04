""" 

Greedy player
@author Will Merrill

"""

def get_move(game):

	min_score = float("inf")
	min_move = None

	# try each move
	for move in game.generate_moves():
		g = game.copy()
		g.play_move(move)

		score = g.score()
		min_score = min(score, min_score)
		if min_score == score:
			min_move = move

	return (-min_score, min_move)
