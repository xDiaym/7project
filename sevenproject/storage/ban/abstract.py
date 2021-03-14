from abc import ABC, abstractmethod


class ABCBanStorage(ABC):
    """ Interface for ban storage. """

    @abstractmethod
    async def ban(self, group_id: int, user_id: int) -> None:
        """ Add user to ban list at group. """
        pass

    @abstractmethod
    async def unban(self, group_id: int, user_id: int) -> None:
        """ Delete user from ban list at group. """
        pass

    @abstractmethod
    async def was_banned(self, group_id: int, user_id: int) -> bool:
        """ Checks if a user is in the ban list. """
        pass
