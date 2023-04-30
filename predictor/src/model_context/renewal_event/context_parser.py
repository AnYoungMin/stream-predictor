"""

"""

from dataclasses import dataclass
from predictor.src.shared.context import ModelContext
from torch import nn
from typing import Dict, List, Union


@dataclass
class ParsedContext:
    id: str
    scaling_map: Dict[str, Dict[str, Union[bool, float]]]
    x_replacing_value_map: Dict[str, float]
    model: nn.Module
    ids_to_be_forwarded: List[str]
    sliding_size: int


class ContextParser:
    def __init__(self, context: ModelContext):
        self.context = context

    def parse_context(self) -> ParsedContext:
        scaling_map = self.__extract_scaling_map()
        x_replace_value_map = self.__extract_x_replace_value_map()
        model = self.__extract_and_create_model()
        ids_to_be_forwarded = self.__extract_ids_to_be_forwarded()
        sliding_size = self.__extract_sliding_size()
        return ParsedContext(
            self.context.id,
            scaling_map,
            x_replace_value_map,
            model,
            ids_to_be_forwarded,
            sliding_size,
        )

    def __extract_scaling_map(self) -> Dict[str, Dict[str, float]]:
        scaling_map = dict()
        for x_n in self.context.variables.x:
            x_n_scaling_map = dict()
            x_n_scaling_map["scaled"] = x_n.scaled
            if x_n.scaled:
                x_n_scaling_map["scaling_strategy"] = x_n.scaling_strategy
                if x_n.scaling_strategy == "minmax":
                    x_n_scaling_map["min"] = x_n.min
                    x_n_scaling_map["max"] = x_n.max
                else:
                    NotImplementedError(
                        f"scsaling strategy is supported minmax only now. get {x_n.variable_id}'s strategy: {x_n.scaling_strategy}"
                    )
            scaling_map[x_n.variable_id] = x_n_scaling_map

        y_scaling_map = dict()
        y = self.context.variables.y
        y_scaling_map["scaled"] = y.scaled
        if y.scaled:
            y_scaling_map["scaling_strategy"] = y.scaling_strategy
            if y.scaling_strategy == "minmax":
                y_scaling_map["min"] = y.min
                y_scaling_map["max"] = y.max
            else:
                NotImplementedError(
                    f"scsaling strategy is supported minmax only now. get {y.variable_id}'s strategy: {y.scaling_strategy}"
                )
        scaling_map[y.variable_id] = y_scaling_map
        return scaling_map

    def __extract_x_replace_value_map(self) -> Dict[str, float]:
        replace_value_map = dict()
        for x_n in self.context.variables.x:
            if x_n.scaled and x_n.scaling_strategy == "minmax":
                replace_value_map[x_n.variable_id] = 0.5
            else:
                # todo:
                replace_value_map[x_n.variable_id] = 1.0
        return replace_value_map

    def __extract_and_create_model(self) -> nn.Module:
        if self.context.model.model_type == "LSTM":
            from predictor.src.shared.model.lstm import LSTM

            model = LSTM(
                input_size=self.context.model.hyperparameter["input_size"],
                hidden_size=self.context.model.hyperparameter["hidden_size"],
                output_size=self.context.model.hyperparameter["output_size"],
                num_layers=self.context.model.hyperparameter["num_layers"],
            )
        else:
            raise NotImplementedError(
                f"model type is supported [lstm] only now. got {self.context.id}'s type: {self.context.model.model_type}"
            )
        model.load_state_dict(self.context.model.state_dict)
        model.eval()
        return model

    def __extract_ids_to_be_forwarded(self) -> List[str]:
        ids = set(map(lambda x: x.variable_id, self.context.variables.x))
        ids.add(self.context.variables.y.variable_id)
        return list(ids)

    def __extract_sliding_size(self) -> int:
        if self.context.model.model_type == "LSTM":
            sliding_size = self.context.model.hyperparameter[
                "seq_len"
            ]  # todo: 맞나 검증해보기
        else:
            NotImplementedError(
                f"model type is supported [lstm] only now. got {self.context.id}'s type: {self.context.model.model_type}"
            )
        return sliding_size
