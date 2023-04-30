"""

"""
import asyncio
from predictor.src.stream_pipeline.pipe import PipeFactory, Pipe
from faust import Topic
import faust
from faust.types import TP
from typing import Optional, List


class FaustChannelPipeFactory(PipeFactory):
    def __init__(self, faust_app: faust.App):
        self.app = faust_app

    def create_pipe(self, pipe_name: Optional[List[str]] = None) -> Pipe:
        """
        If pipe_name is None, then create anonymous faust channel.
        If pipe_name is list of string, then create faust topic with at least one pipe name.
        """
        if pipe_name is None:
            return self.app.channel(
                loop=asyncio.get_running_loop()
            )  # todo wrapper 생성 전략
        else:
            # return self.app.topic(topics=pipe_name, active_partitions=(TP(pipe_name[0], 0)), loop=asyncio.get_running_loop())  # todo wrapper 생성 전략
            return Topic(
                app=self.app,
                topics=pipe_name,
                active_partitions=(TP(pipe_name[0], 0)),
                loop=asyncio.get_running_loop(),
            )  # todo wrapper 생성 전략
