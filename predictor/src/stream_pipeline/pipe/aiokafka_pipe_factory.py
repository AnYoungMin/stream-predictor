"""

"""
import uuid
from predictor.src.stream_pipeline.pipe import PipeFactory, Pipe, AIOKafkaPipe
from typing import Optional, List, Union


class AIOKafkaPipeFactory(PipeFactory):
    def __init__(self):
        return

    def create_pipe(self, pipe_name: Optional[Union[str, List[str]]] = None) -> Pipe:
        if pipe_name is None:
            # todo: ephemeral topic name generating strategy
            pipe_name = [str(uuid.uuid4())]
        elif "str" in str(type(pipe_name)):
            pipe_name = [pipe_name]
        pipe = AIOKafkaPipe(pipe_name)
        return pipe
