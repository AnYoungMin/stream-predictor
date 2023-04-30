"""

"""
from typing import List
from faust import Topic, App
from predictor.src.stream_pipeline.pipe import FaustWrapperPipe


class FaustTopicWrapperPipe(Topic, FaustWrapperPipe):
    def __init__(self, app: App, topics: List[str], *args, **kwargs):
        Topic.__init__(self, app=app, topics=topics, *args, **kwargs)
