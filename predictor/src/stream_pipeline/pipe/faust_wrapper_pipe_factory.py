"""

"""

from predictor.src.stream_pipeline.pipe import (
    PipeFactory,
    Pipe,
    FaustChannelWrapperPipe,
    FaustTopicWrapperPipe,
)
import faust
from typing import Optional, List


class FaustWrapperPipeFactory(PipeFactory):
    def __init__(self, faust_app: faust.App):
        self.app = faust_app

    def create_pipe(self, pipe_name: Optional[List[str]] = None) -> Pipe:
        """
        If pipe_name is None, then create anonymous faust channel.
        If pipe_name is list of string, then create faust topic with at least one pipe name.
        """
        if pipe_name is None:
            return FaustChannelWrapperPipe(self.app)  # todo wrapper 생성 전략
        else:
            return FaustTopicWrapperPipe(self.app, pipe_name)  # todo wrapper 생성 전략
