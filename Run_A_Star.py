"""
Run_A_Star.py
A* Algorithm IN EXCRUCIATING DETAIL!!!
Joel Goodman
joelrgoodman@gmail.com
Use this script to run A_Star_Algorithm.py
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import A_Star


world_file = 'world.csv'
world = []

# Read in CSV
with open(world_file) as world_csv:
	csv_reader = csv.reader(world_csv)
	for row in csv_reader:
		world.append(row)


# Put the world into an array. This is an easy data structure to work with.
world = np.array(world, dtype=int)
# Start and end points. The convention we use is (y, x) for ever coord in this algo.
start_pos, goal_pos = (0, 0), (19, 19)

# You may need to construct a cost map. Sometimes you have to take into account a heuristic
# as well as some edge cost to get where you need to go. I haven't had to do this but a goal of
# mine is to make this algo capable of handling that.
# It's a work in progress so if it is broken, let me know and I'll work on a solution.
# You should represent the edge costs as a numpy array filled with cell objects.
# I'll leave the construction of the array up to you, Below is an example of how to construct a single cell.

# Make an empty np.array with dtype A_Star.cell:
# cost_map = np.empty([world.shape[0], world.shape[1]], dtype=A_Star.cell)
# Populate the cost_map with cells. Arguments are the costs to travel to adjacent cells.
# You could do this in a loop or by hand (if it's a small map)
# If you can only travel up, down, left, and right, only worry about north, south, east, and west.
# The shown values are randomly chosen:
# for x in range(0, cost_map.shape[0]):
# 	for y in range(0, cost_map.shape[1]):
# 		cost_map[x][y] = A_Star.cell(2.0, 1.0, 4.0, 6.0, 3.0, 5.0, 2.5, 1.1)


def main():
	# Send the world and start and end postions to the algorithm. Return solution and cost.
	solution, cost = A_Star.algo(world, start_pos, goal_pos, cost_map=None)
	print(f"Solution cost was {cost}.")
	# Make a copy of the world, and plot the solution path on it
	solved_world = np.array(world, copy=True)
	for x, y in solution:
		solved_world[x][y] = 100

	# Normalize and plot the solution and original map as a colormap
	norm = mpl.colors.Normalize(vmin=0, vmax=100)
	fh1, axh1 = plt.subplots()
	axh1.set_title("Path Resulting From A* Algorithm")
	axh1.imshow(solved_world, cmap='flag', norm=norm, interpolation='none')

	fh2, axh2 = plt.subplots()
	axh2.set_title("World, Unnavigated")
	axh2.imshow(world, cmap='flag', norm=norm, interpolation='none')
	plt.show()


if __name__ == "__main__":
	main()
