"""Set your recent ASUS notebook's maximum charge level on Linux."""

from ._version import __version__

from .__main__ import (
    ChargeThresholdController,
    supported_platform,
    supported_kernel,
    module_loaded,
)
