"""

"""

from typing import Dict
from predictor.src.shared.context import ModelContext
import pickle
import glob
import os


class ContextFilesLoader:
    def __init__(self, context_dir):
        self.context_dir = context_dir

    def load_and_return_model_contexts(self) -> Dict[str, ModelContext]:
        contexts = dict()
        for filename in glob.glob(
            os.path.join(os.path.join(self.context_dir, "*.pkl"))
        ):
            with open(filename, "rb") as file:
                context = pickle.load(file)
                id = context.id
                contexts[id] = context
        return contexts
