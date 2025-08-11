from constants.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

# general mapgen rules
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 8
MAX_ROOMS = 200
MAX_MONSTERS_PER_ROOM = 2
MAX_ITEMS_PER_ROOM = 2
MAP_WIDTH = SCREEN_WIDTH - 2 # bounded by 2 columns of frame
MAP_HEIGHT = SCREEN_HEIGHT - 8 # status/message bar is 5 tall, and bounded by 2 rows of frame

# rules for caves
CA_FIRST_PASSES = 5 # number of times to apply first-wave CA rules
CA_SECOND_PASSES = 3 # number of times to apply second wave CA rules
CA_MIN_WALLS = 5 # number of walls needed for a floor to become a wall
CA_MIN_FLOORS = 6 # number of floors needed for a wall in the second wave to become a floor
