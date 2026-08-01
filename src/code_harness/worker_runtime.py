"""Compatibility export of the contract-gated worker runtime."""

from ._legacy import expose

expose("worker_runtime", globals())

