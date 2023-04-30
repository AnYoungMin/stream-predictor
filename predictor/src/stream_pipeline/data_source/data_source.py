"""

"""


from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.data_source import ForwardingRule
from predictor.src.stream_pipeline.filter import LeafFilter


class DataSource(LeafFilter):
    @abstractmethod
    def link_pipe_with_forwarding_rule(self, forwarding_rule: ForwardingRule):
        pass

    @abstractmethod
    def get_forwarding_rule_by_id(self, id: str) -> ForwardingRule:
        pass

    @abstractmethod
    def remove_rule_by_id(self, id: str):
        pass
