"""

"""
import asyncio

from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.data_source import DataSource, ForwardingRule
from predictor.src.stream_pipeline.message import (
    MessageFormatInvalidException,
    PointOfTimeSeries,
)
from typing import Dict, Any, Optional

from predictor.src.stream_pipeline.message.sensor_data import SensorData
from predictor.src.stream_pipeline.pipe import Pipe


class AgentBasedDataSource(DataSource):  # todo: refactor agent
    def __init__(self, source_name: str, agent_factory: AgentFactory, input_pipe: Pipe):
        self.forwarding_rules: Dict[str, ForwardingRule] = dict()
        super().__init__(source_name, agent_factory, input_pipe)

    def create_agent(
        self, agent_name: str, agent_factory: AgentFactory, input_pipe: Pipe
    ) -> Agent:
        def forward(message_value: Dict[str, Any]) -> None:
            data = message_value["payload"]
            if not self.__validate_data_schema(data):
                raise MessageFormatInvalidException(
                    f"Get value {data}, not expected schema [SensorData]"
                )
            sensor_data = SensorData(**data)
            point = self.__convert_sensor_data_dict_to_point(sensor_data)
            for feature_id, forwarding_rule in self.forwarding_rules.items():
                ss_id = str(data["ss_id"])
                if ss_id in forwarding_rule.ids_to_be_forwarded:
                    asyncio.create_task(
                        self.agent.send_message(point, forwarding_rule.pipe)
                    )
            return None

        agent = agent_factory.create_agent(agent_name, input_pipe, forward)
        return agent

    def __validate_data_schema(self, data: Dict[str, Any]):
        try:
            SensorData(**data)
        except:
            raise MessageFormatInvalidException("invalid data type")
        return True

    def __convert_sensor_data_dict_to_point(
        self, sensor_data: SensorData
    ) -> PointOfTimeSeries:
        feature_id = str(sensor_data.ss_id)
        value = sensor_data.input_data
        timestamp = sensor_data.created_at  # todo: check timezone, precision
        return PointOfTimeSeries(feature_id, value, timestamp)

    def link_pipe_with_forwarding_rule(self, forwarding_rule: ForwardingRule):
        self.forwarding_rules[forwarding_rule.id] = forwarding_rule

    def get_forwarding_rule_by_id(self, id: str) -> ForwardingRule:
        return self.forwarding_rules[id]

    def remove_rule_by_id(self, id: str):
        self.forwarding_rules.pop(id)
