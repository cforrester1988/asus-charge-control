#!/usr/bin/env python

from ._version import __version__

from platform import system, release
from subprocess import run

_MIN_KERNEL_VERSION = [5, 4]
_ASUS_MODULE_NAME = "asus_nb_wmi"
_PS_PATH = "/sys/class/power_supply/"
_CHARGE_FILE = "/charge_control_end_threshold"


def supported_platform() -> bool:
    """Check if the script is running on a supported platform (i.e. Linux)

    Returns:
        bool: true if on Linux, else false
    """
    return system() == "Linux"


def supported_kernel() -> bool:
    """Check if the script is running a supported kernel (>=5.4)

    Returns:
        bool: true if kernel is supported, else false
    """
    return [int(x) for x in release().split(".")[0:2]] >= _MIN_KERNEL_VERSION


def module_loaded() -> bool:
    """Check if the ASUS notebook WMI module is running

    Returns:
        bool: true if asus_nb_wmi in lsmod, else false
    """
    return _ASUS_MODULE_NAME in run(["lsmod"], capture_output=True).stdout.decode()


def main() -> None:
    from argparse import ArgumentParser
    from sys import argv, exit

    cc = ChargeThresholdController()
    parser = ArgumentParser(
        description=(
            "Get or set the current battery charge end threshold on an ASUS notebook. "
            "When the notebook's battery reaches the charge threshold, it will stop charging the battery."
        ),
        prog="asuscharge",
    )
    parser.add_argument(
        "max",
        nargs="?",
        type=int,
        default=None,
        help="set the battery's charge threshold",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    if not supported_platform():
        print(f"{argv[0]} only runs on Linux systems.")
        exit()
    if not supported_kernel():
        print(
            f"{argv[0]} requires a kernel version >= {_MIN_KERNEL_VERSION}. Detected version {release()}."
        )
        exit()
    if not module_loaded():
        print(
            (
                f"Kernel module '{_ASUS_MODULE_NAME}' is not loaded. Try running "
                f"'modprobe {_ASUS_MODULE_NAME}' and then 'lsmod | grep "
                f"{_ASUS_MODULE_NAME}' to verify the module has loaded."
            )
        )
        exit()
    args = parser.parse_args()
    if not args.max:
        print(f"Current charge threshold: {cc.end_threshold}%")
    else:
        try:
            cc.end_threshold = int(args.max)
            if cc.end_threshold == int(args.max):
                print(f"Successfully set charge threshold to {cc.end_threshold}%")
            else:
                print(f"Unable to set charge threshold.")
        except PermissionError:
            print(
                (
                    f"Unable to set charge threshold. Try running with root "
                    f"privileges: 'sudo {argv[0]} {args.max}'."
                )
            )


class ChargeThresholdController:
    """Retrieve and set the charge end threshold."""

    def __init__(self) -> None:
        """On initialization, ChargeThresholdController searches sysfs for
         the system's battery.

        Raises:
            Exception: Raised if unable to locate a compatible battery.
        """
        from os import walk
        from re import compile

        _BAT_RE = compile("(BAT)[0-9T]")
        self._bat_path: str = ""
        for _, dirs, _ in walk(_PS_PATH):
            for dir in dirs:
                if _BAT_RE.fullmatch(dir):
                    self._bat_path = f"{_PS_PATH}{dir}{_CHARGE_FILE}"
                    break
        if self._bat_path == "":
            raise Exception("Unable to find battery.")

    def __str__(self) -> str:
        return f"<AsusChargeThresholdController: charge_control_end_threshold={self.end_threshold}>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def end_threshold(self) -> int:
        """Get the current charge end threshold.

        Returns:
            int: current charge threshold.
        """
        with open(self._bat_path, "r") as f:
            return int(f.read())

    @end_threshold.setter
    def end_threshold(self, value: int) -> bool:
        """Set the charge end threshold.

        Args:
            value (int): a percentage from 0-100 (preferably from 50-100).

        Returns:
            bool: true if set successfully.
        """
        with open(self._bat_path, "w") as f:
            w = f.write(str(value))
            f.flush()
            return bool(w)


if __name__ == "__main__":
    main()
