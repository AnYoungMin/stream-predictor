"""

"""

from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from collections import OrderedDict
from enum import Enum


class ScalingStrategy(Enum):
    MINMAX = "minmax"
    NO_SCALING = "no scaling"


@dataclass
class Variable:
    variable_id: str
    scaled: bool
    scaling_strategy: str = ScalingStrategy.NO_SCALING.value
    min: Optional[float] = None
    max: Optional[float] = None

    def __post_init__(self):
        if isinstance(self.scaling_strategy, ScalingStrategy):
            self.scaling_strategy = self.scaling_strategy.value

        if not isinstance(self.variable_id, str):
            raise TypeError("variable id must be string")

        if self.scaled and self.scaling_strategy == ScalingStrategy.NO_SCALING.value:
            raise ValueError(
                "When scaled is true, scaling strategy can't be NO SCALING"
            )

        if self.scaling_strategy == ScalingStrategy.MINMAX.value:
            if self.min is None or self.max is None:
                raise ValueError(
                    "When scaling strategy is minmax, then min&max value must be set"
                )


@dataclass
class Variables:
    x: List[Variable]
    y: Variable

    def __post_init__(self):
        self.x = [Variable(**x) if isinstance(x, dict) else x for x in self.x]
        if isinstance(self.y, dict):
            self.y = Variable(**self.y)


@dataclass
class Model:
    model_type: str
    hyperparameter: Dict[str, Any]
    state_dict: OrderedDict  # highly-coupled with pytorch


@dataclass
class ModelContext:
    id: str
    variables: "Variables"
    model: "Model"

    def __post_init__(self):
        if isinstance(self.variables, dict):
            self.variables = Variables(**self.variables)
        if isinstance(self.model, dict):
            self.model = Model(**self.model)
