CENTERED_RING = "centered_ring"
ALL_ABOVE = "all_above"
AROUND_THE_EDGE = "around_the_edge"

# Predefined positions for different modes
positions_centered_ring = [
    {"pos_name": 1, "x": 90.4, "y": 137.4},
    {"pos_name": 2, "x": 111.7, "y": 128.2},
    {"pos_name": 3, "x": 128.2, "y": 111.7},
    {"pos_name": 4, "x": 137.4, "y": 90.4},
    {"pos_name": 5, "x": 137.4, "y": 66.6},
    {"pos_name": 6, "x": 128.2, "y": 44.6},
    {"pos_name": 7, "x": 111.7, "y": 28.2},
    {"pos_name": 8, "x": 90.4, "y": 19.6},
    {"pos_name": 9, "x": 65.4, "y": 19.6},
    {"pos_name": 10, "x": 44.6, "y": 27.6},
    {"pos_name": 11, "x": 27.6, "y": 44.6},
    {"pos_name": 12, "x": 17.8, "y": 66.6},
    {"pos_name": 13, "x": 17.8, "y": 90.4},
    {"pos_name": 14, "x": 27.6, "y": 111.7},
    {"pos_name": 15, "x": 44.6, "y": 128.2},
    {"pos_name": 16, "x": 65.4, "y": 137.4}
]

positions_around_the_edge = [
    {"pos_name": 1, "x": 2.3, "y": 153.3},
    {"pos_name": 2, "x": 33.9, "y": 153.3},
    {"pos_name": 3, "x": 63.5, "y": 153.3},
    {"pos_name": 4, "x": 94.1, "y": 153.3},
    {"pos_name": 5, "x": 123.7, "y": 153.3},
    {"pos_name": 6, "x": 153.3, "y": 153.3},
    {"pos_name": 7, "x": 153.3, "y": 123.7},
    {"pos_name": 8, "x": 153.3, "y": 94.1},
    {"pos_name": 9, "x": 153.3, "y": 63.5},
    {"pos_name": 10, "x": 153.3, "y": 33.9},
    {"pos_name": 11, "x": 153.3, "y": 4.3},
    {"pos_name": 12, "x": 123.7, "y": 4.3},
    {"pos_name": 13, "x": 94.1, "y": 4.3},
    {"pos_name": 14, "x": 63.5, "y": 4.3},
    {"pos_name": 15, "x": 33.9, "y": 4.3},
    {"pos_name": 16, "x": 4.3, "y": 4.3},
    {"pos_name": 17, "x": 4.3, "y": 33.9},
    {"pos_name": 18, "x": 4.3, "y": 63.5},
    {"pos_name": 19, "x": 4.3, "y": 94.1},
    {"pos_name": 20, "x": 4.3, "y": 123.7}
]

positions_all_above = [
    {"pos_name": 1, "x": 4.3, "y": 153.3},
    {"pos_name": 2, "x": 33.9, "y": 153.3},
    {"pos_name": 3, "x": 63.5, "y": 153.3},
    {"pos_name": 4, "x": 94.1, "y": 153.3},
    {"pos_name": 5, "x": 124.7, "y": 153.3},
    {"pos_name": 6, "x": 155.3, "y": 153.3},
    {"pos_name": 7, "x": 14.8, "y": 136.5},
    {"pos_name": 8, "x": 45.4, "y": 136.5},
    {"pos_name": 9, "x": 76.0, "y": 136.5},
    {"pos_name": 10, "x": 106.6, "y": 136.5},
    {"pos_name": 11, "x": 137.2, "y": 136.5},
    {"pos_name": 12, "x": 61.7, "y": 117.8},
    {"pos_name": 13, "x": 92.3, "y": 117.8}
]

def get_user_positions(mode):
    positions_map = {
        CENTERED_RING: positions_centered_ring,
        ALL_ABOVE: positions_all_above,
        AROUND_THE_EDGE: positions_around_the_edge
    }
    return positions_map[mode]
