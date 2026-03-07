from collections import defaultdict
from typing import Dict, Type, Any, Generator, Iterable

from ecs.system import System


class World:
    """
    The central ECS manager.

    The World is responsible for:
    - Creating entities
    - Storing components
    - Managing systems
    - Running systems each frame

    Components are stored using the structure:

        ComponentType -> {entity_id -> component_instance}

    Example:
        Position -> {1: Position(10,20), 2: Position(30,40)}
        Velocity -> {1: Velocity(5,0)}
    """

    def __init__(self) -> None:
        """
        Initialize the ECS world.
        """
        self.next_entity_id: int = 1

        # Component storage:
        # ComponentType -> {entity_id -> component_instance}
        self.components: Dict[Type[Any], Dict[int, Any]] = defaultdict(dict)

        self.systems: list[System] = []
        self.running: bool = True

    def create_entity(self) -> int:
        """
        Create a new entity.

        Entities are represented by unique integer IDs.

        Returns:
            int: The ID of the newly created entity.
        """
        entity: int = self.next_entity_id
        self.next_entity_id += 1
        return entity

    def add_component(self, entity: int, component: Any) -> None:
        """
        Attach a component to an entity.

        Args:
            entity (int): The entity ID.
            component (object): The component instance to attach.

        Example:
            world.add_component(player, Position(100, 200))
        """
        self.components[type(component)][entity] = component

    def remove_entity(self, entity: int) -> None:
        """
        Remove an entity and all of its components.

        Args:
            entity (int): The entity ID to remove.
        """
        for component_store in self.components.values():
            component_store.pop(entity, None)

    def get_entities_with(
        self, *component_types: Type[Any]
    ) -> Generator[tuple[int, list[Any]], None, None]:
        """
        Yield entities that contain all requested component types.

        Args:
            *component_types: One or more component classes.

        Yields:
            tuple[int, list[Any]]:
                (entity_id, [component_instances])

        Example:
            for entity, (pos, vel) in world.get_entities_with(Position, Velocity):
                pos.x += vel.dx
        """
        if not component_types:
            return

        component_maps = [self.components[ctype] for ctype in component_types]

        entity_ids = set(component_maps[0].keys())

        for cmap in component_maps[1:]:
            entity_ids &= set(cmap.keys())

        for entity in entity_ids:
            yield entity, [self.components[ctype][entity] for ctype in component_types]

    def add_system(self, system: System) -> None:
        """
        Register a system with the world.

        Systems are executed in the order they are added.

        Args:
            system: The system instance to add.
        """
        self.systems.append(system)

    def update(self, dt: float, events: Iterable[Any]) -> None:
        """
        Run all systems for the current frame.

        Args:
            dt: Delta time since the previous frame.
            events (list): Pygame event list.
        """
        for system in self.systems:
            system.update(self, dt, events)
