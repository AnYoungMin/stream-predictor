"""

"""

from predictor.src.shared.context import ModelContext
from predictor.src.model_context.repository import (
    ContextRepository,
    ContextCache,
    ModelContextNotExistException,
    ContextFileSaver,
)
import logging

logger = logging.getLogger(__name__)


class CachedFileContextRepository(ContextRepository):
    """
    When retrieving model context, it seek a model context just only in cache.
    When saving a model context, it write to cache and file, but it does not guarantee consistency from any exceptional case.
    So it has no synchronizing cache to file.
    """

    def __init__(self, context_cache: ContextCache, saver: ContextFileSaver):
        self.context_cache = context_cache
        self.saver = saver

    def find_by_id_throw_exception_when_not_exist(self, id: str) -> ModelContext:
        if self.context_cache.is_cached(id):
            return self.context_cache.get_model_by_id(id)
        raise ModelContextNotExistException(f"model context id {id} is not exist")

    def save(self, context: ModelContext):
        self.__try_to_save_both_cache_and_file(context)

    def __try_to_save_both_cache_and_file(self, context: ModelContext):
        try:
            self.context_cache.cache_model_context(context)
            self.saver.save_model_context(context)
        except Exception:
            logger.exception("model context save failed")
