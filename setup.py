"""Setup script for the litprinter package."""

import importlib.util
import os

from setuptools import setup


def _patch_install_data() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    helper_path = os.path.join(here, "setup_helpers.py")
    if os.path.isfile(helper_path):
        spec = importlib.util.spec_from_file_location(
            "litprinter_setup_helpers", helper_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.patch_install_data()


_patch_install_data()

if __name__ == "__main__":
    setup()
