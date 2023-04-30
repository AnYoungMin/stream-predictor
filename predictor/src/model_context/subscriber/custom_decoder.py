import json
import torch
import numpy as np

from predictor.src.shared.context import ModelContext, Model, Variables
from collections import OrderedDict


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "x" in obj:
            return Variables(**obj)
        elif "model_type" in obj:
            return Model(**obj)
        elif (
            len(list(filter(lambda key: "weight" in key, obj.keys()))) > 0
            or len(list(filter(lambda key: "bias" in key, obj.keys()))) > 0
        ):
            obj = OrderedDict(obj)
            for key, value in obj.items():
                obj[key] = torch.FloatTensor(value)
            return obj
        elif "variables" in obj:
            return ModelContext(**obj)
        return obj
