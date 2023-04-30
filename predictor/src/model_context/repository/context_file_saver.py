"""

"""

from predictor.src.shared.context import ModelContext
import os
import pickle


class ContextFileSaver:
    def __init__(self, context_dir: str):
        self.context_dir = context_dir

    def save_model_context(self, context: ModelContext):
        if not os.path.exists(self.context_dir):
            os.makedirs(self.context_dir)
        context_filename = os.path.join(self.context_dir, context.id + ".pkl")
        with open(context_filename, "wb") as file:
            pickle.dump(context, file)
