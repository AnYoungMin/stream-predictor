"""

"""
import asyncio

from predictor.src.stream_pipeline.agent import (
    Agent,
    ConcreteDependencyMismatchException,
)
from predictor.src.stream_pipeline.pipe import Pipe, FaustWrapperPipe
from typing import Callable
import faust
import logging


logger = logging.getLogger(__name__)


class FaustAgent(Agent):
    def __init__(
        self,
        faust_app: faust.App,
        agent_name: str,
        input_pipe: FaustWrapperPipe,
        process: Callable,
    ):
        async def stream_process(stream):
            await stream.maybe_start()
            async for data in stream:
                processed_data = process(data)
                logger.info(
                    f"Faust Agent {agent_name} got data: {data}, processed data: {processed_data}"
                )
                if processed_data is not None:
                    yield processed_data

        # self.__check_whether_pipe_is_faust_pipe_raising_exception_if_not(input_pipe)
        self.agent = faust_app.agent(
            channel=input_pipe, name=agent_name, loop=asyncio.get_running_loop()
        )(stream_process)
        self.agent_name = agent_name

    def __check_whether_pipe_is_faust_pipe_raising_exception_if_not(self, pipe: Pipe):
        if not isinstance(pipe, FaustWrapperPipe):
            raise ConcreteDependencyMismatchException("faust agen")

    def get_input_pipe(self) -> Pipe:
        return self.agent.channel

    def add_output_pipe(self, pipe: Pipe):
        # self.__check_whether_pipe_is_faust_pipe_raising_exception_if_not(pipe)
        self.agent.add_sink(pipe)  # todo: check type safety

    async def activate(self):
        await self.agent.maybe_start()
        print(f"###agent starting....{self.agent_name}")
        await self.agent.on_start()
        print(f"###agent started")

    async def deactivate(self):
        await self.agent.maybe_start()

    async def on_start(self):
        await self.agent.on_start()
