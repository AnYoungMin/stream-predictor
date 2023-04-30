"""

"""

from abc import ABC, abstractmethod


class AsyncSubscriber(ABC):
    @abstractmethod
    async def connect_broker(self):
        pass

    @abstractmethod
    async def subscribe(self):
        pass
