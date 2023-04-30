"""

"""


from abc import ABC
from predictor.src.stream_pipeline.filter import LeafFilter


class DataSink(LeafFilter, ABC):
    pass
