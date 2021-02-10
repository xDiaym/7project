from abc import ABC, abstractmethod
from typing import Optional


class ABCHomeworkStorage(ABC):
    """ Interface for homework storage. """

    @abstractmethod
    async def set_homework(
            self, group_id: int, lesson: str, homework: str
    ) -> None:
        """ Writes homework to the storage. Ignores lesson register. """
        pass

    @abstractmethod
    async def get_homework(self, group_id: int, lesson: str) -> Optional[str]:
        """ Read homework from storage. Ignores lesson register. """
        pass
