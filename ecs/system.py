from typing import Iterable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ecs.world import World


class System:
    """
    Base class for ECS systems.
    """

    def update(self, world: "World", dt: float, events: Iterable[Any]) -> None:
        """
        Run system logic for a frame.
        """
        pass
