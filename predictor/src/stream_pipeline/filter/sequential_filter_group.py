"""

"""

from __future__ import annotations
from predictor.src.stream_pipeline.filter import Filter, FilterNotExistException
from predictor.src.stream_pipeline.pipe import Pipe
from typing import List


class SequentialFilterGroup(Filter):
    def __init__(self):
        self.filters: List[Filter] = []

    def get_input_pipe(self) -> Pipe:
        if self.__is_children_filters_empty():
            raise FilterNotExistException("something wrong.. children filter not exist")
        head_filter = self.filters[0]
        input_pipe = head_filter.get_input_pipe()
        return input_pipe

    def __is_children_filters_empty(self):
        return len(self.filters) == 0

    def add_output_pipe(self, pipe: Pipe):
        if self.__is_children_filters_empty():
            raise FilterNotExistException("something wrong.. children filter not exist")
        tail_filter = self.filters[-1]
        tail_filter.add_output_pipe(pipe)

    async def activate(self):
        for _filter in reversed(self.filters):
            await _filter.activate()

    async def deactivate(self):
        for _filter in self.filters:
            await _filter.deactivate()

    def add(self, _filter: Filter) -> SequentialFilterGroup:
        if not self.__is_children_filters_empty():
            tail_filter = self.filters[-1]
            pipe = _filter.get_input_pipe()
            tail_filter.add_output_pipe(pipe)
        self.filters.append(_filter)
        return self
