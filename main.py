from tkinter import *
import tkinter.messagebox
import random



tiles = [] # List of all tiles in the gam
root = Tk() # Root window
c = Canvas(root, width=0, height=0) # Canvas to hold the tiles
size = (0, 0) # Size of the board (in tiles)
num_bombs = 0 # Number of bombs on the board
flagged_tiles = [] # List of tiles that are currently flagged


class Tile:

	loc = (0, 0) # Location of the tile on the board (zero-indexed)
	tk_id = None # The tkinter id
	is_bomb = False # The status of the tile as a bomb
	is_flagged = False # The status of the tile as flagged
	is_shown = False
	num = 0 # Number of the tile (i.e. how many many neighbors are bombs)

	def __init__(self, loc, tk_id):
		self.tk_id = tk_id
		self.loc = loc

	def left_click(self):
		"""
		Handle the left-click event
		:return: None
		"""

		if self.is_shown or self.is_flagged:
			return

		loc_x, loc_y = self.loc

		c.create_text(loc_x * 50 + 25, loc_y * 50 + 25, text=self.num,
					  font="Helvetica -25")
		self.is_shown = True
		c.itemconfig(self.tk_id, fill="gray")
		if self.num == 0:
			auto_expose(self)
		check_loss(self)

	def right_click(self):
		"""
		Handles the right click event.  In this case, it toggles the flagged
		property of the tile and changes the color accordingly.
		:return: None
		"""

		global flagged_tiles

		if not self.is_flagged:
			self.is_flagged = True
			c.itemconfig(self.tk_id, fill="orange")
			root.update()
			flagged_tiles.append(self)
		elif self.is_bomb:
			self.is_flagged = False
			flagged_tiles.remove(self)
		else:
			self.is_flagged = False
			flagged_tiles.remove(self)

		check_win()

	def calculate_num(self):
		"""
		Calculates the number of tiles around this tile which are bombs and 
		updates `self.num` to reflect that count.
		:return: None
		"""
	
		# All possible transformations to go to each of the neighboring tiles
		neighbor_moves = [
			[-1, -1],
			[0, -1],
			[1, -1],
			[-1, 0],
			[1, 0],
			[-1, 1],
			[0, 1],
			[1, 1]]

		loc_x, loc_y = self.loc

		neighbor_sum = 0
		for move in neighbor_moves:

			# Neighboring tile's position
			neighbor_x = loc_x + move[0]
			neighbor_y = loc_y + move[1]

			total_width, total_height = size

			# Make sure the tile exists in the board
			if neighbor_x < 0 or neighbor_y < 0 or neighbor_x > total_width -\
					1 or neighbor_y > total_height - 1:

				continue
	
			# Get the Tile object from the tile's location and update the sum
			# as required.
			neighbor_tile = get_tile_from_loc((neighbor_x, neighbor_y))
			if neighbor_tile.is_bomb:
				neighbor_sum += 1

		self.num = neighbor_sum


def get_tile_from_id(tk_id):
	"""
	Finds the tile object with the specified id
	:param tk_id: The id to be matched with the tile
	:return: The tile with the given id
	"""

	for tile in tiles:
		if tile.tk_id == tk_id:
			return tile


def get_tile_from_loc(loc):
	"""
		Finds the tile object with the specified location
		:param loc: The loc to be matched with the tile
		:return: The tile with the given location
	"""

	for tile in tiles:
		if tile.loc == loc:
			return tile


def check_loss(tile):
	"""
	Checks if the user has lost the game.  If the user has lost, display the
	loss message
	:param tile: The Tile object that has been pressed
	:return: None
	"""

	if tile.is_bomb:
		# Display loss message
		tkinter.messagebox.showinfo(title="Minesweeper",
									message="That was a bomb, you lose!")


def check_win():
	"""
	Checks if the user has won the game.  If the user has won, display the
	win message.
	:return: None
	"""

	if num_bombs == len(flagged_tiles):
		for tile in flagged_tiles:
			if not tile.is_bomb:
				return

		# Display the win message
		tkinter.messagebox.showinfo(title="Minesweeper",
									message="Congratulations, you won!")


def auto_expose(tile):
	# TODO

	"""
	Automatically expose all neighboring zero tiles.
	:param tile: The tile to run auto-exposure on
	:return:
	"""

	# All possible transformations to go to each of the neighboring tiles
	neighbor_moves = [
		[-1, -1],
		[0, -1],
		[1, -1],
		[-1, 0],
		[1, 0],
		[-1, 1],
		[0, 1],
		[1, 1]]

	loc_x, loc_y = tile.loc

	for move in neighbor_moves:

		# Neighboring tile's position
		neighbor_x = loc_x + move[0]
		neighbor_y = loc_y + move[1]

		total_width, total_height = size

		# Make sure the tile exists in the board
		if neighbor_x < 0 or neighbor_y < 0 or neighbor_x > total_width - \
				1 or neighbor_y > total_height - 1:
			continue

		# Get the Tile object from the tile's location and update the sum
		# as required.
		neighbor_tile = get_tile_from_loc((neighbor_x, neighbor_y))
		if neighbor_tile.num == 0:
			neighbor_tile.left_click()
		elif not neighbor_tile.is_bomb:
			# TODO
			loc_x, loc_y = neighbor_tile.loc
			print(f"({loc_x}, {loc_y})")
			c.create_text(loc_x * 50 + 25, loc_y * 50 + 25,
						  text=neighbor_tile.num,
						  font="Helvetica -25")
			neighbor_tile.is_shown = True
			c.itemconfig(neighbor_tile.tk_id, fill="gray")


def click_event(event):
	"""
	Handles click event
	:param event: Event object passed from the keybind
	:return: None
	"""

	clicked_tile_id = c.find_closest(event.x, event.y)[0]
	clicked_tile = get_tile_from_id(clicked_tile_id)
	if clicked_tile is None:
		return

	if event.num == 1:
		clicked_tile.left_click()
	else:
		clicked_tile.right_click()


def set_bombs():
	"""
	Changes `num_bombs` tiles to be bombs
	:return: None
	"""

	bomb_tiles = []

	while len(bomb_tiles) < num_bombs:
		rand_tile = random.choice(tiles)
		if rand_tile not in bomb_tiles:
			bomb_tiles.append(rand_tile)

	for tile in bomb_tiles:
		tile.is_bomb = True


def calculate_nums():
	"""
	Force all tiles on the board to calculate their numbers
	:return: None
	"""
	for tile in tiles:
		tile.calculate_num()


def fill(width, height):
	"""
	Fills the board width he specified number of tiles
	:param width: The number of tiles the board is wide
	:param height: The number of tiles the board is tall
	:return: None
	"""

	global tiles

	for i in range(height):
		for j in range(width):
			r = c.create_rectangle(j*50, i*50, j*50+50, i*50+50,
										fill="white", outline="black")
			tiles.append(Tile((j, i), r))


def get_initial_user_input():
	"""
	Prompts the user for the board width, height, and number of bombs
	:return: A tuple (`width_board`, `height_board`, `num_bombs`) where
	`width_board` represents the width of the board in tiles, `height_board`
	is the height of the board in tiles, and `num_bombs` is the number of
	bombs to be present in the board.
	"""


	width_board = int(input("How many tiles wide is the board? "))
	height_board = int(input("How many tiles tall is the board? "))

	while True:
		num_bombs = int(input("How many bombs are in the board? "))
		if num_bombs <= width_board * height_board:
			break
		else:
			print("The number of bombs must be <= the number of tiles in the "
				  "board.")

	return width_board, height_board, num_bombs


def main():
	"""
	Run the game
	:return: None
	"""


	global root, c, size, num_bombs

	# Get user input to initialize the game
	width_board, height_board, num_bombs = get_initial_user_input()
	size = (width_board, height_board)

	# Set the window geometry accordingly
	root.geometry(f"{width_board * 50}x{height_board * 50}")
	c = Canvas(root, width=width_board*50, height=height_board*50)

	# Get the GUI ready
	fill(width_board, height_board)
	set_bombs()
	calculate_nums()

	# Handle button clicks
	root.bind("<Button-1>", click_event)
	root.bind("<Button-2>", click_event)


main()
c.pack()
c.mainloop()
