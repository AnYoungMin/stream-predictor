"""

"""
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.data_source import DataSource, ForwardingRule
from typing import Dict

from predictor.src.stream_pipeline.pipe import Pipe


class FaustAgentDataSource(DataSource):  # todo: refactor agent
    def __init__(self, source_name: str, agent_factory: AgentFactory, input_pipe: Pipe):
        self.forwarding_rules: Dict[str, ForwardingRule] = dict()
        super().__init__(source_name, agent_factory, input_pipe)

    def create_agent(
        self, agent_name: str, agent_factory: AgentFactory, input_pipe: Pipe
    ) -> Agent:
        def forward(source_data):  # todo 타입
            for feature_id, forwarding_rule in self.forwarding_rules.items():
                if source_data.id in self.forwarding_rule.ids_to_be_forwarded:
                    source_data.forward(forwarding_rule.pipe)

        agent = agent_factory.create_agent(agent_name, input_pipe, forward)
        return agent

    def link_pipe_with_forwarding_rule(self, forwarding_rule: ForwardingRule):
        self.forwarding_rules[forwarding_rule.id] = forwarding_rule

    def get_forwarding_rule_by_id(self, id: str) -> ForwardingRule:
        return self.forwarding_rules[id]

    def remove_rule_by_id(self, id: str):
        self.forwarding_rules.pop(id)
