"""

"""
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.data_sink.data_sink import DataSink
from predictor.src.stream_pipeline.message.prediction_result import PredictionResult
from predictor.src.stream_pipeline.pipe import Pipe


class AgentBasedDataSink(DataSink):
    def __init__(
        self,
        sink_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        sink_pipe: Pipe,
    ):
        super().__init__(sink_name, agent_factory, input_pipe, sink_pipe)

    def create_agent(
        self,
        agent_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        sink_pipe: Pipe,
    ) -> Agent:
        def generate_prediction_event(prediction_result):
            result = PredictionResult(**prediction_result)
            return result

        agent = agent_factory.create_agent(
            agent_name, input_pipe, generate_prediction_event
        )
        agent.add_output_pipe(sink_pipe)
        return agent
