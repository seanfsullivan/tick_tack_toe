#tic tac toe

import sys

#t3 ai
#gets a board and finds the best move according to the corner strategy,
#  which is the only strategy I know that doesnt involve brute forcing the board
def find_move(board, player):
	
	opponent = ""
	if player == 'x':
		opponent = 'o'
	else:
		opponent = 'x'


	#board conditions

	#unblocked win move ~ win
	near_complete = board.find_combos(player,2)
	blocked = board.find_combos(opponent,1)
	winnable = list(set(near_complete) - set(blocked))
	if winnable:
		for tile in board.tile_grouping[winnable[0]]:
			if not board.tile_occupation(tile):
				return tile

	#opponent about to win ~ block
	opponent_near_complete = board.find_combos(opponent,2)
	contesting = board.find_combos(player,1)
	need_to_block = list(set(opponent_near_complete) - set(contesting))
	if need_to_block:
		for tile in board.tile_grouping[need_to_block[0]]:
			if not board.tile_occupation(tile):
				return tile

	corners = {1 : 9, 3 : 7, 7 : 3, 9: 1}

	#if opponent has one x in a corner, the cornering stragegy
	#  doesnt work. In order to pull a tie, need to go to the center and then a side
	#Note, this is a little hacky, maybe the brute force method would have been better...
	if len(board.player_totals[opponent]) == 1 and len(board.player_totals[player]) == 0:
		if board.player_totals[opponent][0] in corners:
			return 5
	if len(board.player_totals[opponent]) == 2 and len(board.player_totals[player]) == 1:
		if board.player_totals[opponent][0] in corners and board.player_totals[opponent][1] in corners:
			return 2

		
	#get a corner, prefer one across from one already owned
	corners_owned = []
	for tile in corners:
		if board.tile_occupation(tile) == player:
			corners_owned.append(tile)

	for tile in corners_owned:
		if not board.tile_occupation(corners[tile]):
			return corners[tile]

	#try to get any corner
	for tile in corners:
		if not board.tile_occupation(tile):
			return tile

	#get whatever is left ~ this should only happen in ties
	for tile in range(1,10):
		if not board.tile_occupation(tile):
			return tile


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
			print "spot already occupied!"
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
			print  "X wins!"
			return "X"

		if this.find_combos('o',3):
			print "O wins!"
			print this.find_combos('o',3)
			return "O"

		return False



'''
print "testtesttest"
b = Board()
b.draw_board()	
b.set_pos('x',2)
b.set_pos('x',10)
#b.set_pos('x',5)
#b.set_pos('o',2)
#b.set_pos('o',3)
b.set_pos('o',5)
b.set_pos('o',9)
b.draw_board()
b.check_win()

print find_move(b,'o')
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
				board.set_pos(current_player, find_move(board, current_player))


			#leave if someone wins
			if board.check_win():
				board.draw_board()
				won = True
				board.check_win() 
				break

		if not won:
			board.draw_board()
			print "Its a Tie!\n"



	except Exception as e:
	
		print "Errors! Most likly bad input, but I wont presume"
		print e
	


	

	

	
