"""

"""

from abc import abstractmethod
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.filter import Filter
from predictor.src.stream_pipeline.pipe import Pipe


class LeafFilter(Filter):
    def __init__(
        self, filter_name: str, agent_factory: AgentFactory, input_pipe: Pipe, *args
    ):
        agent_name = self.__make_agent_name(filter_name)
        self.agent = self.create_agent(agent_name, agent_factory, input_pipe, *args)

    def __make_agent_name(self, filter_name: str):
        agent_name = filter_name + "_agent"  # todo: 겹치는거 생각해서 로직
        return agent_name

    @abstractmethod
    def create_agent(
        self, agent_name: str, agent_factory: AgentFactory, input_pipe: Pipe, *args
    ) -> Agent:
        pass

    def get_input_pipe(self) -> Pipe:
        return self.agent.get_input_pipe()  # todo: wrapper 어케 생성하냐..

    def add_output_pipe(self, pipe: Pipe):
        self.agent.add_output_pipe(pipe)

    async def activate(self):
        await self.agent.activate()

    async def deactivate(self):
        await self.agent.deactivate()
