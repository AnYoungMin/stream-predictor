"""

"""
from typing import List, Dict

from predictor.src.shared.context import ModelContext
from predictor.src.stream_pipeline.pipeline import PipelineManager


class PipelinesLoader:
    def __init__(self, pipeline_manager: PipelineManager):
        self.pipeline_manager = pipeline_manager

    async def load_pipelines(self, contexts: Dict[str, ModelContext]):
        for id, context in contexts.items():
            await self.pipeline_manager.renew_pipeline(context)
