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
    CENTERED_SMALL_MALE,
    FLAT
])

# Automatically expand types to match combinations
edge_types = expand_edge_types(edge_types, opposite, flip)

# Set grid Size
H, W = 4, 4

while True:

    horizontal_edges, vertical_edges = sample_random_grid(H, W, edge_types, border=0)
    #horizontal_edges, vertical_edges = get_grid(H, W, edge_types, border=0)

    # Convert to list of pieces
    pieces = grid_to_pieces(horizontal_edges, vertical_edges, opposite)
    #grid_saveToDisk(horizontal_edges, vertical_edges)
    if has_unique_solution(H, W, pieces, opposite, flip, constraints="border"):
        grid_saveToDisk(horizontal_edges, vertical_edges)
        print("hit")
        break

