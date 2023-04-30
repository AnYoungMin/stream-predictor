"""

"""
from faust import Channel, App
from predictor.src.stream_pipeline.pipe import FaustWrapperPipe


class FaustChannelWrapperPipe(Channel, FaustWrapperPipe):
    def __init__(self, app: App, *args, **kwargs):
        Channel.__init__(self, app=app, *args, **kwargs)
