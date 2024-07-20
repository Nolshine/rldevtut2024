# general mapgen rules
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 8
MAX_ROOMS = 200

# rules for caves
CA_FIRST_PASSES = 10 # number of times to apply first-wave CA rules
CA_SECOND_PASSES = 2 # number of times to apply second wave CA rules
CA_MIN_WALLS = 5 # number of walls needed for a floor to become a wall
CA_MIN_FLOORS = 6 # number of floors needed for a wall in the second wave to become a floor