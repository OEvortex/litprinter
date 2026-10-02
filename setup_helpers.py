"""Build helpers for setuptools.

Not installed as part of the runtime package.
"""

from __future__ import annotations

import setuptools as _setuptools  # noqa: F401

try:  # Importing setuptools first monkey-patches this module.
    from distutils.command.install_data import install_data as _install_data
except Exception:  # pragma: no cover
    from setuptools._distutils.command.install_data import (
        install_data as _install_data,
    )


def _patched_run(self) -> None:
    """Install ``.pth`` files next to the importable library files.

    ``distutils/setuptools`` send ``data_files`` to the wheel's ``.data/data``
    directory, which Python's ``site`` module never scans for ``.pth`` files.
    This moves ``.pth`` files into the pure-lib directory (site-packages),
    where they are actually executed at interpreter startup.
    """

    install_cmd = self.distribution.get_command_obj('install')
    purelib = getattr(install_cmd, 'install_purelib', None) or getattr(
        install_cmd, 'install_lib', None
    )

    if not isinstance(purelib, str) or not purelib:
        original_run(self)
        return

    # install_lib/install_purelib already point at the wheel/install tree
    # where normal Python modules are being installed.
    target_lib = purelib

    pth_files: list[str] = []
    kept_data_files: list = []

    for item in self.data_files or []:
        if isinstance(item, tuple):
            dest, files = item[0], list(item[1])
            keep_files = []
            for filename in files:
                if str(filename).endswith('.pth'):
                    pth_files.append(str(filename))
                else:
                    keep_files.append(filename)
            if keep_files:
                kept_data_files.append((dest, keep_files))
        else:
            if str(item).endswith('.pth'):
                pth_files.append(str(item))
            else:
                kept_data_files.append(item)

    if pth_files:
        self.mkpath(target_lib)
        for filename in pth_files:
            out, _ = self.copy_file(filename, target_lib)
            self.outfiles.append(out)

    old_data_files = self.data_files
    self.data_files = kept_data_files
    try:
        if self.data_files:
            original_run(self)
    finally:
        self.data_files = old_data_files


original_run = _install_data.run

try:
    import setuptools.command.editable_wheel as _editable_wheel
except Exception:  # pragma: no cover
    _editable_wheel = None


def _patch_editable_pth() -> None:
    """Make PEP 660 editable installs also autoload litprinter.

    Editable installs do not run install_data for data_files, so we append a
    plain import line to the editable .pth that setuptools generates.
    """
    if _editable_wheel is None:
        return
    original_encode = _editable_wheel._encode_pth

    def patched_encode(content: str) -> bytes:
        if 'import litprinter_autoload' not in content:
            if not content.endswith('\n'):
                content += '\n'
            content += 'import litprinter_autoload\n'
        return original_encode(content)

    _editable_wheel._encode_pth = patched_encode


def patch_install_data() -> None:
    """Monkey-patch the install_data command used by this build."""
    _install_data.run = _patched_run  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
    _patch_editable_pth()
