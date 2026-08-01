"""Compatibility export of the persistent artifact ledger."""

from ._legacy import expose

expose("artifact_ledger", globals())

