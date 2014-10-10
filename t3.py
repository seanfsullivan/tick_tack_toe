#tic tac toe

import sys
import copy

#t3 ai

#Using the minimax alg
##  recursivly find the best board combination
def mini_max_move(board,player):

	free_pos = board.list_free_loc()
	turn = 10-len(free_pos)

	#board is empty.... everything can be tied so just pick
	# corner and save some processing time
	if turn == 1:
		return 1

	v_points = 0
	v_points_loc = 0

	#determine minimizing player
	opponent = 'o' if player == 'x' else 'x'
	maxing = True 

	sys.stdout.write("Plotting...")
	sys.stdout.flush()


	return mm3_rec(board,player,opponent,maxing,0,True)


#Minimax alg
## Recursivly solve board for victory. Shorter win cases are prioritized
def mm3_rec(board,player,opponent,maxing,turns,root):
	t_win = board.check_win()
	free_locs = board.list_free_loc()

	#Base case, if player (maximizer) wins, a positive value is returned, else neg
	if t_win == player:
		return 11-turns
	elif t_win == opponent:
		return turns-11
	elif not free_locs:
		return 0

	#Maximize score if maximizer, otherwise try to find minimum score
	if maxing:
		best_v = -12
		best_v_loc = 0

		#make all possible moves, then find best value score
		for move in free_locs:
			test_b = copy.deepcopy(board)
			test_b.set_pos(player,move)
			val = mm3_rec(test_b,player,opponent,False,turns+1,False)

			if root:
				sys.stdout.write(".")
				sys.stdout.flush()
				#print "_"+str(val)+" "+str(move)

			if val > best_v:
				best_v = val
				best_v_loc = move

		if root:
			return best_v_loc
		else:
			return best_v

	else:

		best_v = 12
		best_v_loc = 0

		for move in free_locs:
			test_b = copy.deepcopy(board)
			test_b.set_pos(opponent,move)
			val = mm3_rec(test_b,player,opponent,True,turns+1,False)

			if root:
				sys.stdout.write(".")
				sys.stdout.flush()

			if val < best_v:
				best_v = val
				best_v_loc = move

		if root:
			return best_v_loc
		else:
			return best_v



#encapulate board so it can have a persistant board object
class Board:
	def __init__(this):
		this.locations = {}

		#makes for easier grouping calcs
		this.player_totals = {'x' : [], 'o': []}

		#If a space is unoccupied, its number will be in the space
		#  for easy selection
		for pos in range(1,10):
			this.locations[pos] = str(pos)

		'''
		5, #left vert
		7,  #middle vert,
		11, #right vert,
		13, #top hor, 
		17, #middle hor,
		19, #bottom hor,
		23, #left cross,
		29] #right cross
		'''

		#referance for prime factor grouping
		this.tile_grouping = {5: [1,4,7], 7: [2,5,8], 11: [3,6,9], 13: [1,2,3], 
							 17: [4,5,6], 19:[7,8,9], 23: [1,5,9], 29: [3,5,7] }

		this.tile_base_values = {}
		for val in range(1,10):
			this.tile_base_values[val] = 1
		for prime in this.tile_grouping:
			for tile in this.tile_grouping[prime]:
				this.tile_base_values[tile] *= prime

	#render the board, this works in terminal
	def draw_board(this):
		sys.stdout.write("\n\n")
		loc_list = range(1,10)

		#ascii, so print by rows
		for y in range(1,10):

			fill = " "
			print_loc = False

			#I dont know if doing 'in' is slower than straight comparisons,
			#  but it is definatly easier to write

			#Choose wether this line has blank spaces or underscores
			if y in [3,6]:
				fill = "_"
			elif y in [2,5,8]:
				print_loc = True
				
			#print out the line
			for x in range(1,12):
				if x % 4 == 0:
					sys.stdout.write("|")
				elif (x-2)%4 == 0 and print_loc:
					sys.stdout.write(this.locations[loc_list[0]])
					#whats the oppisite of pop?
					loc_list = loc_list[1:]
				else:
					sys.stdout.write(fill)

			sys.stdout.write("\n")
		sys.stdout.write("\n\n")

	#internal use, no validation
	def tile_occupation(this,pos):
		if this.locations[pos].isdigit():
			return False
		else:
			return this.locations[pos] 


	#simple validation, maybe this should be wrapped in a try?
	def set_pos(this, player, pos):
		if pos not in range (1, 10):
			print "bad position"
			return False
		if player not in ['x','o']:
			print "bad player"
			return False
		if not this.locations[pos].isdigit():
			#print "spot already occupied!"
			return False

		this.locations[pos] = player
		this.player_totals[player].append(pos)

		return True

	#checks to see if winning combos is met using factors,
	#  but I dont know if this would me more efficent then just
	#  mapping the board to a multi dimenininal array and crawling it
	def find_combos(this, player, min_match):

		#use prime factors to check if there is a winning condition for a particular player

		match_list = []

		#get all currently owned locations and get totals
		vic_total = 1
		for loc in this.player_totals[player]:
			vic_total*=this.tile_base_values[loc]

		#test for a winning condition
		for win in this.tile_grouping:
			if vic_total % pow(win, min_match) == 0:
				match_list.append(win)

		return match_list

	def check_win(this):
		if this.find_combos('x',3):
			#print  "X wins!"
			return "x"

		if this.find_combos('o',3):
			#print "O wins!"
			#print this.find_combos('o',3)
			return "o"

		return False

	def list_free_loc(this):
		free = []
		for val in range(1,10):
			if this.locations[val].isdigit(): 
				free.append(val)

		return free


'''

print "testtesttest"
b = Board()
b.draw_board()	
b.set_pos('x',2)
b.set_pos('x',10)
#b.set_pos('x',5)
#b.set_pos('o',2)
#b.set_pos('o',3)
b.set_pos('o',1)
b.set_pos('o',9)
b.draw_board()

print b.locations
print b.list_free_loc()
b.check_win()

print mini_max_move(b,'o')
'''


while True:

	option = raw_input('\n\nWelcome to Tic Tac Toe! Please choose and option:\n'
		+'1. Player(X) vs Player(O)\n'
		+'2. AI(X) vs Player(O)\n'
		+'3. Player(X) vs AI(O)\n'
		+'4. AI(X) vs AI(O). This one is boring(deterministic)\n'
		+'Type quit or exit to leave. \n')

	option = option.strip()
	if option.lower()=='quit' or option.lower()=='exit':
		break

	try:
		board = Board()
		option = int(option)
		if option > 4 or option < 1:
			raise "bad input"

		x_player_ai = False
		o_player_ai = False

		if option == 2 or option == 4:
			x_player_ai = True

		if option == 3 or option == 4:
			o_player_ai = True


		#main game loop
		won = False
		for round_num in range(1,10):
			
			board.draw_board()
			
			#x goes first, on the odds
			current_player = ""
			ai = False
			if round_num % 2 != 0:
				current_player = "x"
				print "X's Turn!"
				if x_player_ai:
					ai = True
			else:
				current_player = "o"
				print "O's Turn!"
				if o_player_ai:
					ai = True

			if not ai:
				placed = False
				while not placed:
					loc = raw_input("Choose a location to place: ").strip()
					if loc == "quit" or loc == "exit":
						raise "I dont want to play"
					if loc.isdigit():
						placed = board.set_pos(current_player, int(loc) )
					else:
						print "Cant place to "+loc
			else:

				board.set_pos(current_player, mini_max_move(board, current_player))


			#leave if someone wins
			if board.check_win():
				board.draw_board()
				won = True
				print board.check_win().upper()+" Wins!"
				 
				break

		if not won:
			board.draw_board()
			print "Its a Tie!\n"



	except Exception as e:
	
		print "Errors! Most likly bad input, but I wont presume"
		print e
	




	

	
