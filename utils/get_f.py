"""Compatibility shim: expose Get_F from the problems/continuous implementation.

This keeps one implementation of the benchmark suite while allowing tests
and other modules to import `utils.get_f.Get_F` as before.
"""

from problems.continuous.get_f import Get_F  # re-export

__all__ = ["Get_F"]
