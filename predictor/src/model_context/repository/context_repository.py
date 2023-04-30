"""

"""

from abc import ABC, abstractmethod
from predictor.src.shared.context import ModelContext


class ContextRepository(ABC):
    @abstractmethod
    def find_by_id_throw_exception_when_not_exist(self, id: str) -> ModelContext:
        pass

    @abstractmethod
    def save(self, context: ModelContext):
        pass
