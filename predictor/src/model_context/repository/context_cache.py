"""

"""

from typing import Dict
from predictor.src.utils import SingletonMeta
from predictor.src.shared.context import ModelContext


class ContextCache(metaclass=SingletonMeta):
    def __init__(self, contexts):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            self.contexts: Dict[str, ModelContext] = contexts

    def cache_model_context(self, context: ModelContext):
        id = context.id
        self.contexts[id] = context

    def get_model_context_by_id(self, id: str) -> ModelContext:
        return self.contexts[id]

    def is_cached(self, id: str):
        return id in self.contexts
