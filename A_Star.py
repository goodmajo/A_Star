"""
A_Star.py
A* Algorithm IN EXCRUCIATING DETAIL!!!
Joel Goodman
joelrgoodman@gmail.com
"""
import math
from heapq import *

infinity = float(math.inf)

# These are the directions we can look in at each node.
# Choose whether on not you're confined to moving in the four cardinal directions or diagonal movement is a possibility
directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
# directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

# The heuristic determines the way in which we measure distances.
# Manhattan approches the calculation in terms of the path through a grid, just summing the delta_x and delta_y.
# The alternative is the euclidean distance between two points.
def heuristic(point_a, point_b, manhattan=True):
    if manhattan:
        return abs(point_b[0] - point_a[0]) + abs(point_b[1] - point_a[1])
    else:
        return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])


def algo(world, start_pos, goal_pos, cost_map=None):
    # Initialize open and close sets. For now they're just empty lists.
    open_set, close_set = [], []
    """ Dictionaries are unordered associative array.
        Very valuable for storing values associated with a key if order doesn't matter to you.
        dictionary = {} initializes an empty dictionary
        dictionary = {key: value} initializes a dictionary with a first key and value.
        The initial position's g_score is zero. Initialize the g_score dictionary with an entry for that position.
        Initialize the f_score with an entry for position and the distance from the current position to the goal position.
    """
    path_travelled = {}
    g_score = {start_pos: 0}
    f_score = {start_pos: heuristic(start_pos, goal_pos)}
    """ A heap is a binary tree-based data structure in which parent nodes have values equal to or less than their children.
        This algorithm takes advantage of python's heapq library, which is itself an implementation of a heapsort algorithm.
        our list open_set is our heap, and we will put tuples on it with heappush. Each tuple will be (f_score, coordinate)
    """
    heappush(open_set, (f_score[start_pos], start_pos))

    # While the open_set isn't empty, do stuff
    while open_set:
        """ current is the current cell we are at, defined by it's position in the world.
            We get it's position by using heappop, which returns the smallest member of the heap.
            Of course, we only need the second entry in the tuple.
        """
        current_pos = heappop(open_set)[1]
        # If we've reached our goal, make a quick list of all the places we've been and return it to the user.
        if current_pos == goal_pos:
            final_path = []
            while current_pos in path_travelled:
                final_path.append(current_pos)
                current_pos = path_travelled[current_pos]
            return final_path[::-1], len(final_path)
        # At this point we can add the current position to the closed set.
        close_set.append(current_pos)
        # Check the four nodes corresponding to the cardinal directions we care about.
        for x, y in directions:
            # Which direction are we looking in right now?
            child = current_pos[0] + x, current_pos[1] + y
            # If you have to consider additional edge costs on top of the heuristic, you must take into account the cost to arrive.
            if cost_map is None:
                cost_to_arrive = 0.0
            else:
                cost_to_arrive = get_edge_costs((x, y), cost_map[x][y])
            # temp_g_score will be used when we decide which child node is the best to move to next
            temp_g_score = g_score[current_pos] + heuristic(current_pos, child) + cost_to_arrive
            """ This is important! Are we actually looking at a node that exists in our world?
                The next two ifs determine that. If the node is in the world, it lets the loop go on. If not,
                it returns control to the beginning of the for loop.
                The third if statement makes sure we aren't looking at a node with an obstacle.
            """
            if 0 <= child[0] < world.shape[0]:
                if 0 <= child[1] < world.shape[1]:
                    if world[child] == 1:
                        continue
                else:
                    continue
            else:
                continue
            """ If the node we're looking at is in the closed set and the current best g_score is
                better or equal to the child's g_score (entry 0 in it's dictionary entry), try the next child.
            """
            if child in close_set and temp_g_score >= g_score.get(child, 0):
                continue
            """ This is the case we want to see. If the temp_g_score is less than that of the child,
                or the child's coordinate isn't found in the open set, our new current_pos is the child's
                position.
            """
            if temp_g_score < g_score.get(child, 0) or child not in [i[1]for i in open_set]:
                path_travelled[child] = current_pos
                # Assign new g and f scores to the appropriate dictionary entries for the child.
                g_score[child] = temp_g_score
                f_score[child] = temp_g_score + heuristic(child, goal_pos)
                # Put the child in the open set.
                heappush(open_set, (f_score[child], child))

    return False


def get_edge_costs(direction, cost_map_cell):
    if direction[0] == 1 and direction[1] == 1:
        return cost_map_cell.northeast
    if direction[0] == 1 and direction[1] == -1:
        return cost_map_cell.southeast
    if direction[0] == -1 and direction[1] == 1:
        return cost_map_cell.northwest
    if direction[0] == -1 and direction[1] == -1:
        return cost_map_cell.southwest
    if direction[0] == 1 and direction[1] == 0:
        return cost_map_cell.east
    if direction[0] == -1 and direction[1] == 0:
        return cost_map_cell.west
    if direction[0] == 0 and direction[1] == 1:
        return cost_map_cell.north
    if direction[0] == 0 and direction[1] == -1:
        return cost_map_cell.south


class cell(object):
    def __init__(self, north=0.0, south=0.0, east=0.0, west=0.0, northeast=0.0, southeast=0.0, southwest=0.0, northwest=0.0):
        # These are edge costs.
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.northeast = northeast
        self.southeast = southeast
        self.southwest = southwest
        self.northwest = northeast
