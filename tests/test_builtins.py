"""Tests for the builtins install/uninstall helpers."""

import builtins

from litprinter import DEFAULT_NAMES, install, uninstall
from litprinter import ic


def test_import_registers_every_name():
    for name in DEFAULT_NAMES:
        assert hasattr(builtins, name), name


def test_uninstall_star_then_install_restores():
    uninstall('*')
    for name in DEFAULT_NAMES:
        assert not hasattr(builtins, name), name

    install()
    assert hasattr(builtins, 'ic')


def test_install_under_extra_name():
    install('dbg')
    assert getattr(builtins, 'dbg') is builtins.ic
    uninstall('dbg')
    assert not hasattr(builtins, 'dbg')


def test_uninstall_unknown_name_is_noop():
    uninstall('definitely_not_registered')


def test_uninstall_single_name_leaves_others():
    uninstall('LIT')
    assert not hasattr(builtins, 'LIT')
    assert hasattr(builtins, 'ic')


def test_wrapper_install_methods():
    ic.install('dbg2')
    assert getattr(builtins, 'dbg2') is ic
    ic.uninstall('dbg2')
    assert not hasattr(builtins, 'dbg2')
