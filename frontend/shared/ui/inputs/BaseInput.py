from abc import abstractmethod
from typing import Any


class BaseInput:
    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def is_value_valid(self) -> bool:
        pass