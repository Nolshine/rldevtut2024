from __future__ import annotations

import tcod.ecs
import tcod.path

from components.components import Position, Tiles
from constants.game_constants import PATH_COST_INCREASE
from constants.tags import IsActor, InMap
from dungeon.tiles import TILES



def path_to(actor: tcod.ecs.Entity, dest: Position) -> list[Position]:
    """Compute and return a path from actor to destination.
    
    If there is no valid path, return empty list."""
    map_ = actor.relation_tag[InMap]

    # Copy walkable array.
    cost = TILES["walk_cost"][map_.components[Tiles]]

    for other in actor.registry.Q.all_of(tags=[IsActor], relations=[(InMap, map_)]):
        other_pos = other.components[Position]
        # check that an entity blocks movement and the cost isn't zero (blocking).:
        if cost[other_pos.raw]:
            # Add to the cost of a blocking position.
            # A lower number means enemies will crowd behind each other in hallways.
            # A higher number means enemies will take longer paths to surround the player.
            cost[other_pos.raw] += PATH_COST_INCREASE

    # Create a graph from the cost array and pass that graph to a new pathfinder.
    graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
    pathfinder = tcod.path.Pathfinder(graph)

    # Starting position.
    pathfinder.add_root(actor.components[Position].raw)

    # Compute path to destination and remove starting node.
    path: list[list[int]] = pathfinder.path_to(dest.raw)[1:].tolist()

    # Convert from List[List[int]] to List[Tuple[int, int]]
    return [Position(raw_index[0], raw_index[1]) for raw_index in path]