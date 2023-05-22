#!/bin/python3
import numpy as np
import os

from jigsaw import *
from jigsaw.default import *
from jigsaw.svg import *

if not os.path.exists("output"):
    os.mkdir("output")

# Choose only centered edge types, two sizes
edge_types = np.array([
#    CENTERED_BIG_MALE,
    CENTERED_MEDIUM_MALE,
    CENTERED_SMALL_MALE,
#    RIGHT_BIG_MALE,
    RIGHT_MEDIUM_MALE,
    RIGHT_SMALL_MALE,
#    LEFT_BIG_MALE,
    LEFT_MEDIUM_MALE,
    LEFT_SMALL_MALE,
#    DOUBLE_BIG_MALE,
#    DOUBLE_MEDIUM_MALE,
    DOUBLE_SMALL_MALE,
#    TWISTED_BIG_MALE,
#    TWISTED_MEDIUM_MALE,
    TWISTED_SMALL_MALE,
    FLAT
])

# Automatically expand types to match combinations
edge_types = expand_edge_types(edge_types, opposite, flip)

# Set grid Size
H, W = 4, 4

count = 0

while True:
    count=count+1
    print("try nr.{}".format(count))

    horizontal_edges, vertical_edges = sample_random_grid(H, W, edge_types, border=0)
    #horizontal_edges, vertical_edges = get_grid(H, W, edge_types, border=0)

    # Convert to list of pieces
    pieces = grid_to_pieces(horizontal_edges, vertical_edges, opposite)
    #grid_saveToDisk(horizontal_edges, vertical_edges)
    if has_unique_solution(H, W, pieces, opposite, flip, constraints="border"):
        grid_saveToDisk(horizontal_edges, vertical_edges)
        print("hit")
        break

