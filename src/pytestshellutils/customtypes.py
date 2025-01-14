# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Custom Types.
"""
import copy
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import TYPE_CHECKING

import attr
from typing_extensions import Protocol

from pytestshellutils.utils import format_callback_to_string

if TYPE_CHECKING:
    from pytestshellutils.shell import Daemon


log = logging.getLogger(__name__)


class EnvironDict(Dict[str, str]):
    """
    Environ dictionary type.
    """

    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the class.
        """
        return f"EnvironDict({super().__str__()})"


class GenericCallback(Protocol):
    """
    Generic callback function.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        """
        Call the generic callback.
        """
        ...


class DaemonCallback(Protocol):
    """
    Daemon callback function.
    """

    def __call__(self, daemon: "Daemon") -> None:  # pragma: no cover
        """
        Call the daemon callback.
        """
        ...


@attr.s(kw_only=True, frozen=True)
class Callback:
    """
    Class which "stores" information of a callback.
    """

    func: Callable[..., Any] = attr.ib()
    args: Tuple[Any, ...] = attr.ib(default=None)
    kwargs: Dict[str, Any] = attr.ib(default=None)

    def __str__(self) -> str:
        """
        String representation of the class.
        """
        return format_callback_to_string(self.func, self.args, self.kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call the callback.
        """
        _args = tuple(list(args) + list(self.args or ()))
        _kwargs = copy.deepcopy(self.kwargs)
        _kwargs.update(kwargs)
        log.debug("Running %s", format_callback_to_string(self.func, _args, _kwargs))
        return self.func(*_args, **_kwargs)
